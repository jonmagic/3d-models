// Cousin Camp 2026 -- colour assembly preview.
//
// This exists to be looked at. The parts list and the slicer numbers say the
// crown is printable; only the picture says it is the right object.
//
// Gems are pulled in from the exported STLs, so what you see here is the
// geometry that will actually be sliced, not a second idealised copy of it.
//
//   scad-render assembly.scad -D 'crown_color="blue"' -D 'gem_color="red"'

include <crown.scad>

show_crown  = false;          // overrides the include; last assignment wins
crown_color = "blue";
gem_color   = "red";

color(crown_color) crown();
color(gem_color)   set_gems();

module set_gems() {
    for (g = gems) {
        file = str("out/gem-", g[2], "x", g[3], ".stl");
        // Lip rests on the outer face, plug points inward, so the gem is
        // flipped to send its +Z along the inward normal.
        at_station(g[0], g[1])
            translate([0, 0, t_at(g[0])/2])
                rotate([180, 0, 0])
                    import(file, convexity = 4);
    }
}
