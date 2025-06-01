// === Parameters ===
turns = 8;
segments_per_turn = 60;
total_segments = turns * segments_per_turn;

end_radius = 100;
height = 0;

min_width = 1;
max_width = 4;

min_thickness = 3;
max_thickness = 8;

strip_thickness_y = 2;

center_disc_radius = 4;
center_disc_thickness = min_thickness; // match outer strip height
center_hole_radius = 2.5;

start_radius = center_hole_radius + 1; // e.g. 3.5mm

// === Assembly ===
spiral();
bridge_to_top_disc_aligned();
reinforce_bridge_joint();
top_attachment_disc();

// === Spiral Function ===
module spiral_strip_variable_size() {
  for (i = [0 : total_segments - 2]) {
    hull() {
      place_strip(i);
      place_strip(i + 1);
    }
  }
}

// === Strip Placement ===
module place_strip(i) {
  t = i / total_segments;
  angle = 360 * i / segments_per_turn;

  // Exponential radius shrink toward center (tight inner coils)
  radius = end_radius * pow(start_radius / end_radius, t) - turns;

  z = 0; // flat, printable

  // ✅ Decrease thickness toward center
  thickness = min_thickness + (max_thickness - min_thickness) * (1 - t);

  // ✅ Increase width toward center
  width = min_width + (max_width - min_width) * t;

  translate([radius * cos(angle), radius * sin(angle), z])
    rotate([0, 0, angle])
      cube([width, strip_thickness_y, thickness]);
}

// === Central Disc + Hole ===
module spiral() {
  difference() {
    // Spiral
    spiral_strip_variable_size();

    // Hole
    translate([0, 0, -1])
      cylinder(h=center_disc_thickness + 3, r=center_hole_radius, $fn=50);
  }
}

// === Bridge from spiral end to center (elevated) ===
module bridge_to_top_disc_aligned() {
  // Compute last spiral segment position
  t = (total_segments - 1) / total_segments;
  angle = 360 * (total_segments - 1) / segments_per_turn;
  radius = end_radius * pow(start_radius / end_radius, t);

  end_x = radius * cos(angle);
  end_y = radius * sin(angle);
  z = max_thickness;

  // Compute angle and length from (0,0) to spiral end
  len = end_radius - radius - turns + max_width / 2 - min_width; // distance to center

  // Build bridge from center to that point
  translate([radius, 0, z])
    rotate([0, 0, 0])
      cube([len, min_width, max_thickness]);  // not centered
}

// === New disc at the top (for hanging)
module top_attachment_disc() {
  translate([0, 0, max_thickness])
    difference() {
      cylinder(h = max_thickness, r = center_disc_radius, $fn=100);
      translate([0, 0, -1])
        cylinder(h = max_thickness + 2, r = center_hole_radius, $fn=50);
    }
}

// === Reinforce Bridge Joint ===
module reinforce_bridge_joint() {
  t = (total_segments - 1) / total_segments;
  angle_deg = 360 * (total_segments - 1) / segments_per_turn;
  radius = end_radius * pow(start_radius / end_radius, t);
  z = max_thickness;

  // Convert polar to cartesian
  x = radius * cos(angle_deg);
  y = radius * sin(angle_deg);

  // Block dimensions
  block_len = min_width * 1.5;
  block_depth = strip_thickness_y * 2;
  block_height = max_thickness * 2;

  len = end_radius - radius - turns + max_width;

  translate([len - min_width, 0, 0])
    cube([block_len, block_depth, block_height]);
}
