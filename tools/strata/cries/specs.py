"""Every species' cry: a basis note and a call program.

    folder: (basis, [(call, {options}), ...])

`call` is a function in voices.py (see CALLS); options are its keyword
arguments plus `gap` (seconds before this call; negative overlaps the previous
one, default 0.06) and `gain` (relative level, default 1; each call is
peak-normalised first). Pitch and formants come from the species' mass and
body plan (voices.PLAN_VOICE); `k` scales the plan's pitch for that call.

Basis (shown in the report and docs/strata_art.md):
  living       the species, or genus, is alive and its calls are recorded
  relative     modelled on living relatives or close ecological analogues
  speculative  no living relative with comparable anatomy; a plausible guess
               (non-avian dinosaurs: closed-mouth booms, hisses and nasal honks,
               not roars, following Riede et al. 2016)
  silent       the animal makes no vocal sound; a non-vocal placeholder

Order and pacing: the first ~0.3 s is all the engine plays in double battles
(CRY_MODE_DOUBLES), so the signature sound comes first.
"""

CRIES = {
    # ---- dog starter line (small mammal -> carnivorans -> canids)
    "cimolestes":   ("relative: shrews and tenrecs (squeaks, hiss)",
                     [("squeak", dict(n=3)), ("hiss", dict(dur=0.16, gain=0.5))]),
    "protictis":    ("relative: genets and civets (chatter, growl)",
                     [("chitter", dict(n=7, k=0.7)), ("growl", dict(k=1.0, dur=0.35, gain=0.8))]),
    "miacis":       ("relative: small carnivorans (growl, yelp)",
                     [("growl", dict(k=1.0, dur=0.3)), ("bark", dict(n=2, k=1.35, rough=0.2))]),
    "hesperocyon":  ("relative: foxes and small canids (yips)",
                     [("yip", dict(n=3))]),
    "leptocyon":    ("relative: foxes (yip, short howl)",
                     [("yip", dict(n=2)), ("howl", dict(k=1.4, dur=0.5))]),
    "epicyon":      ("relative: borophagines were hyena-like; spotted hyena growl and whoop",
                     [("growl", dict(k=0.8, dur=0.35)), ("whoop", dict(gap=0.02))]),
    "aenocyon":     ("relative: grey wolf howl",
                     [("howl", dict(k=0.95, dur=1.1))]),
    "canis":        ("living: coyote yip-howl",
                     [("yip", dict(n=3, gap=0.06)), ("howl", dict(dur=0.75, gap=0.03))]),
    "vulpes":       ("living: swift fox barks",
                     [("bark", dict(n=4, k=1.2, dur=0.07, rough=0.25, gap=0.05))]),

    # ---- bird starter line (galloanserans)
    "asteriornis":  ("relative: galloanseran chicks (peeps)",
                     [("peep", dict(n=3))]),
    "gallinuloid":  ("relative: guans and chachalacas (clucks)",
                     [("cluck", dict(n=3))]),
    "meleagris":    ("living: wild turkey gobble",
                     [("gobble", dict())]),
    "centrocercus": ("living: sage-grouse strut (coos, swish, air-sac pops)",
                     [("strut", dict())]),
    "presbyornis":  ("relative: ducks and screamers (quacks)",
                     [("quack", dict(n=3, k=0.75))]),
    "gastornis":    ("speculative: closed-mouth boom, as in cassowaries and emus",
                     [("boom", dict(n=2, k=0.32, dur=0.42))]),

    # ---- snapping-turtle starter line and other turtles
    "emarginachel": ("relative: snapping turtles (hiss, snap)",
                     [("hiss", dict(dur=0.32, centre=3800)), ("jaw_pop", dict(n=1, freq=520))]),
    "protochelyd":  ("relative: snapping turtles (hiss, grunt)",
                     [("hiss", dict(dur=0.38, centre=3100)), ("grunt", dict(n=1, k=0.9))]),
    "chelydra":     ("living: common snapping turtle hiss and snap",
                     [("hiss", dict(dur=0.42, centre=3400)), ("jaw_pop", dict(n=2, freq=460))]),
    "macrochelys":  ("living: alligator snapping turtle hiss and grunt",
                     [("hiss", dict(dur=0.5, centre=2400, bw=2400, low=0.6)), ("grunt", dict(n=1, k=0.8))]),
    "stylemys":     ("relative: gopher tortoises (grunts and groans)",
                     [("grunt", dict(n=3, k=1.0, gap=0.1, decay=0.1))]),

    # ---- Hell Creek dinosaurs (all speculative)
    "tyrannosaur":  ("speculative: closed-mouth boom and hiss (crocodylian/bird bracket)",
                     [("boom", dict(n=2, k=0.75, dur=0.36)), ("hiss", dict(dur=0.26, centre=2200, gap=0.0, gain=0.5))]),
    "triceratops":  ("speculative: closed-mouth rumble and grunts",
                     [("boom", dict(n=1, k=0.95, dur=0.45)), ("grunt", dict(n=2, k=1.25, gap=0.1))]),
    "edmontosaur":  ("speculative: nasal-vestibule honk (hadrosaur nasal resonance)",
                     [("honk", dict(k=1.1, dur=0.5)), ("honk", dict(k=1.0, dur=0.35, gap=0.08, gain=0.7))]),
    "ankylosaurus": ("speculative: snort and resonant honk through looping nasal passages",
                     [("honk", dict(k=0.85, dur=0.45, nasal=0.6)), ("huff", dict(n=2, dur=0.14, centre=500, gap=0.04))]),
    "pachycephalo": ("speculative: grunts; the knock is the dome, not the voice",
                     [("grunt", dict(n=2, k=1.1)), ("knock", dict(n=2, freq=950))]),
    "thescelosaur": ("speculative: closed-mouth hoots, as in tinamous and doves",
                     [("hoot", dict(n=2, k=1.5))]),
    "acheroraptor": ("speculative: hiss and closed-mouth coos (bird-like dromaeosaur)",
                     [("hiss", dict(dur=0.22, centre=4200)), ("hoot", dict(n=2, k=1.9, dur=0.13, gap=0.09))]),
    "anzu":         ("speculative: cassowary-like hoot and boom",
                     [("hoot", dict(n=1, k=1.15, dur=0.28)), ("boom", dict(n=1, k=1.3, dur=0.5, gap=0.04))]),

    # ---- other reptiles
    "champsosaur":  ("speculative: hiss and jaw clap (choristoderes have no living relatives)",
                     [("jaw_pop", dict(n=2, freq=300, gap=0.1)), ("hiss", dict(dur=0.25, centre=2600, gap=0.04))]),
    "borealosuch":  ("relative: crocodylian bellow and hiss",
                     [("growl", dict(k=0.6, dur=0.6, pulse=18)), ("hiss", dict(dur=0.25, centre=2800, gain=0.6))]),

    # ---- small mammals
    "mesodma":      ("relative: mice and shrews (squeaks)",
                     [("squeak", dict(n=4, dur=0.05, gap=0.04))]),
    "didelphodon":  ("relative: Virginia opossum hiss and growl",
                     [("hiss", dict(dur=0.28, centre=3300)), ("growl", dict(k=0.9, dur=0.45, gap=0.02))]),
    "loxolophus":   ("relative: small omnivores (squeak, grunt)",
                     [("squeak", dict(n=2, k=0.8)), ("grunt", dict(n=2, k=0.4))]),
    "carsioptych":  ("relative: peccaries (grunts, snort)",
                     [("grunt", dict(n=3, k=0.36, gap=0.08)), ("snort", dict(dur=0.18))]),
    "taeniolabis":  ("relative: large rodents (chatter, grunt)",
                     [("chitter", dict(n=6, k=0.7, rate=12)), ("grunt", dict(n=1, k=0.5))]),
    "hyopsodus":    ("relative: small herbivores (quick squeaks)",
                     [("squeak", dict(n=4, k=1.1, dur=0.07, gap=0.035, sweep=(1.0, 1.15, 0.7)))]),

    # ---- rodents and rabbits
    "paramys":      ("relative: squirrels and porcupines (chatter, squeak)",
                     [("chitter", dict(n=8, k=0.75, rate=18)), ("squeak", dict(n=1, k=0.9, dur=0.1))]),
    "ischyromys":   ("relative: rodents (squeaks, chitter)",
                     [("squeak", dict(n=3, k=0.85, sweep=(0.9, 1.3, 0.7))), ("chitter", dict(n=4, k=0.8))]),
    "palaeolagus":  ("relative: rabbits are nearly silent: foot thumps and a squeal",
                     [("knock", dict(n=2, freq=190, gap=0.15)), ("squeak", dict(n=1, k=0.6, dur=0.18, noise=0.15))]),
    "douglassciur": ("relative: tree squirrel chatter",
                     [("chitter", dict(n=10, k=0.6, rate=14)), ("squeak", dict(n=1, k=1.1, dur=0.12))]),
    "cynomys":      ("living: black-tailed prairie dog jump-yip and alarm barks",
                     [("yip", dict(n=1, k=0.75, dur=0.22)), ("bark", dict(n=3, k=0.55, dur=0.07, rough=0.1, gap=0.07))]),

    # ---- primates
    "purgatorius":  ("relative: tree shrews and mouse lemurs (trill)",
                     [("twitter", dict(n=6))]),
    "teilhardina":  ("relative: mouse lemurs (squeaks, trill)",
                     [("squeak", dict(n=2, k=0.9)), ("twitter", dict(n=5, k=0.8, drop=0.15))]),
    "omomys":       ("relative: tarsiers (whistles, trill)",
                     [("whistle", dict(k=1.0, dur=0.25)), ("twitter", dict(n=4, k=0.9))]),
    "notharctus":   ("relative: lemurs (plaintive wail)",
                     [("wail", dict())]),

    # ---- bat
    "onychonycter": ("relative: bats; slowed FM sweeps (whether it echolocated is debated) and social squeaks",
                     [("echo", dict(n=7)), ("chitter", dict(n=4, k=0.55, gap=0.05))]),

    # ---- fish and ray
    "knightia":     ("relative: herring 'fast repetitive ticks' from swim-bladder air",
                     [("ticks", dict())]),
    "lepisosteus":  ("relative: gars gulp air at the surface",
                     [("gulp", dict())]),
    "heliobatis":   ("silent: stingrays make no vocal sound; a splash and bubbles",
                     [("splash", dict())]),

    # ---- carnivorans and creodonts
    "eoconodon":    ("speculative: growl and grunt",
                     [("growl", dict(k=0.8, dur=0.45)), ("grunt", dict(n=1, k=0.8))]),
    "oxyaena":      ("speculative: wolverine-like growl and hiss",
                     [("growl", dict(k=1.0, dur=0.45, pulse=34)), ("hiss", dict(dur=0.2, gain=0.6))]),
    "patriofelis":  ("speculative: deep growl and cough",
                     [("growl", dict(k=0.8, dur=0.5, pulse=22)), ("bark", dict(n=1, k=0.9))]),
    "hyaenodon":    ("speculative: barks and growl",
                     [("bark", dict(n=2, k=1.0)), ("growl", dict(k=0.8, dur=0.35))]),
    "hoplophoneus": ("relative: cats (hissing snarl)",
                     [("hiss", dict(dur=0.25, centre=3600)), ("growl", dict(k=0.95, dur=0.5, hiss_amt=0.3))]),
    "miracinonyx":  ("relative: cheetah and puma chirps",
                     [("chirp", dict(n=3, k=2.4))]),
    "panthera":     ("relative: lion roar and grunts",
                     [("roar", dict(dur=0.8))]),
    "arctodus":     ("relative: bears (growl, huff, jaw pops)",
                     [("growl", dict(k=0.9, dur=0.55, pulse=20)), ("huff", dict(n=1)), ("jaw_pop", dict(n=2))]),
    "mustela":      ("living: black-footed ferret dooking",
                     [("dook", dict(n=7, k=0.55))]),

    # ---- horses
    "sifrhippus":   ("relative: horses (a small, high whinny)",
                     [("whinny", dict(dur=0.5))]),
    "eohippus":     ("relative: horses (snort, whinny)",
                     [("snort", dict(dur=0.2)), ("whinny", dict(dur=0.6))]),
    "mesohippus":   ("relative: horses (whinny)",
                     [("whinny", dict(dur=0.8))]),
    "protohippus":  ("relative: horses (whinny, snort)",
                     [("whinny", dict(dur=0.9)), ("snort", dict(dur=0.22))]),
    "hypohippus":   ("relative: horses (soft nicker and snort: a forest browser)",
                     [("nicker", dict()), ("snort", dict(dur=0.25))]),
    "cormohippari": ("relative: zebras and horses (short whinny, barks)",
                     [("whinny", dict(dur=0.5, tremolo=7, k=1.1)), ("bark", dict(n=2, k=1.2, dur=0.1))]),
    "equus":        ("living: horse whinny and nicker",
                     [("whinny", dict(dur=0.9)), ("nicker", dict(dur=0.25))]),

    # ---- slender even-toed ungulates
    "diacodexis":   ("relative: chevrotains and small antelope (bleat)",
                     [("bleat", dict(dur=0.4, trem=9))]),
    "leptomeryx":   ("relative: chevrotains (high double bleat)",
                     [("bleat", dict(k=1.3, dur=0.33, trem=11, depth=0.3)), ("bleat", dict(k=1.22, dur=0.28, trem=11, depth=0.3))]),
    "cosoryx":      ("relative: deer alarm snort and bark",
                     [("snort", dict(dur=0.18)), ("bark", dict(n=2, k=1.0, gap=0.1))]),
    "antilocapra":  ("living: pronghorn snort and fawn bleat",
                     [("snort", dict(dur=0.3, centre=900)), ("bleat", dict(k=0.9, dur=0.3))]),
    "poebrothere":  ("relative: llamas and alpacas hum",
                     [("hum", dict(dur=0.6))]),
    "procamelus":   ("relative: camelids (hum, groan)",
                     [("hum", dict(k=0.8, dur=0.45, rise=1.2)), ("groan", dict(k=0.6, dur=0.55))]),
    "camelops":     ("relative: camel groan and gurgle",
                     [("groan", dict(dur=0.9))]),
    "merycoidodon": ("speculative: bleat and grunts (oreodonts have no living relatives)",
                     [("bleat", dict(k=0.7, dur=0.4, trem=5)), ("grunt", dict(n=2))]),
    "ovis":         ("living: bighorn sheep bleat",
                     [("bleat", dict(dur=0.75))]),

    # ---- heavy hoofed animals
    "coryphodon":   ("relative: hippos (wheeze and honk series)",
                     [("bellow", dict(k=1.1, dur=0.5)), ("grunt", dict(n=3, k=0.9, gap=0.07))]),
    "uintatherium": ("speculative: deep bellow and grunts",
                     [("bellow", dict(k=0.8, dur=0.7)), ("grunt", dict(n=2, k=0.6))]),
    "archaeothere": ("relative: pigs (grunts, snort)",
                     [("grunt", dict(n=4, k=0.7, gap=0.08)), ("snort", dict(dur=0.2))]),
    "bison":        ("living: bison bull bellow",
                     [("bellow", dict(k=0.7, dur=1.1, rough=0.55))]),
    "ovibos":       ("living: musk ox snort and roar",
                     [("snort", dict(dur=0.25)), ("bellow", dict(k=0.9, dur=0.7))]),

    # ---- rhinos
    "hyrachyus":    ("relative: rhinos (snort, calf squeal)",
                     [("snort", dict(dur=0.2)), ("bleat", dict(k=1.6, dur=0.35, trem=5, depth=0.2))]),
    "subhyracodon": ("relative: rhinos (huffs, grunts)",
                     [("huff", dict(n=2)), ("grunt", dict(n=2, k=0.8))]),
    "teleoceras":   ("relative: rhinos and hippos (grunts, rumble)",
                     [("grunt", dict(n=3, k=0.8)), ("rumble", dict(dur=0.45))]),
    "aphelops":     ("relative: rhinos (snort, bellow)",
                     [("snort", dict(dur=0.25)), ("bellow", dict(k=0.9, dur=0.6))]),

    # ---- mammoth
    "mammuthus":    ("relative: elephants (trumpet, rumble)",
                     [("trumpet", dict()), ("rumble", dict(dur=0.45))]),

    # ---- other birds
    "avisaurus":    ("speculative: enantiornithine; a trilled two-voice whistle (no Mesozoic songbird syrinx known)",
                     [("trill", dict(n=9)), ("whistle", dict(k=0.8, dur=0.2))]),
    "balearica":    ("relative: crowned cranes (honk and gular-sac boom)",
                     [("bugle", dict(L=0.35)), ("boom", dict(n=1, f=130, dur=0.35, gain=0.6))]),
    "anchigyps":    ("relative: vultures hiss and grunt",
                     [("hiss", dict(dur=0.38, centre=3000)), ("grunt", dict(n=2, k=0.3))]),
}
