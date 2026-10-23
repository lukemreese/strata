StrataRiver_MapScripts::
	.byte 0

@ Triggers on every way up onto the bluff while VAR_STRATA_STORY is 2.
@ A survival set piece: every way out of the fight except a whiteout finishes the act.
@ Winning or catching gets the "stood your ground" lines; running (or any other exit)
@ is survival too, and sets FLAG_STRATA_TREX_FLED so Dr. Halvorsen says so.
StrataRiver_EventScript_Tyrannosaur::
	lockall
	playmoncry SPECIES_TYRANNOSAUR, CRY_MODE_ENCOUNTER
	msgbox StrataRiver_Text_TyrannosaurAppears, MSGBOX_DEFAULT
	waitmoncry
	strata_boss_prep atk=1
	setwildbattle SPECIES_TYRANNOSAUR, 12
	dowildbattle
	strata_boss_done
	call StrataRiver_EventScript_ResolveTyrannosaur
	goto_if_set FLAG_STRATA_TREX_FLED, StrataRiver_EventScript_RanFromTyrannosaur
	msgbox StrataRiver_Text_AfterTyrannosaur, MSGBOX_DEFAULT
	releaseall
	end

@ The story state after the battle, kept free of messages so the test can run it.
@ Winning and catching are standing your ground; everything else that returns here is running.
StrataRiver_EventScript_ResolveTyrannosaur::
	setvar VAR_STRATA_STORY, STORY_ACT_DONE(ERA_HELL_CREEK)
	clearflag FLAG_STRATA_TREX_FLED
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, StrataRiver_EventScript_StoodGround
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, StrataRiver_EventScript_StoodGround
	setflag FLAG_STRATA_TREX_FLED
StrataRiver_EventScript_StoodGround::
	return

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
	.string "You bolt into the ferns. The\n"
	.string "tyrannosaur's roar rolls past, and\l"
	.string "it doesn't follow.\p"
	.string "Far to the south, the sky flickers\n"
	.string "strangely.\p"
	.string "Better report back to DR. HALVORSEN\n"
	.string "at camp.$"

StrataRiver_Text_Tracks:
	.string "Huge three-toed footprints sink deep\n"
	.string "into the mud, leading up the bluff.$"
