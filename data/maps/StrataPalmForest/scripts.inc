@ Act 3: Corral Bluffs, Denver Basin, Colorado, ~65.7-65.4 Ma.
@ The palm forest is the act's arrival and hub: up to Front Range Creek, left to the
@ Legume Thicket (where the Eoconodon boss waits), right to Concretion Bluffs.
StrataPalmForest_MapScripts::
	.byte 0

StrataPalmForest_EventScript_NotePalms::
	msgbox StrataPalmForest_Text_NotePalms, MSGBOX_SIGN
	end

StrataPalmForest_EventScript_NoteDating::
	msgbox StrataPalmForest_Text_NoteDating, MSGBOX_SIGN
	end

StrataPalmForest_EventScript_NoteFruit::
	msgbox StrataPalmForest_Text_NoteFruit, MSGBOX_SIGN
	end

StrataPalmForest_Text_NotePalms:
	.string "FIELD NOTE: Denver Fm, Corral Bluffs.\n"
	.string "Most of the leaves in this rock are\l"
	.string "palms. A few hundred thousand years\l"
	.string "after the impact, the forest is\l"
	.string "green again.\p"
	.string "But it has few kinds of trees. Palms\n"
	.string "were first to fill the gaps.\l"
	.string "(inferred from the leaf fossils)$"

StrataPalmForest_Text_NoteDating:
	.string "FIELD NOTE: How do we know when?\n"
	.string "Volcanic ash beds give dates, and\l"
	.string "the rock records the flips of\l"
	.string "Earth's magnetic field.\p"
	.string "Together they place these layers a\n"
	.string "few hundred thousand years after the\l"
	.string "impact. Dates carry error bars, so\l"
	.string "the rig shows a span: 65.7 to 65.4\l"
	.string "million years ago.$"

StrataPalmForest_Text_NoteFruit:
	.string "FIELD NOTE: Fruit and seeds.\n"
	.string "The small mammals here have broad,\l"
	.string "bumpy cheek teeth, good for crushing\l"
	.string "fruit, seeds and insects.\p"
	.string "Diet is read from the teeth, not\n"
	.string "seen. (inferred)$"
