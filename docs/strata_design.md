# Pokémon Strata: Game Design Document (draft v0.1)

> Working title. A Pokémon Essentials fan game set in the North American West,
> running from the last days of the dinosaurs to the present. Every creature is a
> real, fossil-documented animal.

---

## 1. Core pillars

1. **Real animals, real place, real time.** Every species existed. Every map is a
   real formation or site in Montana, Wyoming, Colorado, the Dakotas or Nebraska.
2. **Individuals don't evolve, lineages do.** Your party members are *lineages*.
   When time jumps, each one is replaced by its descendant species. There is no
   level-up evolution.
3. **Time accelerates.** Each act covers far more time than the one before it, so
   the clock goes from hours to tens of millions of years.
4. **Selection, not grinding.** Which descendant a lineage becomes depends on the
   pressures you put it under (habitat, diet, climate, battle role).
5. **Extinction is real.** A lineage that fits its new world badly can die out.
   Most species that ever lived did.

## 2. Framing device: climbing the rock column

The prologue is set in the **present day, at a dig in the Hell Creek Formation, Montana**.
The player is a field paleontologist. Older rock lies deeper, so playing
past → present means **climbing up the stratigraphic column**. Each act is
a rock layer the player "reconstructs" and then enters.

- A HUD shows the current layer and age (e.g. `HELL CREEK FM · 66.04 Ma`).
- The Pokédex becomes the **Field Codex**. Each entry gives the real fossil site,
  age, body mass, diet and the evidence behind the reconstruction.
- Ages are written in **Ma** (millions of years ago) and **ka** (thousands of years ago).

**Open question:** who are the "trainers" in deep time? Options:
(a) Reconstructions are simulations, so rival paleontologists can battle using
reconstructed lineages. (b) Deep-time acts have no human trainers. Bosses are
apex animals and territorial rivals, and human trainers appear only in the
present-day hub.

## 3. The timeline (acts = layers = "badges")

| Act | Layer / site | Age | Jump from previous | Clock rate feel | Key event |
|---|---|---|---|---|---|
| 0 | Present-day dig, Hell Creek, MT | today | — | real time | Prologue, starter fossil |
| 1 | Hell Creek Formation, MT | 66.04 Ma | — | hours | Last days of the dinosaurs |
| 2 | Hell Creek, MT, impact aftermath | 66.04 Ma + ~1 yr | days → 1 yr | weeks | Chicxulub impact, impact winter, "fern spike" |
| 3 | Corral Bluffs, CO | ~65.7 Ma | ~300 kyr | millennia | Mammal recovery, first legumes |
| 4 | Bighorn Basin, WY | ~56 Ma | ~10 Myr | ~100 kyr | PETM global warming, horses & primates arrive |
| 5 | Green River lakes / Bridger Basin, WY | ~52–46 Ma | ~5 Myr | ~1 Myr | Subtropical Eocene; bats, giant birds |
| 6 | White River badlands, SD/NE | ~33 Ma | ~15 Myr | ~1 Myr | Eocene–Oligocene cooling, forests open up |
| 7 | Ashfall Fossil Beds, NE | ~11.9 Ma | ~20 Myr | several Myr | Grasslands; Yellowstone-hotspot supereruption |
| 8 | Natural Trap Cave, WY | ~20 ka | ~12 Myr | several Myr | Ice Age megafauna; humans arrive |
| Epilogue | Present day | today | ~20 kyr | — | Survivors, extinctions, reintroduced horses |

Time speeds up most sharply through Acts 1–7. From Act 7 onward the jumps level
off, because the record runs out at the present. That still works: the final
cut from Ice Age to today is the shortest jump and the biggest shock, because the
largest extinction in the epilogue is the one humans were present for.

**Geography that changes across the same map**

- Act 1: the **Western Interior Seaway** is retreating. Its remnant, the Cannonball Sea, is in the Dakotas.
- Acts 1–4: the **Rocky Mountains** are rising (Laramide orogeny).
- Act 5: huge subtropical lakes cover Wyoming (Green River).
- Act 7: the ash cloud of a Yellowstone-hotspot eruption (Bruneau–Jarbidge, Idaho) buries Nebraska.
- Act 8: glaciers sit to the north, and the land bridge to Asia opens and closes.

## 4. Starter lineages: three modes of evolution

