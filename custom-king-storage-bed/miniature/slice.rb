#!/usr/bin/env ruby
# frozen_string_literal: true

require "digest"
require "fileutils"
require "json"
require "open3"

ROOT = __dir__
BUILD = File.join(ROOT, "build")
APP = ENV.fetch("PRUSASLICER_BIN", "/Applications/PrusaSlicer.app/Contents/MacOS/PrusaSlicer")
MESH_CHECK = ENV.fetch("SLICE_BIN", File.expand_path("~/.agents/skills/3d-printer/scripts/slice"))
DATADIR = ENV.fetch("PRUSASLICER_DATADIR", File.expand_path("~/Library/Application Support/PrusaSlicer"))
STATE = ENV.fetch("PRINTER_STATE", File.expand_path("~/.agents/skills/3d-printer/assets/printer.json"))
PROFILE = "0.15mm SPEED @MK4IS 0.4"

def run!(*command)
  output, status = Open3.capture2e(*command)
  abort("#{command.first} failed:\n#{output}") unless status.success?
  output
end

def metadata(path)
  raw = File.binread(path)
  abort("Expected binary g-code, got another format: #{path}") unless raw.start_with?("GCDE")
  text = raw.gsub(/[\x00-\x08\x0b\x0c\x0e-\x1f]/n, "\n").force_encoding("UTF-8").scrub("")
  text.scan(/^([a-z][a-z0-9_ \[\]()]*?)=(.*)$/).to_h
end

def seconds(text)
  fields = text.scan(/(\d+)\s*([dhms])/)
  abort("Missing or invalid printing time: #{text.inspect}") if fields.empty?
  fields.sum { |value, unit| value.to_i * { "d" => 86_400, "h" => 3600, "m" => 60, "s" => 1 }.fetch(unit) }
end

manifest_path = File.join(BUILD, "manifest.json")
abort("Run bash build.sh first.") unless File.file?(manifest_path)
manifest = JSON.parse(File.read(manifest_path))
%w[model.py ../design.py].each do |name|
  abort("Source changed since CAD export: #{name}; run bash build.sh.") unless
    Digest::SHA256.file(File.join(ROOT, name)).hexdigest == manifest.fetch("source_sha256").fetch(name)
end
state = JSON.parse(File.read(STATE))
abort("This slicing contract requires MK4 with a 0.4 mm nozzle and MMU3.") unless
  state.dig("printer", "model") == "Prusa MK4" &&
  state.dig("printer", "nozzle_mm") == 0.4 && state.dig("printer", "mmu") == "MMU3"

selected = ARGV.empty? ? manifest.fetch("parts").keys : ARGV
unknown = selected - manifest.fetch("parts").keys
abort("Unknown part(s): #{unknown.join(', ')}") unless unknown.empty?
FileUtils.mkdir_p(File.join(BUILD, "gcode"))
FileUtils.mkdir_p(File.join(BUILD, "slice-reports"))
results = {}

