"""Blind identification of creature sprites by a local vision model.

The style guide's first test is "the silhouette names the animal" (docs/strata_art.md).
This asks a model that has never seen the roster what each sprite is, and grades the
answer against a keyword list per body plan. A miss is not a verdict on the art: it is
the order in which to look at the sprites. Animals with no living look-alike (a
uintathere, a champsosaur) are graded against what a lay viewer would reasonably say.

Grades: `top1` (first guess matches), `top3` (a later guess matches), `miss`.
"""

import os
import re

from sprites import SPECIES_PLAN, roster
from sprites.core.paths import ROOT, read_pal, read_png, species_dir, write_png
from sprites.core.preview import blit, canvas

from .client import read_bytes, run_batch

SCALE = 6
BACKDROP = (150, 170, 150)  # mid-value, low-saturation: neither battle palette, no sprite's outline

# What a lay viewer may call each body plan. Lower-case; matched as whole words, plural allowed.
BIRD = ["bird", "fowl"]
DINOSAUR = ["dinosaur", "dino"]
PLAN_ACCEPT = {
    "fish": ["fish", "herring", "sardine", "shad", "gar", "pike", "perch", "minnow", "trout", "carp", "bass"],
    "ray": ["ray", "stingray", "skate", "manta"],
    "small_mammal": ["mouse", "rat", "rodent", "shrew", "opossum", "possum", "vole", "mammal"],
    "rodent_lagomorph": ["rodent", "squirrel", "mouse", "rat", "marmot", "prairie dog", "gopher", "beaver",
                         "chipmunk", "groundhog", "hamster", "guinea pig"],
    "primate": ["lemur", "monkey", "primate", "tarsier", "bushbaby", "galago", "loris", "marmoset"],
    "bat": ["bat"],
    "canid": ["dog", "wolf", "fox", "coyote", "jackal", "canine", "dingo"],
    "carnivoran": [],  # too mixed for one list: see SPECIES_ACCEPT
    "equid": ["horse", "pony", "zebra", "donkey", "foal", "mule"],
    "ungulate": [],
    "hoofed_giant": [],
    "rhino_brontothere": ["rhino", "rhinoceros"],
    "proboscidean": ["mammoth", "elephant", "mastodon"],
    "bird_ground": BIRD + ["chicken", "hen", "rooster", "quail", "turkey", "grouse", "pheasant", "partridge"],
    "bird_flying": BIRD + ["sparrow", "finch", "robin", "thrush", "jay", "crow", "hawk", "pigeon", "dove"],
    "crane_raptor": BIRD,
    "theropod": DINOSAUR + ["theropod", "raptor"],
    "ornithischian": DINOSAUR,
    "croc_champsosaur": ["crocodile", "croc", "alligator", "gharial", "gavial", "caiman", "crocodilian"],
    "turtle": ["turtle", "tortoise", "terrapin"],
}

