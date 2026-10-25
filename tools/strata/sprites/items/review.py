"""Review sheet: every replaced asset, stock (from git) next to the new one, plus
the starter-choice and cave-transition screens composed both ways.

    gen_item_art.py --review OUT.png [--before REF]

REF defaults to the parent of the commit that added this package (the last
stock version); before that commit exists, HEAD."""

import os
import struct
import subprocess
import tempfile

from ..core.paths import ROOT, read_pal, write_png, draw_text
from ..core.preview import blit, canvas
from .grid import read_indexed
from .tiers import TIERS

BG = (72, 80, 76)
TEXT = (250, 240, 180)


def git(*args):
    return subprocess.run(["git", "-C", ROOT, *args], capture_output=True, check=False)


def default_ref():
    r = git("log", "--diff-filter=A", "--format=%H", "--", "tools/strata/sprites/items/__init__.py")
    commits = r.stdout.decode().split()
    return commits[-1] + "^" if commits else "HEAD"


class Source:
    """Reads repo files either from disk (ref None) or from a git ref."""
    def __init__(self, ref=None):
        self.ref = ref
        self.tmp = tempfile.mkdtemp(prefix="strata_items_")

    def file(self, rel):
        if self.ref is None:
            return os.path.join(ROOT, rel)
        out = os.path.join(self.tmp, rel.replace("/", "_"))
        if not os.path.exists(out):
            r = git("show", f"{self.ref}:{rel}")
            if r.returncode:
                raise SystemExit(f"gen_item_art: {rel} not in {self.ref}")
            open(out, "wb").write(r.stdout)
        return out

    def image(self, rel, pal=None):
        rows, own = read_indexed(self.file(rel))
        if pal is None:
            colors = own
        elif pal.endswith(".pal"):
            colors = read_pal(self.file(pal))
        else:
            colors = read_indexed(self.file(pal))[1]
        return rows, (list(colors) + [(255, 0, 255)] * 256)[:256]

    def tilemap(self, tiles_rel, map_rel, wt, pal=None, base=None, pal_bank=None):
        rows, colors = self.image(tiles_rel, pal)
        data = open(self.file(map_rel), "rb").read()
        ents = struct.unpack("<%dH" % (len(data) // 2), data)
        ntx = len(rows[0]) // 8
        img = base or [[None] * 240 for _ in range(160)]
        for i, e in enumerate(ents):
            t, hf, vf, pb = e & 0x3FF, (e >> 10) & 1, (e >> 11) & 1, e >> 12
            tx, ty = i % wt, i // wt
            if tx >= 30 or ty >= 20 or not t or t >= ntx * (len(rows) // 8):
                continue
            bank = pal_bank if pal_bank is not None else pb
            for y in range(8):
                for x in range(8):
                    v = rows[(t // ntx) * 8 + (7 - y if vf else y)][(t % ntx) * 8 + (7 - x if hf else x)] & 15
                    if v:
                        img[ty * 8 + y][tx * 8 + x] = colors[bank * 16 + v]
        return img


def assets():
    """(label, png, palette source or None, scale) for every replaced image."""
    out = []
    for key in TIERS:
        out.append((f"balls/{key}", f"graphics/balls/{key}.png", None, 3))
    out.append(("balls/open (shared frame)", "graphics/balls/open.png", "graphics/balls/poke.png", 3))
    for key in TIERS:
        pal = "repeat" if key == "timer" else key
        out.append((f"icon {key}", f"graphics/items/icons/{key}_ball.png",
                    f"graphics/items/icon_palettes/{pal}_ball.pal", 3))
    out.append(("item on map (NPC_3)", "graphics/object_events/pics/misc/ball_poke.png",
                "graphics/object_events/palettes/npc_3.pal", 3))
    for key in ("great", "ultra", "master"):
        out.append((f"follower {key}", f"graphics/object_events/pics/misc/ball_{key}.png", None, 2))
    out += [
        ("status row", "graphics/battle_interface/ball_display.png", None, 6),
        ("caught (healthbox pal)", "graphics/battle_interface/ball_caught_indicator.png",
         "graphics/battle_interface/ball_status_bar.png", 6),
        ("baton pass", "graphics/battle_anims/sprites/pokeball.png", None, 4),
        ("party menu", "graphics/party_menu/pokeball.png", None, 3),
        ("party small", "graphics/party_menu/pokeball_small.png", "graphics/party_menu/pokeball.png", 3),
        ("bag spinner", "graphics/bag/rotating_ball.png", None, 4),
        ("codex caught", "graphics/pokedex/caught_ball.png", "graphics/pokedex/bg_hoenn.pal", 6),
        ("heal machine", "graphics/field_effects/pics/pokeball_glow.png",
         "graphics/field_effects/palettes/pokeball_glow.pal", 6),
        ("trainer transition", "graphics/battle_transitions/pokeball.png",
         "graphics/field_effects/palettes/pokeball.pal", 3),
        ("starter choice", "graphics/starter_choose/pokeball_selection.png", None, 3),
    ]
    return out


def screens(src):
    """Composed screens: starter choice (grass, case/bag, three capsule sprites),
    bag pocket badge, cave transition."""
    grass = src.tilemap("graphics/starter_choose/tiles.png", "graphics/starter_choose/birch_grass.bin", 32)
    starter = src.tilemap("graphics/starter_choose/tiles.png", "graphics/starter_choose/birch_bag.bin", 32,
                          base=[r[:] for r in grass])
    starter = [[c or (0, 0, 0) for c in r] for r in starter]
    sel, cols = src.image("graphics/starter_choose/pokeball_selection.png")
    for cx, cy in ((60, 64), (120, 88), (180, 64)):
        blit(starter, sel[:32], cols, cx - 16, cy - 16)
    bag = src.tilemap("graphics/bag/menu.png", "graphics/bag/menu.bin", 32, pal="graphics/bag/menu_male.pal")
    bag = [[c or (0, 0, 0) for c in r[:64]] for r in bag[:40]]
    big = src.tilemap("graphics/battle_transitions/big_pokeball.png", "graphics/battle_transitions/big_pokeball_map.bin",
                      30, pal="graphics/field_effects/palettes/pokeball.pal", pal_bank=0)
    big = [[c or (24, 24, 32) for c in r] for r in big]
    return [("starter choice", starter, 1), ("bag pocket badge", bag, 3), ("cave transition", big, 1)]


def sheet(out, before=None):
    ref = before or default_ref()
    old, new = Source(ref), Source(None)
    cells = []
    for label, rel, pal, scale in assets():
        a, ca = old.image(rel, pal)
        b, cb = new.image(rel, pal)
        cells.append((label, a, ca, b, cb, scale))
    width = 1600
    x, y, rowh = 8, 22, 0
    placed = []
    for label, a, ca, b, cb, scale in cells:
        w = (len(a[0]) + len(b[0])) * scale + 18
        h = max(len(a), len(b)) * scale + 12
        if x + w > width:
            x, y, rowh = 8, y + rowh + 6, 0
        placed.append((x, y, label, a, ca, b, cb, scale))
        x += w + 10
        rowh = max(rowh, h)
    y += rowh + 10
    scr = screens(old), screens(new)
    sy = y
    for (label, img_a, s), (_, img_b, _) in zip(*scr):
        h = len(img_a) * s
        y += h + 16
    img = canvas(width, y + 8, BG)
    draw_text(img, 8, 6, f"STRATA CAPSULE ART: STOCK ({ref[:12]}) LEFT, NEW RIGHT", TEXT, BG)
    for x, y0, label, a, ca, b, cb, scale in placed:
        draw_text(img, x, y0, label, TEXT, BG)
        for pic, cols, dx in ((a, ca, 0), (b, cb, len(a[0]) * scale + 6)):
            for yy in range(len(pic) * scale):
                for xx in range(len(pic[0]) * scale):
                    img[y0 + 8 + yy][x + dx + xx] = (96, 104, 100)
            blit(img, pic, cols, x + dx, y0 + 8, scale)
    y = sy
    for (label, img_a, s), (_, img_b, _) in zip(*scr):
        draw_text(img, 8, y, label, TEXT, BG)
        for i, pic in enumerate((img_a, img_b)):
            for yy in range(len(pic) * s):
                for xx in range(len(pic[0]) * s):
                    img[y + 8 + yy][8 + i * (len(pic[0]) * s + 12) + xx] = pic[yy // s][xx // s]
        y += len(img_a) * s + 16
    write_png(out, width, len(img), img)
    print("wrote", out)
