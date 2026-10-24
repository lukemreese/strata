"""Species specs for the croc_champsosaur body plan (plans/croc_champsosaur.py).
Owned by the aqua artist. See specs/fish.py for the common keys and the plan
docstring for the knobs."""

from ..core.color import ramp

SPECS = {
    # Champsosaurus, Hell Creek Fm (~66 Ma): a choristodere, not a crocodylian.
    # Gharial-like: a very long, slender snout lined with small conical teeth,
    # the back of the skull flared wide (huge temporal openings), eyes on top,
    # a slim body, short limbs (poorly suited to land; probably only females
    # came ashore to lay eggs) and a long, deep, swimming tail. No osteoderms;
    # skin impressions show small scales. Colour speculative: olive-brown above
    # with faint bands, pale beneath, like many aquatic reptiles.
    "champsosaur": dict(
        ramps={
            "outline": ramp("1c1a12"),
            "hide": ramp("41402a", "62603e", "868456", "a8a672"),
            "band": ramp("31301f", "4a4830"),
            "belly": ramp("b2aa80", "d0c89e", "ece6c4"),
            "eye": ramp("b89c3c"),
            "teeth": ramp("f2eedc"),
            "mouth": ramp("c49c88", "e4c0ac"),
        },
        front=0.78, back=0.95, icon=0.38,
        shiny={"hide": dict(deg=-25, sat=0.7, val=1.1), "band": dict(deg=-25, sat=0.7, val=1.1)},
        snout=23.0, snout_h=1.0, snout_w=1.3, skull=8.5, skull_h=4.4, skull_w=6.4,
        body=26.0, body_h=5.4, body_w=6.0, stance=2.6, legs=0.9, gape=13,
        tail=46.0, tail_r=4.4, tail_arc=6.0, crest=0.0, scutes=False, teeth="fine", head_up=6.0,
        bands=(), tail_bands=(0.12, 0.3, 0.48, 0.64, 0.8),
        ow=dict(tracks="TRACKS_SLITHER", end_zoom=1.25),
    ),
    # Borealosuchus, Hell Creek Fm (~66 Ma): a generalised early crocodylian,
    # ~3.5 m. Medium-broad snout with big interlocking teeth, raised eye sockets,
    # rows of keeled osteoderms down the back and a double crest of scutes on the
    # tail. Colour from living crocodylians: dark olive with faint crossbands,
    # cream belly.
    "borealosuch": dict(
        ramps={
            "outline": ramp("1a1e14"),
            "hide": ramp("3a4028", "586040", "7a8058", "9ea078"),
            "band": ramp("2c3020", "444a30"),
            "belly": ramp("aaa27a", "ccc69e", "eae4c2"),
            "eye": ramp("c8a838"),
            "teeth": ramp("f2eedc"),
            "mouth": ramp("c89c84", "e8c2a8"),
        },
        front=0.86, back=1.0, icon=0.42,
        shiny={"hide": dict(deg=-18, sat=0.45, val=0.82), "band": dict(deg=-18, sat=0.45, val=0.8)},
        snout=15.0, snout_h=1.8, snout_w=2.9, skull=9.0, skull_h=4.6, skull_w=5.4,
        body=26.0, body_h=6.2, body_w=7.6, stance=5.0, legs=1.0,
        tail=40.0, tail_r=5.4, tail_arc=7.0, crest=1.5, scutes=True, teeth="croc", head_up=5.0,
        bands=(), tail_bands=(0.14, 0.32, 0.5, 0.66, 0.82),
    ),
}