# Added to the plan's list for one species.
SPECIES_ACCEPT = {
    # small_mammal
    "cimolestes": ["weasel"], "didelphodon": ["badger", "otter", "tasmanian devil"],
    "loxolophus": ["raccoon", "civet", "dog", "coati"], "carsioptych": ["pig", "hog", "tapir", "peccary"],
    "taeniolabis": ["beaver", "groundhog", "marmot", "capybara"], "hyopsodus": ["weasel", "ferret", "stoat"],
    "mesodma": ["squirrel", "chipmunk"],
    # rodent_lagomorph, primate
    "palaeolagus": ["rabbit", "hare", "bunny", "pika"],
    "purgatorius": ["squirrel", "tree shrew", "treeshrew"],
    # canid
    "epicyon": ["hyena"], "hesperocyon": ["civet", "genet", "mongoose", "weasel"],
    # carnivoran
    "protictis": ["civet", "genet", "weasel", "marten", "mongoose", "cat"],
    "miacis": ["civet", "genet", "weasel", "marten", "mongoose", "cat"],
    "mustela": ["ferret", "weasel", "polecat", "mink", "stoat"],
    "hoplophoneus": ["cat", "sabertooth", "saber-tooth", "saber-toothed cat", "sabre-toothed cat", "smilodon",
                     "sabertooth cat", "saber-toothed tiger", "tiger"],
    "miracinonyx": ["cheetah", "cat", "cougar", "puma", "leopard"],
    "panthera": ["lion", "lioness", "cat", "tiger", "cougar", "puma"],
    "arctodus": ["bear"],
    "oxyaena": ["cat", "wolverine", "badger", "marten", "weasel", "civet"],
    "patriofelis": ["cat", "panther", "wolverine", "bear", "cougar"],
    "hyaenodon": ["hyena", "wolf", "dog", "thylacine"],
    "eoconodon": ["wolf", "bear", "dog", "hyena"],
    # equid: the dawn horses were cat- to dog-sized browsers
    "sifrhippus": ["deer", "tapir", "duiker", "fawn"], "eohippus": ["deer", "tapir", "duiker", "fawn"],
    # ungulate
    "diacodexis": ["deer", "mouse deer", "chevrotain", "antelope", "fawn", "duiker"],
    "leptomeryx": ["deer", "mouse deer", "chevrotain", "antelope", "fawn", "duiker"],
    "cosoryx": ["pronghorn", "antelope", "deer", "gazelle"],
    "antilocapra": ["pronghorn", "antelope", "deer", "gazelle"],
    "poebrothere": ["camel", "llama", "guanaco", "alpaca", "vicuna"],
    "procamelus": ["camel", "llama", "guanaco", "alpaca", "vicuna"],
    "camelops": ["camel", "llama", "guanaco", "alpaca", "dromedary"],
    "merycoidodon": ["pig", "hog", "boar", "sheep", "tapir", "oreodont", "peccary"],
    "ovis": ["sheep", "ram", "bighorn", "bighorn sheep", "goat", "mouflon"],
    # hoofed_giant
    "coryphodon": ["hippo", "hippopotamus", "tapir", "pantodont"],
    "uintatherium": ["rhino", "rhinoceros", "uintathere", "uintatherium"],
    "archaeothere": ["pig", "boar", "warthog", "hog", "entelodont"],
    "bison": ["bison", "buffalo", "cattle", "ox", "bull", "cow"],
    "bootherium": ["musk ox", "muskox", "bison", "ox", "buffalo", "yak"],
    # rhino_brontothere
    "hyrachyus": ["tapir", "horse"], "teleoceras": ["hippo", "hippopotamus"],
    # birds
    "gastornis": ["ostrich", "terror bird", "moa", "emu", "dodo", "cassowary"],
    "presbyornis": ["duck", "goose", "flamingo", "wader", "stilt", "avocet"],
    "balearica": ["crane", "heron", "stork", "egret"],
    "anchigyps": ["vulture", "eagle", "hawk", "condor", "buzzard", "raptor"],
    # dinosaurs
    "tyrannosaur": ["tyrannosaurus", "t-rex", "t. rex", "t rex", "tyrannosaur", "rex"],
    "acheroraptor": ["velociraptor", "dromaeosaur", "deinonychus"],
    "anzu": ["oviraptor", "ostrich", "cassowary", "bird", "emu"],
    "triceratops": ["triceratops", "ceratopsian"],
    "edmontosaur": ["hadrosaur", "duck-billed dinosaur", "duckbill", "edmontosaurus", "iguanodon"],
    "ankylosaurus": ["ankylosaurus", "ankylosaur"],
    "pachycephalo": ["pachycephalosaurus", "pachycephalosaur"],
    "thescelosaur": ["ornithopod"],
    # reptiles
    "champsosaur": ["lizard", "monitor"],
}

SCHEMA = {
    "type": "object",
    "properties": {
        "guesses": {"type": "array", "maxItems": 3,
                    "items": {"type": "string", "description": "a common name, 1-3 words"}},
        "sees": {"type": "string", "description": "one sentence: the features you based it on"},
    },
    "required": ["guesses", "sees"],
}

PROMPT = (
    "This is a small pixel-art sprite of one real animal, enlarged. The animal may be living or "
    "extinct. You are not told which. Look at the body shape, head, limbs, tail and any horns, "
    "shell, wings or fins.\n"
    "Give up to three guesses for what kind of animal it is, most likely first, each a plain common "
    "name of one to three words (for example \"horse\", \"crocodile\", \"small rodent\", \"duck-billed "
    "dinosaur\"). Do not answer with a video-game or cartoon character.")


