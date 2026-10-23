"""Act 6: White River badlands, SD/NE (~33 Ma).

Maps of this act only. Add a map by appending a dict to MAPS (order within an act
is its map-id order), and its MAPSEC to MAP_SECTIONS. Shared helpers are in
common.py; see maps/__init__.py for how the acts are assembled.
"""

from .common import *  # noqa: F401,F403

MAP_SECTIONS = [
    ("MAPSEC_STRATA_WHITE_RIVER", "WHITE RIVER"),
]

MAPS = [
    # ------------------------------------------------------------------
    # Act 6: White River badlands, SD/NE (~33 Ma): cooler, drier open woodland
    # ------------------------------------------------------------------
    dict(
        id="MAP_STRATA_WHITE_RIVER", name="StrataWhiteRiver", era="ERA_WHITE_RIVER",
        crop=dict(**{"from": "LAYOUT_ROUTE114"}, rect=(0, 37, 40, 43), tilesets=("gTileset_GeneralOligocene", "gTileset_FallarborOligocene")),
        patches=[
            dict(rect=(31, 5, 2, 5), metatile=0x001, elevation=3),    # berry-soil plot -> grass
        ],
        # secret-base rock spots and a cave door -> plain rock
        swap={0x208: 0x241, 0x259: 0x265, 0x261: (0x265, 1)},
        music="MUS_ROUTE110", map_type="MAP_TYPE_ROUTE", mapsec="MAPSEC_STRATA_WHITE_RIVER",
        arrival=(17, 3),
        bgs=[anchor(17, 4)],
        coords=boss_triggers("ERA_WHITE_RIVER", "StrataWhiteRiver_EventScript_Archaeotherium",
                             [(13, 32), (14, 32), (24, 34), (25, 34)]),
        encounters=dict(
            land_mons=mons(("MESOHIPPUS", 34, 36), ("MERYCOIDODON", 34, 36), ("LEPTOMERYX", 34, 36), ("ISCHYROMYS", 34, 36),
                           ("MERYCOIDODON", 35, 37), ("STYLEMYS", 35, 37), ("POEBROTHERE", 35, 37), ("HESPEROCYON", 35, 37),
                           ("MESOHIPPUS", 36, 38), ("SUBHYRACODON", 36, 38), ("HOPLOPHONEUS", 37, 39), ("ARCHAEOTHERE", 38, 39)),
        ),
    ),
]
