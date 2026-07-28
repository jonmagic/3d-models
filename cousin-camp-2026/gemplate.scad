// Cousin Camp 2026 -- one plate of stones for one headpiece.
//
// Each design's mix differs. Gems arrive in print orientation already, so this
// is purely a batching plate: one print per headpiece in its accent colour
// instead of nine separate jobs.
//
// Use a brim: each stone lands on a small plug face.

design = "crown";           // crown | diadem | tiara
pitch  = 26;

seq =
    design == "crown" ? [    // crown: focal, two rounds, two rounds, four accents
        "9x9",   "8x8",   "8x8",
        "7x7",   "7x7",   "7x4.5",
        "7x4.5", "7x4.5", "7x4.5",
    ]
  : design == "diadem" ? [    // diadem: wide focal, four rounds, four accents
        "14x10", "7x7",   "7x7",
        "7x7",   "7x7",   "7x4.5",
        "7x4.5", "7x4.5", "7x4.5",
    ]
  : [                        // tiara: tall focal, four rounds, two large studs
        "10x13", "7x7",   "7x7",
        "7x7",   "7x7",   "8x8",
        "8x8",
    ];

for (i = [0 : len(seq) - 1])
    translate([(i % 3) * pitch, floor(i / 3) * pitch, 0])
        import(str("out/gem-", seq[i], ".stl"), convexity = 4);
