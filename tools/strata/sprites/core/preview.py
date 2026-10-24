"""Review images: per-species sheets, battle and overworld mock-ups, and the
contact sheet of every roster species.

Per species (gen_sprite.py <name> --preview DIR):
    <name>_sheet.png     1x row (front frames, back, shiny front + back, icons), then 3x
    <name>_front_x6.png  both front frames at 6x
    <name>_battle.png    foe and player positions on the tall-grass battle BG,
                         stock and impact-winter palettes, 2x
    <name>_ow.png        the 6 overworld frames at 1x and 4x, then the creature
                         next to the player sprite on grass at 3x (scale check)
Contact sheet (gen_sprite.py --contact OUT.png): every roster species' front
frame 0 and overworld west frame, grouped by body plan; borrowed stock art gets
a red frame and the label STOCK.
"""

import os

from .image import bbox
from .paths import ROOT, read_pal, read_png, write_png, draw_text, species_dir

BG = (232, 232, 224)
WHITE = (255, 255, 255)


def blit(img, pic, colors, x, y, scale=1, transparent=0):
    for yy, row in enumerate(pic):
        for xx, v in enumerate(row):
            if v != transparent:
                c = colors[v] if v < len(colors) else (255, 0, 255)
                for dy in range(scale):
                    for dx in range(scale):
                        py, px = y + yy * scale + dy, x + xx * scale + dx
                        if 0 <= py < len(img) and 0 <= px < len(img[0]):
                            img[py][px] = c


def canvas(w, h, color=BG):
    return [[color] * w for _ in range(h)]


def species_previews(outdir, name, front, back, icon, normal, shiny, icon_colors, ow_sheet, ow_size):
    os.makedirs(outdir, exist_ok=True)
    tiles = [(front[0], normal), (front[1], normal), (back, normal), (front[0], shiny), (back, shiny),
             (icon[0], icon_colors), (icon[1], icon_colors)]

    def sheet(scale):
        w = sum(len(t[0][0]) * scale + 4 for t in tiles)
        img = canvas(w, 64 * scale)
        x = 0
        for pic, cols in tiles:
            blit(img, pic, cols, x, 0, scale)
            x += len(pic[0]) * scale + 4
        return img

    one, three = sheet(1), sheet(3)
    w = max(len(one[0]), len(three[0]))
    rows = [r + [BG] * (w - len(r)) for r in one] + [[WHITE] * w] * 4 + [r + [BG] * (w - len(r)) for r in three]
    path = os.path.join(outdir, f"{name}_sheet.png")
    write_png(path, w, len(rows), rows)
    print("wrote", path)
    big = [[normal[v] if v else BG for v in row0 + row1 for _ in range(6)]
           for row0, row1 in zip(front[0], front[1]) for _ in range(6)]
    write_png(os.path.join(outdir, f"{name}_front_x6.png"), len(big[0]), len(big), big)
    write_battle_mock(outdir, name, front[0], back, normal)
    write_overworld_mock(outdir, name, ow_sheet, ow_size, normal, shiny)


def write_battle_mock(outdir, name, front, back, colors):
    """The creature as foe and as your mon on the tall-grass battle background,
    stock (top) and impact-winter palette (bottom), at 2x. Positions follow
    Emerald's battler coords: foe (176, 40), player (72, 80), plus the pic Y
    offsets that gen_sprite writes to CUSTOM."""
    import gen_tilesets
    fb, bb = bbox(front), bbox(back)
    stock = read_pal(os.path.join(ROOT, "graphics/battle_environment/tall_grass/palette.pal"))
    panels = []
    for pal in (stock, gen_tilesets.transform_pal(stock, "impact_winter")):
        img = [r[:240] for r in gen_tilesets.render_battle_bg("tall_grass", pal)[:160]]
        for y in range(112, 160):
            img[y] = [(40, 48, 64)] * 240
        for pic, (cx, cy) in ((front, (176, 40 + 63 - fb[3])), (back, (72, 80 + 63 - bb[3]))):
            for y, row in enumerate(pic):
                for x, v in enumerate(row):
                    sx, sy = cx - 32 + x, cy - 32 + y
                    if v and 0 <= sx < 240 and 0 <= sy < 112:
                        img[sy][sx] = colors[v]
        panels += [r for r in img for _ in range(2)]
        panels += [[WHITE] * 240] * 4
    rows = [[c for c in r for _ in range(2)] for r in panels]
    path = os.path.join(outdir, f"{name}_battle.png")
    write_png(path, len(rows[0]), len(rows), rows)
    print("wrote", path)


def _player_frame():
    """Brendan's south-facing walk frame (16x32) and palette, for scale."""
    try:
        _, _, rows = read_png(os.path.join(ROOT, "graphics/object_events/pics/people/brendan/walking.png"))
        pal = read_pal(os.path.join(ROOT, "graphics/object_events/palettes/brendan.pal"))
        return [r[:16] for r in rows[:32]], pal
    except (OSError, AssertionError):
        return None, None


