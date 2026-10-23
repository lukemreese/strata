"""Act 2: Hell Creek about a year after the Chicxulub impact (impact winter).

Maps of this act only. Add a map by appending a dict to MAPS (order within an act
is its map-id order), and its MAPSEC to MAP_SECTIONS. Shared helpers are in
common.py; see maps/__init__.py for how the acts are assembled.

The act reuses the Act 1 footprints (Levee, River, Backswamp) with winter palettes,
plus a small cave:

    Ashen Swamp (the survival gauntlet)
        |
    Ashen River
        |
    Ashen Levee (arrival from camp) ..mound.. Burrow Refuge

The Fern Glade of Act 1 is not rebuilt here: the herds and the perching birds are gone.
"""

from .common import *  # noqa: F401,F403

MAP_SECTIONS = [
    ("MAPSEC_STRATA_ASHEN_LEVEE", "ASHEN LEVEE"),
    ("MAPSEC_STRATA_ASHEN_RIVER", "ASHEN RIVER"),
    ("MAPSEC_STRATA_ASHEN_SWAMP", "ASHEN SWAMP"),
    ("MAPSEC_STRATA_BURROW", "BURROW REFUGE"),
]

# General primary tileset: the wooden signpost (a field note on open ground).
SIGNPOST = 0x01B


def signpost(x, y, script, facing="BG_EVENT_PLAYER_FACING_ANY"):
    """A patch that plants a (blocked) signpost at (x, y), and the sign event for it."""
    return dict(at=(x, y), tiles=[[SIGNPOST]], collision=1), sign(x, y, script, facing)


# The burrow's mouth in the Ashen Levee: a rock mound with a black opening (the same
# tiles as the Ice Age sinkhole), 3x3 at (5..7, 19..21), entered from row 22.
_BURROW_MOUND = dict(at=(5, 19), collision=1, elevation=0,
                     tiles=[[0x080, 0x081, 0x082], [0x088, 0x071, 0x08A], [0x090, 0x1A2, 0x092]])
_LEVEE_NOTES = [signpost(21, 25, "StrataLeveeWinter_EventScript_NoteDark"),
                signpost(13, 24, "StrataLeveeWinter_EventScript_NoteBurrows")]
_RIVER_NOTES = [signpost(30, 18, "StrataRiverWinter_EventScript_NoteFreshwater")]
_SWAMP_NOTES = [signpost(30, 11, "StrataBackswampWinter_EventScript_NoteFernSpike"),
                signpost(22, 14, "StrataBackswampWinter_EventScript_NoteThin")]
_BURROW_NOTES = [signpost(4, 9, "StrataBurrow_EventScript_NoteCache"),
                 signpost(12, 9, "StrataBurrow_EventScript_NoteBurrowers")]

