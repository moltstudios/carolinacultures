#!/usr/bin/env python3
"""Build the Carolina Cultures Co. logo as layered, animatable SVG.
All coordinates measured from the 1024x1024 source raster.
"""
import math
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

DARK = "#174832"
LEAF = "#7ab744"
INK_ON_DARK = "#f4f8f4"   # reversed version for dark backgrounds

def fmt(v):
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s

def smooth_path(pts, closed=False):
    n = len(pts)
    d = [f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"]
    for i in range(n - 1):
        p0 = pts[i - 1] if i > 0 else pts[i]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[i + 2] if i + 2 < n else pts[i + 1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d.append(f"C{fmt(c1[0])} {fmt(c1[1])} {fmt(c2[0])} {fmt(c2[1])} {fmt(p2[0])} {fmt(p2[1])}")
    if closed: d.append("Z")
    return " ".join(d)

def polar(cx, cy, r, deg):
    a = math.radians(deg); return (cx + r * math.cos(a), cy + r * math.sin(a))

def arc_path(cx, cy, r, a0, a1):
    x0, y0 = polar(cx, cy, r, a0); x1, y1 = polar(cx, cy, r, a1)
    sweep = 1 if a1 > a0 else 0; large = 1 if abs(a1 - a0) > 180 else 0
    return f"M{fmt(x0)} {fmt(y0)} A{r} {r} 0 {large} {sweep} {fmt(x1)} {fmt(y1)}"

# ---------------------------------------------------------------- flask
def flask_path(top_y, left_x, collar_y, neck_x, fillet_y_int, diag_dx_dy, corner_c, corner_r, bottom_y, corner_rr):
    C = 513.0; mirror = lambda x: 2 * C - x
    dvec = (-diag_dx_dy, 1.0); dl = math.hypot(*dvec); dvec = (dvec[0] / dl, dvec[1] / dl)
    nvec = (-dvec[1], dvec[0])
    ccx, ccy = corner_c
    tpx, tpy = ccx + corner_r * nvec[0], ccy + corner_r * nvec[1]
    ix, iy = neck_x, fillet_y_int; tl = 43.0
    fs = (neck_x, iy - tl); fe = (ix + dvec[0] * tl, iy + dvec[1] * tl)
    r = corner_rr
    p = [f"M{fmt(left_x + r)} {fmt(top_y)}", f"H{fmt(mirror(left_x + r))}",
         f"A{r} {r} 0 0 1 {fmt(mirror(left_x))} {fmt(top_y + r)}",
         f"V{fmt(collar_y[0])}", f"L{fmt(mirror(neck_x))} {fmt(collar_y[1])}",
         f"V{fmt(fs[1])}", f"Q{fmt(mirror(ix))} {fmt(iy)} {fmt(mirror(fe[0]))} {fmt(fe[1])}",
         f"L{fmt(mirror(tpx))} {fmt(tpy)}", f"A{corner_r} {corner_r} 0 0 1 {fmt(mirror(ccx))} {fmt(bottom_y)}",
         f"H{fmt(ccx)}", f"A{corner_r} {corner_r} 0 0 1 {fmt(tpx)} {fmt(tpy)}",
         f"L{fmt(fe[0])} {fmt(fe[1])}", f"Q{fmt(ix)} {fmt(iy)} {fmt(fs[0])} {fmt(fs[1])}",
         f"V{fmt(collar_y[1])}", f"L{fmt(left_x)} {fmt(collar_y[0])}", f"V{fmt(top_y + r)}",
         f"A{r} {r} 0 0 1 {fmt(left_x + r)} {fmt(top_y)}", "Z"]
    return " ".join(p)

FLASK_OUTER = flask_path(208, 405, (243, 290), 421, 435, 0.57, (303, 823), 85, 908, 10)
FLASK_INNER = flask_path(233, 433, (247, 290), 445, 442, 0.57, (303, 823), 60, 883, 6)

# ---------------------------------------------------------------- vines
STEM = [(492, 768), (485, 750), (483, 730), (490, 702), (503, 680), (514, 660), (521, 640), (523, 620), (522, 600), (522, 580)]
LOOP = [(522, 580), (505, 560), (489, 540), (475, 520), (468, 500), (466, 480), (467, 460), (471, 440), (479, 420),
        (493, 400), (508, 380), (519, 360), (526, 340), (529, 320), (531, 300), (534, 280), (538, 260), (542, 240),
        (548, 220), (555, 200), (564, 180), (575, 165), (590, 152), (614, 147), (636, 152), (652, 166), (663, 180),
        (670, 200), (675, 220), (683, 240), (691, 260), (700, 280), (707, 300), (710, 320), (712, 340), (712, 355),
        (710, 370), (705, 390), (697, 410), (687, 430), (672, 450), (654, 470), (628, 482), (600, 502), (573, 520),
        (551, 540), (537, 560), (522, 580)]
VINE_LEFT = [(480, 523), (465, 519), (450, 512), (430, 504), (410, 496), (390, 488), (370, 482), (350, 483), (330, 483), (310, 486), (293, 493)]
BRANCH_LEFT = [(382, 482), (364, 470), (354, 460), (346, 450), (341, 440), (336, 430), (332, 420), (330, 410), (327, 400),
               (328, 388), (329, 375), (331, 360), (333, 340), (334, 320), (334, 305), (334, 296)]
PETIOLES = {
    "pet-l-mid":   [(326, 390), (312, 380), (301, 370), (290, 361)],
    "pet-l-bud":   [(333, 384), (340, 378), (346, 370), (350, 366)],
    "pet-center":  [(554, 532), (556, 512), (557, 492)],
    "pet-r-big":   [(688, 446), (705, 453), (720, 456), (737, 459)],
    "pet-r-mid":   [(714, 364), (733, 350), (748, 338), (760, 328)],
    "pet-r-upper": [(708, 286), (716, 278), (726, 272), (735, 268)],
    "pet-r-top":   [(654, 176), (662, 164), (670, 152), (674, 146)],
}
VINE_W = {"stem": 13, "loop": 12.5, "vine-left": 11, "branch-left": 9.5}

# ---------------------------------------------------------------- leaves
LEAVES = [  # id, kind, base, tip, width factor
    ("leaf-l-top",   "ovate", (334, 296), (280, 196), 0.99),
    ("leaf-l-mid",   "ovate", (288, 352), (152, 387), 1.15),
    ("leaf-l-bud",   "bud",   (347, 370), (380, 346), 0.66),
    ("leaf-l-big",   "heart", (298, 493), (164, 639), 0.93),
    ("leaf-center",  "ovate", (557, 492), (512, 411), 0.96),
    ("leaf-r-top",   "ovate", (674, 146), (732, 98),  0.79),
    ("leaf-r-upper", "ovate", (735, 268), (795, 147), 1.25),
    ("leaf-r-neck",  "ovate", (698, 352), (633, 348), 0.85),
    ("leaf-r-mid",   "ovate", (760, 323), (847, 358), 0.91),
    ("leaf-r-big",   "heart", (737, 459), (874, 603), 1.02),
]
SHAPES = {
    "ovate": ("M0 0 C3 -18 20 -29 40 -27 C62 -25 88 -12 100 0 C88 12 62 25 40 27 C20 29 3 18 0 0 Z",
              "M4 0 Q52 -2 92 0 M22 0 Q33 -8 43 -18 M22 0 Q33 8 43 18 M46 0 Q57 -6 67 -13 M46 0 Q57 6 67 13 M68 0 Q76 -4 83 -8 M68 0 Q76 4 83 8"),
    "bud":   ("M0 0 C2 -18 18 -30 40 -30 C66 -28 90 -12 100 0 C90 12 66 28 40 30 C18 30 2 18 0 0 Z",
              "M6 0 Q50 -2 90 0"),
    "heart": ("M0 0 C-4 -6 -9 -14 -7 -22 C-5 -34 10 -42 28 -42 C52 -41 82 -24 100 0 C82 24 52 41 28 42 C10 42 -5 34 -7 22 C-9 14 -4 6 0 0 Z",
              "M2 0 Q50 -2 94 0 M8 0 Q4 -12 -1 -22 M8 0 Q4 12 -1 22 M24 0 Q30 -16 36 -32 M24 0 Q30 16 36 32 M46 0 Q56 -11 66 -22 M46 0 Q56 11 66 22 M70 0 Q78 -6 86 -11 M70 0 Q78 6 86 11"),
}

def leaf_markup():
    out = []
    for lid, kind, base, tip, wf in LEAVES:
        dx, dy = tip[0] - base[0], tip[1] - base[1]
        L = math.hypot(dx, dy); ang = math.degrees(math.atan2(dy, dx)); s = L / 100.0
        shape, veins = SHAPES[kind]
        tr = f"translate({fmt(base[0])} {fmt(base[1])}) rotate({fmt(ang)}) scale({s:.3f} {s * wf:.3f})"
        out.append(
            f'    <g id="{lid}" class="leaf" transform="{tr}">\n'
            f'      <g class="leaf-grow">\n'
            f'        <path class="leaf-shape" d="{shape}" fill="{LEAF}" stroke="{DARK}" stroke-width="{9 / s:.2f}" stroke-linejoin="round"/>\n'
            f'        <path class="leaf-veins" d="{veins}" fill="none" stroke="{DARK}" stroke-width="{5 / s:.2f}" stroke-linecap="round"/>\n'
            f'      </g>\n'
            f'    </g>')
    return "\n".join(out)

BUBBLES = [(532, 54, 16, 528, 49, 4.8), (492, 80, 14.5, 488, 75, 4.4), (547, 114, 20, 542, 107, 5.8),
           (468, 137, 26, 460, 128, 7.8), (521, 170, 20, 516, 163, 5.8)]

# ---------------------------------------------------------------- monogram
# Two interlocking C's built as three filled outlines (no strokes, no overlaps):
#   * left C  - ring band that unrolls at the bottom-right into a tapered tail
#               that rises into the right C's counter (apex ~ (557,705))
#   * right C - top arm that unrolls at the upper-left into a tapered swash
#               that drops into the left C's counter (tip ~ (497,765)), plus a
#               separate bottom arc.
# The vine stem passes over the left C's top-right terminal; that gap is a mask.
# Tail edges are tangent-continuous cubics fitted to the source (rms < 0.6px).
RL, RR, RO, RI = (440, 740), (600, 740), 89, 59   # centres, outer/inner radius (band = 30)

def P(c, r, deg):
    return polar(c[0], c[1], r, deg)

def C(*pts):
    return "C" + " ".join(f"{fmt(x)} {fmt(y)}" for x, y in pts)

def A(r, large, sweep, pt):
    return f"A{r} {r} 0 {large} {sweep} {fmt(pt[0])} {fmt(pt[1])}"

def M(pt):
    return f"M{fmt(pt[0])} {fmt(pt[1])}"

def L(pt):
    return f"L{fmt(pt[0])} {fmt(pt[1])}"

APEX_L, TIP_R = (557.5, 704.5), (497, 765)
# fitted tail edges (all written from the ring outwards to the point)
L_OUT = ((463.0, 826.0), (569.3, 797.5), (562.7, 715.7), APEX_L)   # leaves outer circle at 75deg
L_IN  = ((455.3, 797.0), (532.7, 776.2), (517.7, 737.4), APEX_L)   # leaves inner circle at 75deg
R_OUT = ((572.5, 655.4), (514.8, 674.1), (486.2, 722.1), TIP_R)    # leaves outer circle at -108deg
R_IN  = ((580.8, 684.2), (515.6, 706.7), (527.9, 752.5), TIP_R)    # leaves inner circle at -109deg

LEFT_TERM, RIGHT_TERM, RIGHT_BOTTOM_END = -41, 37.5, 138.5   # degrees

C_LEFT = " ".join([
    M(P(RL, RO, LEFT_TERM)), A(RO, 1, 0, L_OUT[0]),      # outer band, the long way round
    C(L_OUT[1], L_OUT[2], L_OUT[3]),                            # tail outer edge up to the apex
    C(L_IN[2], L_IN[1], L_IN[0]),                               # tail inner edge back down
    A(RI, 1, 1, P(RL, RI, LEFT_TERM)), "Z"])                # inner band back to the terminal

C_RIGHT_TOP = " ".join([
    M(P(RR, RO, -RIGHT_TERM)), A(RO, 0, 0, R_OUT[0]),
    C(R_OUT[1], R_OUT[2], R_OUT[3]),
    C(R_IN[2], R_IN[1], R_IN[0]),
    A(RI, 0, 1, P(RR, RI, -RIGHT_TERM)), "Z"])

C_RIGHT_BOTTOM = " ".join([
    M(P(RR, RO, RIGHT_TERM)), A(RO, 0, 1, P(RR, RO, RIGHT_BOTTOM_END)),
    L(P(RR, RI, RIGHT_BOTTOM_END)), A(RI, 0, 0, P(RR, RI, RIGHT_TERM)), "Z"])

STEM_CUT = STEM[2:]          # only the part of the stem that crosses the left C's terminal
STEM_CUT_W = VINE_W["stem"] + 20   # 10px clearance each side, as in the source

# ---------------------------------------------------------------- wordmark
WORDS = [("CAROLINA", 78, 436), ("CULTURES", 462, 808), ("CO.", 835, 945)]
def wordmark_path(baseline=985, cap_px=46, condense=0.95):
    font = instantiateVariableFont(TTFont("fonts/Montserrat.ttf"), {"wght": 700})
    gs = font.getGlyphSet(); cmap = font.getBestCmap(); hmtx = font["hmtx"]
    sy = cap_px / font["OS/2"].sCapHeight; sx = sy * condense
    def bounds(n):
        bp = BoundsPen(gs); gs[n].draw(bp); return bp.bounds
    pen = SVGPathPen(gs, ntos=fmt)
    for word, x0, x1 in WORDS:
        names = [cmap[ord(ch)] for ch in word]; widths = [hmtx[n][0] for n in names]
        lsb = bounds(names[0])[0] * sx; rsb = (widths[-1] - bounds(names[-1])[2]) * sx
        ink = sum(widths) * sx - lsb - rsb
        tracking = ((x1 - x0) - ink) / (len(word) - 1)
        x = x0 - lsb
        for n, w in zip(names, widths):
            gs[n].draw(TransformPen(pen, (sx, 0, 0, -sy, x, baseline))); x += w * sx + tracking
    return pen.getCommands()

# ---------------------------------------------------------------- assemble
# The vines "pass over" the flask walls and the S-link passes over the rings.
# Those gaps are cut with masks (true transparency) rather than painted white,
# so the mark works on any background.  Bubble highlights are real holes too.
ANIM_CSS = """
  @media (prefers-reduced-motion: no-preference) {
    .draw { stroke-dasharray:100; stroke-dashoffset:100; animation:draw var(--d,1s) var(--t,0s) cubic-bezier(.4,0,.3,1) forwards; }
    #flask-outer { --d:1.3s; --t:0s; } #flask-inner { --d:1.3s; --t:.15s; }
    #stem { --d:.7s; --t:1.0s; } #stem-cut { --d:.55s; --t:1.15s; }
    #loop, #loop-cut { --d:2.1s; --t:1.6s; }
    #vine-left, #vine-left-cut { --d:.9s; --t:1.6s; }
    #branch-left { --d:.9s; --t:2.1s; }
    #pet-l-mid, #pet-l-bud { --d:.35s; --t:2.6s; }
    #pet-r-top { --d:.3s; --t:2.75s; }
    #pet-r-upper { --d:.3s; --t:3.0s; }
    #pet-r-mid { --d:.35s; --t:3.15s; }
    #pet-r-big { --d:.35s; --t:3.3s; }
    #pet-center { --d:.3s; --t:3.6s; }
    .leaf-grow { transform:scale(0); animation:grow .7s var(--t,0s) cubic-bezier(.34,1.4,.64,1) forwards; }
    #leaf-l-big .leaf-grow { --t:2.45s; } #leaf-l-mid .leaf-grow { --t:2.75s; } #leaf-l-bud .leaf-grow { --t:2.8s; }
    #leaf-l-top .leaf-grow { --t:2.95s; } #leaf-r-top .leaf-grow { --t:2.95s; } #leaf-r-upper .leaf-grow { --t:3.15s; }
    #leaf-r-neck .leaf-grow { --t:3.15s; } #leaf-r-mid .leaf-grow { --t:3.3s; } #leaf-r-big .leaf-grow { --t:3.5s; }
    #leaf-center .leaf-grow { --t:3.75s; }
    #monogram { opacity:0; transform-origin:520px 740px; animation:pop .6s .55s cubic-bezier(.34,1.3,.64,1) forwards; }
    #wordmark { opacity:0; animation:rise .8s 3.9s ease-out forwards; }
    #tip { opacity:0; animation:fade .2s 1.05s forwards; }
    .bubble { opacity:0; transform-origin:center; transform-box:fill-box;
              animation:pop .5s calc(4.0s + var(--i)*.18s) cubic-bezier(.34,1.4,.64,1) forwards,
                        bob 3.4s calc(4.5s + var(--i)*.45s) ease-in-out infinite; }
    @keyframes draw { to { stroke-dashoffset:0; } }
    @keyframes grow { to { transform:scale(1); } }
    @keyframes pop { from { opacity:0; transform:scale(.6); } to { opacity:1; transform:scale(1); } }
    @keyframes rise { from { opacity:0; transform:translateY(12px); } to { opacity:1; transform:translateY(0); } }
    @keyframes fade { to { opacity:1; } }
    @keyframes bob { 0%,100% { transform:translateY(0); } 50% { transform:translateY(-7px); } }
  }
"""

def circle_d(cx, cy, r):
    return f"M{fmt(cx - r)} {fmt(cy)} a{fmt(r)} {fmt(r)} 0 1 0 {fmt(2 * r)} 0 a{fmt(r)} {fmt(r)} 0 1 0 {fmt(-2 * r)} 0 Z"

FULL_WHITE = '<rect x="0" y="0" width="1024" height="1024" fill="#fff"/>'

def build(animated, ink=DARK):
    d = ' draw' if animated else ''
    def vine(pid, path, w, cls="vine"):
        return (f'    <path id="{pid}" class="{cls}{d}" d="{path}" pathLength="100" fill="none" '
                f'stroke="{ink}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')
    def cut(ident, path, w):
        return (f'      <path id="{ident}" class="cut{d}" d="{path}" pathLength="100" fill="none" stroke="#000" '
                f'stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')
    stem_d, loop_d, left_d, branch_d = smooth_path(STEM), smooth_path(LOOP, True), smooth_path(VINE_LEFT), smooth_path(BRANCH_LEFT)
    petioles = "\n".join(vine(pid, smooth_path(pts), 7, "petiole") for pid, pts in PETIOLES.items())
    bubbles = "\n".join(
        f'    <path class="bubble" style="--i:{i}" fill-rule="evenodd" fill="{ink}" '
        f'd="{circle_d(cx, cy, r)} {circle_d(hx, hy, hr)}"/>'
        for i, (cx, cy, r, hx, hy, hr) in enumerate(BUBBLES))
    style = f"  <style>{ANIM_CSS}  </style>\n" if animated else ""
    leaves = leaf_markup().replace(f'stroke="{DARK}"', f'stroke="{ink}"')
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024" role="img" aria-labelledby="cc-title">',
        f'  <title id="cc-title">Carolina Cultures Co.</title>',
        style + '  <defs>',
        f'    <mask id="cut-flask" maskUnits="userSpaceOnUse" x="0" y="0" width="1024" height="1024">',
        f'      {FULL_WHITE}', cut("loop-cut", loop_d, 26), cut("vine-left-cut", left_d, 25), '    </mask>',
        f'    <mask id="cut-left-c" maskUnits="userSpaceOnUse" x="0" y="0" width="1024" height="1024">',
        f'      {FULL_WHITE}', cut("stem-cut", smooth_path(STEM_CUT), STEM_CUT_W), '    </mask>',
        '  </defs>', '',
        f'  <g id="flask" fill="none" stroke="{ink}" stroke-width="10" stroke-linejoin="round" mask="url(#cut-flask)">',
        f'    <path id="flask-outer" class="flask{d}" d="{FLASK_OUTER}" pathLength="100"/>',
        f'    <path id="flask-inner" class="flask{d}" d="{FLASK_INNER}" pathLength="100"/>',
        '  </g>', '',
        f'  <g id="monogram" fill="{LEAF}">',
        f'    <path id="c-left" d="{C_LEFT}" mask="url(#cut-left-c)"/>',
        f'    <path id="c-right-top" d="{C_RIGHT_TOP}"/>',
        f'    <path id="c-right-bottom" d="{C_RIGHT_BOTTOM}"/>',
        '  </g>', '',
        '  <g id="vines">',
        vine("stem", stem_d, VINE_W["stem"]),
        f'    <path id="tip" d="M486.5 764 L498.5 764 L492.5 777 Z" fill="{ink}"/>',
        vine("loop", loop_d, VINE_W["loop"]),
        vine("vine-left", left_d, VINE_W["vine-left"]),
        vine("branch-left", branch_d, VINE_W["branch-left"]),
        '    <g id="petioles">', petioles, '    </g>',
        '  </g>', '',
        '  <g id="leaves">', leaves, '  </g>', '',
        '  <g id="bubbles">', bubbles, '  </g>', '',
        '  <g id="wordmark">', f'    <path d="{wordmark_path()}" fill="{ink}"/>', '  </g>',
        '</svg>', '']
    return "\n".join(parts)

if __name__ == "__main__":
    open("carolina-cultures-logo.svg", "w").write(build(False))
    open("carolina-cultures-logo-animated.svg", "w").write(build(True))
    open("carolina-cultures-logo-on-dark.svg", "w").write(build(False, ink=INK_ON_DARK))
    open("carolina-cultures-logo-on-dark-animated.svg", "w").write(build(True, ink=INK_ON_DARK))
    print("written")
