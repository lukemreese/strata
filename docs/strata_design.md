# Strata: Game Design Document (draft v0.1)

> Working title. A science-grounded romhack of pokeemerald-expansion set in the
> North American West, running from the last days of the dinosaurs to the present.
> Every creature is a real, fossil-documented animal.

---

## 0. Vocabulary

The creatures are **never called "Pokémon"** anywhere the player can see. Strata's words are
animals, specimens, lineages, reconstructions and the Codex. These are the terms the game
text uses (the first pass over stock text was done with `tools/strata/terms.py`):

| Stock term | Strata term | Where it shows |
|---|---|---|
| POKéMON (the creature) | **ANIMAL** in menu labels (`ANIMAL INFO`, `WITHDRAW ANIMAL`), **animal / animals** in prose; in battle it is the creature's own name | summary screen, storage, party prompts, item and move text, field messages |
| the party ("POKéMON" in the start menu) | **TEAM** | start menu, battle command menu (`Battle Bag Team Run`), "the TEAM LIST" |
| POKéDEX | **CODEX** | start menu, search help, FIELD CARD |
| Poké Ball | **Specimen Capsule** (item name), "capsule" in prose | bag, shop, battle messages |
| Great / Ultra / Master / ... Ball | Great / Ultra / Master / ... **Capsule** | bag, shop |
| POKé BALLS pocket | **CAPSULES** | bag pocket header |
| POKéMON CENTER | **FIELD STATION** | heal sign, nurse text, region map |
| POKé MART | **CAMP STORE** | sign, healing text |
| TRAINER (opponent class) | **RESEARCHER** (class name; the fight is a peer review) | battle intro |
| PC / BILL'S PC | **STATION PC** (done earlier) | PC menu |
| TRAINER CARD | **FIELD CARD** (done earlier) | start menu |
| POKéNAV | **FIELD LOG** | start menu (not shown in Strata) |
| species category "Cimolestid POKéMON" | **Cimolestid**, no suffix | Codex entry, starter label |
| Poké Flute / Poké Doll / Poké Toy / Poké Radar | Bone Flute / Decoy Doll / Decoy Toy / Field Radar | items |
| HOENN, badges | THE WEST, act (done earlier) | region, story |

