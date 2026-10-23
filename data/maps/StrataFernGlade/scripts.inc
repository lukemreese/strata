@ Act 1: the Fern Glade, east of the Levee. Open ground of ferns and low flowering
@ plants (the "grass" is not grass), a grazing Edmontosaurus herd, and the last tree-
@ perching birds. A pair of Acheroraptor stalk the herd and ambush anyone who walks in.
StrataFernGlade_MapScripts::
	.byte 0

@ The raptor pair (a wild double battle, Lv 8/8). Triggered by the line across the glade
@ or by talking to either raptor; once, whatever the outcome. Running from the fight
@ costs nothing: they were after the herd.
StrataFernGlade_EventScript_RaptorAmbush::
	lockall
	playmoncry SPECIES_ACHERORAPTOR, CRY_MODE_ENCOUNTER
	msgbox StrataFernGlade_Text_RaptorsAppear, MSGBOX_DEFAULT
	waitmoncry
	setwildbattle SPECIES_ACHERORAPTOR, 8, ITEM_NONE, SPECIES_ACHERORAPTOR, 8
	dowildbattle
	setvar VAR_STRATA_ACT1, 1
	setflag FLAG_STRATA_A1_RAPTORS_GONE
	removeobject LOCALID_STRATA_GLADE_RAPTOR_A
	removeobject LOCALID_STRATA_GLADE_RAPTOR_B
	msgbox StrataFernGlade_Text_RaptorsGone, MSGBOX_DEFAULT
	giveitem ITEM_CARRION
	releaseall
	end

StrataFernGlade_EventScript_Herd::
	msgbox StrataFernGlade_Text_Herd, MSGBOX_NPC
	end

StrataFernGlade_EventScript_NoteBirds::
	msgbox StrataFernGlade_Text_NoteBirds, MSGBOX_SIGN
	end

StrataFernGlade_EventScript_NoteHerd::
	msgbox StrataFernGlade_Text_NoteHerd, MSGBOX_SIGN
	end

StrataFernGlade_EventScript_NoteFerns::
	msgbox StrataFernGlade_Text_NoteFerns, MSGBOX_SIGN
	end

StrataFernGlade_Text_RaptorsAppear:
	.string "Something pale shifts in the ferns.\n"
	.string "Then another.\p"
	.string "Two feathered ACHERORAPTORS slip\n"
	.string "out of cover, heads low. They are\l"
	.string "stalking the herd, and you are in\l"
	.string "their way!$"

StrataFernGlade_Text_RaptorsGone:
	.string "The pair melt back into the ferns,\n"
	.string "after bigger game.\p"
	.string "They leave a scrap of their last\n"
	.string "kill behind.$"

StrataFernGlade_Text_Herd:
	.string "An EDMONTOSAURUS grazes in the\n"
	.string "ferns, hundreds of grinding teeth\l"
	.string "working. It ignores you.$"

StrataFernGlade_Text_NoteBirds:
	.string "FIELD NOTE: Perching or walking?\p"
	.string "AVISAURUS belongs to the\n"
	.string "enantiornithines, a bird group that\l"
	.string "mostly perched in trees. It is known\l"
	.string "from foot bones, so its habits are\l"
	.string "inferred.\p"
	.string "After the impact the forests died\n"
	.string "back. Birds that fed on the ground\l"
	.string "or in water left descendants. That\l"
	.string "is a leading hypothesis, not proof.$"

StrataFernGlade_Text_NoteHerd:
	.string "FIELD NOTE: Edmontosaurus\p"
	.string "A duck-billed plant eater. Bone beds\n"
	.string "with many of them are known from\l"
	.string "this region.\p"
	.string "That hints at herds, or at floods\n"
	.string "that drowned many at once. The\l"
	.string "bones can't tell which.$"

StrataFernGlade_Text_NoteFerns:
	.string "FIELD NOTE: Glade cover\p"
	.string "What looks like tall grass is mostly\n"
	.string "ferns and low flowering plants.\p"
	.string "Ferns do well in open, sunny gaps.\n"
	.string "Remember them for later.$"
