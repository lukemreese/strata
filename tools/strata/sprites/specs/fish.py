"""Species specs for the fish body plan (plans/fish.py). Owned by the fish artist.

Every spec: ramps (<= 15 colours incl. the outline), render scales `front`,
`back`, `icon`, the pigment variant `shiny` {ramp: dict(deg, sat, val)}, plus the
plan's parameters (see the plan module). Optional: `ow` dict(size=32|64,
length=<px>, shadow="SHADOW_SIZE_S|M|L", tracks=...), `footprint`, `model`
(a function (p, phase, step) replacing the plan's side view for one-offs).
"""

from ..core.color import ramp

SPECS = {
    # Knightia eocaena, Green River Fm (~51 Ma): a ~15 cm herring (Clupeidae).
    # Fusiform, laterally compressed; terminal, slightly upturned mouth; big eye;
    # one short triangular dorsal fin over the pelvic fins; small anal fin far back;
    # deeply forked caudal; a keel of ventral scutes; no lateral line on the flank
    # (clupeids lack one). Dark dorsum over silver flanks, as in living herrings.
    "knightia": dict(
        ramps={
            "outline": ramp("1c243c"),
            "back": ramp("24466a", "346888", "508ca4", "78b4c4"),
            "flank": ramp("6e7c98", "9eacc4", "ccd6e6", "f4f8fc"),
            "fin": ramp("7a8896", "aab8bc", "d6dedc"),
            "accent": ramp("dcc890"),
        },
        front=1.0, back=1.08, icon=0.58,
        shiny={"back": dict(deg=-165, sat=1.15, val=1.05),
               "fin": dict(deg=-180, sat=2.2, val=1.0)},
        body=dict(x0=-24, x1=14, tilt=(0.6, -0.3),
                  up=[(0, 0.5), (0.04, 2.0), (0.12, 4.4), (0.25, 6.9), (0.42, 7.9), (0.62, 6.6), (0.85, 3.8), (1.0, 2.6)],
                  dn=[(0, 0.5), (0.04, 1.6), (0.12, 4.2), (0.27, 8.2), (0.44, 9.2), (0.64, 7.2), (0.86, 4.0), (1.0, 2.6)]),
        dorsal_line=-0.22,
        caudal=[(13.5, -2.4), (20.5, -6.8), (28, -11.5), (25.5, -6.5), (22.5, -1.0),
                (22.5, 1.0), (25.5, 6.5), (28, 11.5), (20.5, 6.8), (13.5, 2.4)],
        dorsal=[(-6.5, 1.2), (-4.5, -8.0), (-2.5, -6.0), (2.5, -1.6), (3.0, 1.2)],
        anal=[(6.0, -1.0), (8.0, 4.0), (14.0, 2.2), (13.5, -1.0)],
        pelvic=dict(x=-4.0, inset=-1.0, rays=[(7.5, 3.5), (6.0, 5.0)], end=-1.0),
        pectoral=dict(root=(-14.0, 3.2), pivot=(-14, 4.0), rays=[(9.0, 3.2), (8.0, 5.0)], end=(-13.0, 6.0)),
        caudal_rays=dict(x=15.0, v=(-8.5, -4.0, 4.0, 8.5), root=0.2, reach=1.15),
        dorsal_rays=dict(x0=-5.5, x1=1.5, n=2, lean=1.5, h=6, dh=1.6),
        operculum=(-14.5, 1.2, 4.5, 7.0),
        cheek=((-15.2, 3.4), 1.1),
        scale_lattice=True,
        mouth=dict(closed=[(-24.0, 0.6), (-20.0, 1.8)],
                   open=[[(-24.0, 0.3), (-20.0, 1.6)], [(-23.5, 1.4), (-20.5, 2.2)]],
                   gap=(-23.0, 1.0)),
        scutes=dict(x0=-15, x1=6, step=2, inset=0.6),
        eye=((-16.8, -1.4), 3.0),
        thickness=0.38,
    ),
}
