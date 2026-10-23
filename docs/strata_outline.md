# Strata: Master Outline (v0.2)

> The master plan for turning the current thin build (one map and one boss per act)
> into a full game. Companion to `docs/strata_design.md`: that document says *what the
> systems are*; this one says *what to build next, in what order, and why*.
> Engineers should be able to implement any section without asking.
>
> Conventions: **NEW** marks a proposed species, map or system that does not exist
> yet. **⚠** marks a claim that needs a fact-check (see §5). S / M / L sizes are
> agent-days: S ≤ ½ day, M 1–3 days, L ≥ 1 week.

---

## 0. Audit: what the build actually does today

Read before planning. Several of these are bugs in the core loop, not polish.

| # | Finding | Where | Consequence | Fix (task) |
|---|---|---|---|---|
| A1 | Any non-zero pressure beats the default descendant: the default scores 0, and an option scores its raw counter. | `Lineage_GetDescendant`, `src/lineage.c:44` | One knockout (+2 meat) during Act 6 turns *Hesperocyon* into *Epicyon*, and one during Act 7 turns *Leptocyon* into *Aenocyon*. Both are dead ends, so the dog starter almost never reaches the coyote. | Per-option threshold (§3.3), R1 |
| A2 | Every knockout adds `PRESSURE_MEAT_DIET` to any species. | `Selection_OnFoeFainted` | Herbivores "eat meat". Diet stops being a choice. | Knockouts count only for predators/omnivores and are capped (§3.3), R1 |
| A3 | `PRESSURE_PLANT_DIET` has no source. `special Strata_AddPressure` exists but no script calls it. | `src/selection.c`, scripts | The *Gastornis* branch can't be reached. | Forage items (§3.5), R3 |
| A4 | Surf needs badge 5 and a mon that knows Surf. No rod is ever given. | `src/field_move.c:92`, Field Station script | Every `water_mons`/`fishing_mons` table is dead content, and `PRESSURE_WATER` can never rise, so the *Presbyornis* branch can't be reached. | Waders + fishing kit, and shoreline counts as water (§3.3), R2 |
| A5 | `PRESSURE_FOREST`, `OPEN` and `HEAT` select no descendant. | `src/data/lineages.h` | Half the steering system does nothing. | New branches (§2.11), C-tasks |
| A6 | `sMapHabitats` is still the Petalburg Woods placeholder. | `src/selection.c:47` | Palm Forest (a Petalburg crop) is *not* tagged forest. | Generate the table from `maps.py` (R4) |
| A7 | Small species have very low BST: *Teilhardina* 193, *Purgatorius* 202, *Mesodma* 209, the *Gallinuloid* default bird branch 263. | `gen_species.py:76` | The bird starter's default line sits at BST 263 through Act 7 (Lv 40+ vs BST 470–530 wilds). | New formula plus focal bonus (§3.2), R5 |
| A8 | Act 1 boss: a Lv 12 *Tyrannosaurus* (BST 573) vs a Lv ~9 party (BST 272–363). | `StrataRiver/scripts.inc` | Nearly unwinnable, and running away doesn't finish the act. | Make it a survival set piece (§2.2), R10 |
| A9 | There is no PC in the Field Station. PC boxes are reachable only by catching with a full party. | `maps.py` Field Station | You can't manage the PC "seed bank" (see §3.3). | Add a PC (R9) |
| A10 | Leftover Emerald text: start menu (POKéDEX / POKéMON / POKéNAV), "SOMEONE'S PC / BILL'S PC / LANETTE'S PC", Birch's dex rating, whiteout "POKéMON", the Hoenn region map, battle strings. | `src/strings.c`, `data/text/pokedex_rating.inc`, `src/field_screen_effect.c`, `src/battle_message.c`, `src/region_map.c` | Breaks the fiction. | Text pass (R8) |
| A11 | `OW_ENABLE_DNS` is TRUE with the real RTC, so deep time darkens by the player's wall clock. | `include/config/overworld.h:102`, `MapHasNaturalLight` | Hell Creek at 2 a.m. is night for no reason. | Lighting per era (§3.9) |
| A12 | The Pokédex weight field is 16-bit (max 6,553.5 kg). | design doc §7.7 | T. rex, Triceratops and mammoth masses are clamped. | Codex work (M1) |

Facts the plan relies on (all checked in the code):
- Counters reset only on descent, so a lineage in stasis accumulates pressure across several acts.
- PC mons gain nothing, because ticks apply only to the party.
- `setwildbattle` supports a second species (wild doubles) and `settotemboost` exists.
- `B_FLAG_VICTORY_CATCH_*`, `WE_FLAG_NO_RUNNING`, `I_EXP_SHARE_FLAG` and `B_VAR_WILD_AI_FLAGS` all exist as config hooks.
- FRLG layouts ship in `data/layouts/` and can be cropped like the Hoenn ones.

---

## 1. Story spine

### 1.1 Premise and stakes

**Logline:** a first-season field assistant at a Montana dinosaur dig climbs 66 million
years of rock, one layer at a time, inside a reconstruction rig. Meanwhile, back at the
dig, the season's best skeleton is about to be sold out of the ground.

**Theme:** *what survives, and why, and what we choose to keep.* Deep time shows
that survival is mostly contingency (the right size, diet or place when the filter
came). The present-day plot asks the human version of the question: what is lost when
a fossil leaves its layer without its context, and what part do people play in the
extinction happening now.

**Stakes, in two layers:**
1. *Deep time (the model):* your lineages can be lost forever. Each extinction is
   permanent, and the record decides it, not you.
2. *Present day (the people):* a once-in-a-career specimen on a neighbouring ranch,
   "the Pair" (a *Triceratops* and a *Tyrannosaurus* buried together, NEW), is
   headed for private auction. The field station is underfunded, and its rig might be
   sold off when Dr. Halvorsen retires at the end of the season.

### 1.2 Why the rig works, and its limits (the in-fiction rules)

**STRATA** is a reconstruction rig. It is a model you can walk around in, not a time
machine. It takes in a layer's record: body fossils (a PBDB-style occurrence list),
sediment and soils, pollen and spores, leaf shapes and isotopes (for climate), trace
fossils (tracks, bite marks, burrows) and taphonomy. From these it builds the most
likely living world. These rules are the game rules, so every system has an in-fiction
reason:

| Rule | Fiction | Mechanic it justifies |
|---|---|---|
| R-a | It needs a rich layer. It can only load where the record is good. | Acts jump between famous sites, and the gaps are honest. |
| R-b | The model runs forward only, chaining each layer from the one below. | The rig moves up only. Earlier layers close. |
| R-c | **Data anchors:** at each layer the model must match the record. A lineage the record says is gone cannot persist. | Extinction filters are fixed. The player can't save *Tyrannosaurus*. |
| R-d | What the record leaves open (which branch a lineage takes) is set by the conditions you put it under. | Selection pressures steer descents (it's a scenario run, not history rewritten). |
| R-e | Unknowns are best guesses: colour, calls, behaviour. | Codex "inferred" tags, borrowed cries, and the "?" shimmer on low-confidence areas (flavour). |
| R-f | Confidence depends on preservation. Lagerstätten (Green River) render sharply. Thin layers (impact winter) are sparse. | Encounter variety and map size per act. |
| R-g | People are reconstructed **only as traces** (tools, butchery marks), never as characters. That is both an epistemic limit and an ethical choice. | No Clovis NPCs in Act 8 (§2.9). |
| R-h | Injuries in the model are simulated. A full loss is a "model divergence", and the rig drops you back at the station. | Whiteout respawns at the Field Station (already built). |
| R-i | A run snapshots a **time-averaged** window. A fossil layer blurs thousands of years together. | Replaces the "per-act clock rate" idea (§3.9). The HUD shows each act's window. |

Battles, in fiction, are **stress tests** of the model: competitive interactions
(predation, territory) resolved by the simulation. Present-day battles between
researchers are **peer review**: two people pit their reconstructions against each
other. Nobody fights over fossils with monsters.

### 1.3 Protagonist

A summer field assistant (player-named, default sprite in field gear). Motivation,
set up in Act 0: on day one *you* find the three specimens in the badlands, and you
ask Halvorsen the question the game answers: *"Why did these three make it through,
when T. rex didn't?"* By the end the player has an answer (size, diet, habitat, luck),
and has seen that the same question now applies to living species.

### 1.4 Cast (present day; keep it small)

| Character | Role | Sprite (placeholder) | Arc |
|---|---|---|---|
| **Dr. Halvorsen** | Field station director; built the rig with a university consortium. Careful, and always states uncertainty. | `SCIENTIST_1` (existing) | Retiring after this season. Tempted once by Kessler's money to keep the rig funded, and refuses. Their last act is getting the Pair into a public museum. |
| **Theo Okafor** | PhD student, skeptic, and the **rival**. "How do we know that?" | `EXPERT_M` / `SCIENTIST_2` | Peer-review battles at 4 points. Goes from dismissing the rig as a toy to defending it: "the model is wrong, but it's useful." |
| **Josie Lindqvist** | Undergrad on the crew, granddaughter of the ranch owner. | `PICNICKER` (the existing camp "Student") | The bridge between ranch and science. She will inherit the land and the decision. She chooses paleontology. |
| **Dale Brekke** | Crew chief and preparator; ex-oilfield, local. | `HIKER` (the existing "Crew") | Teaches the dig (jacketing, context, field notes). Gives the fishing kit and waders. |
| **Bea Lindqvist** | Rancher who owns the land the Pair is on. In Montana, fossils on private land belong to the surface owner. ⚠ | `WOMAN_*` / `EXPERT_F` | Drought and cattle prices make the auction money hard to refuse. Chooses the museum consortium in the end, and is still paid. |
| **Wade Kessler** | Commercial fossil dealer ("Kessler Natural History"). Legal on private land, articulate, and partly right. | `GENTLEMAN` / `MANIAC` | Not a villain team. His argument: fossils erode if no one collects them, and museums can't pay. His crew's one crime is digging across the fence onto federal (BLM) land, which needs a permit under PRPA 2009 ⚠. He's fined, not destroyed, and stays in business. |
| **Ranger Lucia Ortiz** | BLM paleontology / law-enforcement ranger | `POLICEMAN` recolour | Turns the player's field notes into evidence. Gives the BLM collecting permit (key item, unlocks Sand Arroyo). |
| **Visiting researchers** (one per act) | Peer-review battlers at camp: palynologist, ichthyologist, ornithologist, isotope geochemist, mammalogist, ichnologist, volcanologist, Quaternary ecologist | stock trainer classes, renamed | Each gives one field-note insight about their act, plus money and EXP (§3.7). |

Why the antagonist is grounded: legal commercial sales of US private-land fossils,
multi-million-dollar dinosaur auctions, contested ownership of a Montana specimen pair,
and fossil theft from public land are all real, documented issues. The game uses
the pattern, with **no real names, companies or specimens**.

### 1.5 Act-by-act beats (deep time ↔ present-day interlude)

Rhythm: **enter layer → explore 3–5 maps → boss set piece → return → camp interlude**
(one present-day beat, one peer-review battle, new shop stock). Story flags go in new
`VAR_STRATA_SUBPLOT` (0–10), so `VAR_STRATA_STORY` keeps its 2N/2N+1 meaning.

| Act | Deep-time beat (the lesson) | Interlude at camp (the people) |
|---|---|---|
| 0 Prologue | Arrive in the truck (`InsideOfTruck` layout). Dale's tutorial dig in the badlands: find the three specimens and log their layer ("a bone without its layer is just a rock"). See Kessler's crew on the next ranch. Halvorsen calibrates the rig, and you choose a starter. | Peer review #0 vs Theo (Lv 5, the starter after yours in the cycle mammal→bird→turtle→mammal). |
| 1 Hell Creek, 66.04 Ma | A full food web at its peak. You are a 0.5 kg animal among giants. The tyrant set piece is about **surviving, not winning**. At the end ejecta streaks cross the sky and Halvorsen pulls you out. | Kessler drops by to offer "partnership" (rig output for prospecting). Halvorsen says no. Theo calls the rig "a fancy diorama". |
| 2 Impact winter, +~1 yr | Dark, cold, nothing growing. Who survives? Small animals, burrowers, animals in water, detritus feeders, animals that can go a long time without food. A burrow refuge. The gauntlet. The **fern spike**. | The visiting palynologist explains the fern spike from spore counts. Bea mentions the drought. Ranger Ortiz introduces BLM permits. |
| 3 Corral Bluffs, ~65.4 Ma ⚠ | Recovery in steps: palms → legumes → bigger plant eaters → the first big mammal predator (*Eoconodon*). Mammals filling the empty niches. | Peer review #1 (Theo). Josie finds a fresh, illegal pit on BLM land: new map **Sand Arroyo** (NEW). |
| 4 Bighorn Basin, PETM ~56 Ma | A hothouse world: dwarfing, and immigrants (horses, primates, even-toed ungulates, rodents) arriving over high-latitude land bridges. Halvorsen: the PETM carbon release took thousands of years, and ours is roughly ten times faster ⚠. | Kessler offers Halvorsen a funding deal. Halvorsen refuses, and Theo nearly takes it (he needs funding too). |
| 5 Green River / Bridger, ~52–46 Ma | Exceptional preservation: the rig "renders sharp". Whole fish schools, bats, birds, primates in the canopy. The long cooling begins. | You document the BLM pit with Ortiz (photos, GPS, layer). Peer review with the ichthyologist. |
| 6 White River, ~33 Ma | The Eocene–Oligocene boundary is a visible contact in the cliffs. Forests open up, runners and burrowers do well, and the archaic warm-world fauna is gone. | Bea sets an auction date and Josie argues with her. Peer review #2 (Theo starts to come round). |
| 7 Ashfall, ~11.9 Ma | Clear grassland, then ash arrives from 1,600 km away. Death at the waterhole is slow: small animals first, rhinos last. The map flips to its ash variant after the boss. | Ortiz cites Kessler's crew for the BLM trespass. Kessler, still legal on Bea's land, keeps the auction going. Halvorsen proposes a museum consortium, and you build the "research case" (the Codex side quest, §3.5). |
| 8 Ice Age, ~20 ka + coda ~13 ka | Megafauna at the Last Glacial Maximum, and the trap cave. **Coda: the Colby mammoth site (Bighorn Basin, ~13 ka) ⚠.** A Clovis point lies beside mammoth bones. The rig can't render the people. "Someone made this." | Auction day. Bea picks the consortium. Theo's peer review #3 is a double battle with Josie. |
| Epilogue, today | The last filter runs and the Ice Age giants are lost. Today's prairie holds the descendants, and species that nearly disappeared in the last 150 years (bison, black-footed ferret, swift fox). | The Interpretive Center (NEW) opens with the Pair on display. Final peer review: Halvorsen (Lv 55). Credits roll up the stratigraphic column, listing every lineage you carried and its fate. |

**Ending text (the theme stated once, plainly):** Halvorsen: "Every extinction you saw
was written in the rock before you got there. The one happening now isn't written
yet." The epilogue Codex flags which living species on the prairie were reintroduced
or nearly lost.

---

## 2. Act-by-act content plan

General rules for every act:
- **3–5 maps.** Use `crop` / `patches` in `maps.py`, and preview candidates with
  `tools/strata/maprender.py` / `mapascii.py` before committing to one. Layouts below are
  *candidates*.
- Every map gets a `habitat=` tag (generated into `sMapHabitats`, task R4), **2–3 field-note signs**
  (`sign()` bgs; one claim per sign, written like a field notebook), and hidden **forage
  items** that respawn (`FLAG_TEMP_*`, §3.5).
- **Every new species must pass `test/strata_region.c`** ("Wild Pokemon in each era's maps
  have appeared and are alive in that era"). It fails when a species appears wild before
  its roster `first_era`, after its `last_era`, or after it died out or descended (done, C1).
- **Habitat key:** F = forest (long grass, or a map tagged forest), O = open (tall grass),
  W = water (surf, or a shore tile next to water, §3.3). Diet forage: P = plant, A = animal.

### 2.1 Act 0: Present day, Hell Creek (Garfield County, MT)

| Map | Status | Placeholder layout | Landmarks / content | Field notes |
|---|---|---|---|---|
| Hell Creek Camp | built | Route 111 north | Hub. Add: camp store (quartermaster NPC with a `pokemart` script), the visiting-researcher spot, Josie, Dale | "Lower is older"; the iridium layer |
| Field Station | built | Birch's lab | Rig, Halvorsen. Add **PC** (bg on the desk), **Move Relearner** (the rig "re-derives" behaviours), Codex terminal | Rig rules R-a…R-i as wall posters |
| Hell Creek Badlands | built | Route 111 desert | Tutorial dig (3 hidden "specimen" items before the starter choice), the K-Pg boundary sign | Boundary clay, iridium |
| **Jordan** (town, NEW) | built (C2) | `FallarborTown` crop | General store, café (gossip about fossil prices), BLM field office (Ranger Ortiz) | "Fossils on private land belong to the landowner" ⚠ |
| **Lindqvist Ranch** (NEW) | built (C2) | `Route117` (Day Care house = ranch house, fences) | Bea; fence line to Kessler's lease; the Pair's quarry under a tarp (story-gated) | Ranching vs drought; surface vs mineral rights ⚠ |
| **Sand Arroyo, BLM land** (NEW) | built (C2) | `Route111` desert rows 74+ (joins the badlands seamlessly) | The poached pit (scattered plaster, a broken jacket). Evidence objects to photograph | Why context matters: an illegally dug bone loses its date |

No wild encounters in Act 0. Present-day wildlife appears only in the epilogue (§2.10).

### 2.2 Act 1: Hell Creek Formation, 66.04 Ma

| Map | Status | Layout | Habitat | Species (existing roster) | Notes |
|---|---|---|---|---|---|
| Levee Forest | built | Route 119 S | F (long grass) / W shore | Mesodma, Didelphodon, Thescelosaur, Acheroraptor, Anzu, Pachycephalo, Edmontosaur, Triceratops | Arrival. Field notes: angiosperm forest; "the most common dinosaur here is Triceratops" |
| River Channel | built | Route 119 mid | W / F | add Ankylosaurus; fishing: Lepisosteus, Champsosaur, Borealosuch | The bluff and tracks |
| Backswamp | built | Route 120 marsh | W / F | Champsosaur, Borealosuch, Lepisosteus, Emarginachel (NEW wild slot) | Detritus food web (the survivors' web): sign "what eats dead leaves?" |
| **Fern Glade** (NEW) | NEW | `Route123` grassy crop or `Route110` west | O | Edmontosaur herd, Thescelosaur, **Avisaurus** (NEW: a tree-perching enantiornithine bird, doomed) | Open habitat for the bird's pressure. Sign: "tree-dwelling birds vs ground birds" |
| **Bluff Top** (NEW, optional) | NEW | split from River Channel | O | Tyrannosaur (set piece) | Where the impact's ejecta is seen |

**Boss: "The Tyrant", a survival set piece.** *Tyrannosaurus* Lv 14 with
`settotemboost` +1 Atk, catch rate 3 (as is). **Any outcome except whiteout finishes
the act.** Running is survival, and gets the mentor line "Small and quick: that's how
mammals lived here." Winning or catching gets the existing "stood your ground" line.
Implementation: in `StrataRiver_EventScript_Tyrannosaur`, treat `B_OUTCOME_RAN` like a win
and set a flag `FLAG_STRATA_TREX_FLED` that picks Halvorsen's line. Then **ejecta
cutscene**: screen flash, `WEATHER_DROUGHT`→red tint, and text: "Streaks of light
cross the southern sky, hotter each minute." The light pulse's intensity is debated ⚠
(say "debated", don't depict a firestorm).

**Pressures available:** F (levee, glade edges), O (glade), W (river and backswamp
shores), P (fern fronds, angiosperm fruit), A (carrion near the bluff).
**Enables:** the bird's *Presbyornis* (W) or *Gastornis* (P) branch at the Act 4
load, because the bird's window covers Acts 1–3.

**Extinction leaving the act (Act 2 load, existing list + Avisaurus NEW):** every
non-avian dinosaur, *Didelphodon* and *Avisaurus*.

### 2.3 Act 2: Impact winter, Hell Creek +~1 yr (Tullock base)

| Map | Status | Layout | Habitat | Species | Notes |
|---|---|---|---|---|---|
| Ashen Levee | built | winter palettes | F | survivors (as built) | Fixed "dark" lighting (§3.9), not night |
| Ashen River | built | winter | W | as built | Skull on the bluff (built) |
| Ashen Swamp | built | winter | W | as built | The gauntlet |
| **Burrow Refuge** (NEW) | NEW | `Route114_FossilManiacsTunnel` or `AlteringCave`, small | none | Mesodma, Cimolestes | The burrow where small mammals waited it out. A **forage cache** (seeds = P). Sign: "burrowers survived better" |

**Boss: the gauntlet** (built): 13/14/16 → **14/15/17**, with no healing between fights.
Add `B_VAR_WILD_AI_FLAGS` = smart AI for its duration. Post-boss, the fern spike (built).
**Pressures:** W, and P from the seed cache. **No descents happen at the Act 2 load**
(only extinctions), so tell the player: "This layer is about who's left, not who changes."
**Extinction leaving Act 2 (Act 3 load):** none in the table. That's correct: the survivors
carry on.

### 2.4 Act 3: Corral Bluffs, Denver Basin, CO (~65.7–65.4 Ma) ⚠

> **Status (C5, the Act 3 part of the C3–C10 row in §6): ✅ built.** Four maps (Palm Forest hub; Legume Thicket,
> Concretion Bluffs and Front Range Creek off it). Deviations: Thicket/Bluffs/Creek are Route 120/116/119 crops (the
> FRLG forest layout can't be rendered or checked by the tools); the Bluffs have no water, so *Protochelyd* is wild in
> the creek only; the Taeniolabis mini-boss (Lv 20) is on the Bluffs. Concretions give a note and a small
> item (no Codex entry exists yet).

Relabel the layer **"Denver Fm, ~65.4 Ma"** (or show the span 65.7–65.4). The boss
*Eoconodon* and *Taeniolabis* appear ~700 kyr after the impact, together with the oldest
legumes, not at 300 kyr (§5, H1).

| Map | Status | Layout | Habitat | Species | Notes |
|---|---|---|---|---|---|
| Palm Forest | built | Petalburg Woods | F (tag it, A6) | Loxolophus, Carsioptych, Purgatorius, Mesodma, Protictis | "~300 kyr: palm-dominated forest" |
| **Legume Thicket** (NEW) | NEW | `ViridianForest_Frlg` | F | Taeniolabis, Carsioptych, Loxolophus | Oldest legume pods. P forage (legume pods, high value). Sign: "protein-rich seeds, and bigger bodies?" (labelled hypothesis) |
| **Concretion Bluffs** (NEW) | NEW | `Route112` lower (rocky ledges) | O | Taeniolabis, Protochelyd (shore), Asteriornis | The real site: fossils found by cracking concretions. Hidden items = concretions ("Crack it: a skull!" gives a Codex entry) |
| **Front Range Creek** (NEW) | NEW | `Route102`/`103` river strip | W | Lepisosteus, Champsosaur, Borealosuch, Protochelyd | The Laramide Rockies rising on the horizon (sign) |

**Boss: *Eoconodon*** Lv 22 (keep), on its carcass in the thicket's north path. A
carrion object = an A forage node after the battle.
**Pressures:** F (thicket, palms), O (bluffs), W (creek), P (palm fruit, legumes), A (carcass).
**Enables:** the bird's three-way branch (last act of its window). The turtle's window
starts (heat +1/tick).
**Extinction leaving the act (Act 4 load, existing):** *Purgatorius, Loxolophus,
Carsioptychus, Taeniolabis, Eoconodon*. The rig warns: "the Puercan recovery fauna does
not reach the next layer."

### 2.5 Act 4: Bighorn Basin, WY, PETM (~56 Ma)

| Map | Status | Layout | Habitat | Species | Notes |
|---|---|---|---|---|---|
| Red Beds | built | Route 114 N, PETM palettes | O | Sifrhippus, Hyopsodus, Diacodexis, Teilhardina, Gastornis, Coryphodon | Drought weather. **Remove Protictis** from the wild table ⚠ |
| **Polecat Bench** (NEW) | NEW | `SevenIsland_SevaultCanyon_Frlg` + PETM palette | O | Sifrhippus, Diacodexis, **Paramys** (NEW, an early rodent arriving) | Real PETM section. Signs: "the carbon isotope excursion in these beds"; "immigrants across the Arctic" |
| **Willwood Swamp** (NEW) | NEW | `Route120` south section + PETM palette | W / F | Coryphodon, Borealosuch, Champsosaur, Lepisosteus, Protochelyd | Wallowing pantodonts. A forage (insect larvae) |
| **Clarks Fork Crossing** (NEW, optional) | NEW | `Route110` river (trim the cycling road) | W / O | **Oxyaena** (NEW predator mini-boss), Gastornis | Mini-boss: an *Oxyaena* overworld set piece (§3.7) |

**Boss: *Coryphodon*** Lv 28 on the land bridge (keep), **wild double with a calf**
(`setwildbattle SPECIES_CORYPHODON, 28, ITEM_NONE, SPECIES_CORYPHODON, 24`).
**Heat:** 2/tick, the highest in the game. **Steering note for the player:** "Hot
layers push lineages toward heat-tolerant branches. Keep a lineage in the PC if you
don't want that." (The turtle branch, §2.11.)
**Pressures:** O, W, F, heat. **Enables:** the turtle's *Macrochelys* (heat) branch at the Act 7
load. Dog: Protictis → Miacis at the Act 5 load (no branch).
**Extinction leaving the act (Act 5 load):** none listed. Fine: Act 4 losses come at
White River.

### 2.6 Act 5: Green River lakes and Bridger Basin, WY (~52–46 Ma)

Rename the existing map **"Bridger Shore"**. Most of its lake fauna is from *Fossil Lake*
(Fossil Butte, ~52 Ma), not Lake Gosiute (§5, M5). Split them:

| Map | Status | Layout | Habitat | Species | Notes |
|---|---|---|---|---|---|
| **Fossil Lake** (NEW) | NEW | `Route103` (lake + shore) | W | Knightia, Heliobatis, Presbyornis, Onychonycter, Gallinuloid; fishing: Knightia, Lepisosteus | Lagerstätte. Signs: "schools of fish died at once"; "the oldest bats". Mass-mortality cutscene (lake turnover, labelled hypothesis) |
| Bridger Shore | built (rename) | Route 104 | W / O | Eohippus, Uintatherium, Coryphodon ⚠, Borealosuch, **Hyrachyus** (NEW, early rhino relative) | Boss here |
| **Bridger Forest** (NEW) | NEW | `ThreeIsland_BerryForest_Frlg` | F | Notharctus, **Omomys** (NEW), Miacis, Eohippus, Hyopsodus | Canopy primates. P forage (palm fruit, leaves) |
| **Oil-Shale Cliffs** (NEW, optional) | NEW | `Route115` north cliffs | O | **Patriofelis** (NEW predator mini-boss), Diacodexis | Varved shale: "one stripe = one year" |

**Boss: *Uintatherium*** Lv 34 (keep). Stage it as a bull **charging along the shore**
(a scripted movement of an overworld placeholder sprite, then the battle).
**Pressures:** W (strongest), F, P. **Enables:** horses (Eohippus window = Act 5; no branch);
Miacis → Hesperocyon at the Act 6 load.
**Extinction leaving the act (Act 6 load, existing list + NEW):** Gastornis, Presbyornis,
Champsosaur ⚠, Borealosuch, Mesodma, Hyopsodus, Diacodexis, Coryphodon, Onychonycter,
Heliobatis, Knightia, Notharctus, Uintatherium; NEW: Omomys, Oxyaena, Patriofelis.

### 2.7 Act 6: White River Group, SD/NE (~34–30 Ma)

| Map | Status | Layout | Habitat | Species | Notes |
|---|---|---|---|---|---|
| White River | built | Route 114 S, Oligocene palettes | O | Mesohippus, Merycoidodon, Leptomeryx, Ischyromys, Stylemys, Poebrothere, Hesperocyon, Subhyracodon, Hoplophoneus, Archaeothere | Boss at the bone stash |
| **Badlands Wall** (NEW) | NEW | `SixIsland_RuinValley_Frlg` (patch out ruins) + Oligocene palette | O | Merycoidodon herds, Stylemys, **Palaeolagus** (NEW, rabbit) | A cliff sign at the **Chadron / Brule contact**: "the Eocene–Oligocene boundary is in this cliff" ⚠ |
| **Gallery Forest** (NEW) | NEW | `Route119` north forest band + Oligocene palette | F / W | Mesohippus, Leptomeryx, Hesperocyon, **Douglassciurus** (NEW, the first squirrels ⚠) | Forest strips along the rivers in open country. **This is where the horse's forest branch is steered** |
| **Toadstool Trackways** (NEW) | NEW | `DesertRuins` or `Route111` rocky crop | O | Subhyracodon, **Hyaenodon** (NEW, mini-boss), Poebrothere | Fossil trackways. Hidden items = track casts (Codex) |

**Boss: *Archaeotherium*** Lv 40 at the bone stash (keep). After the battle the stash is an
**A forage node** ("carrion"). That's where the player chooses whether to push
Hesperocyon toward *Epicyon*.
**Pressures:** O (dominant), F (gallery forest), A (bone stash), P.
**Enables:** horse FOREST → *Hypohippus* vs default → *Protohippus*; dog A → *Epicyon* vs
default → *Leptocyon*; rhino (window = Act 6) OPEN → *Aphelops* vs default → *Teleoceras*.
**Extinction leaving the act (Act 7 load, existing + NEW):** Archaeothere,
Hoplophoneus, Merycoidodon, Leptomeryx, Stylemys, Ischyromys; NEW: Hyaenodon,
Palaeolagus. A *Paramys* carried from Act 4 becomes *Ischyromys* at the Act 6 load and
dies at the Act 7 load. That's intended: rodents as a group survive, and this genus doesn't.

### 2.8 Act 7: Ashfall, NE (~11.9 Ma)

**Staging change:** the act opens **before** the ash. The maps start clear, under a
distant haze (`WEATHER_SHADE`). The boss trigger starts the ashfall. After the boss,
each map warps to its **ash variant** (same layout with `*_ash` palettes from
`gen_tilesets.py` plus `WEATHER_VOLCANIC_ASH`), the same technique as the impact-winter
maps.

| Map | Status | Layout | Habitat | Species | Notes |
|---|---|---|---|---|---|
| Grassland | built (pre-ash version needed) | Route 113 | O | Protohippus, **Cormohipparion** (NEW), Procamelus, Leptocyon, Balearica, **Cosoryx** (NEW, pronghorn relative ⚠), Epicyon. **Remove Gallinuloid** (anachronism, §5) | Grass and grazers. Sign: "high-crowned teeth vs grit" |
| **Niobrara River** (NEW) | NEW | `Route120` north river or `Route25_Frlg` | W | Chelydra ⚠, Lepisosteus, Teleoceras, **Aphelops** (NEW) | Turtle fishing spot |
| **Savanna Woodland** (NEW) | NEW | `SafariZone_South` / `North` | O / F | Procamelus, **Hypohippus** (NEW ⚠), Anchigyps, Leptocyon | Mixed browsers and grazers |
| **The Waterhole** (NEW, split from Grassland east) | NEW | `SafariZone_Southwest` (pond) | W | Teleoceras herd | Boss arena. After the boss it becomes the "rhino barn" view (field note about the real excavation shelter) |

**Boss: *Teleoceras* bull + cow, wild double** (46/42) at the waterhole, with the ash
starting to fall during the intro text. After the battle: a fade-to-grey cutscene and the
existing text ("small animals first, rhinos last"). Ash maps have **no** new encounters
in their tables beyond the survivors at higher levels. That is the point.
**Pressures:** O (dominant), W (river), A, P (seed heads).
**Enables:** Leptocyon (window = Act 7) three-way: default → *Canis*, A → *Aenocyon*,
O → *Vulpes* (NEW); horse Protohippus → Equus at the Act 8 load (no branch).
**Extinction leaving the act (Act 8 load, existing + NEW):** Teleoceras, Epicyon,
Balearica, Anchigyps; NEW: Aphelops, Hypohippus, Cormohipparion.

### 2.9 Act 8: Ice Age Wyoming (~20 ka), with a ~13 ka coda

| Map | Status | Layout | Habitat | Species | Notes |
|---|---|---|---|---|---|
| Ice Age Steppe | built | Route 118, ice palettes | O | as built; **drop Aenocyon** ⚠ (or keep with a note) | Sinkhole entrance |
| Natural Trap Cave | built | Granite Cave 1F | none | (boss only) | Rope back out |
| **Meltwater River** (NEW) | NEW | `Route119` (ice palettes) | W | Chelydra, Lepisosteus, Ovibos ⚠ | Braided glacial outwash |
| **Ice Margin** (NEW) | NEW | `FourIsland_IcefallCave_Entrance_Frlg` + exterior strip | O | Ovibos, Mammuthus, Panthera | The Laurentide ice front to the north (sign: "~1–2 km thick") ⚠ |
| **Colby Site, ~13 ka** (NEW coda) | NEW | small `Route118` east crop, late-glacial palette (less snow) | none | no encounters | Mammoth bones and a **Clovis point**. The rig can't render the people (rule R-g). A sign on the evidence for and against a human role ⚠. Leads to the epilogue |

**Boss: *Arctodus*** Lv 52 in the cave (keep). Add a mini-boss on the steppe: an
***Panthera atrox* pair** (double, Lv 48/48) as an overworld set piece.
**Colby coda:** opens after the Arctodus fight via the anchor sign ("Load the late-glacial
sub-layer?"). Same era, so no lineage changes. Needs `FLAG_STRATA_COLBY_SEEN` before the rig
offers "Today".
**Pressures:** O, W. No descents happen at the epilogue load (only extinctions), so
Act 8's pressures steer nothing. Say so in the rig text: "This last step is about who is
left." The bird's *Centrocercus* branch happens at the Act 8 load, steered in the Act 6–7
grasslands.
**Extinction leaving the act (epilogue load, existing):** Aenocyon, Arctodus,
Miracinonyx, Panthera, Mammuthus, Camelops.

### 2.10 Epilogue: Montana today

| Map | Status | Layout | Habitat | Species | Notes |
|---|---|---|---|---|---|
| Montana Prairie | built | Route 102 | O | Cynomys, Antilocapra, Canis, Meleagris, Bison, Ovis; **remove Ovibos** (§5, H2); NEW: **Mustela nigripes**, **Vulpes velox**, **Centrocercus** | Prairie-dog town and ferret |
| **Missouri Breaks** (NEW) | NEW | `Route114` river section | W / O | Chelydra, Lepisosteus ⚠, Ovis, Meleagris | River badlands. The same rocks as Act 1, eroding today |
| **Pryor Mountains** (NEW, optional) | NEW | `Route112` / `JaggedPass` | O | Equus (feral) | "Horses came back with the Spanish in the 1500s" |
| **Interpretive Center** (NEW) | NEW | `LilycoveCity_LilycoveMuseum_1F/2F` | none | none | The Pair on display; the **Hall of Lost Lineages** (your fossil items, §3.4); final peer review vs Halvorsen |

**No boss.** The finale is the Halvorsen peer review (Lv 55 team built from "classic"
reconstructions: Tyrannosaur, Uintatherium, Epicyon, Arctodus, Teleoceras, Chelydra), then
the credits.

### 2.11 Lineage branches (all descents, existing + proposed)

The **window** is when pressure accumulates for that descent: from the previous descent
(or the catch) to the era load. `minScore` is the proposed per-option threshold (§3.3). The default
(`PRESSURE_NONE`) wins whenever no option reaches its threshold.

| Ancestor → (era load) | Default | Branches (pressure ≥ minScore) | Window | Where to steer | Status |
|---|---|---|---|---|---|
| Cimolestes → (A3) | Protictis | none | A1–2 | n/a | existing |
| Protictis → (A5) | Miacis | none | A3–4 | n/a | existing |
| Miacis → (A6) | Hesperocyon | none | A5 | n/a | existing |
| Hesperocyon → (A7) | Leptocyon | Epicyon (A ≥ 64) | A6 | Archaeotherium's bone stash | existing; threshold done (R1) |
| Leptocyon → (A8) | Canis | Aenocyon (A ≥ 64); **Vulpes** (O ≥ 96) | A7 | carrion vs open grassland | ✅ Vulpes added (F8) |
| Asteriornis → (A4) | Gallinuloid | Presbyornis (W ≥ 64); Gastornis (P ≥ 64) | A1–3 | shores; ferns, palms, legumes | existing; needs W/P sources |
| Gallinuloid → (A8) | Meleagris | **Centrocercus** (O ≥ 96) | A4–7 | White River and Ashfall grassland | ✅ added (F8) |
| Emarginachel → (A3) | Protochelyd | none | A1–2 | n/a | existing |
| Protochelyd → (A7) | Chelydra | **Macrochelys** (heat ≥ 160) | A3–6 | carry it through the PETM (heat 2/tick); keep it in the PC to avoid | ✅ added (F8). A party turtle gets there in ~80 PETM ticks (~2,600 steps), so it is close to the default for a carried turtle; revisit after the playtest (Q2) |
| Sifrhippus → (A5) | Eohippus | none | A4 | n/a | existing |
| Eohippus → (A6) | Mesohippus | none | A5 | n/a | existing |
| Mesohippus → (A7) | Protohippus | **Hypohippus** (F ≥ 64) | A6 | Gallery Forest | ✅ added (F8) |
| Protohippus → (A8) | Equus | none | A7 | n/a | existing |
| Poebrothere → (A7) | Procamelus | none | A6 | n/a | existing |
| Procamelus → (A8) | Camelops | none | A7 | n/a | existing |
| **Hyrachyus** → (A6) | Subhyracodon | none | A5 | n/a | ✅ added (F8; gives the rhino line a start) |
| Subhyracodon → (A7) | Teleoceras | **Aphelops** (O ≥ 64) | A6 | open flats | ✅ added (F8; both branches die at A8: "fitness isn't enough") |
| Teilhardina → (A5) | **Omomys** | none | A4 | n/a | ✅ changed (F8/H4; Notharctus is a different primate group and stays wild-only) |
| **Paramys** → (A6) | Ischyromys | none | A4–5 | n/a | ✅ added (F8) |
| **Douglassciurus** → (A8) | Cynomys | none | A6–7 | n/a | ✅ added (F8), stand-in ⚠ (wild in Act 6 only: roster `last_era`) |
| **Cosoryx** → (A8) | Antilocapra | none | A7 | n/a | ✅ added (F8), stand-in ⚠ |

Every starter now has one real choice, and each choice has a visible cost:
- **Dog:** meat → the strong specialist that dies later; open → swift fox (survives,
  nearly lost in the 20th century); default → coyote.
- **Bird:** three-way at Act 4, then the sage-grouse option.
- **Turtle:** stasis, plus the heat-driven alligator snapping turtle (bigger, BST up,
  lives far from Montana today).

### 2.12 Species additions ✅ (C1 done: 17, appended in `tools/strata/roster/part3.py` so IDs never shift)

All 17 are in the roster (none deferred). The in-game names of two are cut to 12 characters:
*Douglassciurus* → `Douglassciur`, *Cormohipparion* → `Cormohippari`. Five borrows differ
from the first plan, so that no descent shows the same placeholder sprite before and
after (Teilhardina→Omomys, Leptocyon→Vulpes, Gallinuloid→Centrocercus,
Protochelyd→Macrochelys), and Oxyaena doesn't look like the player's Protictis in Act 4;
`deerling` has no plain species entry to borrow from. BST = 340 + 50·log10(kg), +40 focal.

| Species | Act(s) | Mass kg | BST | Types | Diet | Borrow | `first_era` | Fact-check notes |
|---|---|---|---|---|---|---|---|---|
| *Avisaurus archibaldi* | 1 | ~1 (est) | 340 | FLYING/DARK | carnivore | `taillow` | HELL_CREEK | Hell Creek Fm, MT ✓. Known from foot bones; raptor-like habit debated (dex says so). Dies at the K-Pg |
| *Paramys* | 4 (5) | ~2 (est) | 355 | NORMAL | herbivore | `sentret` | BIGHORN_PETM | Willwood Fm ✓. Correction: NA's first rodents (*Acritoparamys*) are Clarkforkian, ~57 Ma, just **before** the PETM; dex and the Ischyromys dex now say so |
| *Oxyaena* | 4 | ~20 (est) | 405 | DARK | carnivore | `sneasel` | BIGHORN_PETM | Willwood Fm ✓ (Clarkforkian–Wasatchian) |
| *Omomys carteri* | 5 | ~0.25 (est) | 310 | NORMAL/PSYCHIC | omnivore | `pansage` | GREEN_RIVER | Bridger Fm ✓ (~50–47 Ma). Teilhardina's stand-in descendant (H4) |
| *Hyrachyus modestus* | 5 | ~70 (est) | 432 | GROUND | herbivore | `phanpy` | GREEN_RIVER | Bridger Fm ✓. Rhinocerotoid grade, not a proven ancestor |
| *Patriofelis ferox* | 5 | ~70 (est) | 432 | DARK/FIGHTING | carnivore | `litleo` | GREEN_RIVER | Bridger Fm ✓ |
| *Hyaenodon horridus* | 6 | ~40 (est) | 420 | DARK | carnivore | `mightyena` | WHITE_RIVER | Brule Fm ✓; NA species gone by the late Oligocene |
| *Palaeolagus haydeni* | 6 | ~0.8 (est) | 335 | NORMAL | herbivore | `buneary` | WHITE_RIVER | Brule Fm ✓, very common |
| *Douglassciurus jeffersoni* | 6 | ~0.3 (est) | 314 | NORMAL | herbivore | `pachirisu` | WHITE_RIVER (`last_era` WHITE_RIVER) | ⚠ kept: Chadron Fm, Flagstaff Rim WY, ~36 Ma (late Eocene; slightly older than the act). Tree-squirrel grade standing in for the prairie-dog line; wild in Act 6 only |
| *Hypohippus* | 7 | ~200 (est) | 455 | NORMAL/GRASS | herbivore | `ponyta` | ASHFALL | ⚠ kept with site "Miocene Great Plains, NE" (~17–11 Ma): not recorded in the Ashfall bed itself (M9) |
| *Aphelops* | 7 | ~1,500 (est) | 499 | GROUND | herbivore | `rhyhorn` | ASHFALL | ⚠ kept: present but rare at Ashfall beside *Teleoceras*; the open-country contrast is interpretive |
| *Cormohipparion occidentale* | 7 | ~100 (est) | 440 | NORMAL/GRASS | herbivore | `blitzle` | ASHFALL | ⚠ kept: a common Ashfall horse ✓ |
| *Cosoryx furcatus* | 7 | ~20 (est) | 405 | NORMAL | herbivore | `girafarig` | ASHFALL | ⚠ kept as "Miocene Great Plains, NE" (~13–11 Ma); in the Ashfall bed unverified. Merycodontine stand-in for *Antilocapra* |
| *Macrochelys* | 7 | 80 | 475 (focal) | WATER/ROCK | omnivore | `carracosta` | ASHFALL | ⚠ kept: *M. schmidti*, Miocene of Nebraska ✓. Survives today only in the Southeast; the lineage is not removed at A8 (Codex: "lost from Montana, survives elsewhere") |
| *Vulpes velox* | 8, E | 2.2 | 397 (focal) | NORMAL/DARK | omnivore | `fennekin` | TRAP_CAVE | ⚠ kept: reintroduced (Canada from 1983, Montana from 1998); check dates (M12). Not wild in Act 8 until a Pleistocene WY record is cited |
| *Centrocercus urophasianus* | 8, E | 2.5 | 400 (focal) | NORMAL/FLYING | herbivore | `starly` | TRAP_CAVE | Mass is a large male's. ~44% range loss (Schroeder et al. 2004) |
| *Mustela nigripes* | E | 0.9 | 338 | DARK | carnivore | `furret` | EPILOGUE | ⚠ kept: rediscovered 1981 near Meeteetse, WY (Bighorn Basin ✓); reintroduced in Montana from 1994; check (M12) |

**Suggested encounter placement** (for the C3–C10 / C12 content agents; levels within the
§3.1 bands; `test/strata_region.c` enforces `first_era`, `last_era` and extinctions):

| Act | Map | Species (levels) |
|---|---|---|
| 1 | Levee Forest (F), Fern Glade (O) | Avisaurus 5–10 (forest edge; uncommon) |
| 4 | Polecat Bench, Red Beds | Paramys 20–26 |
| 4 | Clarks Fork Crossing | Oxyaena set piece Lv 26; rare wild 23–26 in Willwood Swamp |
| 5 | Bridger Forest | Omomys 26–31, Paramys 26–30 |
| 5 | Bridger Shore | Hyrachyus 28–33 |
| 5 | Oil-Shale Cliffs | Patriofelis set piece Lv 32 |
| 6 | Badlands Wall, White River | Palaeolagus 32–36 (common) |
| 6 | Gallery Forest | Douglassciur 33–37 (Act 6 only) |
| 6 | Toadstool Trackways | Hyaenodon set piece Lv 38; rare wild 35–38 |
| 7 | Grassland | Cormohippari 38–43 (common), Cosoryx 38–42 |
| 7 | Savanna Woodland | Hypohippus 39–43, Cosoryx 38–42 |
| 7 | Niobrara River | Aphelops 40–44 (shore), Macrochelys 38–42 (surf/fishing) |
| E | Montana Prairie | Mustela 46–50 (rare, prairie-dog town), Vulpes 46–50, Centrocercus 46–50 |

Optional cameo (only with tribal consultation): *Ekgmowechashala* (Lakota-named, last NA
primate, ~29 Ma, SD) as a White River field note, not a species.

---

## 3. Mechanics specs

### 3.1 Difficulty and level curve

| Act | Wild levels (now → proposed) | Mini-boss | Boss (Lv) | Expected party Lv at the boss | **Era floor** on load |
|---|---|---|---|---|---|
| 0 | none | Theo sim Lv 5 | none | 5 | 5 (starter) |
| 1 | 3–10 → 3–10 | Acheroraptor pair (double, 8/8) | T. rex 14 (survival) | 10 | 5 |
| 2 | 10–16 → 9–15 | none | gauntlet 14/15/17 | 15 | 10 |
| 3 | 15–20 → 14–21 | Taeniolabis 20 | Eoconodon 22 | 21 | 14 |
| 4 | 20–28 → 20–27 | Oxyaena 26 | Coryphodon 28 + calf 24 | 27 | 20 |
| 5 | 26–34 → 26–33 | Patriofelis 32 | Uintatherium 34 | 33 | 26 |
| 6 | 34–39 → 32–39 | Hyaenodon 38 | Archaeotherium 40 | 39 | 32 |
| 7 | 40–45 → 38–45 | Epicyon 44 | Teleoceras 46 + cow 42 | 45 | 38 |
| 8 | 46–51 → 44–51 | Panthera pair 48/48 | Arctodus 52 | 51 | 44 |
| E | 46–54 → 46–54 | none | Halvorsen 55 (peer review) | 55 | 46 |

**Era floor** (coordinate with the in-flight floor work; these are the target values):
on `Lineage_AdvanceToEra` completion, every party and PC mon below `sEraLevelFloor[era]`
has its EXP set to that level's EXP (same code path as `KeepBoxMonLevel`) and its stats
recalculated. The floor is the act's wild minimum. The fallback survivor in
`EnsurePartyNotEmpty` is created at the floor instead of Lv 10. Rationale: a fresh catch
is always at era level, so the floor only rescues the lineages you *carried*, which is the
emotional core. Test: "A lineage carried into an era below its floor arrives at the floor".

**Bosses:** level = expected party level +1, plus `settotemboost` +1 in their signature stat,
plus `B_VAR_WILD_AI_FLAGS` smart AI for the battle only (set before `dowildbattle`, clear
after). Megafauna stay strong by BST, not by level.

**EXP:** turn on `I_EXP_SHARE_FLAG` (new flag, set in the intro). Wild-only acts give
too little EXP for a team of 6. `B_EXP_CATCH` is already on.

**Balance tooling (NEW, S):** `tools/strata/balance.py` prints, per act, the BST and stats at
level of every wild, boss and expected-party species from roster plus `maps.py`, and flags
any wild whose effective stat total at level exceeds the party median by more than 35%.
Run it in CI-style checks before every content merge.

### 3.2 Stats: BST formula

Current: `BST = 300 + 70·log10(kg)`, clamped to 180–600. That gives a 3× spread between the
smallest and largest species, too much for a game where a 0.04 kg bat meets an
8-tonne theropod at the same level.

**Proposed (three parts):**
1. **Compress:** `BST = 340 + 50·log10(kg)`, clamped to 250–600. Mass still orders
   everything, but the spread drops to about 2×.
2. **Focal lineage bonus +40** for the 16 starter-line species (new roster field
   `focal=True`). It's a game concession, and documented as such in the design doc.
3. **Lineage resilience:** each era a mon *survives* (party or PC), raise each IV by +3
   (cap 31). +1 more if its species did not change that era (stabilising-selection
   flavour for the turtle). IVs avoid the 510 EV cap. Implement it in
   `Lineage_AdvanceToEra` after `ApplyExtinctions`. Test it.

Selected results (old → new incl. focal): Cimolestes 279→365, Asteriornis 272→360,
Gallinuloid 263→354, Leptocyon 321→395, Canis 378→436, Emarginachel 363→425,
Mesodma 209→275, Teilhardina 193→264, Knightia 209→275, Tyrannosaur 573→535,
Mammuthus 577→538, Teleoceras 528→503, Arctodus 507→488.
The change sits in `base_stat_total()` in `gen_species.py`. Regenerate the data and update any
test that hard-codes stats. Small mons should also be **fast and evasive**: keep the
existing speed-heavy weights. No per-era scaling is needed after this change. Revisit
only if `balance.py` flags Acts 7–8.

Also widen the weight field (A12) before Codex work: switch the Strata species to a u32
weight, or store mass in 0.1 kg units with a separate display path in the Codex.

### 3.3 Selection pressures: scoring and sources

**Scoring (fixes A1):** add `u8 minScore` to `struct DescentOption` (default 64 via a macro).
An option is eligible only if `pressures[p] >= minScore`. Among eligible options the highest
counter wins (ties go to the first listed). With none eligible, the default
(`PRESSURE_NONE`) wins. Keep `PRESSURE_NONE` options at score 0.

**Sources (per party mon; PC mons gain nothing, the "seed bank" rule, explained in the rig help):**

| Pressure | Source | Rate |
|---|---|---|
| FOREST | Walking on long grass, or anywhere on a map tagged `habitat="forest"` | +1 per 32 steps (existing tick) |
| OPEN | Tall grass, or maps tagged open | +1 per 32 steps |
| WATER | Surfing; **or standing on a tile orthogonally next to surfable water (shore)**; fishing (+2 per hooked encounter) | tick / event |
| PLANT | **Forage items** (fern frond, palm fruit, legume pod, seed head, browse): +12 each | item use |
| ANIMAL (rename the "meat" label) | Carrion / larvae forage: +12 each. Knockouts: **+1, only if the species has `diet` = carnivore or omnivore** (new roster field), **capped at 24 per era** | item / battle |
| HEAT | Era climate per tick (existing `sEraHeat`) | 0–2 per tick |

**Water access (fixes A4):** Dale gives **Waders** (key item, Act 1 interlude). With
the flag set, the "surf?" prompt works without a badge or HM (patch the Surf unlock in
`src/field_move.c` to also accept `FLAG_STRATA_WADERS`, and allow the surf prompt from
`IsPlayerFacingSurfableFishableWater`). Dale also gives a **Fishing Kit** (= Old Rod, then
upgraded to Good Rod after Act 4). Placeholder flavour: "you wade; the reconstruction
handles the depth."

Rationale: the thresholds make every branch a **deliberate choice** (around 3 forage items, or
most of an act spent in one habitat), so the default path is the generalist that history
mostly kept.

### 3.4 Feedback to the player

The player must always be able to see *what they are steering*.

| Feature | What | Implementation sketch | Size |
|---|---|---|---|
| **Pressure chart** | A 5-axis radar of Forest / Open / Water / Plant / Animal, plus Heat as the "sheen" bar, per mon | Reuse Emerald's **condition graph** (the PokéNav/Pokéblock "Condition" screen already draws cool/beauty/cute/smart/tough + sheen, *exactly our counters*). Relabel the axes and open it from a new party-menu action "LINEAGE". | M |
| **Branch hints** | Below the chart: "Lineage may branch next layer: ▲ Animal 41/64 → *Epicyon*" (shown only after the branch is discovered in the Codex or hinted by a field note) | Read `sLineageDescents` for (species, next era). Show the closest option's progress. | S |
| **Rig forecast** | Before `RIG_NEXT`: per party mon, "→ descendant (pressure)" or "LOST (extinct in the record)"; PC losses as a count | New `special Strata_RigForecast` doing a dry run of `Lineage_GetDescendant` + `Lineage_IsExtinctInEra` over the party, buffered into a scrolling list menu. Players can still bank lineages in the PC or swap before confirming. | M |
| **Descent scene** | Each changed party mon gets an evolution-style morph with custom text ("Over 10 million years, the lineage of X became Y.") | Use `BeginEvolutionScene(mon, newSpecies, FALSE, slot)` per party mon *before* the species is set, with a Strata text variant. Box mons change silently, listed in the summary message. This also teaches new level-up moves via the evolution move check. | M |
| **Field notes** | 2–3 signs per map hinting at pressures ("Gars and turtles crowd these shallows", "Look at the bone pile") | `sign()` in maps.py | S per act |
| **Layer HUD** | Map popup shows "LEVEE FOREST · 66.04 Ma · window ~100 kyr" | Extend the map-name popup with a second string from the per-map era table (`sStrataMapEras` gains an age string) | S |

### 3.5 Extinction feedback, Fossil Case, and Codex

- **Fossil items:** when a lineage is lost, set `FLAG_STRATA_FOSSIL_<species>` (one flag
  per species). Save cost is 87 flags, from the unused flag range. A key item, the **Fossil
  Case**, lists them (custom list menu) with "extinct by ~X Ma, carried by you from Act N".
  In the epilogue they fill the **Hall of Lost Lineages** (one sign/plaque per flag).
- **Extinction message:** the current message names only the first loss plus a count.
  Replace it with a list menu of all losses and each one's era of last appearance. Show the
  Codex entry for one if the player picks it.
- **Codex** (rename the Pokédex; base it on the expansion's HGSS dex): pages for **Entry**
  (full genus, site, age, mass with "est." flag, dex text), **Evidence** (what the
  reconstruction is based on: bones / teeth only / tracks; from the roster `notes` field), and
  **Lineage**: reuse the HGSS **evolution page** but feed it from `sLineageDescents` (ancestor
  and descendants, with undiscovered branches as silhouettes). A status line says "Living",
  "Extinct ~X Ma", or "Lost from Montana, survives elsewhere".
- **Research case (Act 7 side quest):** Halvorsen's museum pitch needs N Codex entries with
  *Evidence* logged (from catching, or finding a field-note item in each map). Rewards: the
  epilogue museum display grows with your count; the stipend pays per entry (§3.6).
- **Gentle Deep Time** (an option at new game: "Strict record / Gentle record"): in Gentle, a
  lost mon is replaced at the same level by a surviving relative from a small table
  (`sGentleReplacement[]`, e.g. Epicyon → Canis, Teleoceras → Bison, Gastornis → Meleagris).
  The fossil is still awarded. Store it in a flag. Default: Strict.

### 3.6 Healing, items, economy

| System | Spec |
|---|---|
| Healing at camp | Halvorsen heals (existing). Add a healing cot in the station, so the player isn't forced through dialogue every time |
| **Field Kit** (key item) | Fully heals the party; **2 charges per rig entry** (3 after Act 4); recharged on every camp visit. A var holds the charges. Rationale: one map per act made returning cheap; with 4 maps per act the walk back matters |
| Forage (hidden items, respawn) | Each heals a party mon a little (20 HP) **and** adds pressure (§3.3). Placed as hidden items whose flags are `FLAG_TEMP_*` (cleared on map change, so they respawn on each visit). 3–6 per map. Item names: Fern Frond, Palm Fruit, Legume Pod, Seed Head, Browse (P); Larvae, Carrion (A) |
| Camp store | Opens in Act 0: Specimen Capsules (Poké Ball renamed, same art), Potions; adds Great Capsules after Act 3, Super/Hyper Potions by act. Uses the stock `pokemart` script |
| Money | Peer-review battles (one researcher per act, plus Theo) and a **survey stipend**: Halvorsen pays $150 × (new Codex "caught" entries since last payment). `special Strata_PayStipend` compares the caught count with `VAR_STRATA_STIPEND_COUNT` |
| Move Relearner | In the Field Station, free: "the rig re-derives behaviours" |
| PC | In the Field Station (A9) |

### 3.7 Trainers and set pieces

- **Humans battle only in the present day.** It follows from rule R-g, and it keeps deep
  time feeling wild.
- **Peer review:** one visiting researcher per act appears at camp after its boss. Their team is
  2–4 species from the act just finished, at the boss's level, themed by field. Theo at
  Acts 0/3/6/8. Trainer data goes in `src/data/trainers.party` with renamed classes
  (`TRAINER_CLASS_RESEARCHER` etc.), reusing stock trainer pics (Scientist, Hiker, Expert,
  Picnicker, Ruin Maniac) until art lands.
- **Deep-time set pieces** (instead of trainers): 1–2 **visible creatures per act**
  (object events using the borrowed species' overworld/follower sprite, so copy it in
  `gen_species.py` the same way front/back are copied). Talk, or step into the line of sight,
  to get a scripted `setwildbattle` (single or double), a field note before and after, and a forage
  reward after. Respawn: none (one-time, flagged).
- **Herd and pack doubles:** use the second-species form of `setwildbattle`.

### 3.8 Catching rules

- Every wild species can be caught ("sampling the reconstruction"), including bosses, at
  their own catch rates. The T. rex at catch rate 3 stays as a lottery ticket.
- A caught mon belongs to its lineage. Extinct-bound catches are a **one-act trophy**: they
  turn into fossils at the next load. Say so in the catch message the first time
  (`FLAG_STRATA_TIP_EXTINCT_CATCH`).
- No duplicate or first-encounter restrictions. Ball supply is the limit (store stock by act).
- Running is always allowed (no `WE_FLAG_NO_RUNNING`), except during the gauntlet.

### 3.9 Lighting and "clock rate"

- **Present day:** keep real-time DNS (camp, Jordan, ranch, prairie).
- **Deep time:** **fixed lighting per map**, chosen in `maps.py` (`light="day" | "dusk" |
  "dark" | "ash"`) and generated into the era table. In `MapHasNaturalLight` (and the DNS
  time-of-day lookup in `src/overworld.c`), return the fixed time for maps that have an
  entry. Choices: Act 1 day, Bluff Top dusk; Act 2 **dark** (impact winter, permanent); Act 7
  pre-ash day, post-ash "ash"; Act 8 day; trap cave and caves untinted. Rationale: the light is
  part of the reconstruction's content, not the player's wall clock.
- **Clock rate → time-averaging window.** Drop the per-act RTC ratio. Instead each act
  shows its **window** in the HUD and rig text: Act 1 "~100 kyr of floodplain", Act 2 "~1
  year", Act 5 "varves: single years", Act 7 "weeks", Act 8 "~150 kyr of cave fill"
  ⚠ (the values need checking). It's more truthful, and it costs nothing. Keep `OW_USE_FAKE_RTC` FALSE.

### 3.10 Other loop requirements

| Item | Spec | Size |
|---|---|---|
| Start menu | CODEX / TEAM / FIELD BAG / FIELD LOG (replaces POKéNAV; opens the Fossil Case and quest log) / {PLAYER} / SAVE / OPTIONS | S |
| Region map | Replace Hoenn with a West map (MT/WY/CO/SD/NE) showing the act sites; one image, palette-swapped per era | M (art) |
| Quest log | `FIELD LOG` lists the current objective from `VAR_STRATA_STORY` + `VAR_STRATA_SUBPLOT` (table of strings in `strata_acts.c`) | S |
| Split `maps.py` and the roster for parallel work | `maps.py` → package `tools/strata/maps/` (`act0_present.py … act8_ice_age.py`, `epilogue.py`, `common.py`, aggregated in `__init__.py`); roster → package `tools/strata/roster/` with append-only `part3.py` (**done, R0**) | S (do it first) |
| Saves | New vars: `VAR_STRATA_SUBPLOT`, `VAR_STRATA_FIELDKIT`, `VAR_STRATA_STIPEND_COUNT`; flags: waders, fossils (87), tips, set pieces (~20), Colby | S |

---

## 4. Graphics and audio plan

### 4.1 Inventory

| Asset | Count | GBA constraint | Current | Priority |
|---|---|---|---|---|
| Creature front sprite | 87 (70 + 17) | 64×64, 4bpp, 15 colours + transparent; optional 2-frame anim (64×128) | borrowed stock | **1** |
| Creature back sprite | 87 | 64×64, same palette as the front | borrowed | 1 |
| Shiny palette | 87 | 16 colours | borrowed | 4: generate as a "pigment variant" (a script hue/value shift; labelled a reconstruction choice in the Codex) |
| Icon | 87 | 32×32 ×2 frames, one of the 6 shared icon palettes | borrowed | 2 |
| Footprint | 87 | 16×16 1bpp | borrowed | 5: blank, or real track shapes for the dinosaurs only |
| Overworld creature sprite (set pieces) | ~20 | 32×32 or 64×64 objects | none | 3 |
| Overworld tilesets per era | 9 eras | 4bpp tiles, 16-colour palettes, metatiles (primary + secondary) | palette swaps (winter, petm, oligocene, ice_age) | 2 (palettes) / 4 (new tiles) |
| New era palettes | Paleocene humid, Eocene lush, Ashfall clear + ash, late-glacial, present prairie | via `gen_tilesets.py` | missing | **1** (cheap) |
| Battle backgrounds per era | ~6 environments × 9 eras | tiles + tilemap + palette | stock | **1** for the palettes (the same transforms as `gen_tilesets.py`), 4 for new art |
| Tall-grass field-effect palette | 1 per era | sprite palette | stock | 1 |
| NPC overworld sprites | 8 cast + 8 researchers | 16×32 / 32×32 | stock reuse | 3 |
| Trainer battle pics | ~10 | 64×64 | stock reuse | 4 |
| Player sprite in field gear | 2 genders | OW + back pic | stock | 4 |
| Item icons | ~15 (field kit, waders, forage ×7, fossil case, capsules) | 24×24 4bpp | stock | 3 |
| UI | Codex pages, rig forecast window, lineage chart labels, region map, popup | BG tiles | stock | 2 |
| Title | done (`gen_title.py`) | none | done | none |
| Cries | 87 | direct-sound samples | borrowed stock | 5: keep borrowed. Later: procedural cries via a script; archosaurs get closed-mouth "booms", which is a speculative hypothesis and labelled so ⚠ |
| Music | per era | m4a | Hoenn tracks | 5: keep. Retag per era for mood |

### 4.2 Production approach

1. **Palettes before pixels.** Every era-identity win that is palette-only (tilesets, battle
   BGs, grass overlay, a region-map tint) comes first: script-generated, deterministic,
   reviewable.
2. **Creature art in tiers.**
   - *Tier A (procedural "reconstruction plates"):* a script, `tools/strata/gen_sprite.py`
     (NEW), that rasterises a small per-species body-plan spec (ellipses and capsules for
     torso/neck/head/limbs/tail, on templates: quadruped, theropod, bird, turtle, fish, ray, bat,
     proboscidean). It draws at 4× resolution, downsamples, outlines in 1 px, quantises to a 15-colour
     palette with the colour (`color` field) as the base hue, and writes indexed PNG + `.pal`
     in the expansion's layout. The result is honest, consistent, uncertainty-friendly placeholder art
     with no stock-IP dependency. Expect "museum silhouette" quality.
   - *Tier B (hand pixel art):* replaces Tier A in priority order: starters (16) → bosses (8)
     → most common wilds per act (~24) → the rest. Budget ~3 h per species (front, back,
     icon) for a competent pixel artist, about 260 h total. Commission or volunteer. Track
     licences in `CREDITS.md`.
   - Do **not** downscale paleoart unless it is CC0, or CC BY with attribution, and has been
     checked for scientific currency. Old public-domain art (e.g. tail-dragging dinosaurs)
     goes in museum *field notes* about outdated science, not in sprites.
3. **Tiles:** new metatiles only where palettes can't lie: palms/cycads/ferns (Acts 1–5),
   **banded badland cliffs** (Acts 0, 4, 6: the visual motif of the game), ash drifts,
   sagebrush, snow steppe.

### 4.3 Pilot (do next; two S–M tasks, parallelisable)

**Pilot P1, "one creature, end to end":** write `gen_sprite.py` with the *fish* and
*quadruped* templates. Generate **Knightia** (simplest outline; the in-battle back view
is the same side profile mirrored) and **Mesodma** (small quadruped). Produce front, back, icon
(2 frames) and a normal + pigment-variant palette. Wire both into `gen_species.py` with a new
roster field `art="generated"`, which takes precedence over `borrow`. Acceptance: the build
passes; the sprites validate (≤16 colours, 64×64, transparent index 0); a screenshot in battle and
on the party screen.

**Pilot P2, "one era battle background":** extend `gen_tilesets.py` with a
`battle_bg` mode that applies the existing `impact_winter` transform to the stock
grass, long-grass, water and sand battle-environment palettes. Select them when
`VAR_STRATA_ERA == ERA_IMPACT_WINTER` (hook: the battle environment / palette load in
`battle_bg.c`). Then do the tall-grass overlay palette the same way. Acceptance: a screenshot
pair, Hell Creek vs the Ashen Levee battle.

**Status: both pilots are done.** The pipeline, how to add a creature, and the lessons are in
[`strata_art.md`](strata_art.md). Two things differ from the plan above:
(1) Generated art opts out of borrowing through a `CUSTOM` marker file in the
species' graphics folder, written by `gen_sprite.py`, instead of a roster `art=` field.
The marker also carries the measured pic sizes and offsets and the icon palette.
(2) Era art is chosen by the *current map's* era (`sStrataMapEras`), not `VAR_STRATA_ERA`.
It covers all four transformed eras (winter, PETM, Oligocene, ice age) and 9 outdoor
battle environments, plus the shared grass/ripple field-effect palette. The previews
are rendered offline (`--preview`), not taken from emulator screenshots.

---

## 5. Scientific integrity: fact-check list

Ranked by risk: **High** = a likely error in shipped text/data, or central to an act; **Medium** =
plausible but unverified co-occurrence or timing; **Low** = wording.

| # | Risk | Claim (where) | Concern | Action |
|---|---|---|---|---|
| H1 | High | Act 3 = "Denver Fm, 65.7 Ma", "~300 kyr" (`strata_acts.c`, design doc), while the boss *Eoconodon* and *Taeniolabis* are listed ~65.4 Ma (roster) | Corral Bluffs reporting puts *Taeniolabis* (with the oldest legumes) ~700 kyr post-impact; *Eoconodon* is in the same study | Relabel Act 3 to ~65.4 Ma, or say the window spans ~300–700 kyr. Check Lyson et al. 2019 (*Science*). **Layer name, roster, maps and design doc relabelled 65.7–65.4 Ma (R7)**; mentor and boss lines still say 300,000 years |
| H2 | High | *Ovibos* wild on the present-day Montana prairie (`maps.py`) | Musk oxen don't live in Montana today | Remove it from the epilogue tables. **Done (R7)**: still wild on the Ice Age Steppe |
| H3 | High | *Gallinuloides* wild at Ashfall, 11.9 Ma (`maps.py`); it's a ~52 Ma Green River bird | ~40 Myr anachronism. It's only there as a stasis placeholder | Remove it from the Act 7 wild table; keep it as a lineage only. Add a `first_era`/`last_era` test. **Removed (R7)**; **test done (C1)**: roster `first_era`/`last_era` → `sStrataSpeciesEras`, checked against every encounter table (Gallinuloid `last_era` = Green River) |
| H4 | High | Teilhardina → Notharctus descent (`lineages.h`) | *Teilhardina* is omomyiform-grade; *Notharctus* is an adapiform: different primate groups | Descend to *Omomys* (NEW); Notharctus stays a wild species. **Done (C1/F8)**: Teilhardina → Omomys at the Act 5 load; Omomys dies at the Act 6 load |
| H5 | High | *Aenocyon dirus* at Natural Trap Cave (roster site, steppe table) | Summaries of the cave's fauna list a Beringian-type wolf, not the dire wolf | Verify against the primary NTC faunal lists. If absent, change the site to another Wyoming/region locality and keep it regionally |
| H6 | High | Ischyromys dex: "Rodents spread just as the last multituberculates vanished, and may have outcompeted them" | Rodents arrived in NA around the PETM, ~20 Myr before the last multis; competitive replacement is debated | Rewrite; *Paramys* (NEW) carries the arrival story. **Dex rewritten (R7)** |
| H7 | High | PETM vs today's carbon-release rate (planned Act 4 line) | Needs a citable figure (e.g. "~10× faster today") | Cite before shipping (Zeebe et al. 2016 is the usual source) |
| M1 | Med | *Protictis* wild in the PETM Willwood (Act 4 table) | *Protictis* is mainly a mid/late Paleocene genus; Willwood viverravids are *Didymictis*, *Viverravus* | Remove it from Act 4 (done in §2.5). Keep it as the dog-line stand-in, labelled. **Done (R7)**: still wild in Act 3 |
| M2 | Med | *Mesodma* in the PETM and at Green River (Acts 4–5) | Last appearance of *Mesodma* specifically (vs *Ectypodus*) | Check PBDB; if needed, show it as "multituberculate (Mesodma-grade)" |
| M3 | Med | *Champsosaurus* at Green River ~50 Ma (Act 5 water) | Eocene champsosaurs are known mostly from the high Arctic; Wyoming Eocene uncertain | Check, or drop it from Act 5 |
| M4 | Med | *Coryphodon* at Green River/Bridger ~50–46 Ma | Mostly a Wasatchian (~55–50 Ma) genus | Keep in Fossil Lake only if it fits the dates |
| M5 | Med | Map named "Lake Gosiute shore" with Fossil Lake fauna (Knightia, Heliobatis, Onychonycteris) | They're mostly Fossil Butte (Fossil Lake) | Split the maps (§2.6) |
| M6 | Med | Natural Trap Cave co-occurrence: *Mammuthus columbi*, *Ovibos*, *Camelops* (site "Wyoming"), *Meleagris*, *Panthera atrox* | Some summaries list mammoth, musk-ox, camels and lions; species-level identities need checking | Verify each at species level; set `site` to the true locality |
| M7 | Med | Subhyracodon → Teleoceras presented as a descent | *Teleoceras* is a teleoceratine, likely an Old World immigrant, not a descendant of *Subhyracodon* | Codex: "rhino grade, not a direct ancestor" |
| M8 | Med | Dog chain Cimolestes → Protictis → Miacis → Hesperocyon → Leptocyon/Epicyon | Each step is a grade, not an ancestor; Hesperocyon, Borophaginae and Caninae are sister subfamilies | Make sure every Codex entry says "stand-in / grade" (rule §8.2 of the design doc) |
| M9 | Med | All NEW Act 7 species at Ashfall specifically (Aphelops, Cormohipparion, Hypohippus, Cosoryx, Macrochelys) and Douglassciurus timing | Locality and age unverified | Verify before adding to the roster; fall back to "Great Plains, ~12 Ma" sites. **C1:** Aphelops and Cormohipparion kept at "Ashfall, NE"; Hypohippus, Cosoryx and Macrochelys use "Miocene Great Plains, NE"; Douglassciurus is Chadron Fm, ~36 Ma (`notes` say so). Primary-source check still open |
| M10 | Med | Tanis / "the first hour after impact" (if anyone writes Act 1 impact text) | Contested site and data | Don't depend on it; describe ejecta reentry generically |
| M11 | Med | Montana fossil ownership ("belong to the surface owner"), and PRPA 2009 on BLM land | Legal claims in dialogue | Phrase them generally; check the current state law and PRPA wording |
| M12 | Med | Black-footed ferret rediscovery (Meeteetse, WY, 1981) and swift fox / ferret reintroductions in Montana | Dates and places in the epilogue text | Check with USFWS / state sources |
| L1 | Low | "Ash from 1,600 km away; Bruneau–Jarbidge; supereruption" | Distance and source fine; "supereruption" magnitude wording | Say "massive eruption" unless a VEI-8 source is cited |
| L2 | Low | Mentor: "In 300,000 years the biggest mammals tripled in size" | Exact multiples from Lyson et al. | Check the figure |
| L3 | Low | Onychonycteris "probably could not echolocate" | Debated since 2008 | Add "debated". **Done (R7)** |
| L4 | Low | Masses: Triceratops 9 t, T. rex 8 t, Arctodus 900 kg, Uintatherium 2 t | Upper-range picks | Fine; show ranges in the Codex |
| L5 | Low | Design doc multituberculate chain "Mesodma → Taeniolabis → Ptilodus" | Not ancestral; Ptilodus is mid-Paleocene | Fix the design doc wording |
| L6 | Low | "Time-averaging window" values (§3.9) | New text | Check per act |
| L7 | Low | The Act 8 Colby site (~13 ka, Clovis mammoth kill, Worland WY) | Age and interpretation ("kill" vs scavenging debated) | Word it as "mammoth bones with Clovis tools" |

Process: one research agent works through this table using the Paleobiology Database and primary
papers, and writes results into the roster `notes` / `site` / `age` fields. It runs **in parallel
from day one**. Content agents treat any ⚠ species as provisional.

---

## 6. Roadmap

Ordered by leverage ÷ risk. Tasks inside a milestone can run in parallel unless the
**Deps** column says otherwise. "Track" suggests agent assignment: **SYS** (C systems),
**CON** (maps/scripts content), **ART**, **SCI** (fact-check), **TXT** (text/UI).

### M0: Fix the loop (do first; mostly S, high leverage, low risk)

| ID | Task | Size | Deps | Track |
|---|---|---|---|---|
| R0 | Split `maps.py` into per-act modules, and the roster part 3 file (unlocks parallel content work) | S | none | CON |
| R1 | Per-option `minScore` in descents; knockout pressure only for `diet` carnivore/omnivore, +1, capped at 24/era; tests | S | none | SYS |
| R2 | Waders (surf without badge/HM) + Fishing Kit (Old→Good Rod) + shoreline counts as WATER; tests | M | none | SYS |
| R3 | ✅ **Done.** Forage items (7) with heal + pressure (`Selection_EatForage`), `forage(x, y, item)` placement helper in `maps/common.py` (hidden items under `FLAG_TEMP_11..1F`, era-checked), 1–3 spots per deep-time map; tests | M | R0 | SYS + CON |
| R4 | ✅ **Done.** `habitat=` and `light=` per map in `maps/`, generated into `sStrataMapInfo` (`strata_map_eras.h`, `src/strata_map.c`); Petalburg placeholder removed; every map tagged (table in design doc §7.2) | S | R0 | SYS |
| R5 | ✅ **Done.** BST formula compression + `focal` bonus in `gen_species.py`; regenerate; update tests; `balance.py` (lineage resilience, §3.2 part 3, is F7) | S | none | SYS |
| R6 | Era level floor at the §3.1 values (verify the in-flight work matches; fallback survivor at the floor) | S | (in flight) | SYS |
| R7 | ✅ **Done** (data/text). Drop Ovibos (prairie), Gallinuloid (Ashfall), Protictis (Act 4); relabel Act 3 age; rewrite the Ischyromys dex. Left for owners of other files: H4 descent (done in C1/F8), the "300,000 years" lines in `sMentorLines` and the Palm Forest boss text, H5 site check, H7 citation | S | none | CON + SCI |
| R8 | Text pass: start menu, PC names, whiteout, dex rating, battle "POKéMON" → reconstruction terms; grep audit of `src/strings.c`, `battle_message.c`, `data/text/*` | M | none | TXT |
| R9 | PC + Move Relearner + healing cot in the Field Station; `I_EXP_SHARE_FLAG`; camp store | S | none | CON |
| R10 | T. rex survival rule (running = done) + mentor variant; boss smart-AI var + totem boosts on all bosses | S | none | CON |

### M1: Make the systems legible

| ID | Task | Size | Deps | Track |
|---|---|---|---|---|
| F1 | Rig forecast special + list menu before `RIG_NEXT` | M | R1 | SYS |
| F2 | Pressure chart (relabelled condition graph) from the party menu, with branch hints | M | R1 | SYS |
| F3 | Descent scene via the evolution scene for party mons | M | none | SYS |
| F4 | Extinction list message + Fossil Case + fossil flags | M | none | SYS |
| F5 | Map popup age/window line. Hook: add an `age=` string key per map and a `const u8 *age` field to `struct StrataMapInfo` (`include/strata_map.h`, written by `write_map_info` in `gen_maps.py`), then print it in `map_name_popup.c` | S | R4 | SYS |
| F6 | ✅ **Done** with R4. `light=` overrides the clock in `UpdateTimeOfDay`; `none` turns tinting off (`MapHasNaturalLight`) | S | R4 | SYS |
| F7 | Lineage resilience (IV raise per era survived) | S | none | SYS |
| F8 | ✅ **Done.** Lineage table additions/changes from §2.11 (data only; needs the new species), new extinctions, H4; tests | S | C1 | SYS |

### M2: Content (parallel by act once R0 lands)

| ID | Task | Size | Deps | Track |
|---|---|---|---|---|
| C1 | ✅ **Done.** Add the 17 species (roster part 3, borrow placeholders, dex text, `diet`, `focal`, `first_era`) + `first_era` test. `diet` now generates `strata_diets.h`; `last_era` added for stand-ins. Encounter placement is left to C3–C10/C12 (suggestions in §2.12) | M | R0, SCI checks for ⚠ entries | CON + SCI |
| C2 | ✅ **Done.** Act 0 hub: Jordan (+ store, café, BLM office), Lindqvist Ranch, Sand Arroyo; cast NPCs; tutorial dig. Camp → ranch → Jordan by connections; Jordan's west highway now gates the epilogue prairie (was the camp's west road). The dig runs *after* the starter choice (Halvorsen sends you to Dale), so the new-game flow is unchanged. Hooks: `FLAG_STRATA_DIG_*`, `FLAG_STRATA_BLM_PERMIT` (Ortiz, after Act 2; opens the arroyo), `FLAG_STRATA_SAW_PAIR`, `FLAG_STRATA_MET_KESSLER`; Kessler at the ranch until Act 1 is done. Left for others: Theo's peer review #0 (C13), the truck arrival, Ortiz's evidence scene at the pit (S1) | L | R0, R9 | CON |
| C3–C10 | Acts 1–8: new maps per §2, field notes, forage, set pieces, boss restaging. **One agent per act, 8 in parallel.** ✅ **C3 (Act 1) and C4 (Act 2) done**: Fern Glade and Burrow Refuge added (the Bluff Top stays part of the River Channel), Avisaurus and Emarginachel placed, Acheroraptor pair set piece, T. rex Lv 14 plus ejecta and rig pull-out, gauntlet 14/15/17 across the whole swamp width. ✅ **C10 (Act 8) done**: Meltwater River, Ice Margin and the Colby coda site added; Panthera pair (double 48/48) on the steppe, Aenocyon dropped from the wild table, Lepisosteus left out of the Meltwater tables (no Pleistocene Wyoming record), field notes and forage on all maps; the Colby sub-layer opens from a marker by the steppe anchor and sets `FLAG_STRATA_COLBY_SEEN` (the "Today" gate itself is S3) | M each | R0, R3, R4, C1 (for acts using new species) | CON |
| C7 | ✅ **Done** (Act 5, `act5_green_river.py`). Four maps: Bridger Shore (the old map, boss on its beach; the *Uintatherium* bull now charges in along the shore), Fossil Lake (Route 103; mass-mortality scene, a labelled hypothesis), Bridger Forest (Route 116; *Omomys*, *Paramys*, *Notharctus*), Oil-Shale Cliffs (Route 115 canyon; *Patriofelis* set piece Lv 32). *Hyrachyus* on the shore. Champsosaur dropped from Act 5 (M3). 13 field notes, 20 forage spots | M | R0, R3, R4, C1 | CON |
| C6 | ✅ **Done (Act 4).** Bighorn PETM: Red Beds + Polecat Bench, Willwood Swamp, Clarks Fork Crossing (ring of 4 maps, `act4_bighorn.py`); 19 forage spots, 12 field notes, *Paramys* and *Oxyaena* placed; *Oxyaena* set piece at the Clarks Fork gravel bar; Coryphodon boss as a wild double with a calf (single-mon fallback); fishing kit becomes the Good kit after the boss; H7 rate figure in a Polecat Bench sign. Flags `FLAG_STRATA_ACT4_*`, `VAR_STRATA_ACT4` | M | R0, R3, R4, C1 | CON |
| C11 | Act 7 pre-ash / ash map pairs (palette + warp swap after the boss) | M | C9, palettes (A1) | CON |
| C12 | Epilogue maps + Interpretive Center + Hall of Lost Lineages | M | F4 | CON |
| C13 | Peer-review trainers (8 researchers + Theo ×4 + Halvorsen) and the stipend special | M | R8 | CON + SYS |
| C14 | Codex pages (Evidence, Lineage via the HGSS evolution page) + weight widening | L | F8 | SYS |

### M3: Story

| ID | Task | Size | Deps | Track |
|---|---|---|---|---|
| S1 | `VAR_STRATA_SUBPLOT` + quest log strings + all camp interludes (§1.5) | L | C2, C13 | CON + TXT |
| S2 | Halvorsen lines rewritten per story × subplot (extend `sMentorLines`) | M | S1 | TXT |
| S3 | Act 8 Colby coda + epilogue ending + credits up the column (lineage fates from the fossil flags) | M | C10, C12, F4 | CON |
| S4 | Gentle Deep Time option | S | F4 | SYS |

### M4: Art (starts in parallel with M0)

| ID | Task | Size | Deps | Track |
|---|---|---|---|---|
| A1 | Era palettes: Paleocene, Eocene, Ashfall clear/ash, late-glacial, prairie (`gen_tilesets.py`) | S | none | ART |
| A2 | **Pilot P2:** battle BG + tall-grass overlay palettes per era | M | none | ART + SYS |
| A3 | **Pilot P1:** `gen_sprite.py` + Knightia + Mesodma, end to end | M | none | ART |
| A4 | Tier A procedural sprites for all 87 (templates for the rest) | L | A3 | ART |
| A5 | Tier B hand art, by priority (starters → bosses → commons) | L (ongoing) | A3 format | ART |
| A6 | Banded-cliff and palm/fern metatiles | L | A1 | ART |
| A7 | Region map of the West; Codex/rig UI frames; item icons | M | none | ART |

### M5: Science and balance (continuous)

| ID | Task | Size | Deps | Track |
|---|---|---|---|---|
| Q1 | Work through the §5 table; update roster sites/ages/notes | L | none | SCI |
| Q2 | Balance pass: `balance.py` report per act + a full playtest on each starter | M | M2 | SYS |
| Q3 | Codex text review: every stand-in labelled, every inference tagged | M | Q1, C14 | SCI + TXT |

### Top 8, in order

1. **R1** Descent thresholds and diet-aware knockout pressure (fixes the broken dog branch)
2. **R2** Waders, fishing kit and shoreline water (revives all the water content and the water branch)
3. **R5** BST compression + focal bonus + `balance.py`
4. **R0** Split `maps.py` and the roster (unblocks 8 parallel content agents)
5. **R7** High-risk data fixes (Ovibos, Gallinuloid, Protictis, Act 3 age, Ischyromys)
6. **R3 + R4** Forage items, habitat and light tags (gives PLANT a source and forest maps a tag)
7. **F1** Rig forecast (the single biggest player-comprehension win)
8. **A2 / A3** Art pilots (battle BG palettes; one generated creature end to end)

Parallel lanes from day one: SYS (R1, R2, R5), CON (R0, then R7, R9, R10), TXT (R8), ART (A1–A3),
SCI (Q1). Merge rule: generated files (`strata_families.h`, layouts, `strata_map_eras.h`) are
regenerated after each merge and never hand-merged.
