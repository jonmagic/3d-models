// Cousin Camp 2026 -- parametric headpiece, three distinct forms.
//
// One sweep engine, three silhouettes:
//
//   crown   seven alternating major/minor spikes, tall and regal
//   diadem  one broad low arch on a deep band, wide and elegant
//   tiara   a single dramatic spire with descending scrolls
//
// Heads are ovals, not circles. Sizing a circular ring to circumference/pi
// gives a ring ~20 mm too short front-to-back to pass over the head, so the
// band is swept along a true ellipse solved from the measured circumference.
//
// The whole part is a vertical wall, so there is no overhang anywhere and it
// prints without supports. Points are cosine bumps, which are inherently
// blunt at the tip, and the wall tapers with height so tall points are
// thickest where they would otherwise snap.

// === Parameters ===
design      = "crown"; // crown | diadem | tiara
head_circ   = 550;     // measure the actual head with a soft tape; see README
ease        = 4;       // extra circumference for hair and comfort
cephalic    = 0.78;    // head width / head length

arc_deg     = 200;     // open at the back
stations    = 240;     // sweep resolution

ribbon_d    = 3.2;
ribbon_z    = 5.5;

$fn         = 48;

// === Per-design shape ===
is_crown  = design == "crown";
is_diadem = design == "diadem";

// Detail tracks the age of the wearer. The crown is the tallest and busiest
// piece and suits the oldest; the diadem's broad arch is the sturdiest form
// here; the tiara's spire is shorter, wider and blunter, on a thicker wall,
// with fewer and larger stones, because a tall narrow spike is the wrong thing
// to hand a young child -- it snaps across the layer lines and it sits near
// the face.
t_base = is_crown ? 2.6 : is_diadem ? 2.6 : 2.9;   // wall at the bed
t_tip  = is_crown ? 1.7 : is_diadem ? 1.8 : 2.1;   // wall at the tallest point

// A diadem needs a deep band to read as a band; a tiara wants a shallow one so
// the spire dominates.
band_h = is_diadem ? 20 : is_crown ? 16 : 14;
end_h  = is_diadem ? 13 : 11;

// Soft arch for the diadem, crisp spikes for the crown, blunt for the tiara.
point_sharp = is_diadem ? 1.6 : is_crown ? 2.2 : 2.4;

// Rising points: [centre u, height, half-width in u]
bumps =
    is_crown ? [
        [0.100, 34, 0.062], [0.233, 26, 0.058],
        [0.367, 34, 0.062], [0.500, 46, 0.070],
        [0.633, 34, 0.062], [0.767, 26, 0.058],
        [0.900, 34, 0.062],
    ]
  : is_diadem ? [
        [0.130, 18, 0.075], [0.290, 24, 0.100],
        [0.500, 40, 0.180],
        [0.710, 24, 0.100], [0.870, 18, 0.075],
    ]
  : [
        [0.280, 22, 0.075], [0.395, 29, 0.075],
        [0.500, 38, 0.115],
        [0.605, 29, 0.075], [0.720, 22, 0.075],
    ];

// Gems: [u, centre height, width, height]. Width is horizontal on the head.
// The crown gets bold rounds, the diadem a wide horizontal focal over a row of
// band accents, the tiara a tall vertical focal and larger stones throughout --
// small press-fit parts are the ones a young child loses.
gems =
    is_crown ? [
        [0.500, 19.0, 9.0, 9.0],
        [0.367, 17.0, 8.0, 8.0], [0.633, 17.0, 8.0, 8.0],
        [0.100, 16.0, 7.0, 7.0], [0.900, 16.0, 7.0, 7.0],
        [0.233, 13.5, 7.0, 4.5], [0.767, 13.5, 7.0, 4.5],
        [0.167,  7.5, 7.0, 4.5], [0.833,  7.5, 7.0, 4.5],
    ]
  : is_diadem ? [
        [0.500, 24.0, 14.0, 10.0],
        [0.290, 20.0,  7.0,  7.0], [0.710, 20.0, 7.0, 7.0],
        [0.130, 16.0,  7.0,  7.0], [0.870, 16.0, 7.0, 7.0],
        [0.210,  9.0,  7.0,  4.5], [0.790,  9.0, 7.0, 4.5],
        [0.395,  9.0,  7.0,  4.5], [0.605,  9.0, 7.0, 4.5],
    ]
  : [
        [0.500, 20.0, 10.0, 13.0],
        [0.395, 18.5,  7.0,  7.0], [0.605, 18.5, 7.0, 7.0],
        [0.280, 16.0,  7.0,  7.0], [0.720, 16.0, 7.0, 7.0],
        [0.180,  7.5,  8.0,  8.0], [0.820,  7.5, 8.0, 8.0],
    ];

