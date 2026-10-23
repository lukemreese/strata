"""Act 7: Ashfall, NE (~11.9 Ma).

Maps of this act only. Add a map by appending a dict to MAPS (order within an act
is its map-id order), and its MAPSEC to MAP_SECTIONS. Shared helpers are in
common.py; see maps/__init__.py for how the acts are assembled.
"""

from .common import *  # noqa: F401,F403

MAP_SECTIONS = [
    ("MAPSEC_STRATA_ASHFALL", "ASHFALL"),
]

MAPS = [
    # ------------------------------------------------------------------
    # Act 7: Ashfall, NE (~11.9 Ma): a grassland waterhole under volcanic ash
    # ------------------------------------------------------------------
    dict(
        id="MAP_STRATA_GRASSLAND", name="StrataGrassland", era="ERA_ASHFALL",
        crop=dict(**{"from": "LAYOUT_ROUTE113"}, rect=(15, 0, 85, 20)),
        patches=[
            dict(rect=(16, 1, 6, 5), like=(37, 6)),     # house -> ash plain
        ],
        music="MUS_ROUTE113", weather="WEATHER_VOLCANIC_ASH", map_type="MAP_TYPE_ROUTE", mapsec="MAPSEC_STRATA_ASHFALL",
        arrival=(5, 11),
        bgs=[anchor(5, 12)],
        coords=boss_triggers("ERA_ASHFALL", "StrataGrassland_EventScript_Teleoceras", [(70, y) for y in range(7, 12)]),
        encounters=dict(
            land_mons=mons(("PROTOHIPPUS", 40, 42), ("PROCAMELUS", 40, 42), ("LEPTOCYON", 40, 42), ("BALEARICA", 40, 42),
                           ("PROTOHIPPUS", 41, 43), ("GALLINULOID", 41, 43), ("PROCAMELUS", 41, 43), ("ANCHIGYPS", 41, 43),
                           ("TELEOCERAS", 42, 44), ("CHELYDRA", 42, 44), ("EPICYON", 43, 45), ("TELEOCERAS", 43, 45)),
        ),
    ),
]
