"""Which body plan draws each roster species: the one table.

Keys are art folder names (graphics/pokemon/strata/<folder>, the roster name
lower-cased). Every roster species must appear exactly once; gen_sprite.py
checks this against tools/strata/roster on every run. Moving a species to
another plan means moving its spec to that plan's spec file too.

Each plan has plans/<plan>.py (the template) and specs/<plan>.py (the species
data). An artist agent owns both files of its plans and nothing else.
"""

# plan: (what it covers, [species folders])
PLANS = {
    "fish": ("ray-finned fish, side view: clupeids, gars",
             ["knightia", "lepisosteus"]),
    "ray": ("stingrays, seen from above / banking",
            ["heliobatis"]),
    "small_mammal": ("generalised small quadrupeds: multituberculates, cimolestids, stagodontids, "
                     "condylarths, periptychids",
                     ["mesodma", "cimolestes", "didelphodon", "loxolophus", "carsioptych", "taeniolabis", "hyopsodus"]),
    "rodent_lagomorph": ("rodents and rabbits: gnawing incisors, big hind feet, squirrels, prairie dogs",
                         ["ischyromys", "paramys", "palaeolagus", "douglassciur", "cynomys"]),
    "primate": ("arboreal primates and plesiadapiforms: grasping hands, long tails, big eyes",
                ["purgatorius", "teilhardina", "notharctus", "omomys"]),
    "bat": ("bats: wing membranes, perched or in flight",
            ["onychonycter"]),
    "canid": ("dogs and foxes (the dog starter lines)",
              ["hesperocyon", "leptocyon", "epicyon", "aenocyon", "canis", "vulpes"]),
    "carnivoran": ("cats, bears, mustelids, miacids/viverravids, creodonts (oxyaenids, hyaenodonts), triisodonts",
                   ["protictis", "miacis", "mustela", "hoplophoneus", "miracinonyx", "panthera", "arctodus",
                    "oxyaena", "patriofelis", "hyaenodon", "eoconodon"]),
    "equid": ("horses, from dawn horses to Equus: toe count, muzzle length and mane change along the line",
              ["sifrhippus", "eohippus", "mesohippus", "protohippus", "hypohippus", "cormohippari", "equus"]),
    "ungulate": ("slender even-toed ungulates: early artiodactyls, ruminants, pronghorns, camels, oreodonts, sheep",
                 ["diacodexis", "leptomeryx", "cosoryx", "antilocapra", "poebrothere", "procamelus", "camelops",
                  "merycoidodon", "ovis"]),
    "hoofed_giant": ("heavy-bodied large herbivores/omnivores: pantodonts, uintatheres, entelodonts, bovines",
                     ["coryphodon", "uintatherium", "archaeothere", "bison", "ovibos"]),
    "rhino_brontothere": ("rhinocerotoids (hornless and horned) and brontotheres",
                          ["hyrachyus", "subhyracodon", "teleoceras", "aphelops"]),
    "proboscidean": ("mammoths and mastodons: trunk, tusks, domed head",
                     ["mammuthus"]),
    "bird_ground": ("ground fowl and terror-bird-sized galloanserans: galliforms, Gastornis",
                    ["asteriornis", "gallinuloid", "meleagris", "centrocercus", "gastornis"]),
    "bird_flying": ("small flying/perching birds, wings folded or spread: enantiornithines",
                    ["avisaurus"]),
    "crane_raptor": ("long-legged waders and raptorial birds: cranes, presbyornithid ducks, vultures",
                     ["presbyornis", "balearica", "anchigyps"]),
    "theropod": ("bipedal theropods: tyrannosaurs, dromaeosaurs (feathered), oviraptorosaurs",
                 ["tyrannosaur", "acheroraptor", "anzu"]),
    "ornithischian": ("ceratopsians, hadrosaurs, ankylosaurs, pachycephalosaurs, small ornithopods",
                      ["triceratops", "edmontosaur", "ankylosaurus", "pachycephalo", "thescelosaur"]),
    "croc_champsosaur": ("low-slung aquatic reptiles: crocodylians, choristoderes",
                         ["champsosaur", "borealosuch"]),
    "turtle": ("turtles and tortoises: snappers, the tortoise Stylemys",
               ["emarginachel", "protochelyd", "chelydra", "stylemys", "macrochelys"]),
}

# Suggested artist lanes (one agent each), balanced by species count and shared
# anatomy. The lead may regroup; ownership is per plan.
LANES = [
    ["canid", "carnivoran"],
    ["equid", "ungulate"],
    ["hoofed_giant", "rhino_brontothere", "proboscidean"],
    ["small_mammal", "rodent_lagomorph", "primate", "bat"],
    ["theropod", "ornithischian"],
    ["bird_ground", "bird_flying", "crane_raptor"],
    ["fish", "ray", "croc_champsosaur", "turtle"],
]

SPECIES_PLAN = {folder: plan for plan, (_, folders) in PLANS.items() for folder in folders}