// === Derived ===
// Taken from the bumps so the wall taper never has to be kept in sync by hand.
peak_h = max([for (b = bumps) b[1]]);

// Solve the ellipse whose perimeter equals the measured circumference.
function ram(a, b) = PI * (3*(a+b) - sqrt((3*a+b)*(a+3*b)));
function solve_a(c, lo = 10, hi = 300, n = 60) =
    n == 0 ? (lo+hi)/2
           : (ram((lo+hi)/2, cephalic*(lo+hi)/2) < c
                ? solve_a(c, (lo+hi)/2, hi, n-1)
                : solve_a(c, lo, (lo+hi)/2, n-1));

a_len = solve_a(head_circ + ease);   // semi-axis front-to-back
b_wid = cephalic * a_len;            // semi-axis side-to-side

t0 = -arc_deg/2;
function theta(u) = t0 + u*arc_deg;

// Smooth bump, zero slope at the apex, so no point is ever sharp.
// point_sharp trades silhouette crispness against tip bluntness.
function bumpf(x) = abs(x) >= 1 ? 0 : pow((1 + cos(180*x)) / 2, point_sharp);

// Band drops to end_h at the open ends so the ribbon tabs stay low.
function bandtop(u) =
    lookup(u, [[0, end_h], [0.09, band_h], [0.91, band_h], [1, end_h]]);

function hgt(u) = max(concat(
    [bandtop(u)],
    [for (b = bumps) bandtop(u) + (b[1] - band_h) * bumpf((u - b[0]) / b[2])]
));

// Wall thins with height: strongest at the base, refined at the tips.
function t_at(u) =
    let (f = (hgt(u) - band_h) / (peak_h - band_h))
    t_base + (t_tip - t_base) * max(0, min(1, f));

function ctr(u) = [b_wid*sin(theta(u)), a_len*cos(theta(u))];
function nrm(u) = let (n = [a_len*sin(theta(u)), b_wid*cos(theta(u))]) n / norm(n);

// === Assembly ===
// Guarded so assembly.scad can include this file and re-draw it in colour.
show_crown = true;
if (show_crown) crown();

module crown() {
    difference() {
        band();
        gem_holes();
        ribbon_holes();
    }
}

// Swept trapezoidal section: four vertices per station, quads between
// stations, and a cap at each open end.
module band() {
    us = [for (i = [0:stations]) i/stations];

    pts = [
        for (u = us) let (c = ctr(u), n = nrm(u), z = hgt(u),
                          hb = t_base/2, ht = t_at(u)/2)
        each [
            [c.x - n.x*hb, c.y - n.y*hb, 0],
            [c.x + n.x*hb, c.y + n.y*hb, 0],
            [c.x + n.x*ht, c.y + n.y*ht, z],
            [c.x - n.x*ht, c.y - n.y*ht, z],
        ]
    ];

    faces = concat(
        [[0, 1, 2, 3]],
        [for (i = [0:stations-1], k = [0:3])
            let (j = (k+1) % 4)
            [i*4+k, (i+1)*4+k, (i+1)*4+j, i*4+j]],
        [[stations*4+3, stations*4+2, stations*4+1, stations*4+0]]
    );

    polyhedron(points = pts, faces = faces, convexity = 8);
}

// Holes are drilled along the local outward normal so they stay round.
module at_station(u, z) {
    c = ctr(u);
    n = nrm(u);
    translate([c.x, c.y, z])
        rotate([0, 0, atan2(n.y, n.x)])
            rotate([0, 90, 0])
                children();
}

// After at_station, local X points down the head and local Y runs tangentially,
// so scaling X sets the stone's vertical size and Y its horizontal size.
module gem_holes() {
    for (g = gems)
        at_station(g[0], g[1])
            scale([g[3], g[2], 1])
                cylinder(h = t_base*6, d = 1, center = true, $fn = 64);
}

module ribbon_holes() {
    for (u = [0.022, 0.978])
        at_station(u, ribbon_z)
            cylinder(h = t_base*6, d = ribbon_d, center = true);
}
