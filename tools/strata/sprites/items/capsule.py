"""The specimen capsule: the field rig's portable sample canister.

A squat upright cylinder seen from slightly above (3/4 view): a gunmetal lid
with a carry grip on top, a bright metal latch over the lid seam, a status
light on the lid, and a body in the tier colour with the tier marking. It is
deliberately not a ball: flat top ellipse, straight sides, a handle.

`capsule(...)` draws it at any size as a role grid (see grid.py). Roles:
    o            outline (and the lid seam)
    b0..b3       body, darkest first          l0..l2  lid (gunmetal)
    m0, m1       latch / grip metal           s0, s1  tier marking (dark, light)
    led          status light                 in, glow  open interior, its light
`tiny(...)` is the hand-made 7x7 version for 8x8 tiles (status row, caught
indicator, Codex list, heal machine), where a drawn cylinder turns to mush.
"""

import math

from .grid import Grid

ROLES = ("o", "b0", "b1", "b2", "b3", "l0", "l1", "l2", "m0", "m1", "s0", "s1", "led", "in", "glow")


def _light(u, s):
    """Cylinder side lit from the upper left and front."""
    return max(0.0, -0.5 * u + 0.85 * s)


def _level(light, n):
    cuts = {4: (0.25, 0.55, 0.82), 3: (0.32, 0.72)}[n]
    return sum(light > c for c in cuts)


