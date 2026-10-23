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
| 3 | Corral Bluffs, CO | ~65.7–65.4 Ma | ~300–700 kyr | millennia | Mammal recovery, first legumes (~700 kyr, with *Taeniolabis*) |
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

**Maps built so far** (defined in `tools/strata/maps/`, one module per act; scripts in `data/maps/Strata*/`)

| Map | Era | Layout source (placeholder) | Notes |
|---|---|---|---|
| Hell Creek Camp | present | Route 111 north | Hub; field station door at (26, 18); Theo, Josie, Marge's store; ranch road west to the Lindqvist Ranch |
| Field Station | present | Birch's lab | STRATA rig at (10–11, 7); mentor Dr. Halvorsen; respawn point; PC, cot, relearner Wren, rig-rules notes |
| Hell Creek Badlands | present | Route 111 desert | K-Pg boundary clay; Dale's tutorial dig (3 survey stakes, `FLAG_STRATA_DIG_*`); BLM boundary on the south edge (needs `FLAG_STRATA_BLM_PERMIT`); no encounters |
| Sand Arroyo | present | Route 111 desert rows 74–100 (joins the badlands) | BLM land: the poached pit, a broken jacket, spoil and tire tracks |
| Lindqvist Ranch | present | Route 117 | Bea; Kessler and a crew hand (until Act 1 is done); the Pair under a tarp (`FLAG_STRATA_SAW_PAIR`) |
| Jordan | present | Fallarbor Town (tent and Pokémon Center removed) | General store (Mart), café (House 2, heals), BLM field office (Lanette's house; Ranger Ortiz gives the permit after Act 2); the highway west leads to the prairie in the epilogue |
| Levee Forest | 66.04 Ma | Route 119 south | Arrival point; south edge returns to camp; east side opens into the Fern Glade; 3 field notes; *Avisaurus* at the forest edge |
| River Channel | 66.04 Ma | Route 119 middle | The tyrannosaur waits on the bluff (survival set piece); the ejecta streaks end the act and the rig pulls you out |
| Backswamp | 66.04 Ma | Route 120 marsh | Gar, champsosaurs, crocodylians, *Emarginachelys*; field notes on the detritus food web |
| Fern Glade | 66.04 Ma | Route 120 open grassland (east of the cliff) | Open habitat east of the Levee: Edmontosaurus herd, *Avisaurus*, the *Acheroraptor* pair ambush (wild double Lv 8/8, once); notes on perching vs ground birds |
| Ashen Levee / River / Swamp | 66.04 Ma + ~1 yr | Same layouts, `*_winter` palettes | Impact winter: survivors only; survival gauntlet in the swamp (the trigger line spans the swamp's whole width) |
| Burrow Refuge | 66.04 Ma + ~1 yr | Island Cave, top chamber | Mouth is a rock mound in the Ashen Levee; *Mesodma*/*Cimolestes*; seed cache (browse item balls), notes on burrowers |
| Palm Forest | ~65.7–65.4 Ma | Petalburg Woods | Act 3; *Eoconodon* boss (Lv 22) on the north path |
| Red Beds | ~56 Ma | Route 114 north, `*_petm` palettes, drought | Act 4; *Coryphodon* boss (Lv 28) on the land bridge |
| Lake Gosiute shore | ~50 Ma | Route 104 | Act 5; *Uintatherium* boss (Lv 34) across the south shore |
| White River badlands | ~33 Ma | Route 114 south, `*_oligocene` palettes | Act 6 arrival valley; north edge joins the Gallery Forest; *Archaeotherium* boss (Lv 40) on the stash plateau (hell-pig object plus the stair triggers); 4 carrion forage spots at the stash; 3 field notes; *Palaeolagus* (common) |
| Gallery Forest | ~33 Ma | Route 114 north (joins White River at offset 0), `*_oligocene` palettes | Act 6; forest strips along a river and lake (plank bridge replaced by a sandbar, house and berry plots removed); *Douglassciurus*, Mesohippus, Leptomeryx, Hesperocyon, gars in the water; the horse forest branch is steered here (forest habitat); 3 field notes |
| Badlands Wall | ~33 Ma | Route 113 left half, `*_oligocene` palettes | Act 6; open red-soil flats under a banded cliff, with the Chadron / Brule contact note; oreodont herd (flavour objects), *Palaeolagus* (common), Stylemys, Merycoidodon; ash grass swapped for tall grass; east edge joins the Trackways at offset 0 |
| Toadstool Trackways | ~33 Ma | Route 113 right half, `*_oligocene` palettes | Act 6; floodplain with trackway notes; *Hyaenodon* mini-boss (Lv 38, once, line of sight at x = 10; rare wild 35-38) with a carrion reward; Subhyracodon, Poebrothere |
| Ashfall grassland | ~11.9 Ma | Route 113, volcanic ash | Act 7; *Teleoceras* bull (Lv 46) at the waterhole |
| Ice Age Steppe | ~20 ka | Route 118, `*_ice_age` palettes, snow | Act 8; the sinkhole drops into the trap cave |
| Natural Trap Cave | ~20 ka | Granite Cave 1F | Act 8; *Arctodus* boss (Lv 52); a rope climbs back out |
| Montana Prairie | today | Route 102 | Epilogue; open once the present layer is loaded, via the highway west of Jordan |

The present-day hub sits outside time: returning to camp does not change `VAR_STRATA_ERA`.
The rig only moves up: once a layer is loaded, earlier layers are closed.
Story progress is `VAR_STRATA_STORY`: 0 new game, 1 starter chosen, then for act N
`2N` while in the act and `2N + 1` once its boss is done (`STORY_IN_ACT`,
`STORY_ACT_DONE` in `include/constants/strata.h`); 18 is the epilogue. The rig
(`src/strata_acts.c`) loads the next layer only after the act is done; Dr.
Halvorsen has a line for every story value. Each deep-time map has an anchor sign
that returns to the field station.

`python3 tools/strata/mapcheck.py` walks every Strata map from its arrival point and
connected edges and reports any trigger, sign or edge the player can't reach on foot.

**Era variants of a map** reuse its layout with palette-only variants of its tilesets
(`tools/strata/gen_tilesets.py`), so the place is recognizably the same while the era
changes. Known gaps: battle backgrounds and the tall-grass overlay sprite keep
their stock colours.

**No gym badges**, so `B_OBEDIENCE_MECHANICS` is GEN_7: the player's own Pokémon
always obey (Gen 8+ rules would make anything caught above Lv 10 disobey forever).

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
| 6c | 8 | *Vulpes velox* (swift fox) | Open-grassland branch (OPEN ≥ 96 in Act 7) → survives; nearly lost in the 20th century |

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
| 3b | 8 | *Centrocercus* (greater sage-grouse) | Open-grassland branch (OPEN ≥ 96 over Acts 4–7); a present-day conservation story |

Lesson: one survivor radiates into many body plans. Big and flightless is a dead end here.

### 🐢 Reptile: Snapping turtle line (stasis)
Snapping turtles have lived in Montana from the Cretaceous to today with very little change.

| Stage | Act | Species | Notes |
|---|---|---|---|
| 1 | 1–3 | *Emarginachelys cretacea* | Hell Creek chelydrid |
| 2 | 4–6 | *Protochelydra zangerli* | Paleocene, North Dakota |
| 3 | 7–E | *Chelydra serpentina* | Common snapping turtle |
| 3b | 7–E | *Macrochelys* (alligator snapper) | Heat branch (HEAT ≥ 160 over Acts 3–6, i.e. carried through the PETM); Miocene fossils in Nebraska, today only in the warm Southeast |

Lesson: if a body plan works, **stabilising selection** keeps it. This line
changes form rarely, but gets big stat boosts from surviving every extinction filter.
It is the "hard mode / safe mode" starter.

## 5. Other signature lineages (wild / catchable)

- **Horse line** *(immigrates at the PETM; it did not originate here)*: *Sifrhippus* →
  *Eohippus*/*Protorohippus* → *Orohippus* → *Mesohippus* → *Merychippus* →
  *Cormohipparion* / *Pliohippus* → *Equus*. Horses **die out in North America ~11 ka**
  and return with the Spanish in the 1500s, which is part of the epilogue.
  In the game: *Sifrhippus* → *Eohippus* → *Mesohippus* → *Protohippus* (default) → *Equus*,
  or the forest browser *Hypohippus* (FOREST ≥ 64 in Act 6; dies by the Ice Age).
- **Camel line** (also North American in origin): *Poebrotherium* → *Procamelus* → *Aepycamelus* → *Camelops*.
- **Multituberculates**: *Mesodma* → *Taeniolabis* → *Ptilodus* → extinct by ~34 Ma.
  They were the most long-lived mammal order of all time. Their dying out is a midgame story beat.
- **Rhinos**: *Hyrachyus* (Bridger) → *Subhyracodon* → *Teleoceras* (barrel-bodied, preserved
  at Ashfall) or the open-country *Aphelops* (OPEN ≥ 64 in Act 6) → both extinct in NA.
  Grades, not ancestors: the Miocene rhinos were immigrants.
- **Primates**: *Teilhardina* → *Omomys* (both omomyiforms; extinct by White River).
  *Notharctus* is an adapiform, a different branch, and only a wild species.
- **Rodents and squirrels**: *Paramys* → *Ischyromys* (dies by Ashfall); *Douglassciurus*,
  the oldest squirrel, → *Cynomys* (stand-in).
- **Pronghorn**: *Cosoryx* → *Antilocapra* (stand-in: a merycodontine side branch). *Antilocapra* runs much faster than any living predator needs. That speed is a
  "ghost" of the extinct American cheetah (*Miracinonyx*) in Act 8.

## 6. Bosses (one apex per layer)

| Act | Boss | Why |
|---|---|---|
| 1 | *Tyrannosaurus rex* | Apex of Hell Creek |
| 2 | **The impact winter** (survival gauntlet) | The "boss" is the environment |
| 3 | *Eoconodon* | First big mammal predator after the impact |
| 4 | *Coryphodon* | Largest animal of the PETM hothouse |
| 5 | *Uintatherium* | Six-horned Bridger giant |
| 6 | *Archaeotherium* ("hell pig") | White River apex |
| 7 | **The ashfall** + *Teleoceras* bull | The eruption ends the act |
| 8 | *Arctodus simus* (short-faced bear) | Ice Age apex, trapped in Natural Trap Cave |

Each boss is a one-off wild battle on a line of triggers. Running away leaves it in
place; winning or catching it finishes the act. The exception is the act 1 Tyrannosaurus,
a survival set piece: every way out of that fight except a whiteout finishes the act.
Running sets `FLAG_STRATA_TREX_FLED`, which switches Dr. Halvorsen to a line about being
small and quick ("that's how mammals lived here").

**Boss settings.** Every boss script brackets its battle with the `strata_boss_prep` and
`strata_boss_done` macros (`asm/macros/event.inc`). Prep does two things for that battle
only:

- Smart wild AI: it sets `VAR_STRATA_BOSS_AI` (the config var `B_VAR_WILD_AI_FLAGS`) to
  `STRATA_BOSS_AI_FLAGS` = `AI_FLAG_CHECK_BAD_MOVE | TRY_TO_FAINT | CHECK_VIABILITY`
  (the basic trainer set). `strata_boss_done` clears it; whiteouts clear it in
  `Overworld_ResetBattleFlagsAndVars`. `src/strata_acts.c` asserts the number still matches the flags.
- A totem-style stage boost (`settotemboost`) of +1 in the boss's signature stat, applied
  to the first foe when the battle starts.

| Boss | Lv | Boost |
|---|---|---|
| Act 1 *Tyrannosaurus* | 14 | +1 Atk |
| Act 2 gauntlet, all three foes | 14 / 15 / 17 | smart AI; the last foe (old *Borealosuch*) also +1 Atk |
| Act 3 *Eoconodon* | 22 | +1 Atk |
| Act 4 *Coryphodon* | 28 | +1 Def |
| Act 5 *Uintatherium* | 34 | +1 Atk |
| Act 6 *Archaeotherium* | 40 | +1 Atk |
| Act 7 *Teleoceras* | 46 | +1 Def |
| Act 8 *Arctodus* | 52 | +1 Atk |

Boss strength comes from base stats and the one boost, not from extra levels. New boss
scripts should use the same two macros; a double boss gets the boost on its left foe.

### Field station services

The Field Station has the services the player needs between acts: two desk computers
at (3, 1) and (4, 1) open the stock PC menu (Pokémon storage, the player's item PC), a
cot at (1..2, 4) heals the party, and the station tech Wren at (9, 3) re-teaches level-up
moves for free (party and PC mons). Dr. Halvorsen still heals on talk. The intro sets
`FLAG_STRATA_EXP_SHARE` (= `I_EXP_SHARE_FLAG`), so the whole party shares experience.
The camp quartermaster (Marge, at (29, 19) in Hell Creek Camp) runs the store: Poké Ball
and Potion, plus Great Ball and Super Potion once act 3 is done and Hyper Potion once
act 6 is done.

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

**As built** (`src/selection.c`, `src/lineage.c`, `src/data/lineages.h`):

| Counter | Source now | Rate | Missing / later |
|---|---|---|---|
| FOREST (`cool`) | Anywhere on a map tagged `habitat="forest"`; on untagged maps, long grass | +1 per 32 steps (whole party) | n/a |
| OPEN (`beauty`) | Anywhere on a map tagged `habitat="open"`; on untagged maps, tall grass | +1 per 32 steps | n/a |
| WATER (`cute`) | Surfing/wading; **standing next to surfable water** (shore); anywhere on a map tagged `habitat="water"`; hooking a fish | +1 per 32 steps; +2 per fish hooked (whole party) | n/a |
| PLANT (`smart`) | Eating plant forage: Fern Frond, Palm Fruit, Legume Pod, Seed Head, Browse | +12 per item (one mon) | n/a |
| ANIMAL (`tough`, `PRESSURE_MEAT_DIET`) | Eating animal forage: Larvae, Carrion; knocking out a foe with a move, **only for carnivores/omnivores** (roster `diet`, generated into `src/data/strata_diets.h`) | +12 per item; +1 per KO, KOs stop at 24 | n/a |
| HEAT (`sheen`) | Era climate (`sEraHeat`) | 0–2 per tick | n/a |

- **Habitat order:** water (surfing, water tiles, shores) beats the map's tag, and the
  tag beats the grass underfoot. Map tags (`habitat=` in `tools/strata/maps/`) are
  generated into `sStrataMapInfo` (`src/data/strata_map_eras.h`, read by
  `src/strata_map.c`), one row per Strata map with its era, habitat and light:

  | Map | Habitat | Light |
  |---|---|---|
  | Field Camp, Field Station | none (grass decides) | real clock |
  | Badlands | open | real clock |
  | Levee Forest, Backswamp (Act 1) | forest | day |
  | Fern Glade (Act 1) | open | day |
  | River Channel (Act 1) | water | day |
  | Ashen Levee (Act 2) | open (dead forest) | dark |
  | Ashen River, Ashen Swamp (Act 2) | water | dark |
  | Burrow Refuge (Act 2) | none | none (never tinted) |
  | Corral Bluffs palm forest (Act 3) | forest | day |
  | Bighorn red beds (Act 4) | open | day |
  | Lake Gosiute forest (Act 5) | forest | day |
  | White River, Badlands Wall, Toadstool Trackways (Act 6) | open | day |
  | Gallery Forest (Act 6) | forest | day |
  | Ashfall grassland (Act 7) | open | ash |
  | Ice Age steppe (Act 8) | open | day |
  | Natural Trap Cave (Act 8) | none | none (never tinted) |
  | Montana prairie (epilogue) | open | real clock |
- **Forage** (`ITEM_FERN_FROND` … `ITEM_CARRION`, `Selection_EatForage`): used from the
  bag on one party mon. Heals 20 HP and adds +12 of its pressure (the item's
  `secondaryId`); it works at full HP (the diet is the point) but not on a fainted mon
  or an egg. Six of one kind (72) pass a branch's 64. Placed per map with
  `forage(x, y, item)` (`tools/strata/maps/common.py`) as hidden items, or item balls with
  `visible=True`, under the temp flags `FLAG_TEMP_11..1F`, which every map load clears:
  forage **regrows each time the player re-enters the map**, so steering a diet is
  a choice the player can always make, not a scarce resource. Each spot is
  era-checked (no palm fruit after the Eocene, no legume pods before Corral Bluffs,
  grass seed heads from White River on). Hidden items store their flag as a wrapping
  13-bit offset (`GET_HIDDEN_ITEM_FLAG`), which is what lets temp flags work.
- **Light** (`light=`): deep-time maps have a fixed day/night tint (day, dusk, dark,
  ash), which `UpdateTimeOfDay` uses instead of the wall clock; `none` is never tinted;
  present-day maps follow the real clock (`OW_ENABLE_DNS`).

- **Thresholds:** a branch only competes once its counter reaches its `minScore`
  (`DESCENT_MIN_SCORE` = 64 for every branch today). The highest eligible counter wins,
  ties go to the first listed, and the default wins if none is eligible.
- **KO cap storage:** there is no spare per-mon field to count KOs per era, so knockouts
  simply can't lift ANIMAL above 24 (other sources can). Counters reset on descent, and
  both diet-steered descents (Hesperocyon, Leptocyon) have one-era windows, so this is
  24 per era wherever it matters. Since 24 < 64, a hunting dog still becomes the coyote;
  *Epicyon*/*Aenocyon* need carrion forage on top.
- **Water access:** the **Waders** key item lets the player surf (wade) any surfable water
  with no badge or HM; the **Fishing Kit** is the Old Rod renamed (Good/Super Fishing Kit
  after upgrades). Both are given at the Field Station after the starter choice
  (`data/scripts/strata_gear.inc`).

### 7.3 Extinction
- Each era has **filters**: e.g. the impact kills all non-avian dinosaurs and anything
  above ~25 kg, and the Eocene–Oligocene cooling hits warmth-dependent lineages.
- A lineage that fails its filter is lost from the party and PC (implemented in
  `src/lineage.c`, filters in `src/data/lineages.h`). Filters run after that era's
  descents, so a lineage that descends into a survivor escapes. If the party would
  be left empty, a PC survivor is brought out, or a small survivor joins.
- Planned: the lost lineage becomes a **fossil item** for the Codex.
- Difficulty option: "Gentle Deep Time" (extinct lineages respawn as a related survivor).

#### Era level floor
A descendant arrives as a mature adult of its era. After each era's descents and
extinctions, every party and PC mon below that era's floor is raised to it
(`sEraLevelFloor` in `src/data/lineages.h`), so a lineage left in the PC since Hell
Creek is still usable later. A multi-era jump raises it era by era, so it ends at
the last era's floor. Raised mons:
- get the EXP of the start of the floor level and, in the party, recalculated stats;
- keep the HP they had lost, as on a normal level-up (a fainted mon stays fainted;
  a PC mon's lost HP is all a box mon stores anyway);
- learn the level-up moves they passed, in order, forgetting the oldest move when
  all four slots are full and skipping moves they already know.

Mons at or above the floor and eggs are untouched. The survivor that joins an
empty party joins at the floor (at least level 10), as Mesodma until it dies out
at White River, then as the gar.

Floor = the era's lowest land encounter level (`tools/strata/maps/`) − 3. Fishing
runs lower on purpose and doesn't count.

| Era | Wild (land and surf) | Floor |
|---|---|---|
| Present dig, Hell Creek | — / 3–11 | none |
| Impact winter | 10–16 | 7 |
| Corral Bluffs | 15–20 | 12 |
| Bighorn PETM | 22–28 | 19 |
| Green River | 28–34 | 25 |
| White River | 32–39 | 31 |
| Ashfall | 40–45 | 37 |
| Trap Cave (Ice Age) | 46–51 | 43 |
| Epilogue | 48–53 | 45 |

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
- The roster lives in the package `tools/strata/roster/`. `tools/strata/gen_species.py`
  generates the C data from it. Never hand-edit the generated files.
- **How to add a species:** append it to the end of `roster/part3.py` (or, for parallel
  work, a new `roster/partN.py` that you also append to `PARTS` in `roster/__init__.py`).
  A species' position in the global list is its species ID and National Dex number, so
  new species are *always appended at the end*, even when they belong to an early act.
  Never insert, remove or reorder species in the act modules. Then run
  `python3 tools/strata/gen_species.py`. The fields are documented in `roster/__init__.py`.
  Every species needs a `first_era` (the first era it exists, wild or as a descendant);
  stand-ins whose lineage outlives the genus get a `last_era` for wild appearances; animal
  eaters get a `diet`. They generate `src/data/strata_species_eras.h` and
  `src/data/strata_diets.h`, and the tests check every encounter table and descent
  against them. If the species joins a lineage, add its descent and extinction to
  `src/data/lineages.h`.
- **How to add a map:** append a dict to `MAPS` in the act's module under
  `tools/strata/maps/` (`act0_present.py` ... `act8_ice_age.py`, `epilogue.py`), with its
  MAPSEC in the same module's `MAP_SECTIONS`, write `data/maps/<Name>/scripts.inc`, and run
  `python3 tools/strata/gen_maps.py`. Shared helpers (`trigger`, `sign`, `anchor`,
  `boss_triggers`, `mons`, `winter`, ...), `ERAS` and crops used by several acts are in
  `maps/common.py`. The aggregator in `maps/__init__.py` concatenates the acts in order;
  map-id order = act order, then order within the act's `MAPS`.
- **Names** are at most 12 characters (the save format's nickname length). Use the
  genus if it fits. Otherwise use the informal anglicized form (*Tyrannosaurus* →
  Tyrannosaur). Otherwise cut the genus at a morpheme boundary (*Pachycephalosaurus* →
  Pachycephalo). The Codex always shows the full scientific name.
- **Stats come from body mass:** BST = 340 + 50·log10(mass in kg), clamped to 250–600
  (`base_stat_total()` in `gen_species.py`). Mass still orders every species, but the
  spread between a 40 g primate (270) and an 8 t theropod (535) is about 2×, not 3×,
  because a 0.04 kg bat and an 8-tonne animal can meet at the same level.
  Each species' anatomy then splits that total: bite/weapons → Attack,
  armour → Defence, locomotion → Speed, senses → Sp. Atk, hardiness → Sp. Def.
  Small species keep speed-heavy weights, so they are fast rather than bulky.
  Masses without a published estimate are flagged `mass_est` and shown as estimates.
- **Focal bonus (a game concession, not biology):** species with `focal=True` in the
  roster, the 19 species of the three starter lines, get a flat +40 BST (capped at 600).
  The player carries these lineages through every act, and a 0.3 kg ground bird would
  otherwise sit far below the wilds of Acts 6–8. Examples: *Cimolestes* 365,
  *Gallinuloides* 354, *Leptocyon* 395, *Canis* 436, *Emarginachelys* 425; for comparison,
  non-focal *Mesodma* 275, *Teilhardina* 264, *Tyrannosaurus* 535, *Mammuthus* 538.
  When a new species joins a starter line (as *Vulpes*, *Centrocercus* and *Macrochelys*
  did), give it `focal=True` too: `test/lineage.c` checks that the focal species are
  exactly those a starter can become.
- **Balance report:** `python3 tools/strata/balance.py` prints, per act, the wild species
  and levels, the boss fights, the era level floor and the expected starter-line party,
  with stat totals at level, and flags gaps (`--strict` exits 1 on any flag). Run it after
  any roster, encounter or boss change.
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
2. Acts 3–4 (proves selection pressures, e.g. *Sifrhippus* dwarfing). **Built.**
3. Acts 5–8 content. **Built** (one map per act, plus the trap cave).
4. Epilogue (**prairie built**), Codex polish, scientific fact-check pass.
5. Next: balance (small species have low BST at high levels; a player who skips
   ahead can be left with one low-level survivor), real map art for the sinkhole and
   rope, more maps per act, trainers/NPCs in the present-day hub.

## 11. Open questions

- Trainers in deep time: simulations, or wild-only? (§2)
- Art: pixel art by hand, commission, or placeholders first?
- How many species per act? (Suggest 12–20 → ~120 total.)
- Should players ever choose a lineage branch directly, or only through pressures?
- Should humans (Clovis people, Act 8) appear as characters?