def accept(folder):
    return PLAN_ACCEPT[SPECIES_PLAN[folder]] + SPECIES_ACCEPT.get(folder, [])


def matches(guess, keywords):
    g = guess.lower()
    return any(re.search(rf"\b{re.escape(k)}(e?s)?\b", g) for k in keywords)


def grade(guesses, keywords):
    for i, g in enumerate(guesses[:3]):
        if matches(g, keywords):
            return "top1" if i == 0 else "top3"
    return "miss"


def render(folder, path):
    """The first front frame at SCALE on a plain backdrop, written as a PNG. Returns its bytes."""
    d = species_dir(folder)
    _, _, rows = read_png(os.path.join(d, "anim_front.png"))
    frame = [r[:64] for r in rows[:64]]
    img = canvas(64 * SCALE, 64 * SCALE, BACKDROP)
    blit(img, frame, read_pal(os.path.join(d, "normal.pal")), 0, 0, SCALE)
    write_png(path, len(img[0]), len(img), img)
    return read_bytes(path)


def review(client, out, folders=None, quiet=False):
    species = [sp for sp in roster() if not folders or sp["folder"] in folders]
    unknown = set(folders or ()) - {sp["folder"] for sp in species}
    if unknown:
        raise SystemExit(f"not roster species: {', '.join(sorted(unknown))}")
    os.makedirs(os.path.join(out, "sprites"), exist_ok=True)

    def one(sp):
        png = render(sp["folder"], os.path.join(out, "sprites", sp["folder"] + ".png"))
        answer = client.ask_json(PROMPT, SCHEMA, images=[png], max_tokens=400)
        return {"guesses": answer["guesses"], "sees": answer["sees"],
                "grade": grade(answer["guesses"], accept(sp["folder"]))}

    results = run_batch(species, one, label=lambda sp: sp["folder"], quiet=quiet)
    rows = [dict(r, folder=sp["folder"], genus=sp["genus"], plan=SPECIES_PLAN[sp["folder"]])
            for sp, r in zip(species, results)]
    for r in rows:
        r.setdefault("grade", "error")
    return rows


def report(rows, model):
    order = {"error": 0, "miss": 1, "top3": 2, "top1": 3}
    count = {g: sum(r["grade"] == g for r in rows) for g in order}
    lines = [
        "# Sprite blind identification", "",
        f"Model: `{model}`. {len(rows)} sprites: **{count['top1']} named first try**, "
        f"{count['top3']} within three guesses, **{count['miss']} missed**"
        + (f", {count['error']} errors" if count["error"] else "") + ".", "",
        "A miss means *look at this sprite*, not *this sprite is wrong*: the model may not know the "
        "animal, or the keyword list in `tools/strata/localmodel/sprites.py` may be too narrow. Open "
        "`sprites/<folder>.png` (what the model saw) before changing any art.", "",
        "| Grade | Species | Plan | Guesses | Model saw |", "|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda r: (order[r["grade"]], r["plan"], r["folder"])):
        guesses = ", ".join(r.get("guesses", [])) or r.get("error", "")[:80]
        lines.append(f"| {r['grade']} | *{r['genus']}* (`{r['folder']}`) | {r['plan']} | "
                     f"{guesses} | {r.get('sees', '')} |")
    by_plan = {}
    for r in rows:
        by_plan.setdefault(r["plan"], []).append(r["grade"])
    lines += ["", "| Plan | top1 | top3 | miss |", "|---|---|---|---|"]
    lines += [f"| {p} | {g.count('top1')} | {g.count('top3')} | {g.count('miss')} |" for p, g in by_plan.items()]
    return "\n".join(lines) + "\n"


def missing_keywords():
    """Roster species with nothing to grade against (a unit test keeps this empty)."""
    return [sp["folder"] for sp in roster() if not accept(sp["folder"])]


__all__ = ["review", "report", "render", "grade", "accept", "missing_keywords", "ROOT"]
