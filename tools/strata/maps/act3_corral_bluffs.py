"""Act 3: Corral Bluffs, CO (~65.7 Ma).

Maps of this act only. Add a map by appending a dict to MAPS (order within an act
is its map-id order), and its MAPSEC to MAP_SECTIONS. Shared helpers are in
common.py; see maps/__init__.py for how the acts are assembled.
"""

from .common import *  # noqa: F401,F403

MAP_SECTIONS = [
    ("MAPSEC_STRATA_CORRAL_BLUFFS", "CORRAL BLUFFS"),
]

MAPS = [
    # ------------------------------------------------------------------
    # Act 3: Corral Bluffs, CO (~65.7 Ma): recovering palm and legume forest
    # ------------------------------------------------------------------
    dict(
        id="MAP_STRATA_PALM_FOREST", name="StrataPalmForest", era="ERA_CORRAL_BLUFFS",
        crop=dict(**{"from": "LAYOUT_PETALBURG_WOODS"}, rect=(0, 0, 48, 44)),
        # Petalburg Woods' wooden fences, arrow-warp mats and ledge logs -> plain ground
        swap={0x149: GROUND(0x001), 0x203: GROUND(0x001), 0x204: GROUND(0x001),
              0x087: GROUND(0x001), 0x0D5: GROUND(0x001), 0x0D6: GROUND(0x001)},
        music="MUS_PETALBURG_WOODS", map_type="MAP_TYPE_ROUTE", mapsec="MAPSEC_STRATA_CORRAL_BLUFFS",
        arrival=(15, 33),
        bgs=[anchor(14, 32)],
        coords=boss_triggers("ERA_CORRAL_BLUFFS", "StrataPalmForest_EventScript_Eoconodon",
                             [(x, 7) for x in range(31, 37)] + [(x, 7) for x in range(41, 46)]),
        encounters=dict(
            land_mons=mons(("LOXOLOPHUS", 15, 17), ("CARSIOPTYCH", 15, 17), ("MESODMA", 15, 16), ("PURGATORIUS", 15, 17),
                           ("LOXOLOPHUS", 16, 18), ("CARSIOPTYCH", 16, 18), ("PROTICTIS", 16, 18), ("ASTERIORNIS", 16, 18),
                           ("TAENIOLABIS", 17, 19), ("PROTOCHELYD", 17, 19), ("TAENIOLABIS", 18, 20), ("EOCONODON", 18, 20)),
        ),
    ),
]