def capsule(r, e, side, lid, handle=2, lift=0, marking="plain", beam=False, latch=True):
    """r: radius (px), e: half-height of the top ellipse, side: side height,
    lid: lid height on the side, handle: grip height above the lid (0 none),
    lift: open frame, lid raised by this many px over a glowing interior,
    marking: plain | band | label | hazard | double | cross.
    Returns an outlined role grid sized to fit."""
    W = int(math.ceil(2 * r)) + 2
    cx = W / 2
    ty = 1 + handle + lift + e
    H = int(math.ceil(ty + side + e)) + 3 + (6 if beam else 0)
    g = Grid(W, H)
    sw = 1 if r < 18 else 2        # seam width
    bh = side - lid - sw           # body side height below the seam

    def body_marking(x, y, u, s, db, light):
        """Tier marking on the body side; db = rows below the seam."""
        if marking in ("band", "hazard"):
            b0 = max(1, round(bh * 0.30))
            bw = max(1, round(bh * (0.28 if marking == "band" else 0.36)))
            if b0 <= db < b0 + bw:
                if marking == "hazard":
                    k = 2 if r >= 7 else 1
                    return "s1" if ((x + y) // k) % 2 else "s0"
                return "s1" if light > 0.45 else "s0"
        if marking == "double":
            b0 = max(1, round(bh * 0.22))
            gap = max(2, round(bh * 0.3))
            if db in (b0, b0 + gap) or (r >= 9 and db in (b0 + 1, b0 + gap + 1)):
                return "s1" if light > 0.45 else "s0"
        if marking in ("label", "cross"):
            lh = max(2, round(bh * 0.5))
            l0 = max(1, round(bh * 0.18))
            if -0.72 <= u <= -0.02 and l0 <= db < l0 + lh:
                if marking == "cross":
                    mid_u, mid_d = -0.37, l0 + (lh - 1) / 2
                    ux = abs(u - mid_u) * r
                    if ux < 0.6 or abs(db - mid_d) < 0.6:
                        return "s0"
                    return "s1"
                if lh >= 3 and db == l0 + lh // 2 and -0.6 <= u <= -0.15:
                    return "s0"                     # a written line on the label
                return "s1"
        return None

    for y in range(H):
        py = y + 0.5
        for x in range(W):
            px = x + 0.5
            u = (px - cx) / r
            if abs(u) >= 1:
                continue
            s = math.sqrt(1 - u * u)
            light = _light(u, s)
            front = ty + e * s
            bottom = ty + side + e * s
            seam = front + lid
            role = None
            # body (and, when open, its glowing mouth)
            if lift:
                if ty + lid - e * s <= py < seam:
                    inner = abs(u) < 0.62 and abs(py - (ty + lid)) < e * s * 0.62 + 0.2
                    role = "glow" if inner else "in"
            elif ty - e * s <= py < front:
                role = "l2" if u < 0.4 else "l1"
            if role is None and (front if not lift else seam) <= py < bottom:
                d = py - front
                if d < lid:
                    role = "l1" if light > 0.62 else "l0"
                elif d < lid + sw:
                    role = "o"
                else:
                    db = int(d - lid - sw)
                    role = body_marking(x, y, u, s, db, light)
                    if role is None:
                        lv = _level(light, 4)
                        if bottom - py < 1:
                            lv = max(0, lv - 1)
                        role = "b%d" % lv
            # the raised lid is drawn over the mouth
            if lift:
                lpy = py + lift
                if ty - e * s <= lpy < front:
                    role = "l2" if u < 0.4 else "l1"
                elif front <= lpy < seam:
                    role = "l1" if light > 0.62 else "l0"
            if role:
                g.px[y][x] = role

    # latch: bright metal across the seam (on the lid only when open)
    k = max(1, int(round(r / 9)))                   # detail scale (1 up to r ~13)
    if latch:
        lw = (2 if r < 9 else 3) if k == 1 else int(round(r * 0.26))
        x0 = int(round(cx - lw / 2))
        y_seam = int(ty + e + lid)                  # seam row at the front centre
        lh = 1 if k == 1 else max(2, int(round(lid * 0.5)))
        if lift:                                    # open: the hasp hangs from the lid
            rows = list(range(y_seam - 2 * lh - lift + 1, y_seam - lift + 1))
        else:
            rows = list(range(y_seam - lh, y_seam + 2 * lh))
        for yy in rows:
            for xx in range(x0, x0 + lw):
                g.set(xx, yy, "m1" if yy < rows[0] + k else "m0")
    # status light on the lid side, right of the latch
    lx = int(cx + 0.48 * r)
    us = (lx + 0.5 - cx) / r
    ly = int(ty + e * math.sqrt(1 - us * us) + lid / 2) - lift
    for dy in range(k):
        for dx in range((2 if r >= 9 else 1) * k):
            g.set(lx + dx, ly + dy - k // 2, "led")
    # carry grip on the lid
    if handle:
        gw = max(2, int(round(r * 0.9)))
        gx0 = int(round(cx - gw / 2))
        top = int(ty - lift - e * 0.35) - handle
        pw = (2 if r >= 9 else 1) * k               # a bail: two posts and a bar
        for yy in range(top, top + handle + 1):
            for i in range(pw):
                g.set(gx0 + i, yy, "m1")
                g.set(gx0 + gw - 1 - i, yy, "m0")
        for xx in range(gx0, gx0 + gw):
            for t in range(k):
                g.set(xx, top + t, "m1")
            if r >= 9:
                for t in range(k):
                    g.set(xx, top + k + t, "m0")
    # a soft beam rising from an open capsule (overworld release frame)
    if beam and lift:
        bx = int(cx) - 1
        for yy in range(0, int(ty - lift - e)):
            for xx in (bx, bx + 1):
                if g.get(xx, yy) is None:
                    g.set(xx, yy, "glow")
    g.outline()
    return g.outline(thicken=True) if r >= 30 else g


TINY = {
    # 7x7 in an 8x8 tile. T top face, L lid side, M latch, g light,
    # B / b body light / dark, o outline. Variants override cells.
    "closed": [
        ".ooooo.",
        "oTTTTTo",
        "oLLMLgo",
        "ooMMMoo",
        "oBBBbbo",
        "oBBBbbo",
        ".ooooo.",
    ],
    "empty": [
        ".ooooo.",
        "o.....o",
        "o.....o",
        "oo...oo",
        "o.....o",
        "o.....o",
        ".ooooo.",
    ],
}


def tiny(kind="closed"):
    g = Grid(7, 7)
    roles = {"o": "o", "T": "l2", "L": "l1", "M": "m1", "g": "led", "B": "b2", "b": "b1"}
    for y, row in enumerate(TINY[kind]):
        for x, ch in enumerate(row):
            if ch != ".":
                g.px[y][x] = roles[ch]
    return g


# Sizes used by the targets (r, e, side, lid, handle)
SIZE_16 = dict(r=5.5, e=1.5, side=8, lid=2, handle=2)      # battle ball sheet, small menu icons
SIZE_24 = dict(r=8, e=2.5, side=12, lid=3, handle=3)       # bag icons, party menu
SIZE_32 = dict(r=10, e=3, side=15, lid=4, handle=4)        # starter choice, rolling transition