MAPS = [
    # ------------------------------------------------------------------
    # Hell Creek, ~1 year after the Chicxulub impact (Act 2): the same
    # place, soot-darkened and ash-covered. Only the survivors remain.
    # ------------------------------------------------------------------
    dict(
        id="MAP_STRATA_LEVEE_WINTER", name="StrataLeveeWinter", era="ERA_IMPACT_WINTER",
        habitat="open", light="dark", forage=[forage(6, 25, "CARRION"), forage(34, 12, "FERN_FROND")],
        crop=winter(LEVEE_CROP), patches=LEVEE_PATCHES + [_BURROW_MOUND] + [p for p, _ in _LEVEE_NOTES],
        music="MUS_ABANDONED_SHIP", weather="WEATHER_VOLCANIC_ASH", map_type="MAP_TYPE_ROUTE",
        mapsec="MAPSEC_STRATA_ASHEN_LEVEE",
        connections=[connection("up", "MAP_STRATA_RIVER_WINTER")],
        coords=return_edge() + [
            # The way into the burrow, along the mound's south side.
            trigger(x, 22, "VAR_TEMP_1", 0, "StrataLeveeWinter_EventScript_BurrowMouth") for x in (5, 6, 7)
        ],
        bgs=[s for _, s in _LEVEE_NOTES],
        encounters=dict(
            land_mons=mons(("MESODMA", 10, 11), ("MESODMA", 10, 12), ("MESODMA", 11, 12), ("CIMOLESTES", 10, 12),
                           ("MESODMA", 11, 13), ("CHAMPSOSAUR", 11, 13), ("ASTERIORNIS", 11, 13), ("CIMOLESTES", 12, 13),
                           ("EMARGINACHEL", 12, 13), ("ASTERIORNIS", 12, 14), ("CHAMPSOSAUR", 12, 14), ("BOREALOSUCH", 13, 14)),
            water_mons=mons(("LEPISOSTEUS", 10, 13), ("LEPISOSTEUS", 10, 13), ("CHAMPSOSAUR", 11, 13),
                            ("EMARGINACHEL", 11, 13), ("BOREALOSUCH", 12, 14)),
        ),
    ),
    dict(
        id="MAP_STRATA_RIVER_WINTER", name="StrataRiverWinter", era="ERA_IMPACT_WINTER",
        habitat="water", light="dark", forage=[forage(27, 15, "CARRION"), forage(34, 19, "LARVAE")],
        crop=winter(RIVER_CROP), patches=RIVER_PATCHES + [p for p, _ in _RIVER_NOTES], swap=RIVER_SWAP,
        music="MUS_ABANDONED_SHIP", weather="WEATHER_VOLCANIC_ASH", map_type="MAP_TYPE_ROUTE",
        mapsec="MAPSEC_STRATA_ASHEN_RIVER",
        connections=[connection("down", "MAP_STRATA_LEVEE_WINTER"), connection("up", "MAP_STRATA_BACKSWAMP_WINTER")],
        bgs=[
            sign(29, 12, "StrataRiverWinter_EventScript_Bluff"),
        ] + [s for _, s in _RIVER_NOTES],
        encounters=dict(
            land_mons=mons(("MESODMA", 11, 12), ("MESODMA", 11, 13), ("CIMOLESTES", 11, 13), ("CHAMPSOSAUR", 12, 13),
                           ("MESODMA", 12, 13), ("ASTERIORNIS", 12, 14), ("CHAMPSOSAUR", 12, 14), ("EMARGINACHEL", 12, 14),
                           ("CIMOLESTES", 13, 14), ("ASTERIORNIS", 13, 14), ("BOREALOSUCH", 13, 15), ("BOREALOSUCH", 14, 15)),
            water_mons=mons(("LEPISOSTEUS", 11, 14), ("CHAMPSOSAUR", 11, 14), ("LEPISOSTEUS", 12, 14),
                            ("EMARGINACHEL", 12, 15), ("BOREALOSUCH", 13, 15)),
            fishing_mons=mons(("LEPISOSTEUS", 10, 12), ("LEPISOSTEUS", 10, 12), ("LEPISOSTEUS", 11, 13), ("CHAMPSOSAUR", 11, 13),
                              ("LEPISOSTEUS", 11, 13), ("CHAMPSOSAUR", 12, 14), ("EMARGINACHEL", 12, 14), ("LEPISOSTEUS", 12, 14),
                              ("BOREALOSUCH", 13, 15), ("BOREALOSUCH", 13, 15)),
        ),
    ),
    dict(
        id="MAP_STRATA_BACKSWAMP_WINTER", name="StrataBackswampWinter", era="ERA_IMPACT_WINTER",
        habitat="water", light="dark", forage=[forage(5, 2, "FERN_FROND"), forage(14, 12, "CARRION")],
        crop=winter(BACKSWAMP_CROP), patches=[p for p, _ in _SWAMP_NOTES],
        music="MUS_ABANDONED_SHIP", weather="WEATHER_VOLCANIC_ASH", map_type="MAP_TYPE_ROUTE",
        mapsec="MAPSEC_STRATA_ASHEN_SWAMP",
        connections=[connection("down", "MAP_STRATA_RIVER_WINTER")],
        coords=[
            # The starving season: the survivors guard the last open water. The line
            # covers the whole width of the swamp, so the gauntlet can't be walked around.
            trigger(x, 13, "VAR_STRATA_STORY", 4, "StrataBackswampWinter_EventScript_Gauntlet")
            for x in range(13, 38)
        ],
        bgs=[s for _, s in _SWAMP_NOTES],
        encounters=dict(
            land_mons=mons(("MESODMA", 12, 13), ("CHAMPSOSAUR", 12, 14), ("MESODMA", 12, 14), ("CIMOLESTES", 12, 14),
                           ("CHAMPSOSAUR", 13, 14), ("EMARGINACHEL", 13, 14), ("ASTERIORNIS", 13, 15), ("BOREALOSUCH", 13, 15),
                           ("MESODMA", 13, 15), ("CHAMPSOSAUR", 14, 15), ("BOREALOSUCH", 14, 16), ("BOREALOSUCH", 15, 16)),
            water_mons=mons(("LEPISOSTEUS", 12, 15), ("CHAMPSOSAUR", 12, 15), ("BOREALOSUCH", 13, 15),
                            ("EMARGINACHEL", 13, 16), ("BOREALOSUCH", 14, 16)),
            fishing_mons=mons(("LEPISOSTEUS", 11, 13), ("LEPISOSTEUS", 11, 13), ("LEPISOSTEUS", 12, 14), ("CHAMPSOSAUR", 12, 14),
                              ("LEPISOSTEUS", 12, 14), ("CHAMPSOSAUR", 13, 15), ("EMARGINACHEL", 13, 15), ("BOREALOSUCH", 13, 15),
                              ("BOREALOSUCH", 14, 16), ("BOREALOSUCH", 14, 16)),
        ),
    ),
    # The burrow where small mammals waited the winter out: the top chamber of the stock
    # Island Cave, with a seed cache (browse) on the floor.
    dict(
        id="MAP_STRATA_BURROW", name="StrataBurrow", era="ERA_IMPACT_WINTER",
        habitat=None, light="none",
        forage=[forage(6, 5, "BROWSE", visible=True), forage(10, 5, "BROWSE", visible=True),
                forage(8, 9, "LARVAE"), forage(3, 6, "FERN_FROND")],
        crop=dict(**{"from": "LAYOUT_ISLAND_CAVE"}, rect=(0, 0, 17, 15)),
        patches=[p for p, _ in _BURROW_NOTES],
        music="MUS_ABANDONED_SHIP", map_type="MAP_TYPE_UNDERGROUND", mapsec="MAPSEC_STRATA_BURROW",
        arrival=(8, 10),
        # The glowing slab at the bottom is the way out: stepping down toward it offers the climb.
        coords=[trigger(x, 11, "VAR_TEMP_1", 0, "StrataBurrow_EventScript_Exit") for x in range(4, 13)],
        bgs=[s for _, s in _BURROW_NOTES],
        encounters=dict(
            land_mons=mons(("MESODMA", 10, 11), ("MESODMA", 10, 12), ("CIMOLESTES", 10, 12), ("MESODMA", 11, 12),
                           ("CIMOLESTES", 11, 12), ("MESODMA", 11, 13), ("CIMOLESTES", 11, 13), ("MESODMA", 12, 13),
                           ("CIMOLESTES", 12, 13), ("MESODMA", 12, 13), ("CIMOLESTES", 12, 13), ("CIMOLESTES", 13, 13)),
        ),
    ),
]
