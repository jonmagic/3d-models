// Cousin Camp 2026 -- five-finger piano keyboard.
//
// C D E F G with C#, D# and F#: a real pentascale, and the exact hand position
// a beginner learns first. Key width is true piano scale (23.5 mm) because that
// is the whole point -- a child can put an actual hand down on it. Key *length*
// is shortened; a real 145 mm white key would double the print for no gain in
// how it reads.
//
// Two prints, two colours, no MMU:
//   part = "chassis"  black -- bed, cheeks, back rail, and the three sharps
//   part = "keys"     silver -- five naturals that press onto the chassis pegs
//
// The sharps are part of the chassis because they are the same colour as it.
// That turns what looks like a nine-piece assembly into two prints.

part = "chassis";           // chassis | keys | assembly
material = "PLA";           // PLA | PETG -- chassis material; sets the press fit

// The keys are silver PLA either way, so material only ever changes the peg
// side of the fit. See the press fit block below for what it moves and why.

// === Piano geometry ===
w        = 23.5;            // white key width, true scale
b        = 13.7;            // black key width, true scale
key_len  = 95;              // white key length (real is ~145; shortened)
blk_len  = 62;              // black key length, same 0.65 ratio as a real board
key_t    = 8;               // white key thickness
blk_rise = 9;               // how far the sharps stand above the naturals
gap      = 1.0;             // visible air between adjacent keys

// === Chassis ===
bed_t    = 3.6;             // base plate; sized so the rail top lands on a layer
cheek_w  = 5;               // side blocks framing the keyboard
rail_d   = 15;              // back rail, doubles as the name plate
label    = "PIANO";         // set to the recipient's name with -D label="..."
label_h  = 7;               // text cap height
label_t  = 1.2;             // raised 6 layers, so it can be a colour change

// The nameplate is the only geometry above rail_z, which is deliberate. Insert a
// single colour change at that height in PrusaSlicer and the label comes out
// silver to match the keys, for one tool swap and essentially no purge.
// Everything below it stays black. rail_z is a whole multiple of 0.2 mm so the
// change lands exactly on a layer boundary.
//
// That trick is PLA-only. On a PETG chassis the swap would feed silver PLA
// through a 240 C nozzle over an 85 C bed, which jams rather than prints. A PETG
// chassis gets a black-on-black nameplate unless there is silver PETG to change
// to. The geometry is unaffected either way.

// === Press fit ===
// Same trick as the crown gems: a straight peg plus crush ribs seats flush,
// where a taper wedges at an unpredictable depth and leaves the key proud.
// UNCALIBRATED for this printer -- this is the first number to adjust.
//
// PETG needs its own numbers, and not because of shrinkage. Two things change.
// It lays a wider bead than PLA, so a peg modelled at 4.7 comes off the bed
// fatter. And it is ductile: where a PLA rib shaves down to size on the way in,
// a PETG rib folds over and keeps pushing outward. The key it is pushing into
// is brittle PLA. Left at PLA numbers the peg either refuses to seat or splits
// the key, and the key is the part that is hard to reprint.
//
// So the PETG column takes 0.35 mm out of the modelled interference -- 0.15 off
// the peg to cancel the extra bead width, 0.10 off each rib because the ribs no
// longer give. The hole is untouched; the keys do not change.
//
//                 PLA    PETG
//   peg_d         4.70   4.55
//   rib_t         0.30   0.20
//   over hole     +0.30  -0.05   (rib envelope vs the 5.0 hole)
//
// PETG is the tougher choice for the sharps, which stand 17 mm off the bed on a
// 13.7 mm footprint and are the obvious thing to snap.
petg     = material == "PETG";
peg_d    = petg ? 4.55 : 4.7;
peg_h    = 5.0;
hole_d   = 5.0;             // keys are PLA in both versions, so this never moves
hole_h   = 5.6;             // deeper than the peg, so the key lands on the bed
rib_t    = petg ? 0.2 : 0.3;
rib_n    = 4;

$fn = 48;
eps = 0.01;

// === Derived layout ===
// Sharps sit where the white tails divide evenly. In the C-D-E group three
// tails share the width left over by two sharps; in F-G-A-B it is four tails
// and three sharps. Only F# of that second group is on this keyboard.
t_cde = (3 * w - 2 * b) / 3;
t_fg  = (4 * w - 3 * b) / 4;

sharps = [
    [t_cde,             t_cde + b],              // C#
    [2 * t_cde + b,     2 * t_cde + 2 * b],      // D#
    [3 * w + t_fg,      3 * w + t_fg + b],       // F#
];

