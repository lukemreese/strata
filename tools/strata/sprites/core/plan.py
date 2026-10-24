"""The body-plan interface every plans/<name>.py module fills in.

A body plan is a parametric template: functions that turn a species spec
(a dict from specs/<plan>.py, merged over the plan's DEFAULTS) into a Model.

    side(p, phase=0, step=None) -> Model
        The side profile, head to the LEFT. Required.
        phase 0/1: the two battle front frames (idle, then a small action:
                   sniff, gape, tail sweep...).
        step 0/1:  the overworld walk cycle (contact pose, passing pose). When
                   step is not None, phase is 0. Default: step 1 = phase 1.
    back(p, phase=0) -> Model                      optional
        A dedicated back-sprite view. Without it the back sprite is the side
        model mirrored at the spec's `back` scale.
    overworld(p, view, step) -> Model              optional
        view "south" (facing the camera) or "north" (facing away), step 0/1.
        Without it the overworld uses the side view in all four directions and
        `gen_sprite.py --borrowed` reports the species as "ow: side only".

Defaults every plan may override:
    footprint  16 strings of 16 chars ("#" = ink) or None (blank)
    tracks     TRACKS_FOOT / TRACKS_NONE / TRACKS_SLITHER / TRACKS_SPOT ...
"""

FRONT_VIEWS = ("south", "north")


class BodyPlan:
    def __init__(self, name, covers, side=None, back=None, overworld=None, defaults=None,
                 footprint=None, tracks="TRACKS_FOOT", notes=""):
        self.name, self.covers, self.notes = name, covers, notes
        self._side, self.back, self.overworld = side, back, overworld
        self.defaults = defaults or {}
        self.footprint, self.tracks = footprint, tracks

    @property
    def ready(self):
        return self._side is not None

    def side(self, p, phase=0, step=None):
        if self._side is None:
            raise NotImplementedError(
                f"body plan '{self.name}' is a stub: implement side() in tools/strata/sprites/plans/{self.name}.py")
        return self._side(p, phase, step)

    def params(self, spec):
        """The spec merged over the plan defaults (dict values merge one level deep)."""
        p = {}
        for k, v in self.defaults.items():
            p[k] = dict(v) if isinstance(v, dict) else v
        for k, v in spec.items():
            if isinstance(v, dict) and isinstance(p.get(k), dict):
                p[k] = {**p[k], **v}
            else:
                p[k] = v
        return p


def stub(name, covers, notes=""):
    """A registered body plan with no template yet (an artist agent owns it)."""
    return BodyPlan(name, covers, notes=notes)
