@ Act 7: Ashfall Fossil Beds, Nebraska, ~11.9 Ma.
StrataGrassland_MapScripts::
	.byte 0

StrataGrassland_EventScript_Teleoceras::
	lockall
	msgbox StrataGrassland_Text_Waterhole, MSGBOX_DEFAULT
	playmoncry SPECIES_TELEOCERAS, CRY_MODE_ENCOUNTER
	msgbox StrataGrassland_Text_TeleocerasAppears, MSGBOX_DEFAULT
	waitmoncry
	strata_boss_prep def=1
	setwildbattle SPECIES_TELEOCERAS, 46
	dowildbattle
	strata_boss_done
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, StrataGrassland_EventScript_Ran
	setvar VAR_STRATA_STORY, 15
	msgbox StrataGrassland_Text_TeleocerasDone, MSGBOX_DEFAULT
	releaseall
	end

StrataGrassland_EventScript_Ran::
	msgbox StrataGrassland_Text_Ran, MSGBOX_DEFAULT
	releaseall
	end

StrataGrassland_Text_Waterhole:
	.string "Grey ash drifts down without end.\n"
	.string "It came from a volcano 1,600 km\l"
	.string "away, in what is now Idaho.\p"
	.string "Animals crowd the last waterhole.\n"
	.string "Many are coughing.$"

StrataGrassland_Text_TeleocerasAppears:
	.string "A TELEOCERAS bull stands between\n"
	.string "you and the water, ash caked on its\l"
	.string "hide!$"

StrataGrassland_Text_TeleocerasDone:
	.string "The bull staggers back to the herd.\p"
	.string "Breathing the glassy ash will make\n"
	.string "them sick for weeks. The small\l"
	.string "animals die first, then the horses\l"
	.string "and camels, the rhinos last.\p"
	.string "Their skeletons will be found here,\n"
	.string "still standing in the ash.\p"
	.string "Report back to DR. HALVORSEN.$"

StrataGrassland_Text_Ran:
	.string "You stumble back through the ash.\n"
	.string "The bull still guards the water.$"