Each starter shows a different pattern seen in the fossil record.
All three are lineages with a continuous presence in North America.

### 🦊 Mammal: Dog line (directional change + branching)
The whole dog family (Canidae) **originated in North America**.

| Stage | Act | Species | Notes |
|---|---|---|---|
| 1 | 1–2 | Small burrowing placental (*Cimolestes*-grade) | Stand-in; true ancestor unknown |
| 2 | 3–4 | *Protictis* (viverravid) | Early carnivoramorph, Paleocene MT/WY |
| 3 | 5 | *Miacis* / *Vulpavus* | Tree-climbing Eocene carnivoran |
| 4 | 6 | *Hesperocyon* | Earliest true canid, White River |
| 5a | 7 | *Epicyon* (borophagine) | Bone-crushing "hyena-dog" → **extinct** |
| 5b | 7 | *Leptocyon* | Small fox-like generalist |
| 6a | 8 | *Aenocyon dirus* (dire wolf) | Megafauna specialist → **extinct** |
| 6b | 8 | *Canis latrans* (coyote) | Generalist → **survives to today** |

Lesson: the specialist branches are stronger in their own era but die out later.

### 🦃 Bird: Galloanseran line (adaptive radiation)
Ground-dwelling birds survived the impact. Tree-dwelling birds mostly did not.

| Stage | Act | Species | Notes |
|---|---|---|---|
| 1 | 1–2 | Small ground fowl (*Asteriornis*-grade) | "Wonderchicken" grade; stand-in |
| 2a | 4–5 | *Gastornis* | 2 m flightless giant → **extinct** by mid-Eocene |
| 2b | 5 | *Presbyornis* | Long-legged lake duck, Green River |
| 2c | 5 | *Gallinuloides* | Early galliform, Green River |
| 3 | 6–8 | (galliform chain) → *Meleagris* | Turkey, endemic to North America |

Lesson: one survivor radiates into many body plans. Big and flightless is a dead end here.

### 🐢 Reptile: Snapping turtle line (stasis)
Snapping turtles have lived in Montana from the Cretaceous to today with very little change.

| Stage | Act | Species | Notes |
|---|---|---|---|
| 1 | 1–3 | *Emarginachelys cretacea* | Hell Creek chelydrid |
| 2 | 4–6 | *Protochelydra zangerli* | Paleocene, North Dakota |
| 3 | 7–E | *Chelydra serpentina* | Common snapping turtle |

Lesson: if a body plan works, **stabilising selection** keeps it. This line
changes form rarely, but gets big stat boosts from surviving every extinction filter.
It is the "hard mode / safe mode" starter.

## 5. Other signature lineages (wild / catchable)

