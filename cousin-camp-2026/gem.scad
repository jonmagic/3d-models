// Cousin Camp 2026 -- press-fit gem for the crown.
//
// Seats into the crown's stone holes. The plug is a straight cylinder rather
// than a taper: a taper wedges at an unpredictable depth and leaves the lip
// standing proud, whereas a straight plug always seats flush and the crush
// ribs supply the grip. A drop of glue is optional insurance, not required.
//
// Sizing is split deliberately. The footprint scales to whatever oval the
// crown asks for, but the plug keeps its absolute height so it always reaches
// through the band wall, and the faceted top scales by the SMALLER of the two
// footprint dimensions so small accent stones stay flat instead of becoming
// spikes.
//
// Printed plug-down. Nothing exceeds a 45 degree overhang, so no supports --
// but use a brim, the footprint is small.

// === Parameters ===
gem_w     = 8.0;    // horizontal size on the head; must match crown.scad gems[]
gem_h     = 8.0;    // vertical size on the head
nominal   = 8.0;    // the size this stone is modelled at before scaling

plug_d    = 7.7;    // clearance fit through a nominal 8 mm hole
plug_h    = 2.2;    // just under the band wall, so nothing protrudes inside

rib_n     = 4;      // crush ribs that grip the hole
rib_out   = 0.35;
rib_w     = 0.9;

lip_d     = 11.0;   // seats against the crown face
lip_h     = 0.6;
chamfer_h = 1.6;    // 45 degrees from plug up to lip

facets    = 8;      // octagonal, like a cut stone
top_h     = 5.0;    // keeps the crown facets at ~43 degrees
top_tip   = 1.8;    // blunt -- this sits near a child's forehead

$fn       = 48;

// === Derived ===
// X is vertical on the head, Y is horizontal, matching the crown's hole frame.
sx   = gem_h / nominal;
sy   = gem_w / nominal;
sz   = min(gem_w, gem_h) / nominal;
seat = plug_h + chamfer_h + lip_h;

// === Assembly ===
gem();

module gem() {
    scale([sx, sy, 1]) seat_body();
    translate([0, 0, seat - 0.01])
        scale([sx, sy, sz])
            cylinder(h = top_h + 0.01, d1 = lip_d, d2 = top_tip, $fn = facets);
}

module seat_body() {
    plug();
    translate([0, 0, plug_h - 0.01])
        cylinder(h = chamfer_h + 0.01, d1 = plug_d, d2 = lip_d);
    translate([0, 0, plug_h + chamfer_h - 0.01])
        cylinder(h = lip_h + 0.02, d = lip_d);
}

module plug() {
    cylinder(h = plug_h, d = plug_d);
    for (i = [0 : rib_n - 1])
        rotate([0, 0, i * 360 / rib_n])
            rib();
}

// Rib ramps out from flush to full height over the first 0.6 mm, so the gem
// enters the hole square before the ribs start to bite.
module rib() {
    w    = 0.4 + rib_out;
    x    = plug_d/2 - 0.2;
    lead = 0.6;
    hull() {
        translate([x, -rib_w/2, lead]) cube([w, rib_w, plug_h - lead]);
        translate([x, -rib_w/2, 0])    cube([w - rib_out, rib_w, 0.01]);
    }
}
