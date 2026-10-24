"""Builds every output file of one species from its spec and body plan.

graphics/pokemon/strata/<folder>/
    anim_front.png  64x128, two 64x64 frames, 4bpp      back.png  64x64
    normal.pal / shiny.pal   JASC, 16 colours, index 0 transparent
    icon.png        32x64, two frames, in one of the 6 shared icon palettes
    footprint.png   16x16 1bpp
    overworld.png   6 frames in a row (south, south step, north, north step,
                    west, west step; east = west mirrored by the engine),
                    32x32 each (192x32) or 64x64 each (384x64), same palette
    CUSTOM          marker + presentation fields read by gen_species.py
"""

import os
import sys

from .color import Palette, pigment_variant, icon_palette_fit
from .image import bbox, place, hcat, write_indexed_png, write_pal, coords_size
from .paths import species_dir
from .raster import render

CANVAS = 96        # battle/icon render canvas (model origin at its centre)
OW_CANVAS = 160
OW_BOTTOM = {32: 30, 64: 62}   # lowest pixel row of the art in an overworld frame
OW_VIEWS = ("south", "north", "west")


def ow_defaults(mass):
    """Overworld frame size and west-view body length in pixels, from mass.
    Stylised: a mouse is not 3 px long next to the 16x32 player."""
    if mass < 1:
        return 32, 20
    if mass < 30:
        return 32, 24
    if mass < 300:
        return 32, 27
    if mass < 1000:
        return 32, 30
    if mass < 3000:
        return 64, 44
    return 64, 56


class Species:
    """A spec bound to its plan: parameters plus the view functions."""
    def __init__(self, folder, plan, spec, mass):
        self.folder, self.plan, self.spec, self.mass = folder, plan, spec, mass
        self.p = plan.params(spec)
        custom = spec.get("model")
        self._side = (lambda p, phase=0, step=None: custom(p, phase, step)) if custom else plan.side

    def side(self, phase=0, step=None):
        return self._side(self.p, phase, step)

    def back_model(self, phase=0):
        return self.plan.back(self.p, phase) if self.plan.back else None

    def ow_model(self, view, step):
        if view == "west" or not self.plan.overworld:
            return self.side(0, step)
        return self.plan.overworld(self.p, view, step)

    @property
    def palette(self):
        return Palette(self.side(0).ramps)


def render_battle(sp, pal):
    """(front frames [2], back, icon frames [2]) as index images."""
    p = sp.p

    def frames(make, scale, flip, out, bottom=None, what="art"):
        imgs = [render(make(ph), CANVAS, scale, flip, (CANVAS / 2, CANVAS / 2), pal) for ph in (0, 1)]
        return place(imgs, out, bottom, what=f"{sp.folder} {what}")

    front = frames(sp.side, p["front"], False, 64, what="front")
    if sp.plan.back:
        back = frames(sp.back_model, p["back"], False, 64, what="back")[0]
    else:
        back = frames(sp.side, p["back"], True, 64, what="back")[0]
    icon = frames(sp.side, p["icon"], False, 32, bottom=29, what="icon")
    icon[1] = icon[1][1:] + [[0] * 32]  # frame 2 bobs up a pixel
    return front, back, icon


