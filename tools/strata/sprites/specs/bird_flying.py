"""Species specs for the bird_flying body plan (plans/bird_flying.py, built on the
shared bird template in plans/bird_ground.py). See specs/fish.py for the common keys."""

from ..core.color import ramp

SPECS = {
    # Avisaurus archibaldi, Hell Creek Fm (~66 Ma): an enantiornithine ("opposite
    # bird") known only from its tarsometatarsus; avisaurids were among the largest
    # enantiornithines (mass estimated ~1 kg). The rest follows better-known
    # enantiornithines: a toothed snout, clawed fingers on the wing, a pygostyle
    # with a short feather fan, strong grasping (perching) feet. Plumage is a
    # reconstruction: melanosome studies of enantiornithines found dark and grey
    # tones, so dark grey-brown above with a buff breast; the pale wing bar is a
    # guess. Shown perched on a branch (tree-dwellers vanished with the forests at
    # the K-Pg). Frame 2: wings raised with a gape. Shiny: a paler grey population.
    "avisaurus": dict(
        ramps={
            "outline": ramp("1e1a18"),
            "body": ramp("3a3430", "5a524a", "7e746a", "a29888"),
            "belly": ramp("a8946e", "ccb890", "e8dcbc"),
            "wing": ramp("2c2622", "4a423a", "6c6256"),
            "beak": ramp("2a2624", "565048"),
            "wood": ramp("5e4a36", "86704e"),
        },
        front=1.0, back=1.0, icon=0.44,
        shiny={"body": dict(deg=0, sat=0.4, val=1.3), "wing": dict(deg=0, sat=0.4, val=1.45)},
        leg_ramp="beak",
        body=[(3.0, 1.0, 10.0, 7.0, 35), (-2.0, -2.0, 7.0, 6.5, 0)],
        regions=[dict(ramp="belly", below=(-1.0, -0.6), on="body"),
                 dict(ramp="belly", ellipse=(-9.0, -9.5, 3.4, 2.6), on="head")],
        neck=dict(pts=[(-3.0, -6.0), (-6.0, -11.0)], radii=[4.6, 3.6]),
        head=[(-7.5, -13.5, 4.6, 4.0, 0)],
        beak=dict(upper=dict(pts=[(-11.0, -14.0), (-15.0, -13.4), (-17.8, -12.7)], radii=[1.6, 1.0, 0.5]),
                  lower=dict(pts=[(-11.0, -12.3), (-16.8, -12.1)], radii=[1.1, 0.5]),
                  hinge=(-11.0, -12.6)),
        eye=((-8.0, -14.6), 1.5, 0.9), eye_hi=("belly", 2), eye_ring=("body", 3),
        spread=dict(root=(0.0, -4.0), far=(3.0, -3.5),
                    poly=[(-1.0, -5.0), (6.0, -14.0), (12.0, -17.0), (22.0, -18.5), (20.0, -15.5), (21.5, -13.5),
                          (18.0, -12.0), (19.0, -9.5), (15.0, -8.5), (15.5, -6.0), (11.0, -5.0), (10.0, -1.0),
                          (5.0, 1.0)],
                    coverts=(5.0, -7.5, 6.0, 4.0, -28),
                    claw=dict(pts=[(6.0, -14.0), (4.4, -15.8), (3.4, -15.4)], radii=[0.7, 0.5, 0.35])),
        feather_lines=[[(8.0, -12.0), (18.0, -14.5)], [(8.0, -9.5), (16.5, -10.5)], [(7.0, -6.5), (13.0, -6.5)]],
        tail=[[(8.0, 5.0), (17.0, 14.0), (13.5, 17.5), (6.0, 9.0)]],
        tail_root=(7.0, 6.0),
        legs=[
            dict(near=False, swing=-1, hip=(5.0, 6.0), ankle=(8.0, 10.5), foot=(6.0, 14.5),
                 toes=[(2.5, 15.5), (3.2, 17.0)], hallux=(9.0, 16.0), tibia_r=(3.0, 1.4), tarsus_r=(0.9, 0.8),
                 toe_r=0.6, tibia_ramp="body"),
            dict(near=True, swing=1, hip=(2.0, 6.0), ankle=(5.0, 10.5), foot=(3.0, 14.5),
                 toes=[(-0.5, 15.5), (0.2, 17.0)], hallux=(6.0, 16.0), tibia_r=(3.2, 1.5), tarsus_r=(0.95, 0.85),
                 toe_r=0.65, tibia_ramp="body"),
        ],
        perch=dict(pts=[(-16.0, 16.4), (4.0, 15.9), (24.0, 16.8)], radii=[1.8, 2.0, 1.6], ramp="wood"),
        wing_lift=30, gape=22, neck_pivot=(-3.0, -6.0),
        scallops=dict(ramps=("body",), rows=3, period=4, shift=2),
        marks=[
            dict(pts=[(-13.0, -12.9)], color=("belly", 2), on="head", phase=1),   # teeth, seen when it gapes
            dict(pts=[(-15.0, -12.6)], color=("belly", 2), on="head", phase=1),
            dict(pts=[(1.5, -8.0), (6.0, -11.2), (9.5, -12.0)], color=("belly", 1), on="wing"),  # pale wing bar
            dict(pts=[(-12.0, -15.6), (-9.0, -17.0), (-5.0, -16.4)], color=("body", 3), on="head"),  # pale brow
            dict(pts=[(-15.4, -13.9)], color="outline", on="head"),      # nostril
        ],
        ow=dict(tracks="TRACKS_NONE", length=22),
    ),
}