- **Horse line** *(immigrates at the PETM; it did not originate here)*: *Sifrhippus* →
  *Eohippus*/*Protorohippus* → *Orohippus* → *Mesohippus* → *Merychippus* →
  *Cormohipparion* / *Pliohippus* → *Equus*. Horses **die out in North America ~11 ka**
  and return with the Spanish in the 1500s, which is part of the epilogue.
- **Camel line** (also North American in origin): *Poebrotherium* → *Procamelus* → *Aepycamelus* → *Camelops*.
- **Multituberculates**: *Mesodma* → *Taeniolabis* → *Ptilodus* → extinct by ~34 Ma.
  They were the most long-lived mammal order of all time. Their dying out is a midgame story beat.
- **Rhinos**: *Subhyracodon* → *Teleoceras* (hippo-like, preserved at Ashfall) → extinct in NA.
- **Pronghorn**: *Antilocapra* runs much faster than any living predator needs. That speed is a
  "ghost" of the extinct American cheetah (*Miracinonyx*) in Act 8.

## 6. Bosses (one apex per layer)

| Act | Boss | Why |
|---|---|---|
| 1 | *Tyrannosaurus rex* | Apex of Hell Creek |
| 2 | **The impact winter** (survival gauntlet) | The "boss" is the environment |
| 3 | *Taeniolabis* herd / crocodyliform | First large mammals after the impact |
| 4 | *Gastornis* | Giant bird during the PETM |
| 5 | *Uintatherium* | Six-horned Bridger giant |
| 6 | *Archaeotherium* ("hell pig") or *Hoplophoneus* | White River apex |
| 7 | **The ashfall** + *Epicyon* | The eruption ends the act |
| 8 | *Arctodus simus* (short-faced bear) / *Smilodon* | Ice Age apex |

## 7. Systems

### 7.1 Lineage descent (replaces evolution)
- Evolution by level is turned off. Species have **no** `Evolutions=` lines in PBS.
- New PBS file `PBS/lineages.txt` maps `ancestor → [descendant candidates + conditions]`.
- On an era jump, every Pokémon in the party and PC is processed:
  1. Read its **selection pressures** (see 7.2).
  2. Pick the best-fitting descendant for the new era.
  3. If no descendant fits the new era → **extinction check**.
  4. Play a "deep time" lapse animation (strata scrolling, silhouette morph).
- The descendant **inherits** nickname, OT, a share of EVs/IVs (heredity) and
  learned moves where they still make sense.

### 7.2 Selection pressures (tracked per lineage)
Hidden counters stored on each Pokémon. The game has no contests, so the six `u8`
contest stats in `struct BoxPokemon` (`cool`, `beauty`, `cute`, `smart`, `tough`,
`sheen`) are repurposed as pressure counters. They are already saved for both the
party and the PC boxes.

| Pressure | Raised by | Pushes toward |
|---|---|---|
| Habitat | Battling/walking in forest, open plain, water, burrow | Body plan (climbing vs running vs swimming) |
| Diet | Feeding items (fruit, grass, meat, bone) | Teeth/jaws (e.g. grazing horse vs browsing horse) |
| Climate | Time in hot vs cold maps | Body size (warming → dwarfing, as in *Sifrhippus*) |
| Role | Damage dealt vs damage taken vs fled | Predator/defender/runner branch |

### 7.3 Extinction
- Each era has **filters**: e.g. the impact kills all non-avian dinosaurs and anything
  above ~25 kg, and the Eocene–Oligocene cooling hits warmth-dependent lineages.
- A lineage that fails its filter is lost. It becomes a **fossil item** for the Codex.
- Difficulty option: "Gentle Deep Time" (extinct lineages respawn as a related survivor).

### 7.4 Clock
- pokeemerald-expansion has a fake RTC (`OW_USE_FAKE_RTC`, `OW_ALTERED_TIME_RATIO`
  in `include/config/overworld.h`) that runs on play time. Extend it so the ratio
  is set per act (hours → millennia → Myr per in-game "day") and show it in the HUD.
- Seasons are re-skinned as **climate cycles** (e.g. Milankovitch glacial cycles in Act 8).

### 7.5 Maps
- Each act is a copy of the same base region map with changed terrain, water and
  vegetation. Landmarks (a particular butte, a river bend) stay put so the player
  can *see* deep time act on one place.

### 7.6 Types
Keep the standard 18 types for compatibility, but assign them by ecology.
(Could be revisited later in favour of a custom type chart.)

| Type | Meaning | Examples |
|---|---|---|
| Normal | Generalists, small omnivores | *Mesodma*, *Canis* |
| Fighting | Animals that fight with horns, domes, clubs or kicks | *Triceratops*, *Pachycephalosaurus* |
| Rock | Heavy armour or shells | *Ankylosaurus*, snapping turtles |
| Grass | Plant specialists | *Edmontosaurus*, *Thescelosaurus*, *Gastornis* |
| Dark | Predators and ambushers | *Tyrannosaurus*, *Acheroraptor*, dog line |
| Steel | Bone-crushers | *Didelphodon*, *Epicyon* |
| Dragon | Large archosaur predators | *Tyrannosaurus*, *Borealosuchus* |
| Water | Aquatic | gar, *Champsosaurus*, turtles |
| Flying | Fliers | bird line |
| Ground | Burrowers | *Mesodma* |
| Ice / Fire | Cold- / heat-adapted (later eras) | — |
| Electric | Electroreceptive fish (later) | — |

### 7.7 Species data
- The roster lives in `tools/strata/roster.py`. `tools/strata/gen_species.py`
  generates the C data from it. Never hand-edit the generated files.
- **Names** are at most 12 characters (the save format's nickname length). Use the
  genus if it fits. Otherwise use the informal anglicized form (*Tyrannosaurus* →
  Tyrannosaur). Otherwise cut the genus at a morpheme boundary (*Pachycephalosaurus* →
  Pachycephalo). The Codex always shows the full scientific name.
- **Stats come from body mass:** BST = 300 + 70·log10(mass in kg), clamped to 180–600.
  Each species' anatomy then splits that total: bite/weapons → Attack,
  armour → Defence, locomotion → Speed, senses → Sp. Atk, hardiness → Sp. Def.
  Masses without a published estimate are flagged `mass_est` and shown as estimates.
- **Placeholder art and cries** are copied from a similar stock Pokémon (`borrow`)
  into `graphics/pokemon/strata/` and `sound/direct_sound_samples/cries/strata_*`.
  Strata species therefore never depend on the stock Pokémon, which are disabled in
  the game build. They stay enabled in the test build for the expansion's tests.
- **Known limitation:** the weight field is 16-bit (max 6,553.5 kg), so the masses of
  *Tyrannosaurus*, *Triceratops* and *Ankylosaurus* are clamped. Widen the field and
  the Pokédex weight display before the Codex work.

## 8. Scientific integrity rules

1. Every species entry cites a real fossil occurrence (formation + approximate age).
2. When a fossil species is a *relative* of the true ancestor rather than the ancestor
   itself, the Codex says so ("stand-in", "grade").
3. Dates are rounded and marked "~". Uncertainty is shown, not hidden.
4. Speculative behaviour (colour, calls, mating displays) is labelled as reconstruction.
5. **Fact-check pass needed:** the dates, sites and species placements in this draft
   come from general knowledge and must be checked against the primary
   literature / Paleobiology Database (paleobiodb.org) before content lock.

## 9. Tech plan (GBA romhack: pokeemerald-expansion)

- **Target:** a `.gba` ROM playable on any GBA emulator (PC, phone, handhelds, flash cart).
  Distributed as a **.bps patch** for players to apply to their own Emerald ROM, never as a ROM.
- **Base:** [rh-hideout/pokeemerald-expansion](https://github.com/rh-hideout/pokeemerald-expansion)
  (v1.17.1, `master`), written in C.
- **Toolchain:** WSL2 Ubuntu with `gcc-arm-none-eabi` + `libnewlib-arm-none-eabi`.
  The repo lives on the Linux filesystem at `~/projects/strata` for build speed.
  Build with `make -j16`, which outputs `pokeemerald.gba`.
- **Tools:** Porymap (maps/encounters), Poryscript (optional, for event scripts),
  an emulator with a debugger (mGBA).
- **Custom code** (new C files under `src/`, headers under `include/`):
  - `lineage.c`: descent table (`src/data/lineages.h`), descent resolver, and the era-jump
    routine that walks the party + all PC boxes and changes species / recalculates stats
  - `selection.c`: updates the pressure counters (the repurposed contest stats) from battle,
    map and item hooks
  - `extinction.c`: per-era filters, converting extinct lineages into fossil items
  - Era clock: per-act time ratio on top of the existing fake RTC
  - Field Codex: rework of the Pokédex screens (the expansion's HGSS-style dex is a good base)
- **Data:** species in `src/data/pokemon/species_info/`. Turn level evolutions off and
  replace the real Pokémon with our creatures in reused species slots, cutting unused ones
  via `include/config/species_enabled.h`.
- **GBA constraints:**
  - Battle sprites are 64×64 with 16-colour palettes, plus small 32×32 icons.
  - ROM limit is 32 MB, which is plenty for ~8 copies of the region map.
  - Save space is tight, so there is no per-Pokémon data beyond the repurposed fields.
- **Art:** every creature needs original sprites (front/back/icon). This is the biggest
  production cost; see the open questions below.

## 10. Milestones

1. **Vertical slice:** Act 0 + Act 1 + the era jump to Act 2. That covers 3 starters,
   ~10 Hell Creek species, the descent + extinction systems working end-to-end.
2. Acts 3–4 (proves selection pressures, e.g. *Sifrhippus* dwarfing).
3. Acts 5–8 content.
4. Epilogue, Codex polish, scientific fact-check pass.

## 11. Open questions

- Trainers in deep time: simulations, or wild-only? (§2)
- Art: pixel art by hand, commission, or placeholders first?
- How many species per act? (Suggest 12–20 → ~120 total.)
- Should players ever choose a lineage branch directly, or only through pressures?
- Should humans (Clovis people, Act 8) appear as characters?