def render_overworld(sp, pal):
    """Returns (sheet rows, size, shadow, tracks, views drawn, west-view scale).
    spec `ow` keys: size (32|64), length (west-view px), scale (overrides
    length), end_zoom (south/north relative to west, default 1.25), shadow, tracks."""
    ow = dict(sp.p.get("ow") or {})
    size, length = ow_defaults(sp.mass)
    size, length = ow.get("size", size), ow.get("length", length)
    if size not in OW_BOTTOM:
        sys.exit(f"gen_sprite: {sp.folder}: ow size must be 32 or 64")
    c = OW_CANVAS
    probe = render(sp.side(0, 0), c, sp.p["front"], False, (c / 2, c / 2), pal)
    b = bbox(probe)
    scale = ow.get("scale") or sp.p["front"] * length / (b[2] - b[0] + 1)
    sheet = []
    for view in OW_VIEWS:
        # end-on views are drawn a little larger (chibi, as overworld creatures are)
        s = scale * (ow.get("end_zoom", 1.25) if view != "west" and sp.plan.overworld else 1.0)
        imgs = [render(sp.ow_model(view, st), c, s, False, (c / 2, c / 2), pal) for st in (0, 1)]
        sheet += place(imgs, size, OW_BOTTOM[size], what=f"{sp.folder} overworld {view}")
    wb = bbox(sheet[4])
    width = wb[2] - wb[0] + 1
    shadow = ow.get("shadow") or ("SHADOW_SIZE_L" if size == 64 else
                                  "SHADOW_SIZE_S" if width < 22 else "SHADOW_SIZE_M")
    tracks = ow.get("tracks") or sp.plan.tracks
    views = "south+north+west" if sp.plan.overworld else "side-only"
    return hcat(*sheet), size, shadow, tracks, views, scale


def build(sp, preview_dir=None, log=print):
    pal = sp.palette
    front, back, icon = render_battle(sp, pal)
    ow_sheet, ow_size, ow_shadow, ow_tracks, ow_views, ow_scale = render_overworld(sp, pal)

    dst = species_dir(sp.folder)
    os.makedirs(dst, exist_ok=True)
    shiny = pigment_variant(pal, sp.p["shiny"])
    write_indexed_png(os.path.join(dst, "anim_front.png"), front[0] + front[1], pal.colors)
    write_indexed_png(os.path.join(dst, "back.png"), back, pal.colors)
    write_pal(os.path.join(dst, "normal.pal"), pal.colors)
    write_pal(os.path.join(dst, "shiny.pal"), shiny)
    icon_pal, remap, icon_colors = icon_palette_fit(icon, pal)
    icon = [[[remap[v] for v in row] for row in f] for f in icon]
    write_indexed_png(os.path.join(dst, "icon.png"), icon[0] + icon[1], icon_colors)
    fp = sp.p.get("footprint", sp.plan.footprint) or ["." * 16] * 16
    write_indexed_png(os.path.join(dst, "footprint.png"), [[1 if ch == "#" else 0 for ch in row] for row in fp],
                      [(255, 255, 255), (98, 98, 98)], depth=1)
    write_indexed_png(os.path.join(dst, "overworld.png"), ow_sheet, pal.colors)
    for old in ("front.png", "overworld_normal.pal", "overworld_shiny.pal"):  # leftovers of borrowed art
        if os.path.exists(os.path.join(dst, old)):
            os.remove(os.path.join(dst, old))

    fb, bb = bbox(front[0]), bbox(back)
    fields = [
        f".frontPicSize = {coords_size(fb[2] - fb[0] + 1, fb[3] - fb[1] + 1)},",
        f".frontPicYOffset = {63 - fb[3]},",
        f".backPicSize = {coords_size(bb[2] - bb[0] + 1, bb[3] - bb[1] + 1)},",
        f".backPicYOffset = {63 - bb[3]},",
        f".iconPalIndex = {icon_pal},",
    ]
    with open(os.path.join(dst, "CUSTOM"), "w") as f:
        f.write("# Generated by tools/strata/gen_sprite.py. While this file exists, gen_species.py\n"
                "# keeps the sprites in this folder and uses these presentation fields.\n")
        f.write("\n".join(fields) + "\n")
        f.write(f"@overworld SIZE_{ow_size}x{ow_size} {ow_shadow} {ow_tracks} {ow_views}\n")
    log(f"{sp.folder}: front {fb}, back {bb}, icon palette {icon_pal}, "
        f"{sum(1 for c in pal.colors if c)} colours, overworld {ow_size}x{ow_size} {ow_views}")

    if preview_dir:
        from . import preview
        preview.species_previews(preview_dir, sp.folder, front, back, icon, pal.colors, shiny, icon_colors,
                                 ow_sheet, ow_size)
