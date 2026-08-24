#!/usr/bin/env ruby

require "digest"

project_dir = File.expand_path(__dir__)
repo_dir = File.expand_path("..", project_dir)
html_path = File.join(repo_dir, "docs", "custom-king-storage-bed", "index.html")
source_paths = %w[
  bed.py
  build.sh
  build-guide.md
  build-guide.sh
  design.py
  guide-images.py
  integrated.py
  modules.py
  README.md
  guide-assets/build-sequence.d2
  guide-assets/build-sequence.svg
  guide-assets/chassis-overview.png
].map { |path| File.join(project_dir, path) }
source_paths.concat(Dir.glob(File.join(project_dir, "guide-assets", "steps", "*.svg")).sort)

missing = source_paths.reject { |path| File.file?(path) }
abort "Missing guide source: #{missing.join(", ")}" unless missing.empty?

digest = Digest::SHA256.new
source_paths.each do |path|
  digest << path.delete_prefix("#{project_dir}/")
  digest << "\0"
  digest << File.binread(path)
  digest << "\0"
end
stamp = "<!-- build-guide-source-sha256: #{digest.hexdigest} -->"

case ARGV.fetch(0, "check")
when "stamp"
  html = File.read(html_path)
  html = html.sub(/\n?<!-- build-guide-source-sha256: [0-9a-f]{64} -->\n?\z/, "")
  File.write(html_path, "#{html.rstrip}\n#{stamp}\n")
  puts stamp
when "check"
  abort "Missing generated guide: #{html_path}" unless File.file?(html_path)
  abort "Generated guide is stale; run custom-king-storage-bed/build-guide.sh" unless File.read(html_path).include?(stamp)
  puts "Guide freshness check passed"
else
  abort "Usage: #{$PROGRAM_NAME} [stamp|check]"
end