def write_overworld_mock(outdir, name, sheet, size, normal, shiny):
    n = 6
    frames = [[row[i * size:(i + 1) * size] for row in sheet] for i in range(n)]
    pad = 4
    w = max(n * (size + pad), n * (size * 4 + pad))
    img = canvas(w, size + pad + size * 4 + pad + 34 * 3 + (size - 32) * 3)
    for i, f in enumerate(frames):
        blit(img, f, normal, i * (size + pad), 0)
        blit(img, f, normal, i * (size * 4 + pad), size + pad, 4)
    # scene: grass, the player, the creature facing south, west and (shiny) east
    y0 = size + pad + size * 4 + pad
    grass = (120, 184, 88)
    scene_h = max(32, size) + 2
    scene = canvas(16 + 8 + 3 * (size + 8), scene_h, grass)
    player, ppal = _player_frame()
    if player:
        blit(scene, player, ppal, 0, scene_h - 34)
    east = [list(reversed(r)) for r in frames[4]]
    for k, (f, cols) in enumerate(((frames[0], normal), (frames[4], normal), (east, shiny))):
        blit(scene, f, cols, 24 + k * (size + 8), scene_h - size - 2 + (2 if size == 32 else 0))
    blit_rgb(img, scene, 0, y0, 3)
    path = os.path.join(outdir, f"{name}_ow.png")
    write_png(path, len(img[0]), len(img), img)
    print("wrote", path)


def blit_rgb(img, src, x, y, scale):
    for yy, row in enumerate(src):
        for xx, c in enumerate(row):
            for dy in range(scale):
                for dx in range(scale):
                    py, px = y + yy * scale + dy, x + xx * scale + dx
                    if 0 <= py < len(img) and 0 <= px < len(img[0]):
                        img[py][px] = c


def _front_frame(folder):
    d = species_dir(folder)
    for fname in ("anim_front.png", "front.png"):
        path = os.path.join(d, fname)
        if os.path.exists(path):
            _, _, rows = read_png(path)
            return [r[:64] for r in rows[:64]], read_pal(os.path.join(d, "normal.pal"))
    return None, None


def contact_sheet(out, roster, species_plan, plan_order, scale=2):
    """Every roster species in a grid grouped by body plan: front frame 0 (64x64)
    and the overworld west frame, name and status under it."""
    cell_w, cell_h = 64 + 4 + 32, 64 + 14
    cols = 8
    groups = [(plan, [sp for sp in roster if species_plan[sp["folder"]] == plan]) for plan in plan_order]
    w = cols * (cell_w + 6) + 6
    h = 4 + sum(10 + (len(g) + cols - 1) // cols * (cell_h + 6) for _, g in groups if g)
    img = canvas(w, h)
    y = 4
    borrowed = 0
    for plan, members in groups:
        if not members:
            continue
        own = sum(1 for sp in members if sp["custom"])
        draw_text(img, 6, y, f"{plan}  {own}/{len(members)} own art", (32, 32, 48), BG)
        y += 10
        for k, sp in enumerate(members):
            x = 6 + (k % cols) * (cell_w + 6)
            if k and k % cols == 0:
                y += cell_h + 6
            pic, pal = _front_frame(sp["folder"])
            if not sp["custom"]:
                borrowed += 1
                for yy in range(y - 2, y + 66):
                    for xx in (x - 2, x + 65):
                        img[yy][xx] = (208, 40, 40)
                for xx in range(x - 2, x + 66):
                    img[y - 2][xx] = img[y + 65][xx] = (208, 40, 40)
            if pic:
                blit(img, pic, pal, x, y)
            owp = os.path.join(species_dir(sp["folder"]), "overworld.png")
            if sp["custom"] and os.path.exists(owp):
                ow_w, ow_h, ow_rows = read_png(owp)
                sz = ow_h
                pal = read_pal(os.path.join(species_dir(sp["folder"]), "normal.pal"))
                for i, fi in enumerate((0, 4)):
                    frame = [r[fi * sz:(fi + 1) * sz] for r in ow_rows]
                    if sz == 64:  # show giants at half size in the grid
                        frame = [r[::2] for r in frame[::2]]
                    blit(img, frame, pal, x + 68, y + i * 32)
            draw_text(img, x, y + 67, sp["name"][:12], (16, 16, 16), BG)
            if not sp["custom"]:
                draw_text(img, x + 68, y + 67, "STOCK", (208, 40, 40), BG)
        y += cell_h + 6
    big = [[c for c in row for _ in range(scale)] for row in img for _ in range(scale)]
    write_png(out, len(big[0]), len(big), big)
    print(f"wrote {out}: {len(roster)} species, {borrowed} still borrowed")