selected.each do |name|
  part = manifest.fetch("parts").fetch(name)
  slot = part.fetch("slot")
  spool = state.fetch("loaded").find { |loaded| loaded["slot"] == slot }
  abort("Slot #{slot} is not recorded as PLA; update filament state before slicing.") unless spool && spool["material"] == "PLA"
  source = File.join(BUILD, "parts", "#{name}.stl")
  mesh = run!(MESH_CHECK, source, "--info")
  abort("Mesh is not one watertight part: #{name}") unless
    mesh.match?(/^manifold = yes$/) && mesh.match?(/^number_of_parts =\s+1$/)
  File.write(File.join(BUILD, "slice-reports", "#{name}-mesh.txt"), mesh)

  brim = %w[drawer foot headboard-pin seam-key pod-left pod-right base-insert mattress headboard].include?(name) ? 3 : 0
  x, y, z = part.fetch("size_mm")
  # Reserve the larger of the skirt or brim, plus an extrusion-width margin.
  margin = [brim, 3].max + 0.6
  abort("Insufficient oriented bed margin for #{name}") unless x+2*margin <= 250 && y+2*margin <= 210 && z <= 220
  output = File.join(BUILD, "gcode", "#{name}.bgcode")
  command = [
    APP, "--datadir", DATADIR,
    "--printer-profile", "Original Prusa MK4 MMU3 0.4 nozzle",
    "--print-profile", PROFILE, "--material-profile", "Prusament PLA @PGIS",
    "--binary-gcode", "--no-support-material", "--no-wipe-tower",
    "--post-process", "", "--perimeters", "4", "--fill-density", "15%",
    "--fill-pattern", "gyroid", "--top-solid-layers", "6", "--bottom-solid-layers", "6",
    "--first-layer-height", "0.2", "--elefant-foot-compensation", "0.15",
    "--perimeter-extruder", slot.to_s, "--infill-extruder", slot.to_s,
    "--solid-infill-extruder", slot.to_s, "--support-material-extruder", "0",
    "--support-material-interface-extruder", "0", "--brim-type", "outer_only",
    "--brim-width", brim.to_s, "--skirt-distance", "3", "--skirts", "1",
    "--center", "125,105", "-g", source, "-o", output
  ]
  sliced = run!(*command)
  File.write(File.join(BUILD, "slice-reports", "#{name}-slicer.txt"), sliced)
  meta = metadata(output)
  abort("Unexpected printer for #{name}: #{meta['printer_model']}") unless meta["printer_model"] == "MK4ISMMU3"
  abort("Supports enabled for #{name}") unless meta["support_material"] == "0"
  abort("Unexpected layer height for #{name}") unless meta["layer_height"] == "0.15"
  abort("Unexpected nozzle for #{name}") unless
    meta.fetch("nozzle_diameter").split(",").all? { |diameter| Float(diameter) == 0.4 }
  grams = meta.fetch("filament used [g]").split(",").map { |v| Float(v) }
  active = grams.each_index.select { |index| grams[index].positive? }
  abort("Wrong or multiple active MMU slots for #{name}: #{active}") unless active == [slot-1]
  abort("Unexpected material for #{name}") unless meta.fetch("filament_type").split(";").fetch(slot-1) == "PLA"
  time = meta.fetch("estimated printing time (normal mode)")
  record = {
    "quantity" => part.fetch("quantity"), "slot" => slot, "color" => spool.fetch("color"),
    "material" => "PLA", "profile" => PROFILE, "layer_height_mm" => 0.15,
    "brim_mm" => brim, "support_material" => false, "in_print_tool_changes" => 0,
    "size_mm" => part.fetch("size_mm"), "reserved_footprint_mm" => [x+2*margin, y+2*margin],
    "time" => time, "seconds" => seconds(time), "grams" => grams.sum.round(2),
    "filament_mm" => meta.fetch("filament used [mm]").split(",").sum { |v| Float(v) }.round(2),
    "filament_cm3" => meta.fetch("filament used [cm3]").split(",").sum { |v| Float(v) }.round(2),
    "calibration_only" => part.fetch("calibration_only"),
    "fit_per_side_mm" => manifest.fetch("fit_per_side_mm"),
    "stl_sha256" => Digest::SHA256.file(source).hexdigest,
    "gcode_sha256" => Digest::SHA256.file(output).hexdigest
  }
  File.write(File.join(BUILD, "slice-reports", "#{name}.json"), JSON.pretty_generate(record)+"\n")
  results[name] = record
  puts "#{name}: #{time}, #{record['grams']} g, slot #{slot} #{record['color']}, brim #{brim} mm"
end

# A partial run never leaves a misleading old aggregate report behind.
summary_path = File.join(BUILD, "print-summary.json")
if selected.sort == manifest.fetch("parts").keys.sort
  production = results.values.reject { |part| part.fetch("calibration_only") }
  summary = {
    "manifest_sha256" => Digest::SHA256.file(manifest_path).hexdigest,
    "slicer_script_sha256" => Digest::SHA256.file(__FILE__).hexdigest,
    "fit_per_side_mm" => manifest.fetch("fit_per_side_mm"),
    "production_piece_count" => production.sum { |part| part.fetch("quantity") },
    "production_seconds" => production.sum { |part| part.fetch("seconds")*part.fetch("quantity") },
    "production_grams" => production.sum { |part| part.fetch("grams")*part.fetch("quantity") }.round(2),
    "calibration_seconds" => results.values.select { |part| part.fetch("calibration_only") }.sum { |part| part.fetch("seconds") },
    "calibration_grams" => results.values.select { |part| part.fetch("calibration_only") }.sum { |part| part.fetch("grams") }.round(2),
    "parts" => results
  }
  File.write(summary_path, JSON.pretty_generate(summary)+"\n")
  puts "Complete production kit: #{summary['production_piece_count']} pieces, #{summary['production_grams']} g."
else
  FileUtils.rm_f(summary_path)
  puts "Partial run; individual reports written. Run without part names for complete kit totals."
end