// [front x0, front x1, tail x0, tail x1] before the visual gap is taken out
naturals = [
    [0 * w, 1 * w, 0 * w,        sharps[0][0]],  // C
    [1 * w, 2 * w, sharps[0][1], sharps[1][0]],  // D
    [2 * w, 3 * w, sharps[1][1], 3 * w       ],  // E
    [3 * w, 4 * w, 3 * w,        sharps[2][0]],  // F
    [4 * w, 5 * w, sharps[2][1], 5 * w       ],  // G
];

board_w  = 5 * w;
front_d  = key_len - blk_len;       // depth over which every natural is full width
total_w  = board_w + 2 * cheek_w;
total_d  = key_len + rail_d;
rail_z   = bed_t + key_t + blk_rise;

// === Assembly ===
if      (part == "chassis") chassis();
else if (part == "keys")    key_plate();
else                        assembly();

// Colour preview. This is the only view that shows whether the naturals and the
// sharps actually read as a keyboard rather than as a tray with ribs in it.
module assembly() {
    color("dimgray") chassis();
    color("silver")
        for (n = naturals) translate([0, 0, bed_t]) natural(n);
}

// === Chassis ===

module chassis() {
    difference() {
        union() {
            // Bed, cheeks and back rail as one solid frame.
            translate([-cheek_w, 0, 0]) cube([total_w, total_d, bed_t]);
            translate([-cheek_w, 0, 0]) cube([cheek_w, total_d, rail_z]);
            translate([board_w, 0, 0]) cube([cheek_w, total_d, rail_z]);
            translate([-cheek_w, key_len, 0]) cube([total_w, rail_d, rail_z]);

            for (s = sharps) sharp(s[0], s[1]);
            for (n = naturals) pegs(n);
        }
        // Nothing to remove; the difference wrapper is here so the label can be
        // switched to an engraving by moving the next line inside it.
    }
    nameplate();
}

// A sharp rises straight off the bed. Its front face is a plain vertical wall,
// which is what a real black key looks like from the player's side.
module sharp(x0, x1) {
    translate([x0, key_len - blk_len, bed_t - eps])
        cube([x1 - x0, blk_len, key_t + blk_rise + eps]);
}

module pegs(n) {
    peg((n[0] + n[1]) / 2, front_d / 2);
    peg((n[2] + n[3]) / 2, (front_d + key_len) / 2);
}

module peg(x, y) {
    translate([x, y, bed_t - eps]) {
        cylinder(d = peg_d, h = peg_h + eps);
        // Full interference down the peg, relieved over the top 0.6 mm so the
        // key finds the peg square before it starts to crush anything.
        for (i = [0 : rib_n - 1])
            rotate([0, 0, i * 360 / rib_n])
                hull() {
                    translate([peg_d / 2 - 0.4, -0.5, 0])
                        cube([0.4 + rib_t, 1.0, peg_h - 0.6]);
                    translate([peg_d / 2 - 0.4, -0.5, peg_h - 0.1])
                        cube([0.4, 1.0, 0.1]);
                }
    }
}

// Raised on the top face of the back rail, where a piano puts its maker's name.
module nameplate() {
    translate([board_w / 2, key_len + rail_d / 2, rail_z - eps])
        linear_extrude(label_t + eps)
            text(label, size = label_h, halign = "center", valign = "center",
                 font = "Liberation Sans:style=Bold", spacing = 1.15);
}

// === Keys ===

// Printed flat on their own bottoms. The peg holes bridge at 5 mm, which is
// nothing, and a flat bottom face matters more because it sets how the key sits.
module key_plate() {
    for (i = [0 : len(naturals) - 1])
        translate([i * (w + 3) - naturals[i][0], 0, 0])
            natural(naturals[i]);
}

module natural(n) {
    g = gap / 2;
    difference() {
        union() {
            translate([n[0] + g, 0, 0])
                cube([n[1] - n[0] - gap, front_d + eps, key_t]);
            translate([n[2] + g, front_d, 0])
                cube([n[3] - n[2] - gap, key_len - front_d, key_t]);
        }
        translate([(n[0] + n[1]) / 2, front_d / 2, -eps])
            cylinder(d = hole_d, h = hole_h + eps);
        translate([(n[2] + n[3]) / 2, (front_d + key_len) / 2, -eps])
            cylinder(d = hole_d, h = hole_h + eps);
    }
}
