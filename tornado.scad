// === PARAMETERS ===
turns = 12;
height = 200;
min_radius = 5;
max_radius = 50;
strip_thickness = 1.2;
strip_width = 2.5;
segments_per_turn = 60;
hook_radius = 6;
hook_thickness = 1.5;
bridge_height = 8;

// === FUNNEL SPIRAL (wide → narrow) ===
module funnel_spiral() {
  step_angle = 360 / segments_per_turn;
  total_steps = turns * segments_per_turn;
  z_step = height / total_steps;

  for (i = [0 : total_steps - 2]) {
    angle1 = i * step_angle;
    angle2 = (i + 1) * step_angle;

    r1 = max_radius - (max_radius - min_radius) * (i / total_steps);
    r2 = max_radius - (max_radius - min_radius) * ((i + 1) / total_steps);

    x1 = r1 * cos(angle1);
    y1 = r1 * sin(angle1);
    z1 = height - i * z_step;

    x2 = r2 * cos(angle2);
    y2 = r2 * sin(angle2);
    z2 = height - (i + 1) * z_step;

    hull() {
      translate([x1, y1, z1])
        cube([strip_width, strip_thickness, strip_thickness], center=true);
      translate([x2, y2, z2])
        cube([strip_width, strip_thickness, strip_thickness], center=true);
    }
  }
}

// === RETURN BRIDGE TO CENTER ===
module return_bridge_to_center() {
  steps = 30;
  for (i = [0 : steps - 2]) {
    t1 = i / steps;
    t2 = (i + 1) / steps;

    r1 = max_radius * (1 - t1);
    r2 = max_radius * (1 - t2);

    angle1 = 360 * t1;
    angle2 = 360 * t2;

    x1 = r1 * cos(angle1);
    y1 = r1 * sin(angle1);
    z1 = height + bridge_height * sin(t1 * 180);

    x2 = r2 * cos(angle2);
    y2 = r2 * sin(angle2);
    z2 = height + bridge_height * sin(t2 * 180);

    hull() {
      translate([x1, y1, z1])
        cube([strip_width, strip_thickness, strip_thickness], center=true);
      translate([x2, y2, z2])
        cube([strip_width, strip_thickness, strip_thickness], center=true);
    }
  }
}

// === CENTER HOOK ===
module hook() {
  translate([0, 0, height + bridge_height + 3])
    rotate([90, 0, 0])
      rotate_extrude(angle=300)
        translate([hook_radius, 0])
          square([hook_thickness, hook_thickness]);
}

// === ASSEMBLY ===
funnel_spiral();
return_bridge_to_center();
// hook();
