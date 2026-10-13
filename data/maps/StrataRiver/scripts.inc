StrataRiver_MapScripts::
	.byte 0

@ Triggers on every way up onto the bluff while VAR_STRATA_STORY is 2.
StrataRiver_EventScript_Tyrannosaur::
	lockall
	playmoncry SPECIES_TYRANNOSAUR, CRY_MODE_ENCOUNTER
	msgbox StrataRiver_Text_TyrannosaurAppears, MSGBOX_DEFAULT
	waitmoncry
	setwildbattle SPECIES_TYRANNOSAUR, 12
	dowildbattle
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, StrataRiver_EventScript_RanFromTyrannosaur
	setvar VAR_STRATA_STORY, 3
	msgbox StrataRiver_Text_AfterTyrannosaur, MSGBOX_DEFAULT
	releaseall
	end

StrataRiver_EventScript_RanFromTyrannosaur::
	msgbox StrataRiver_Text_RanFromTyrannosaur, MSGBOX_DEFAULT
	releaseall
	end

StrataRiver_EventScript_Tracks::
	msgbox StrataRiver_Text_Tracks, MSGBOX_SIGN
	end

StrataRiver_Text_TyrannosaurAppears:
	.string "The ground shudders. A TYRANNOSAURUS\n"
	.string "steps out of the ferns!$"

StrataRiver_Text_AfterTyrannosaur:
	.string "Bruised, the tyrannosaur limps away\n"
	.string "into the forest.\p"
	.string "Far to the south, the sky flickers\n"
	.string "strangely.\p"
	.string "Better report back to DR. HALVORSEN\n"
	.string "at camp.$"

StrataRiver_Text_RanFromTyrannosaur:
	.string "You slipped away. The tyrannosaur\n"
	.string "still rules the bluff.$"

StrataRiver_Text_Tracks:
	.string "Huge three-toed footprints sink deep\n"
	.string "into the mud, leading up the bluff.$"
