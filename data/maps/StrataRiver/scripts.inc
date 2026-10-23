StrataRiver_MapScripts::
	.byte 0

@ Triggers on every way up onto the bluff while VAR_STRATA_STORY is 2 (or talk to the
@ tyrannosaur standing on it).
@ A survival set piece: every way out of the fight except a whiteout finishes the act.
@ Winning or catching gets the "stood your ground" lines; running (or any other exit)
@ is survival too, and sets FLAG_STRATA_TREX_FLED so Dr. Halvorsen says so.
@ Then the impact's light show crosses the sky and the rig pulls the player out.
StrataRiver_EventScript_Tyrannosaur::
	lockall
	turnobject LOCALID_STRATA_RIVER_TYRANT, DIR_SOUTH
	playmoncry SPECIES_TYRANNOSAUR, CRY_MODE_ENCOUNTER
	msgbox StrataRiver_Text_TyrannosaurAppears, MSGBOX_DEFAULT
	waitmoncry
	strata_boss_prep atk=1
	setwildbattle SPECIES_TYRANNOSAUR, 14
	dowildbattle
	strata_boss_done
	call StrataRiver_EventScript_ResolveTyrannosaur
	setflag FLAG_STRATA_A1_TYRANT_GONE
	removeobject LOCALID_STRATA_RIVER_TYRANT
	goto_if_set FLAG_STRATA_TREX_FLED, StrataRiver_EventScript_RanFromTyrannosaur
	msgbox StrataRiver_Text_AfterTyrannosaur, MSGBOX_DEFAULT
	goto StrataRiver_EventScript_Ejecta

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
	goto StrataRiver_EventScript_Ejecta

@ The end of the layer: ejecta streaks cross the southern sky (how hot the glow got is
@ debated, so it is only a reddening), and Dr. Halvorsen pulls the player out of the rig.
StrataRiver_EventScript_Ejecta::
	playse SE_M_EXPLOSION
	fadescreenspeed FADE_TO_WHITE, 4
	setweather WEATHER_DROUGHT
	doweather
	fadescreenspeed FADE_FROM_WHITE, 4
	msgbox StrataRiver_Text_Ejecta, MSGBOX_DEFAULT
	msgbox StrataRiver_Text_PullOut, MSGBOX_DEFAULT
	playse SE_WARP_OUT
	warp MAP_STRATA_FIELD_STATION, 10, 8
	waitstate
	releaseall
	end

StrataRiver_EventScript_Tracks::
	msgbox StrataRiver_Text_Tracks, MSGBOX_SIGN
	end

StrataRiver_EventScript_NoteChannel::
	msgbox StrataRiver_Text_NoteChannel, MSGBOX_SIGN
	end

StrataRiver_Text_TyrannosaurAppears:
	.string "The ground shudders. A TYRANNOSAURUS\n"
	.string "steps out of the ferns!\p"
	.string "Nothing here can beat it. Fight,\n"
	.string "or run. Either way, you'll live to\l"
	.string "tell it.$"

StrataRiver_Text_AfterTyrannosaur:
	.string "Bruised, the tyrannosaur limps away\n"
	.string "into the forest.$"

StrataRiver_Text_RanFromTyrannosaur:
	.string "You bolt into the ferns. The\n"
	.string "tyrannosaur's roar rolls past, and\l"
	.string "it doesn't follow.$"

StrataRiver_Text_Ejecta:
	.string "Far to the south, streaks of light\n"
	.string "cross the sky, brighter by the\l"
	.string "minute.\p"
	.string "How hot that glow got is still\n"
	.string "debated. But something enormous has\l"
	.string "happened a long way away.$"

StrataRiver_Text_PullOut:
	.string "DR. HALVORSEN: {PLAYER}, the layer\n"
	.string "is breaking up! I'm pulling you out\l"
	.string "now. Hang on!$"

StrataRiver_Text_Tracks:
	.string "Huge three-toed footprints sink deep\n"
	.string "into the mud, leading up the bluff.$"

StrataRiver_Text_NoteChannel:
	.string "FIELD NOTE: Channel sandstone\p"
	.string "Rivers like this one wandered over\n"
	.string "a low coastal plain, while the\l"
	.string "inland sea retreated east.\p"
	.string "Flood sand and mud buried the\n"
	.string "bones we dig up at camp.$"
