@ Act 6: the White River badlands, South Dakota, ~33 Ma.
StrataWhiteRiver_MapScripts::
	.byte 0

StrataWhiteRiver_EventScript_Archaeotherium::
	lockall
	playmoncry SPECIES_ARCHAEOTHERE, CRY_MODE_ENCOUNTER
	msgbox StrataWhiteRiver_Text_ArchaeotheriumAppears, MSGBOX_DEFAULT
	waitmoncry
	strata_boss_prep atk=1
	setwildbattle SPECIES_ARCHAEOTHERE, 40
	dowildbattle
	strata_boss_done
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, StrataWhiteRiver_EventScript_Ran
	setvar VAR_STRATA_STORY, 13
	msgbox StrataWhiteRiver_Text_ArchaeotheriumDone, MSGBOX_DEFAULT
	releaseall
	end

StrataWhiteRiver_EventScript_Ran::
	msgbox StrataWhiteRiver_Text_Ran, MSGBOX_DEFAULT
	releaseall
	end

StrataWhiteRiver_Text_ArchaeotheriumAppears:
	.string "A stink of rotting meat. Bones are\n"
	.string "piled against the rocks.\p"
	.string "An ARCHAEOTHERIUM, the hell pig,\n"
	.string "guarding its stash!$"

StrataWhiteRiver_Text_ArchaeotheriumDone:
	.string "The ARCHAEOTHERIUM grunts and\n"
	.string "trots away.\p"
	.string "The air is cooler and drier than\n"
	.string "in the Eocene. Forest is giving way\l"
	.string "to open woodland.\p"
	.string "Report back to DR. HALVORSEN.$"

StrataWhiteRiver_Text_Ran:
	.string "You leave the hell pig to its\n"
	.string "stash. It's still up there.$"
