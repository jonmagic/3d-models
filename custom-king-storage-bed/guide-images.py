#!/usr/bin/env python3
"""Generate the dimensioned SVG construction diagrams used by the build guide."""

from html import escape
from pathlib import Path

from design import (
    ADAPTER_PANEL_THICKNESS,
    CENTER_MODULE_WIDTH,
    CROSSMEMBER_DEPTH,
    CROSSMEMBER_NOTCH_CLEARANCE,
    CROSSMEMBER_WIDTH,
    DRAWER_FACE_HEIGHT,
    FLOOR_CLEARANCE,
    FRAME_WIDTH,
    MODULE_LENGTH,
    OVERALL_LENGTH,
    PEDESTAL_HEIGHT,
    SERVICE_OPENING_WIDTH,
    SIDE_MODULE_WIDTH,
    SLEEP_SYSTEM_X,
    STRUCTURAL_FRAME_WIDTH,
    STRUCTURAL_LENGTH,
    STRUCTURAL_PLYWOOD_THICKNESS,
    STRUCTURAL_SUPPORT_SIZE,
    SUPPORT_PAD_THICKNESS,
)

OUT = Path(__file__).parent / "guide-assets" / "steps"
W, H = 1200, 720


class SVG:
    def __init__(self, title, subtitle):
        self.title = title
        self.subtitle = subtitle
        self.items = []

    def rect(self, x, y, w, h, fill="#dbeafe", stroke="#334155", sw=3, rx=4, label=None):
        self.items.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
        )
        if label:
            self.text(x + w / 2, y + h / 2 + 7, label, anchor="middle", size=22, weight=700)

    def line(self, x1, y1, x2, y2, stroke="#334155", sw=3, dash=None, arrow=False):
        attrs = f' stroke-dasharray="{dash}"' if dash else ""
        marker = ' marker-end="url(#arrow)"' if arrow else ""
        self.items.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"{attrs}{marker}/>'
        )

    def circle(self, cx, cy, r, fill="#fff", stroke="#334155", sw=3):
        self.items.append(
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
        )

    def text(self, x, y, value, anchor="start", size=22, weight=500, fill="#0f172a"):
        self.items.append(
            f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="system-ui,-apple-system,sans-serif" font-size="{size}" font-weight="{weight}" fill="{fill}">{escape(str(value))}</text>'
        )

    def dim(self, x1, y1, x2, y2, value, offset=0):
        vertical = abs(x2 - x1) < abs(y2 - y1)
        if vertical:
            x1 += offset
            x2 += offset
            self.line(x1, y1, x2, y2, "#2563eb", 2)
            self.line(x1 - 8, y1, x1 + 8, y1, "#2563eb", 2)
            self.line(x2 - 8, y2, x2 + 8, y2, "#2563eb", 2)
            self.text(x1 + 14, (y1 + y2) / 2 + 7, value, size=19, weight=700, fill="#1d4ed8")
        else:
            y1 += offset
            y2 += offset
            self.line(x1, y1, x2, y2, "#2563eb", 2)
            self.line(x1, y1 - 8, x1, y1 + 8, "#2563eb", 2)
            self.line(x2, y2 - 8, x2, y2 + 8, "#2563eb", 2)
            self.text((x1 + x2) / 2, y1 - 10, value, anchor="middle", size=19, weight=700, fill="#1d4ed8")

    def callout(self, x, y, lines, color="#fff7ed", border="#c2410c"):
        width = 350
        height = 42 + 28 * len(lines)
        self.rect(x, y, width, height, color, border, 3, 10)
        for index, line in enumerate(lines):
            self.text(x + 18, y + 34 + index * 28, line, size=18, weight=600)

    def save(self, name):
        body = "\n".join(self.items)
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
<title id="title">{escape(self.title)}</title>
<desc id="desc">{escape(self.subtitle)}</desc>
<defs>
  <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#334155"/></marker>
  <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#cbd5e1" stroke-width="1"/></pattern>
