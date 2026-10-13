@ Act 5: the Green River lakes and Bridger Basin, Wyoming, ~52-46 Ma.
StrataLakeForest_MapScripts::
	.byte 0

StrataLakeForest_EventScript_Uintatherium::
	lockall
	playmoncry SPECIES_UINTATHERIUM, CRY_MODE_ENCOUNTER
	msgbox StrataLakeForest_Text_UintatheriumAppears, MSGBOX_DEFAULT
	waitmoncry
	setwildbattle SPECIES_UINTATHERIUM, 34
	dowildbattle
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, StrataLakeForest_EventScript_Ran
	setvar VAR_STRATA_STORY, 11
	msgbox StrataLakeForest_Text_UintatheriumDone, MSGBOX_DEFAULT
	releaseall
	end

StrataLakeForest_EventScript_Ran::
	msgbox StrataLakeForest_Text_Ran, MSGBOX_DEFAULT
	releaseall
	end

StrataLakeForest_Text_UintatheriumAppears:
	.string "On the lakeshore stands a beast with\n"
	.string "six bony knobs on its head.\p"
	.string "A UINTATHERIUM! It bares its long\n"
	.string "upper tusks.$"

StrataLakeForest_Text_UintatheriumDone:
	.string "The UINTATHERIUM lumbers into the\n"
	.string "forest.\p"
	.string "Fish die in schools here and sink\n"
	.string "into the still lake mud. Millions\l"
	.string "of years from now, they'll be found\l"
	.string "whole.\p"
	.string "Report back to DR. HALVORSEN.$"

StrataLakeForest_Text_Ran:
	.string "You slip away along the shore. The\n"
	.string "UINTATHERIUM keeps its ground.$"
