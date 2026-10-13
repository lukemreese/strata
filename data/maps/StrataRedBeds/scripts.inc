@ Act 4: Bighorn Basin, Wyoming, ~56 Ma: the Paleocene-Eocene Thermal Maximum.
StrataRedBeds_MapScripts::
	.byte 0

StrataRedBeds_EventScript_Coryphodon::
	lockall
	playmoncry SPECIES_CORYPHODON, CRY_MODE_ENCOUNTER
	msgbox StrataRedBeds_Text_CoryphodonAppears, MSGBOX_DEFAULT
	waitmoncry
	setwildbattle SPECIES_CORYPHODON, 28
	dowildbattle
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, StrataRedBeds_EventScript_Ran
	setvar VAR_STRATA_STORY, 9
	msgbox StrataRedBeds_Text_CoryphodonDone, MSGBOX_DEFAULT
	releaseall
	end

StrataRedBeds_EventScript_Ran::
	msgbox StrataRedBeds_Text_Ran, MSGBOX_DEFAULT
	releaseall
	end

StrataRedBeds_Text_CoryphodonAppears:
	.string "The heat is fierce. A huge shape\n"
	.string "heaves itself out of the shallows.\p"
	.string "A CORYPHODON, the largest animal\n"
	.string "in this hothouse world!$"

StrataRedBeds_Text_CoryphodonDone:
	.string "The CORYPHODON wallows back into\n"
	.string "the cool mud.\p"
	.string "The soils here are banded red: old\n"
	.string "ground baked in the PETM heat.\p"
	.string "Report back to DR. HALVORSEN.$"

StrataRedBeds_Text_Ran:
	.string "You retreat up the bank. The\n"
	.string "CORYPHODON still blocks the way.$"