Style: ALL CAPS only for menu labels and proper nouns the stock text already capitalised
(CODEX, TEAM, FIELD STATION, CAMP STORE, CAPSULES); sentences use lower case ("an animal",
"wild animals"). Keep the original line breaks and box widths: `animal` is shorter than
`Pokémon`, so a rewrite never needs more room. `test/text.c` checks item names and
descriptions and every battle string against the real box widths.

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
- The stock dex becomes the **Field Codex**. Each entry gives the real fossil site,
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
| Hell Creek Camp | present | Route 111 north | Hub; field station door at (26, 18); Theo (four peer reviews), Josie, Marge's store, the ornithologist and mammalogist (visiting researchers); ranch road west to the Lindqvist Ranch |
| Field Station | present | Birch's lab | STRATA rig at (10–11, 7); mentor Dr. Halvorsen; respawn point; PC, cot, relearner Wren, rig-rules notes; interludes 1, 4, 5, 9 (S1) on the trigger row y 10, visitors (Kessler, Theo, Josie) just inside the door |
| Hell Creek Badlands | present | Route 111 desert | K-Pg boundary clay; Dale's tutorial dig (3 survey stakes, `FLAG_STRATA_DIG_*`); BLM boundary on the south edge (needs `FLAG_STRATA_BLM_PERMIT`); no encounters |
| Sand Arroyo | present | Route 111 desert rows 74–100 (joins the badlands) | BLM land: the poached pit, a broken jacket, spoil and tire tracks; Ortiz's evidence scene after act 5 (S1: three records, `FLAG_STRATA_STORY_EVIDENCE_*`) |
| Lindqvist Ranch | present | Route 117 | Bea; Kessler and a crew hand (until Act 1 is done, and on auction day); the Pair under a tarp (`FLAG_STRATA_SAW_PAIR`); interludes 2, 7, 10 (S1) play on arrival, their cast by the road from camp |
| Jordan | present | Fallarbor Town (tent and healing building removed) | General store (Mart), café (House 2, heals), BLM field office (Lanette's house; Ranger Ortiz gives the permit after Act 2, interlude 3); the citation (interlude 8) on the street on arrival after Act 7; the highway west leads to the prairie in the epilogue |
| Levee Forest | 66.04 Ma | Route 119 south | Arrival point; south edge returns to camp; east side opens into the Fern Glade; 3 field notes; *Avisaurus* at the forest edge |
| River Channel | 66.04 Ma | Route 119 middle | The tyrannosaur waits on the bluff (survival set piece); the ejecta streaks end the act and the rig pulls you out |
| Backswamp | 66.04 Ma | Route 120 marsh | Gar, champsosaurs, crocodylians, *Emarginachelys*; field notes on the detritus food web |
| Fern Glade | 66.04 Ma | Route 120 open grassland (east of the cliff) | Open habitat east of the Levee: Edmontosaurus herd, *Avisaurus*, the *Acheroraptor* pair ambush (wild double Lv 8/8, once); notes on perching vs ground birds |
| Ashen Levee / River / Swamp | 66.04 Ma + ~1 yr | Same layouts, `*_winter` palettes | Impact winter: survivors only; survival gauntlet in the swamp (the trigger line spans the swamp's whole width) |
| Burrow Refuge | 66.04 Ma + ~1 yr | Island Cave, top chamber | Mouth is a rock mound in the Ashen Levee; *Mesodma*/*Cimolestes*; seed cache (browse item balls), notes on burrowers |
| Palm Forest | ~65.7–65.4 Ma | Petalburg Woods | Act 3 arrival and hub (palms, ~300 kyr after the impact); exits up (creek), left (thicket), right (bluffs) |
| Legume Thicket | ~65.4 Ma | Route 120 (thicket and marsh) | Act 3; oldest legumes (~700 kyr); *Eoconodon* boss (Lv 22) at its carcass in the north marsh |
| Concretion Bluffs | ~65.4 Ma | Route 116 | Act 3; *Taeniolabis* mini-boss (Lv 20), three crackable concretions (`VAR_STRATA_ACT3`) |
| Front Range Creek | ~65.5 Ma | Route 119 upper river | Act 3; water map (waders, fishing), notes on the rising Rockies |
| Red Beds | ~56 Ma | Route 114 north, `*_petm` palettes, drought | Act 4 (40×34), arrival; field notes (red soils, heat, dwarfing, land bridges); *Coryphodon* boss (Lv 28 + calf Lv 24, wild double) on the land bridge; east → Polecat Bench, south (the bridge) → Willwood Swamp |
| Bridger Shore (`StrataLakeForest`) | ~50 Ma | Route 104, whole | Act 5 arrival; Lake Gosiute shore. Gaps open the north shore (to Fossil Lake) and the east forest (to Bridger Forest). *Uintatherium* boss (Lv 34): a bull charges along the beach when the player crosses the boss line (y 61) |
| Fossil Lake | ~52 Ma | Route 103 west half | Act 5; Fossil Butte lagerstätte, water map. Mass-mortality scene (labelled hypothesis) on the east shore; field notes on fish, the oldest bats, shorebirds |
| Bridger Forest | ~50–47 Ma | Route 116 west half, trees planted | Act 5; canopy primates (*Omomys*, *Notharctus*), *Paramys*; plant forage |
| Oil-Shale Cliffs | ~50 Ma | Route 115 canyon below the ridge | Act 5; varve and kerogen notes; *Patriofelis* set piece (Lv 32, one-time) on the sand path |
| Polecat Bench | ~56 Ma | Route 113 (x 52–100), `*_petm` palettes, drought | Act 4 (48×18); open ash flats: *Paramys*, *Sifrhippus*; notes on the carbon isotope excursion, immigrants, and the release rate (H7); south → Clarks Fork |
| Willwood Swamp | ~56 Ma | Route 114 south basin (rows 34–64), two ponds drawn with the route's own pond tiles, `*_petm` palettes | Act 4 (40×30); *Coryphodon*, *Borealosuch*, *Champsosaur*, rare *Oxyaena*; larvae forage; notes on wallowers, leaf damage, warm-water reptiles; north → the land bridge, east cut → Clarks Fork |
| Clarks Fork Crossing | ~56 Ma | Route 115 (rows 44–74), sea as the river, `*_petm` palettes | Act 4 (40×30); a gravel-bar ford (patched across the river) with the *Oxyaena* set piece (Lv 26); *Gastornis*; trees give the forest pressure; north → Polecat Bench, west (the ford) → Willwood Swamp |
| Lake Gosiute shore | ~50 Ma | Route 104 | Act 5; *Uintatherium* boss (Lv 34) across the south shore |
| White River badlands | ~33 Ma | Route 114 south, `*_oligocene` palettes | Act 6 arrival valley; north edge joins the Gallery Forest; *Archaeotherium* boss (Lv 40) on the stash plateau (hell-pig object plus the stair triggers); 4 carrion forage spots at the stash; 3 field notes; *Palaeolagus* (common) |
| Grassland / Grassland (ash) | ~11.9 Ma | Route 113 (x 15-69), `*_oligocene` palettes before the ash, stock ash tiles after | Act 7 arrival; the haze on the horizon (once); grazers; connects east to the Waterhole, north to the Niobrara River, south to the Savanna Woodland; field notes on teeth, seeds, cranes, ash depth, order of death |
| Waterhole / Waterhole (ash) | ~11.9 Ma | Route 113 east end (x 70-99), the south plateau cut into a pond | Act 7 boss: *Teleoceras* bull + cow (wild double Lv 46/42); the ashfall starts in the intro text and the win fades into the ash version ("rhino barn" notes) |
| Savanna Woodland / (ash) | ~11.9 Ma | Route 114 meadow, trees added | Act 7; *Hypohippus* (browser), the *Epicyon* mini-boss (Lv 44, once) at a carcass; ash version: scavengers |
| Niobrara River / (ash) | ~11.9 Ma | Route 114 north lake (bridge made a gravel bar, tall grass on the banks) | Act 7; *Aphelops*, *Teleoceras*, *Macrochelys* and *Lepisosteus* (surf and fishing); notes on rhinos, turtles, river-laid ash |
| Gallery Forest | ~33 Ma | Route 114 north (joins White River at offset 0), `*_oligocene` palettes | Act 6; forest strips along a river and lake (plank bridge replaced by a sandbar, house and berry plots removed); *Douglassciurus*, Mesohippus, Leptomeryx, Hesperocyon, gars in the water; the horse forest branch is steered here (forest habitat); 3 field notes |
| Badlands Wall | ~33 Ma | Route 113 left half, `*_oligocene` palettes | Act 6; open red-soil flats under a banded cliff, with the Chadron / Brule contact note; oreodont herd (flavour objects), *Palaeolagus* (common), Stylemys, Merycoidodon; ash grass swapped for tall grass; east edge joins the Trackways at offset 0 |
| Toadstool Trackways | ~33 Ma | Route 113 right half, `*_oligocene` palettes | Act 6; floodplain with trackway notes; *Hyaenodon* mini-boss (Lv 38, once, line of sight at x = 10; rare wild 35-38) with a carrion reward; Subhyracodon, Poebrothere |
| Ashfall grassland | ~11.9 Ma | Route 113, volcanic ash | Act 7; *Teleoceras* bull (Lv 46) at the waterhole |
| Ice Age Steppe | ~20 ka | Route 118, `*_ice_age` palettes, snow | Act 8 hub (80x20): arrival and anchor; the *Panthera* pair set piece (wild double Lv 48/48, once, in the only corridor to the sinkhole); 4 field notes; the sinkhole drops into the trap cave; Meltwater River east, Ice Margin north; the sub-layer marker by the anchor opens Colby once the boss is done |
| Natural Trap Cave | ~20 ka | Granite Cave 1F | Act 8; *Arctodus* boss (Lv 52); 3 field notes; a rope climbs back out |
| Meltwater River | ~20 ka | Route 118 west half, `*_ice_age` palettes, snow, sand-bar ford patched across the channel | Act 8; braided outwash, water habitat; *Chelydra* stand-in (surf and fishing), glacial-edge grazers on land; 3 field notes |
| Ice Margin | ~20 ka | Route 111 desert rows 60-83, `*_ice_age` palettes, snow | Act 8; open habitat; *Ovibos*, *Mammuthus*, *Panthera*, *Ovis*; the ice, sea-level and mixed-bone-bed notes. Not a Laurentide front (that was hundreds of km north): mountain glaciers, drawn close |
| Colby Site | ~13 ka | Route 118 east crop, `*_ice_age` palettes, no snow | Act 8 coda (same era, a late-glacial sub-layer reached by a marker, not a connection); no encounters; mammoth bone pile (the meat-cache reading, flagged as debated) and a Clovis point (the stock fossil stone; reading it sets `FLAG_STRATA_COLBY_SEEN`, which the rig needs before "Today", §7.9); an evidence-for-and-against note |
| Montana Prairie | today | Route 102 | Epilogue; open once the present layer is loaded, via the highway west of Jordan. Prairie-dog town and a one-time black-footed ferret encounter (`FLAG_STRATA_EPI_FERRET_MET`), swift fox, sage-grouse, bison, pronghorn; 4 field notes; the Interpretive Center is the building in the east half (door warp); east edge opens to the Breaks, south edge to the Pryor Mountains |
| Missouri Breaks | today | Route 114 top (river, badlands ground; house, berry plots and bridge removed) | Epilogue; water habitat: *Chelydra*, *Lepisosteus*, *Ovis*, *Meleagris*; 3 field notes (the same Hell Creek rock eroding today) |
| Pryor Mountains | today | Route 112 south (red limestone plateau, stairs, lowland) | Epilogue, optional; feral *Equus* (3 visible horses), pronghorn, *Ovis*, sage-grouse; 3 field notes |
| Interpretive Center | today | Lilycove Museum 1F | Epilogue; the Pair in the round case, paleoart murals of the layers, Halvorsen (the final peer review, Lv 46-52, then the ending lines, the save prompt and the credits, §7.9), Josie, Bea, Dale, Theo; stairs up |
| Hall of Lost Lineages | today | Lilycove Museum 2F | Epilogue; five cases (one plaque per extinction filter: K-Pg, Paleocene recovery, Eocene-Oligocene, Miocene grassland, Ice Age) and two statues (end-Pleistocene; the case not written yet). Generic until F4 adds fossil flags |

The present-day hub sits outside time: returning to camp does not change `VAR_STRATA_ERA`.
The rig only moves up: once a layer is loaded, earlier layers are closed.
Story progress is `VAR_STRATA_STORY`: 0 new game, 1 starter chosen, then for act N
`2N` while in the act and `2N + 1` once its boss is done (`STORY_IN_ACT`,
`STORY_ACT_DONE` in `include/constants/strata.h`); 18 is the epilogue. The rig
(`src/strata_acts.c`) loads the next layer only after the act is done. Each deep-time map has
an anchor sign that returns to the field station.

The present-day subplot is a second var, `VAR_STRATA_SUBPLOT` (0x40DC, `SUBPLOT_*` 0–10 in
`include/constants/strata_act_flags.h`): the last camp interlude played. Interlude N is due once
its act is done (`VAR_STRATA_STORY >= STORY_ACT_DONE(act)`) and the subplot is N − 1; it plays
on its own hub map (`sStoryBeats` in `src/strata_story.c`; the beats, places and triggers are
the "As built" table in outline §1.5). Skipped beats wait in order; none gates the rig. Every
hub map's on-transition script calls `special Strata_StoryPrepareMap` (`VAR_TEMP_2` = the beat
due here, `VAR_TEMP_3` = 1 if any, `VAR_TEMP_4` = the beat due anywhere). The start menu shows
the next objective for every (story, subplot) in a box top left (`Story_QuestLine`).

Dr. Halvorsen's talk depends on both vars: the science of the layer by story (`sMentorLines`,
with the T. rex-fled variant), then the people by subplot: where the next interlude waits, or
what she makes of the last one (`src/strata_acts.c`).

`python3 tools/strata/mapcheck.py` walks every Strata map from its arrival point and
connected edges and reports any trigger, sign or edge the player can't reach on foot.

**Era variants of a map** reuse its layout with palette-only variants of its tilesets
(`tools/strata/gen_tilesets.py`), so the place is recognizably the same while the era
changes. Known gaps: battle backgrounds and the tall-grass overlay sprite keep
their stock colours.

**No gym badges**, so `B_OBEDIENCE_MECHANICS` is GEN_7: the player's own animals
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
at (3, 1) and (4, 1) open the stock PC menu (animal storage, the player's item PC), a
cot at (1..2, 4) heals the party, and the station tech Wren at (9, 3) re-teaches level-up
moves for free (party and PC mons). Dr. Halvorsen still heals on talk. The intro sets
`FLAG_STRATA_EXP_SHARE` (= `I_EXP_SHARE_FLAG`), so the whole party shares experience.
The camp quartermaster (Marge, at (29, 19) in Hell Creek Camp) runs the store: Specimen Capsule
and Potion, plus Great Capsule and Super Potion once act 3 is done and Hyper Potion once
act 6 is done.

### Peer review and the stipend (C13)

Humans battle only in the present day, framed as **peer review**: two people pit their
reconstructions against each other. All present-day trainers are class RESEARCHER and
fight when talked to (no line of sight); each is one battle, no rematches. Their data is
`src/data/trainers_strata.party` (generated into `trainers_strata.h`, included by `src/data.c`
after the stock trainers), their trainer IDs are in `include/constants/opponents.h`.
Because every trainer owns a flag and the flag range is fixed, the 15 Strata trainers reuse
the slots of stock trainers nothing refers to (RED, LEAF, the two placeholders, AMY & LIV 3
and GINA & MIA 2) plus the nine spare ones.

**Teams** use only species that exist by the act just finished (`first_era`), IV 15 (a wild catch's
average), the last four level-up moves, `AI: Basic Trainer`. Levels come from the Q2 balance pass:
the last (strongest) animal at about the level a normal player has after the act's boss (the EXP
model in `balance.py`), the others a level or two below, checked with the headless starter runs
(below, "Balance pass (Q2)"). Pics are stock human trainer pics. `balance.py` prints a
"Peer review" table (each animal's stat total against the expected party median) and flags
`REVIEW OVERTUNED` (an animal over 115% of it, 125% for Halvorsen) and `REVIEW WEAK`.

| Trainer | Where | Unlocks | Team (Lv) | Prize |
|---|---|---|---|---|
| Theo #0 | Hell Creek Camp | starter chosen | the next starter in the cycle mammal, bird, turtle: Asteriornis 4 (vs the mammal), Emarginachel 5, Cimolestes 5 | 160 / 200 |
| ARLO, ornithologist | Hell Creek Camp (22, 8) | act 1 done | Avisaurus 11, Anzu 12, Asteriornis 13 | 624 |
| PRIYA, palynologist | Lindqvist Ranch (33, 8) | act 2 done | Mesodma 15, Champsosaur 16, Emarginachel 17 | 816 |
| TOMAS, mammalogist | Hell Creek Camp (26, 8) | act 3 done | Taeniolabis 18, Loxolophus 19, Protictis 20 | 960 |
| Theo #1 | Hell Creek Camp | act 3 done | Champsosaur 19, Loxolophus 20, Protictis 21 | 840 |
| INGRID, isotope geochemist | Field Station (11, 4) | act 4 done | Sifrhippus 24, Hyopsodus 25, Coryphodon 26 | 1248 |
| KEOLA, ichthyologist | Lindqvist Ranch, stock pond (19, 12) | act 5 done | Knightia 27, Heliobatis 28, Lepisosteus 29, Presbyornis 30 | 1440 |
| OSKAR, ichnologist | Jordan (13, 10) | act 6 done | Stylemys 33, Merycoidodon 34, Mesohippus 35 | 1680 |
| Theo #2 | Hell Creek Camp | act 6 done | Stylemys 32, Leptomeryx 33, Mesohippus 34, Hesperocyon 35 | 1400 |
| HOLLIS, volcanologist | Jordan (3, 13) | act 7 done | Balearica 41, Hypohippus 42, Procamelus 42 | 2016 |
| ASHA, Quaternary ecologist | Lindqvist Ranch (53, 10) | act 8 done | Equus 43, Antilocapra 44, Camelops 45, Ovibos 46 | 2208 |
| Theo #3 | Hell Creek Camp | act 8 done | double battle with Josie's pair: Canis 42, Meleagris 43, Ovis 44, Equus 45 | 3600 |
| Dr. Halvorsen | Interpretive Center | epilogue (`FLAG_STRATA_EPI_PEER_REVIEW_DONE`) | Chelydra 46, Teleoceras 47, Epicyon 48, Uintatherium 49, Arctodus 50, Tyrannosaur 52 | 2912 |

**Unlocking.** Researcher N hides under `FLAG_TEMP_N` until `VAR_STRATA_STORY >= STORY_ACT_DONE(N)`;
every hub map calls `special Strata_HideLockedReviewers` when it loads (`src/strata_review.c`).
Each leaves a field note after the fight (their act's insight) and a one-line reminder
afterwards. Theo offers the earliest review the player hasn't had, so none is missed; his
arc runs from "how do we know that?" to "the model is wrong, but it's useful" (#3, which is
also what he tells the player in the Interpretive Center). Halvorsen asks first (YES/NO)
and sets the flag on a win; the player can come back until then.

**Prizes** are the stock formula: 4 x the last animal's level x the class multiplier
(`gTrainerClasses`: researchers 12, Theo 10, Halvorsen 14; a double battle pays twice).
Against the camp store (Specimen Capsule 200, Great 600, Potion 200, Super 700, Hyper 1500): a
first researcher is worth three capsules, the act 8 one about one and a half Hyper Potions.

**Survey stipend** (the renewable income): talking to Dr. Halvorsen in the Field Station pays
`special Strata_PayStipend`: every Codex "caught" entry since the last payment
(`VAR_STRATA_STIPEND_COUNT`) at **150 + 25 per act finished** (150 at the start, 350 once the Ice
Age is done). The starter doesn't count (`Strata_StipendBaseline` in the intro). Fully
completing the Codex (87 entries) is worth about 21,000 (the rate rises as acts are done); peer review adds about 21,000.
That keeps capsules (200 each) affordable at 2 to 3 per new species without making money
free, since most of it comes from catching and from fighting.

### Hub flags

Present-day content has no act of its own. Its section at the end of
`include/constants/strata_act_flags.h` holds `FLAG_STRATA_HUB_BASE` (0x2AC..0x2B3, one used:
`FLAG_STRATA_HUB_STIPEND_TOLD`) and `VAR_STRATA_STIPEND_COUNT` (0x40DB).

The subplot (S1) has its own "Story" section after it: `FLAG_STRATA_STORY_BASE` (0x4D4..0x4DD,
inside the saved flag array): `FLAG_STRATA_STORY_SAW_PIT` and Ortiz's evidence records
(`FLAG_STRATA_STORY_EVIDENCE_STARTED`, `_PIT`, `_JACKET`, `_TRACKS`); 5..9 are free. The var is
`VAR_STRATA_SUBPLOT` (0x40DC, named in `vars.h`). On the hub maps the interlude cast hides under
`FLAG_TEMP_9..B` (the researchers keep `FLAG_TEMP_1..8`, Kessler at the ranch `FLAG_TEMP_1F`).

## 7. Systems

### 7.1 Lineage descent (replaces evolution)
- Evolution by level is turned off. Species have **no** `Evolutions=` lines in PBS.
- New PBS file `PBS/lineages.txt` maps `ancestor → [descendant candidates + conditions]`.
- On an era jump, every animal in the party and PC is processed:
  1. Read its **selection pressures** (see 7.2).
  2. Pick the best-fitting descendant for the new era.
  3. If no descendant fits the new era → **extinction check**.
  4. Play a "deep time" lapse animation (strata scrolling, silhouette morph).
- The descendant **inherits** nickname, OT, a share of EVs/IVs (heredity) and
  learned moves where they still make sense.

### 7.2 Selection pressures (tracked per lineage)
Hidden counters stored on each animal. The game has no contests, so the six `u8`
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
| MEAT (`tough`, `PRESSURE_MEAT_DIET`) | Eating animal forage: Larvae, Carrion; knocking out a foe with a move, **only for carnivores/omnivores** (roster `diet`, generated into `src/data/strata_diets.h`) | +12 per item; +1 per KO, KOs stop at 24 | n/a |
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
  | Bighorn red beds, Polecat Bench (Act 4) | open | day |
  | Willwood Swamp (Act 4) | water | day |
  | Clarks Fork Crossing (Act 4) | forest (riverside trees; shore and surf count as water) | day |
  | Bridger Shore, Bridger Forest (Act 5) | forest | day |
  | Fossil Lake (Act 5) | water | day |
  | Oil-Shale Cliffs (Act 5) | open | day |
  | White River (Act 6) | open | day |
  | Grassland, Savanna Woodland (Act 7, before the ash) | open / forest | day |
  | Niobrara River, Waterhole (Act 7, before the ash) | water | day |
  | Ashfall, all four maps after the boss (Act 7) | same as the clear version | ash |
  | Ice Age steppe (Act 8) | open | day |
  | Natural Trap Cave (Act 8) | none | none (never tinted) |
  | Meltwater River (Act 8) | water | day |
  | Ice Margin (Act 8) | open | day |
  | Colby Site (Act 8 coda) | none | day |
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
- Every lost lineage becomes a **fossil** (`src/strata_fossils.c`): a save flag per lineage
  (`FLAG_STRATA_FOSSIL_BASE` + its row in `src/data/strata_fossils.h`), listed by the
  **Fossil Case** key item and by the Hall of Lost Lineages plaques in the epilogue.
- After a jump the rig lists every loss, one message each: who (team animals by nickname,
  PC animals counted per species) and why that filter took it (one reason per lineage).
- Difficulty option **Gentle Deep Time**, chosen at new game (default: strict): a lost mon
  is replaced at the same level by a related survivor (its moves for that level, fresh
  pressures); the fossil is still recorded.

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
| Bighorn PETM | 20–27 | 19 |
| Green River | 28–34 | 25 |
| White River | 32–39 | 31 |
| Ashfall | 40–45 | 37 |
| Trap Cave (Ice Age) | 46–51 | 43 |
| Epilogue | 48–53 | 45 |

### 7.3a Feedback: rig forecast and pressure chart
The player sees what they are steering before it happens (`src/strata_forecast.c`;
outline §3.4, roadmap F1/F2).

**Rig forecast (F1).** When the rig would load the next layer (`RIG_NEXT`), after
Halvorsen's warning and before the YES/NO, `special Strata_RigForecast` (+ `waitstate`)
opens a scrolling list (the expansion's list menu, 5 rows) over a 3-line detail window:

| Row | Detail when selected |
|---|---|
| `FORECAST: <layer name>` (header) | |
| `Cimolestes → Protictis   Lv12` | "Default descent: no branch reached." / "Open-country branch: OPEN 96/96." / "Its one descendant in the record." |
| `Mesodma: no change   Lv31` | "No descent in this layer (stasis)." and the next layer that changes it |
| `Borealosuch: will not survive` (red) | "Extinct in the record: the lineage ends." / "Becomes X, which dies out." |
| `PC: 34 animals   3 lost` | "12 descend, 19 no change, 3 lost." / "Lost: Gastornis and 2 more." / who joins an emptied TEAM |

Each TEAM row's detail also lists the branches it didn't take ("Epicyon if ANIMAL
reaches 64 (now 41).", or "…outscored (100)." when a higher branch wins) and the
level-floor raise ("Raised to the era floor: Lv35 → Lv37."). The window waits 12
frames before taking input, so the A that closed the message can't skip it; A or B
closes it. Saying NO leaves time to bank lineages in the PC (which gains no pressure)
or feed forage, then ask the rig again.

The forecast is a dry run of `Lineage_AdvanceToEra` with lineage's public API, era by
era: descend (counters reset on a descent), extinction filter on the result, level
floor; plus the empty-TEAM refill (first surviving PC animal in box order, else the
gift survivor). The target era comes from `Strata_GetRigTargetEra`, which
`Strata_RigLoadNext` also uses. `test/strata_forecast.c` holds it to the real load:
128 generated teams and PCs across every rig load and multi-era jumps, compared slot
by slot (species, level, losses, refill), plus branch, extinction, PC-count, refill
and window-width tests. The last forecast is kept in `gStrataRigForecast` (the harness
compares it with the TEAM after the load).

**Pressure chart (F2).** TEAM menu → an animal → **LINEAGE** (after SUMMARY; field
menu only). A full-screen chart: a title band (species, level, TEAM slot), one bar per
counter (FOREST, OPEN, WATER, PLANT, MEAT, HEAT; 0–255, colour per pressure), a black
marker at each threshold of the next descent's branches with `now/threshold` beside
it, and below: "Next change: <layer>", the default descendant, and each branch's state
(on course / "X if OPEN reaches 96 (now 50)." / outscored); or "Dies out by <layer>",
or "No change ahead in the record." Up/Down pages through the TEAM; A/B returns to the
TEAM menu on the last animal viewed (as the summary screen does). Branch names are
shown whether or not the Codex has them (the outline's "only once discovered" gate is
not built).

### 7.4 Clock
- pokeemerald-expansion has a fake RTC (`OW_USE_FAKE_RTC`, `OW_ALTERED_TIME_RATIO`
  in `include/config/overworld.h`) that runs on play time. Extend it so the ratio
  is set per act (hours → millennia → Myr per in-game "day") and show it in the HUD.
- Seasons are re-skinned as **climate cycles** (e.g. Milankovitch glacial cycles in Act 8).

### 7.5 Maps
- Each act is a copy of the same base region map with changed terrain, water and
  vegetation. Landmarks (a particular butte, a river bend) stay put so the player
  can *see* deep time act on one place.
- Ground cover follows the plants of the era. Grasses existed by the latest Cretaceous
  but stayed rare until the Oligocene, so in Acts 1-5 the encounter "grass" is drawn as
  undergrowth (fern brakes and clumps; dead ferns and fiddleheads after the impact;
  fan-palm seedlings and legume thickets; broad-leaved herbs; ferns among horsetails) and
  the lawn as litter, ash, soil or moss. Act 6 keeps sparse grass, Acts 7-8 and the present
  are grassy. Same metatile behaviours, so encounters work as before
  (`docs/strata_art.md`, "Era ground cover").

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
  any roster, encounter or boss change. Its **EXP model** (`exp_model()`) gives the level a
  normal player has at each fight: 20 wild knockouts per act from the act's land table, Gen 9
  scaled EXP with the party-wide Exp. Share, carried from act to act and raised to the floor.
  From act 5 on the floors bind: a normal player arrives at the floor and reaches the boss
  about three levels above it.
- **Lineage resilience (F7, a game concession):** every era a lineage survives, its IVs rise
  by 3 (4 if its species didn't change), capped at 31, so a starter carried from Hell Creek
  reaches IV 31 by Ashfall (`Lineage_ResilientIV`, `include/lineage.h`).
- **Balance pass (Q2):** `python3 tools/strata/playtest/run.py starter_runs --out <dir>` plays
  each starter's line through all 29 bosses, set pieces and peer reviews (a quick-start per
  fight: the line's animal for the act, with its inherited moves and resilience IVs, plus the
  same typical catches for every starter, at the EXP model's level; best-damage moves, no
  items, no switching), then `balance.py --playtest <dir>` tabulates them. The runs behind the
  numbers below are kept in `tools/strata/playtest/q2_results/` (`before/`: the game at
  f7eac559f5, played by the same harness; `after/`), so `balance.py --playtest
  tools/strata/playtest/q2_results/after` works without rerunning. Targets and result
  (3 attempts per fight): every boss and set piece is won by all three starters, the TEAM
  ending at 18-94% HP (mean 58-61% per starter); the act reviews are won in 106 of 108 tries;
  the tyrannosaur still beats a Lv 14 TEAM (run from it); Halvorsen's final review is hard at
  a Lv 52 TEAM (2 and 5 of 9 won in two runs) and won 9 of 9 at Lv 55. Known: with a Sifrhippus that has Magical
  Leaf (Lv 28), the Coryphodon (Water/Ground, x4 to Grass) is easy.
- **Art and cries are original:** `gen_sprite.py` draws every species and `gen_cry.py`
  synthesises every cry (docs/strata_art.md). The `borrow` stock species only supplies
  leftover presentation fields; its sprites and cry would be copied in as placeholders,
  but `ART_STRICT`/`CRY_STRICT` in `gen_species.py` make that a build error. Strata
  species never depend on the stock species, which are disabled in the game build and
  stay enabled in the test build for the expansion's tests.
- **Weight field limit:** `weight` in species_info is a u16 in hectograms (max 6,553.5 kg),
  so the masses of *Tyrannosaurus*, *Triceratops*, *Ankylosaurus* and *Mammuthus* are clamped
  there. Battle only compares weights with brackets far below the clamp, so it keeps that
  field (stock tests assert its hectogram values). The Codex does not use it: see 7.8.

### 7.8 The Codex (numbers, units, pages)

The Codex is the expansion's regional dex, filled with Strata species. The stock National
Dex never unlocks (`IsNationalPokedexEnabled()` is always false, so an old save that had it
set behaves the same), so there is one dex and it lists only Strata animals.

- **Order:** Codex number = position in the list sorted by `first_era`, then roster order
  (`codex_order()` in `tools/strata/gen_species.py`). The roster puts the starter lines
  first, then the act's own animals, then later additions, so the three Hell Creek starter
  animals are 001-003 and the Epilogue animals come last. `gen_species.py` writes the order
  into `include/constants/pokedex.h` (`FOREACH_STRATA_CODEX_ORDER`, which
  `FOREACH_SPECIES_IN_HOENN_DEX_ORDER` expands to) and the size into `HOENN_DEX_COUNT`. A new
  species slots into its era and every later animal moves up one. The numbers are derived,
  not stored: seen/caught flags stay indexed by National number (species order), which never
  changes, so saves are unaffected.
- **Where the number shows:** the Codex list and its A to Z / HEAVIEST / LIGHTEST / TALLEST /
  SMALLEST orders and search results (`CreateMonDexNum`), the entry page and the registration
  screen after a capture (`PrintMonInfo`: regional number when the National Dex is off), and
  the summary screen (`SpeciesToPokedexNum`, which returns 0xFFFF, so no number, for an
  animal outside the Codex). The sort tables are generated too
  (`src/data/strata_pokedex_orders.h`); the stock `pokedex_orders.h` is no longer compiled.
- **Units:** `UNITS` is `UNITS_METRIC`. The entry page reads exact mass (g) and length (cm)
  from `src/data/strata_codex.h` (generated from the roster) through `src/strata_codex.c`:

  | Value | Shown | Rule |
  |---|---|---|
  | *Mesodma* 0.05 kg | `50 g` | under 1 kg: grams |
  | *Vulpes* 2.2 kg | `2.2 kg` | under 100 kg: one decimal |
  | *Equus* 300 kg | `300 kg` | from 100 kg: whole kg |
  | *Mammuthus* 9000 kg | `9.0 t` | from 1 t: tonnes, one decimal (C14) |
  | 120,000 kg | `120 t` | from 100 t: whole tonnes, thousands comma (`4,295 t` is the u32 top) |
  | length 0.1 m | `10 cm` | under 1 m: cm; otherwise `1.5 m`, `12.3 m`, cap `999.9+ m` |

  Each step is picked by the rounded value (99,950 g is `100 kg`, 999,500 g is `1.0 t`).
  Stock species fall back to their species_info fields (hectograms, decimeters). The
  strings stay under 64 px so they clear the footprint (`test/strata_codex.c` measures every
  species). `weight` is never 0 (minimum 1 hg) so tiny animals are not weightless in battle;
  it stays the clamped u16 for battle (7.7), and the Codex sort orders use the exact grams.
- **Pages (C14).** The info screen's bar is EVIDENCE | LINEAGE | CRY | CANCEL. Left/Right pick a
  slot and A opens it; on a page Left/Right step to the neighbouring page and B returns to the
  info page. The labels are drawn in code (`DrawCodexBarLabels`, `FONT_SMALL_NARROW` in three
  BG1 windows over each slot's interior, in the bar art's colour indices so the slot highlight
  recolours them); the baked-in stock labels underneath are covered. The stock AREA screen (a
  Hoenn map with nothing for Strata) and SIZE screen (affine scales borrowed from stock species;
  a 10 cm *Mesodma* and a 12 m *Tyrannosaurus* can't share the screen with the player) are no
  longer reachable; their code is untouched. Both new pages use one white box below the bar,
  built from the info screen's description-box tiles (`DrawCodexPageFrame`).
  - **EVIDENCE** (caught animals only, as the stock SIZE screen was): the full genus, `Site:`,
    `Age:` (the roster's `~` is written "about": the game font has no tilde) plus ", mass
    estimated" for `mass_est`, `Record:` (a confidence tag), a rule, then 2-4 lines: what the
    reconstruction rests on, `Inferred: ...` (R-e) and `Stand-in: ...` or a caveat
    (`Debated:`, `Unverified:`). Data: `tools/strata/roster/evidence.py`, keyed by species
    constant, kept apart from the roster modules so balance work and evidence work don't
    collide; `gen_species.py` (`gen_evidence()`) joins it with the roster's genus/site/age/
    `mass_est`/`first_era` into `src/data/strata_evidence.h` and fails on a missing entry,
    an unknown key, a tilde or more than 4 wrapped lines.
  - **LINEAGE** (seen is enough): `Codex_BuildLineage` walks `sLineageDescents` up to the root
    and lists the chain, the animal, then its descendants depth first (each era's default before
    its branches). Sister branches off the chain are not listed (Canis shows its ancestors, not
    Epicyon). Columns: name (indented 6 px per generation), tag (`default` or the branch's
    pressure: FOREST, OPEN, WATER, PLANT, MEAT, HEAT), fate (`living`; `lost` when the species is
    in an extinction list; blank when it descends). Five rows show; Up/Down move the cursor and
    scroll (arrows mark more rows). The box below: where it comes from ("Root of the line, at
    Hell Creek", "From Hesperocyon at Ashfall: MEAT", "No descents: a line of its own."), its
    fate ("Descends: Canis, Aenocyon or Vulpes.", "Lost at the K-Pg boundary." with the fossil
    reason from `sStrataFossils`, "Living today." with the evidence file's `today` note, e.g.
    *Macrochelys*, *Equus*, *Ovibos*). **Spoilers:** an animal not yet seen in the Codex is "?"
    in its row and in other rows' details, its fate column is "?", and its detail says "Not yet
    seen in the Codex."; its branch tag stays (the pressure chart already hints branches).
- **Tests:** `test/strata_codex.c` (unique 001-087 numbers, no stock species, era order,
  sort orders, unit formatting for g/kg/t and every species' width; an evidence entry of 2-4
  lines for every species with one `Inferred:` line, `Stand-in:` on every grade, every page row
  in the normal font within 224 px; the lineage builder for the dog line from Hesperocyon
  (a MEAT branch lost before the Ice Age, an OPEN branch alive), Canis (chain only), the bird
  line (three-way split, two branches lost in the cooling), Tyrannosaurus (a line of its own,
  lost at the K-Pg, with the fossil reason), Macrochelys (the `today` note); "?" for unseen
  animals; every row and detail line of every species within its column; ends are lost or
  living; at most one ancestor per species; bar label widths). Harness: `codex_pages` (START →
  CODEX; Info, Evidence, Lineage and Cry for Cimolestes, Tyrannosaurus, Hesperocyon and
  Mammuthus, the cursor to both ends, a seen-only Epicyon).

### 7.9 The ending: Colby gate, last lines, credits up the column (S3)

- **Colby gate** (`Strata_IsTodayGated`, `src/strata_acts.c`): at story 17 (Ice Age done) and
  without `FLAG_STRATA_COLBY_SEEN`, `Strata_GetRigState` answers `RIG_REENTER`, so the rig
  re-enters the Ice Age instead of loading today (`Strata_GetRigTargetEra` = none, no filter
  runs). `Strata_RigQuery` puts the reason in front of the layer name in `STR_VAR_1` ("Today
  can't load yet. Each layer is chained from the one below..."), which the field station's
  "Enter the reconstruction?" box reads out, so no hub script changed. The Steppe's sub-layer
  marker leads to Colby; reading the Clovis point sets the flag.
- **Ending** (`data/maps/StrataInterpretive1F/scripts.inc`): Halvorsen's review win, then three
  boxes (the theme line; bison, the black-footed ferret and swift foxes, with the hedged
  numbers in the script's comment), `FLAG_STRATA_ENDING_SEEN`, the stock save prompt
  (`Common_EventScript_SaveGame`, so the save continues after the ending), a fade and
  `special Strata_RollCredits`. Later talks offer the roll again (with the save prompt). There
  is no Hall of Fame screen: the stock one is league text and trainer art.
- **Credits** (`src/credits.c`, data and fates in `src/strata_ending.c`): the camera rises from
  below Hell Creek to today, so each layer comes in at the top, above the last. Ten bands (the
  nine layers plus a thin Colby sub-band), each a coloured header strip (name, age) over its
  layer. Under it: the player's losses there (`Ending_BuildFates`: every fossil flag, under the
  layer it was lost leaving, "lost at the K-Pg boundary", "gone by the late Paleocene", ...);
  a band with none says "Every lineage you carried came through." Under today: one row per
  living species in the TEAM (first) and PC, "descended to Canis" from its root in the descent
  table (Cimolestes) or "living today" (overflow summed up), and "The Pair: in a public museum
  case." once `VAR_STRATA_SUBPLOT` (0x40DC, read through a local define) is 10. On top: the
  credits proper (the Strata team; the science in general; thanks), then THE END and a soft
  reset to the title, as the stock credits do. Two scrolling BGs: band colour tiles on BG1, a
  30x32-tile text window on BG0, drawn one 16 px row ahead into the wrapping tilemaps. Text
  falls back to `FONT_NARROW` (`Ending_FitFont`). A or B held speeds it up.
- **Flags:** "Ending" section 0x4DE..0x4E5 (`FLAG_STRATA_ENDING_BASE`; +0 `ENDING_SEEN`).
- **Not recorded:** whether a living animal was carried or caught today; a prairie catch is
  listed as living too.
- **Tests:** `test/strata_ending.c` (gate states, rig message and every ending/Colby text width,
  lineage roots, the fate list from given fossil flags + TEAM + PC, overflow, every roll line
  width); harness `colby_gate`, `ending_smoke` (`gStrataCreditsState`: 1 roll, 2 THE END).

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
  - Field Codex: the stock dex screens as a single Strata-only dex with metric units (see 7.8)
- **Data:** species in `src/data/pokemon/species_info/`. Turn level evolutions off and
  replace the stock species with our creatures in reused species slots, cutting unused ones
  via `include/config/species_enabled.h`.
- **GBA constraints:**
  - Battle sprites are 64×64 with 16-colour palettes, plus small 32×32 icons.
  - ROM limit is 32 MB, which is plenty for ~8 copies of the region map.
  - Save space is tight, so there is no per-animal data beyond the repurposed fields.
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
