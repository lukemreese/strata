@ Act 3: Corral Bluffs, Denver Basin, Colorado, ~65.7-65.4 Ma.
StrataPalmForest_MapScripts::
	.byte 0

StrataPalmForest_EventScript_Eoconodon::
	lockall
	playmoncry SPECIES_EOCONODON, CRY_MODE_ENCOUNTER
	msgbox StrataPalmForest_Text_EoconodonAppears, MSGBOX_DEFAULT
	waitmoncry
	strata_boss_prep atk=1
	setwildbattle SPECIES_EOCONODON, 22
	dowildbattle
	strata_boss_done
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, StrataPalmForest_EventScript_Ran
	setvar VAR_STRATA_STORY, 7
	msgbox StrataPalmForest_Text_EoconodonDone, MSGBOX_DEFAULT
	releaseall
	end

StrataPalmForest_EventScript_Ran::
	msgbox StrataPalmForest_Text_Ran, MSGBOX_DEFAULT
	releaseall
	end

StrataPalmForest_Text_EoconodonAppears:
	.string "Under the palms, something big is\n"
	.string "gnawing a carcass.\p"
	.string "An EOCONODON! A predator as big as\n"
	.string "a wolf, less than a million years\l"
	.string "after there were none at all.$"

StrataPalmForest_Text_EoconodonDone:
	.string "The EOCONODON slinks off into the\n"
	.string "ferns.\p"
	.string "With the dinosaurs gone, mammals are\n"
	.string "filling the empty roles: big plant\l"
	.string "eaters, and now big hunters.\p"
	.string "Report back to DR. HALVORSEN.$"

StrataPalmForest_Text_Ran:
	.string "You back away. The EOCONODON goes\n"
	.string "back to its meal.$"