</defs>
<rect width="1200" height="720" fill="#f8fafc"/>
<rect x="24" y="24" width="1152" height="672" rx="18" fill="url(#grid)" stroke="#cbd5e1" stroke-width="2"/>
<text x="60" y="72" font-family="system-ui,-apple-system,sans-serif" font-size="30" font-weight="800" fill="#0f172a">{escape(self.title)}</text>
<text x="60" y="104" font-family="system-ui,-apple-system,sans-serif" font-size="19" font-weight="500" fill="#475569">{escape(self.subtitle)}</text>
{body}
</svg>
"""
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / name).write_text(svg)


def room_survey():
    s = SVG("1. Verify the room and delivery route", "Tape the complete moving envelope, not only the closed bed.")
    s.rect(210, 155, 576, 456, "#e2e8f0", label="96 x 76 in closed bed")
    s.rect(114, 155, 96, 456, "#fef3c7", "#a16207", label="pod")
    s.rect(786, 155, 96, 456, "#fef3c7", "#a16207", label="pod")
    s.line(210, 155, 786, 155, "#b91c1c", 5)
    s.text(498, 145, "wall datum", anchor="middle", size=20, weight=800, fill="#b91c1c")
    s.dim(210, 630, 786, 630, f"{OVERALL_LENGTH:.0f} in", 0)
    s.dim(900, 155, 900, 611, f"{FRAME_WIDTH:.0f} in", 0)
    s.callout(835, 205, ["Mark drawer extension", "Mark 16 in pod sweep", "Photograph all four sides"])
    s.save("01-room-survey.svg")


def material_coupons():
    s = SVG("2. Qualify material and make coupons", "Measure the actual sheet and prove both joints before final routing.")
    s.rect(90, 185, 320, 230, "#f5deb3", label="structural plywood")
    for x, y in ((115, 210), (380, 210), (115, 390), (380, 390), (250, 300)):
        s.circle(x, y, 9, "#2563eb", "#1d4ed8")
    s.text(250, 455, "10 thickness readings per sheet", anchor="middle", size=20, weight=700)
    s.rect(510, 250, 260, 95, "#f5deb3", label="wall coupon")
    s.rect(510, 345, 260, 75, "#fde68a", label="bottom")
    s.line(510, 345, 770, 345, "#dc2626", 6)
    s.text(640, 445, "Glue + screw; inspect after cure", anchor="middle", size=19, weight=700)
    s.rect(850, 215, 80, 260, "#a78bfa", label="2-ply")
    s.rect(835, 200, 110, 290, "none", "#2563eb", 3)
    s.dim(850, 510, 930, 510, f"{CROSSMEMBER_WIDTH:.4f} in nominal", 0)
    s.callout(805, 530, ["Route notch from coupon", f"Start near +{CROSSMEMBER_NOTCH_CLEARANCE:.4f} in", "Final fit must be measured"])
    s.save("02-material-coupons.svg")


def support_detail():
    s = SVG("3. Fabricate the seventeen floor supports", "Keep the full wood footprint on the LVP and capture it in both axes without point feet.")
    s.rect(410, 190, 250, 315, "#92400e", "#78350f", label=f"{STRUCTURAL_SUPPORT_SIZE:.1f} x {STRUCTURAL_SUPPORT_SIZE:.1f}")
    s.rect(410, 505, 250, 15, "#475569", label=None)
    s.rect(365, 180, 35, 350, "#d97706", label=None)
    s.rect(670, 180, 35, 350, "#d97706", label=None)
    s.rect(330, 145, 410, 35, "#f5deb3", label="module bottom")
    s.dim(750, 180, 750, 520, f"{FLOOR_CLEARANCE:.0f} in total", 0)
    s.dim(410, 555, 660, 555, f"{STRUCTURAL_SUPPORT_SIZE:.1f} in", 0)
    s.callout(80, 215, [f"{SUPPORT_PAD_THICKNESS:.4f} in provisional pad", "Nearly full-face contact", "LVP approval required"])
    s.callout(790, 270, ["Four-sided capture", "1/16 in side clearance", "Shim only above block"])
    s.save("03-support-detail.svg")


def panel_breakdown():
    s = SVG("4. Break down and label the structural panels", "Cut oversize, establish one reference edge, then finish-cut and label.")
    s.rect(90, 160, 650, 440, "#f5deb3", label="23/32 in structural sheet")
    for x in (270, 475, 635):
        s.line(x, 160, x, 600, "#2563eb", 4, "12 8")
    for y in (315, 455):
        s.line(90, y, 740, y, "#2563eb", 4, "12 8")
    labels = ["bottoms", "walls", "bulkheads", "rails", "crossmember strips", "coupons"]
    positions = [(180, 240), (370, 240), (570, 240), (180, 395), (420, 395), (670, 535)]
    for label, (x, y) in zip(labels, positions):
        s.text(x, y, label, anchor="middle", size=19, weight=700)
    s.callout(790, 175, ["Blue tape labels:", "LH-1, CH-1, RH-1", "LF-1, CF-1, RF-1"])
    s.callout(790, 410, ["Mark face + grain", "Keep paired parts together", "Do not cut adapter yet"])
    s.save("04-panel-breakdown.svg")


def routed_joinery():
    s = SVG("5. Route dados, rabbets, and crossmember seats", "Use one reference face and the approved full-thickness coupon.")
    s.rect(155, 380, 730, 110, "#f5deb3", label="module wall")
    s.rect(450, 225, 145, 265, "#a78bfa", label="crossmember")
    s.line(435, 380, 435, 490, "#dc2626", 4, "10 8")
    s.line(610, 380, 610, 490, "#dc2626", 4, "10 8")
    s.dim(450, 535, 595, 535, f"{CROSSMEMBER_WIDTH:.4f} in + verified clearance", 0)
    s.dim(930, 225, 930, 490, f"{CROSSMEMBER_DEPTH:.1f} in", 0)
    s.callout(70, 150, ["Template references", "the same face on", "every repeated part"])
    s.callout(760, 145, ["Seat by hand", "No hammering", "No visible side play"])
    s.save("05-routed-joinery.svg")


def center_modules():
    s = SVG("6. Assemble the two center modules", "The center beam carries the split-base seam; the head module preserves service access.")
    s.rect(105, 180, 435, 350, "#bae6fd", label="head-center module")
    s.rect(660, 180, 435, 350, "#bbf7d0", label="foot-center module")
    s.rect(305, 180, 40, 350, "#7dd3fc", label="beam")
    s.rect(860, 180, 40, 350, "#86efac", label="beam")
    s.rect(105, 380, 90, 90, "#f8fafc", "#dc2626", 4, label="service")
    s.dim(105, 575, 540, 575, f"{MODULE_LENGTH:.3f} in", 0)
    s.dim(585, 180, 585, 530, f"{CENTER_MODULE_WIDTH:.2f} in", 0)
    s.callout(400, 575, [f"Service opening: {SERVICE_OPENING_WIDTH:.0f} in", "Keep glue and screws clear", "Confirm beam starts beyond notch"])
    s.save("06-center-modules.svg")


def side_modules():
    s = SVG("7. Build one master side module, then copy it", "Raised full-depth carrier webs support slides while preserving the seam-bolt socket corridor below.")
    s.rect(120, 170, 760, 370, "#bae6fd", label="master side module")
    for x in (150, 490, 850):
        s.rect(x, 170, 30, 370, "#7dd3fc", label=None)
    for x in (205, 465, 535, 795):
        s.rect(x, 245, 18, 220, "#d97706", label=None)
    s.rect(150, 205, 700, 35, "#f5deb3", label="outer top rail")
    s.rect(150, 470, 700, 35, "#f5deb3", label="bottom")
    s.rect(255, 270, 210, 155, "#fed7aa", label="drawer bay 1")
    s.rect(535, 270, 210, 155, "#fed7aa", label="drawer bay 2")
    s.dim(120, 590, 880, 590, f"{MODULE_LENGTH:.3f} in", 0)
    s.dim(930, 170, 930, 540, f"{SIDE_MODULE_WIDTH:.2f} in", 0)
    s.callout(820, 240, ["Fit 4 carrier webs", "Keep socket path below", "Dry-seat three stations"])
    s.save("07-side-modules.svg")


def support_grid():
    s = SVG("8. Lay out the 17-support grid and set six modules", "Station A supports both split members; stations B-E use left, center, and right supports.")
    s.rect(80, 145, 680, 470, "#e2e8f0", label=None)
    station_xs = (90, 255, 420, 585, 750)
    for label, x in zip(("A", "B", "C", "D", "E"), station_xs):
        if label == "A":
            s.rect(x, 145, 20, 198, "#a78bfa", label=None)
            s.rect(x, 417, 20, 198, "#a78bfa", label=None)
            support_ys = (170, 330, 430, 590)
        else:
            s.rect(x, 145, 20, 470, "#a78bfa", label=None)
            support_ys = (170, 380, 590)
        for y in support_ys:
            s.rect(x - 17, y - 27, 54, 54, "#92400e", label=None)
        if label == "A":
            s.rect(x + 3, 353, 54, 54, "#92400e", label=None)
        s.text(x + 10, 130, label, anchor="middle", size=18, weight=800)
    s.line(420, 145, 420, 615, "#dc2626", 5, "14 10")
    s.line(80, 317, 760, 317, "#334155", 3)
    s.line(80, 443, 760, 443, "#334155", 3)
    s.text(420, 640, "midpoint module seam", anchor="middle", size=20, weight=800, fill="#b91c1c")
    s.callout(790, 155, ["A Y=0 block: X 3.8125-7.3125", "A: Y -33.25, -8, 0, 8, 33.25", "B-E: Y -33.25, 0, 33.25"])
    s.callout(790, 440, ["Four cleats per block", "Check every edge bears", "6 modules last"])
    s.save("08-support-grid.svg")


def seam_connection():
    s = SVG("9. Align and bolt the midpoint seams", "Alignment features establish position; bolts clamp paired bulkheads.")
    s.rect(180, 210, 260, 300, "#bae6fd", label="head bulkhead")
    s.rect(460, 210, 260, 300, "#bbf7d0", label="foot bulkhead")
    for y in (275, 360, 445):
        s.line(145, y, 755, y, "#64748b", 8)
        s.circle(150, y, 16, "#cbd5e1")
        s.circle(750, y, 16, "#cbd5e1")
    for y in (315, 405):
        s.circle(450, y, 14, "#f59e0b", "#92400e")
    s.dim(180, 560, 720, 560, "paired bulkheads clamped flush", 0)
    s.callout(790, 190, ["3 bolts per side pair", "2 bolts at center pair", "8 total at midpoint"])
    s.callout(790, 420, ["Large washers", "Tool access from drawers", "Do not bury hardware"])
    s.save("09-seam-connection.svg")


def crossmembers():
    s = SVG("10. Laminate, fit, label, and retain crossmembers", "Five load stations use six physical pieces because station A is split.")
    s.rect(120, 185, 850, 65, "#c4b5fd", label="two glued plywood laminations")
    s.rect(120, 300, 850, 65, "#a78bfa", label="finished laminated member")
    s.rect(330, 430, 430, 110, "#f5deb3", label="receiving notch")
    s.rect(470, 365, 150, 175, "#a78bfa", label="member")
    s.dim(120, 275, 970, 275, "full station width; head station is split", 0)
    s.dim(1030, 365, 1030, 540, f"{CROSSMEMBER_DEPTH:.1f} in", 0)
    s.callout(75, 565, ["Label A-L, A-R, B, C, D, E", "Dry-fit before hold-downs"])
    s.callout(760, 565, ["Retain against uplift", "Fasten into face-grain cleats", "Keep removable"])
    s.save("10-crossmembers.svg")


def chassis_checks():
    s = SVG("11. Square, level, and rack-test the chassis", "Record measurements before finish panels hide the structure.")
    s.rect(180, 170, 720, 420, "#dbeafe", label="assembled lower chassis")
    s.line(180, 170, 900, 590, "#dc2626", 5)
    s.line(900, 170, 180, 590, "#2563eb", 5)
    s.dim(180, 625, 900, 625, "diagonals equal within approved tolerance", 0)
    s.line(115, 550, 965, 550, "#16a34a", 5)
    s.text(540, 540, "level reference", anchor="middle", size=20, weight=800, fill="#15803d")
    s.callout(790, 210, ["Push at each corner", "Recheck diagonals", "Inspect every support"])
    s.save("11-chassis-checks.svg")


def powerflex_measurement():
    s = SVG("12. Measure each delivered Power-Flex half", "The law label and full articulation envelope control the adapter.")
    s.rect(135, 260, 760, 105, "#94a3b8", label="stationary base frame")
    s.rect(230, 195, 180, 65, "#fb923c", label="motor")
    s.rect(610, 195, 165, 65, "#fb923c", label="control")
    s.line(135, 365, 85, 165, "#334155", 8)
    s.line(895, 365, 970, 140, "#334155", 8)
    for x, label in ((180, "bearing"), (470, "factory hole"), (840, "bearing")):
        s.circle(x, 315, 14, "#22c55e", "#15803d")
        s.text(x, 405, label, anchor="middle", size=18, weight=700)
    s.callout(75, 455, ["Photograph law label", "Measure both halves", "Mark stationary contact only"])
    s.callout(770, 455, ["Cycle flat/head/foot", "Map moving no-go zones", "Map cords and service"])
    s.save("12-powerflex-measurement.svg")


def adapter_lattice():
    s = SVG("13. Transfer the base map to removable adapters", "Each 1/4-inch panel becomes a field-fitted lattice with replaceable backing.")
    s.rect(110, 155, 760, 450, "#94a3b8", label=None)
    s.rect(180, 210, 620, 340, "#f8fafc", "#dc2626", 4, label="cutout / no-go zone")
    for x in (150, 450, 830):
        s.rect(x, 155, 40, 450, "#64748b", label=None)
    for y in (180, 385, 565):
        s.rect(110, y, 760, 35, "#64748b", label=None)
    s.circle(245, 360, 17, "#22c55e", "#15803d")
    s.circle(730, 360, 17, "#22c55e", "#15803d")
    s.callout(835, 160, [f"Blank: 84 x 36 x {ADAPTER_PANEL_THICKNESS:.2f} in", "Trace one half per panel", "Cut openings with jigsaw"])
    s.callout(835, 430, ["Backing only at verified holes", "Screw adapter to chassis", "Never drill base frame"])
    s.save("13-adapter-lattice.svg")


def drawers():
    s = SVG("14. Build drawers on independent slide carriers", "Keep hardware off removable crossmembers and preserve midpoint bolt access.")
    s.rect(90, 205, 680, 330, "#bae6fd", label="side module")
    s.rect(150, 270, 240, 190, "#fed7aa", label="drawer box")
    s.rect(465, 270, 240, 190, "#fed7aa", label="drawer box")
    for x in (135, 390, 450, 705):
        s.rect(x, 285, 15, 160, "#64748b", label=None)
    s.rect(120, 260, 25, 210, "#d97706", label=None)
    s.rect(390, 260, 25, 210, "#d97706", label=None)
    s.rect(450, 260, 25, 210, "#d97706", label=None)
    s.rect(720, 260, 25, 210, "#d97706", label=None)
    s.line(770, 205, 770, 535, "#dc2626", 4, "12 8")
    s.circle(770, 345, 13, "#f59e0b", "#92400e")
    s.text(765, 385, "module seam bolt", anchor="end", size=18, weight=800)
    s.callout(800, 180, ["Use hardware's side clearance", "Shim mounting faces flat", "Test disconnect/reinstall"])
    s.callout(800, 430, ["Remove drawer", "Reach every seam bolt", "Then fit overlay front"])
    s.save("14-drawers.svg")


def headboard_modules():
    s = SVG("15. Build and anchor three headboard modules", "The removable wall cleat carries weight and pod overturning; lower bolts locate the cabinet.")
    s.rect(115, 190, 270, 350, "#fde68a", label="left pod module")
    s.rect(395, 155, 410, 385, "#f5deb3", label="center cabinet")
    s.rect(815, 190, 270, 350, "#fde68a", label="right pod module")
    s.line(385, 190, 385, 540, "#dc2626", 4, "12 8")
    s.line(805, 190, 805, 540, "#dc2626", 4, "12 8")
    s.rect(520, 420, 160, 120, "#f8fafc", "#2563eb", 4, label="service bay")
    s.rect(140, 220, 350, 28, "#d97706", label="wall cleat")
    s.rect(710, 220, 350, 28, "#d97706", label="wall cleat")
    s.dim(115, 595, 1085, 595, f"{FRAME_WIDTH:.0f} in finished width", 0)
    s.callout(420, 565, ["Anchor cleat to verified framing", "Lower bolts locate; cleat restrains", "Keep center service route open"])
    s.save("15-headboard-modules.svg")


def pod_cassette():
    s = SVG("16. Build and test each pull-out pod cassette", "End section: both 9308-E16 slides mount vertically on opposite faces of the fixed rail.")
    s.rect(455, 285, 230, 235, "#f5deb3", label="fixed rail")
    s.rect(425, 300, 30, 205, "#64748b", label=None)
    s.rect(685, 300, 30, 205, "#64748b", label=None)
    s.rect(350, 260, 75, 285, "#fde68a", label="moving")
    s.rect(715, 260, 75, 285, "#fde68a", label="moving")
    s.rect(330, 545, 480, 35, "#d6b98c", label="pod module floor + reinforced backing")
    s.text(440, 245, "side-mounted slide", anchor="middle", size=17, weight=800)
    s.text(700, 245, "side-mounted slide", anchor="middle", size=17, weight=800)
    s.line(345, 220, 795, 220, "#dc2626", 4, "12 8")
    s.text(570, 205, "upper anti-rack guide", anchor="middle", size=19, weight=800, fill="#b91c1c")
    s.callout(80, 340, ["Through-bolt rail to floor", "Back both bolt faces", "Check downward + uplift"])
    s.callout(800, 350, ["Slides stay vertical", "Verify lock/release", "No sitting or climbing"])
    s.save("16-pod-cassette.svg")


def finish_panels():
    s = SVG("17. Fit birch skins, fronts, fascia, and edges", "Dry-fit every reveal before finish; visible pieces remain removable where service requires.")
    s.rect(145, 200, 800, 340, "#e2e8f0", label="structural chassis")
    s.rect(120, 185, 25, 370, "#f5deb3", label=None)
    s.rect(945, 185, 25, 370, "#f5deb3", label=None)
    s.rect(120, 555, 850, 28, "#d6b98c", label="foot fascia")
    for x in (165, 355, 545, 735):
        s.rect(x, 285, 160, 150, "#fde68a", label="front")
    s.dim(120, 625, 970, 625, f"{FRAME_WIDTH:.0f} in maximum", 0)
    s.callout(785, 150, ["1/8 in planned front gaps", "Ease and seal all edges", "Finish off the LVP"])
    s.save("17-finish-panels.svg")


def service_routing():
    s = SVG("18. Route power, pump hoses, and moving slack", "Every connection remains visible, ventilated, strain-relieved, and clear of articulation.")
    s.rect(110, 180, 850, 360, "#e2e8f0", label="under-head service zone")
    s.rect(135, 255, 150, 100, "#c4b5fd", label="pump")
    s.rect(380, 255, 155, 100, "#94a3b8", label="base supply")
    s.rect(650, 255, 170, 100, "#94a3b8", label="base supply")
    s.line(210, 255, 210, 145, "#2563eb", 7)
    s.line(460, 255, 460, 145, "#f59e0b", 7)
    s.line(735, 255, 735, 145, "#f59e0b", 7)
    s.line(285, 305, 380, 305, "#334155", 4, "10 8")
    s.line(535, 305, 650, 305, "#334155", 4, "10 8")
    s.callout(790, 385, ["No buried power strips", "Service loops move freely", "Label both base halves"])
    s.save("18-service-routing.svg")


def proof_load():
    s = SVG("19. Proof-load the empty chassis in stages", "Use distributed dead load, pause at each stage, and stop at any change.")
    s.rect(145, 405, 830, 140, "#bae6fd", label="finished lower chassis")
    for x in (220, 380, 540, 700, 860):
        s.rect(x, 320, 90, 85, "#64748b", label="load")
    s.line(145, 585, 975, 585, "#16a34a", 5)
    s.callout(75, 155, ["Stage 1: light distributed load", "Measure level and diagonals", "Inspect joints and LVP"])
    s.callout(425, 155, ["Stage 2: increase evenly", "Pause and listen", "Recheck supports"])
    s.callout(775, 155, ["Stage 3: approved target", "Hold, unload, remeasure", "Stop on noise or movement"])
    s.save("19-proof-load.svg")


def final_install():
    s = SVG("20. Install the sleep system and complete inspection", "Two base halves, mattress, drawers, and pods must move without contact or inaccessible service.")
    s.rect(160, 420, 800, 130, "#d6b98c", label="completed furniture chassis")
    s.rect(225, 355, 335, 65, "#94a3b8", label="left Power-Flex")
    s.rect(560, 355, 335, 65, "#94a3b8", label="right Power-Flex")
    s.rect(225, 245, 670, 110, "#f8fafc", label="72 x 84 in mattress")
    s.rect(160, 135, 800, 110, "#b45309", label="full-width headboard")
    s.dim(1015, 245, 1015, 550, f"{FLOOR_CLEARANCE + PEDESTAL_HEIGHT + ADAPTER_PANEL_THICKNESS + 3 + 11:.2f} in provisional mattress top", 0)
    s.callout(70, 565, ["Cycle both halves", "Open every drawer and pod", "Confirm wall and cable clearance"])
    s.callout(760, 565, ["Retorque after initial use", "Reinspect pads and joints", "Keep service map with guide"])
    s.save("20-final-install.svg")


GENERATORS = [
    room_survey,
    material_coupons,
    support_detail,
    panel_breakdown,
    routed_joinery,
    center_modules,
    side_modules,
    support_grid,
    seam_connection,
    crossmembers,
    chassis_checks,
    powerflex_measurement,
    adapter_lattice,
    drawers,
    headboard_modules,
    pod_cassette,
    finish_panels,
    service_routing,
    proof_load,
    final_install,
]

for generate in GENERATORS:
    generate()

print(f"Generated {len(GENERATORS)} guide diagrams in {OUT}")
