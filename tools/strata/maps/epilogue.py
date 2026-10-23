"""Epilogue: the Montana prairie today.

Maps of this act only. Add a map by appending a dict to MAPS (order within an act
is its map-id order), and its MAPSEC to MAP_SECTIONS. Shared helpers are in
common.py; see maps/__init__.py for how the acts are assembled.
"""

from .common import *  # noqa: F401,F403

MAP_SECTIONS = [
    ("MAPSEC_STRATA_PRAIRIE", "MONTANA PRAIRIE"),
]

MAPS = [
    # ------------------------------------------------------------------
    # Epilogue: the Montana prairie today, open only once the present is loaded
    # ------------------------------------------------------------------
    dict(
        id="MAP_STRATA_PRAIRIE", name="StrataPrairie", era="ERA_EPILOGUE",
        crop=dict(**{"from": "LAYOUT_ROUTE102"}, rect=(0, 0, 50, 20)),
        patches=[
            dict(rect=(23, 2, 4, 2), metatile=0x001, elevation=3),    # berry-soil plot -> grass
        ],
        music="MUS_ROUTE101", weather="WEATHER_SUNNY", map_type="MAP_TYPE_ROUTE", mapsec="MAPSEC_STRATA_PRAIRIE",
        arrival=(2, 9),
        bgs=[sign(2, 10, "StrataPrairie_EventScript_TrailToCamp")],
        encounters=dict(
            land_mons=mons(("CYNOMYS", 48, 50), ("ANTILOCAPRA", 48, 50), ("CYNOMYS", 48, 50), ("CANIS", 48, 50),
                           ("MELEAGRIS", 49, 51), ("ANTILOCAPRA", 49, 51), ("BISON", 49, 51), ("OVIS", 49, 51),
                           ("CANIS", 50, 52), ("BISON", 50, 52), ("EQUUS", 50, 52), ("OVIBOS", 50, 52)),
            water_mons=mons(("CHELYDRA", 48, 52), ("LEPISOSTEUS", 48, 52), ("CHELYDRA", 49, 52),
                            ("LEPISOSTEUS", 50, 53), ("CHELYDRA", 51, 53)),
            fishing_mons=mons(("LEPISOSTEUS", 46, 49), ("LEPISOSTEUS", 46, 49), ("LEPISOSTEUS", 47, 50), ("CHELYDRA", 47, 50),
                              ("LEPISOSTEUS", 48, 51), ("CHELYDRA", 48, 51), ("LEPISOSTEUS", 49, 52), ("CHELYDRA", 49, 52),
                              ("CHELYDRA", 50, 53), ("CHELYDRA", 51, 54)),
        ),
    ),
]
