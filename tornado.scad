// === Parameters ===
turns = 12;
segments_per_turn = 60;
total_segments = turns * segments_per_turn;

end_radius = 100;
height = 0;

min_width = 3;
max_width = 8;

min_thickness = 3;
max_thickness = 8;

strip_thickness_y = 1;

center_disc_radius = 6;
center_disc_thickness = min_thickness; // match outer strip height
center_hole_radius = 2.5; // 5mm hole

start_radius = center_hole_radius + 1; // e.g. 3.5mm

// === Assembly ===
spiral_strip_variable_size();
center_attachment_disc();
bridge_to_top_disc_aligned();
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
  radius = start_radius + (end_radius - start_radius) * t;
  z = height * t;

  width = min_width + (max_width - min_width) * t;
  thickness = min_thickness + (max_thickness - min_thickness) * t;

  translate([radius * cos(angle), radius * sin(angle), 0])
    rotate([0, 0, angle])
      cube([width, strip_thickness_y, thickness]);
}

// === Central Disc + Hole ===
module center_attachment_disc() {
  difference() {
    // Disc
    translate([0, 0, 0])
      cylinder(h=center_disc_thickness, r=center_disc_radius, $fn=100);

    // Hole
    translate([0, 0, -1])
      cylinder(h=center_disc_thickness + 2, r=center_hole_radius, $fn=50);
  }
}

// === Bridge from spiral end to center (elevated) ===
module bridge_to_top_disc_aligned() {
  t = 1;
  angle = 360 * (total_segments - 1.35) / segments_per_turn;
  radius = start_radius + (end_radius - start_radius) * t;

  end_x = radius * cos(angle);
  end_y = radius * sin(angle);

  z = max_thickness / 2;

  // ✅ Add buffer to fully intersect spiral edge
  len = sqrt(end_x * end_x + end_y * end_y) + max_width - min_width;

  mid_x = end_x / 2;
  mid_y = end_y / 2;

  translate([mid_x + max_width - min_width, mid_y, z + max_thickness])
    rotate([0, 0, angle])
      cube([len, max_width, max_thickness], center=true);
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
