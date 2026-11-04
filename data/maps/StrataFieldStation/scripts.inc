@ Field station at the Hell Creek camp: the STRATA reconstruction rig.
@ VAR_STRATA_STORY and the acts are described in include/strata_acts.h and
@ src/strata_acts.c, which also holds Dr. Halvorsen's lines for each stage.

StrataFieldStation_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, StrataFieldStation_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, StrataFieldStation_OnFrame
	.byte 0

StrataFieldStation_OnTransition:
	special Strata_HideLockedReviewers
	@ The interlude visitors only come in during their beat (S1, src/strata_story.c).
	special Strata_StoryPrepareMap
	setflag FLAG_TEMP_9
	setflag FLAG_TEMP_A
	setflag FLAG_TEMP_B
	end

StrataFieldStation_OnFrame:
	map_script_2 VAR_STRATA_STORY, 0, StrataFieldStation_EventScript_Intro
	.2byte 0

StrataFieldStation_EventScript_Intro::
	lockall
	msgbox StrataFieldStation_Text_Welcome, MSGBOX_DEFAULT
	special ChooseStarter
	@ The starter is a gift, not a find: the survey stipend starts counting after it.
	special Strata_StipendBaseline
	msgbox StrataFieldStation_Text_Lineages, MSGBOX_DEFAULT
	call Strata_EventScript_AskDeepTimeMode
	msgbox StrataFieldStation_Text_Capsules, MSGBOX_DEFAULT
	giveitem ITEM_POKE_BALL, 5
	msgbox StrataFieldStation_Text_WaterGear, MSGBOX_DEFAULT
	call Strata_EventScript_GiveWaterGear
	setflag FLAG_SYS_POKEMON_GET
	setflag FLAG_SYS_POKEDEX_GET
	setflag FLAG_SYS_B_DASH
	setflag FLAG_STRATA_EXP_SHARE
	setrespawn HEAL_LOCATION_STRATA_FIELD_CAMP
	setvar VAR_STRATA_STORY, 1
	msgbox StrataFieldStation_Text_Codex, MSGBOX_DEFAULT
	releaseall
	end

StrataFieldStation_EventScript_Mentor::
	lock
	faceplayer
	msgbox StrataFieldStation_Text_Rest, MSGBOX_DEFAULT
	special HealPlayerParty
	@ The consortium interlude is hers: talking to her plays it as well as the trigger row.
	goto_if_eq VAR_TEMP_2, SUBPLOT_CONSORTIUM, StrataFieldStation_EventScript_MentorConsortium
	@ Science by story, then people by subplot (src/strata_acts.c).
	special Strata_BufferMentorText
	msgbox gStringVar4, MSGBOX_DEFAULT
StrataFieldStation_EventScript_MentorServices::
	@ Saves from before the gear existed get it here.
	checkitem ITEM_WADERS
	call_if_eq VAR_RESULT, FALSE, StrataFieldStation_EventScript_LateWaterGear
	call StrataFieldStation_EventScript_Stipend
	release
	end

@ The survey stipend (docs/strata_design.md, "Peer review"): money for every Codex entry the
@ player has caught since the last payment, 150 each at the start and 25 more per act done.
@ special Strata_PayStipend leaves the entries in {STR_VAR_1}, the rate in {STR_VAR_2} and the
@ total in {STR_VAR_3}.
StrataFieldStation_EventScript_Stipend::
	special Strata_PayStipend
	goto_if_ne VAR_RESULT, 0, StrataFieldStation_EventScript_StipendPaid
	goto_if_set FLAG_STRATA_HUB_STIPEND_TOLD, StrataFieldStation_EventScript_StipendNone
	setflag FLAG_STRATA_HUB_STIPEND_TOLD
	msgbox StrataFieldStation_Text_StipendExplain, MSGBOX_DEFAULT
	return

StrataFieldStation_EventScript_StipendPaid::
	playse SE_SHOP
	goto_if_set FLAG_STRATA_HUB_STIPEND_TOLD, StrataFieldStation_EventScript_StipendPaidTold
	setflag FLAG_STRATA_HUB_STIPEND_TOLD
	msgbox StrataFieldStation_Text_StipendExplain, MSGBOX_DEFAULT
StrataFieldStation_EventScript_StipendPaidTold::
	msgbox StrataFieldStation_Text_StipendPaid, MSGBOX_DEFAULT
	return

StrataFieldStation_EventScript_StipendNone::
	msgbox StrataFieldStation_Text_StipendNone, MSGBOX_DEFAULT
	return

@ The isotope geochemist (act 4): a visiting researcher, one battle.
StrataFieldStation_EventScript_Ingrid::
	lock
	faceplayer
	trainerbattle_single TRAINER_STRATA_REVIEW_ACT4, StrataFieldStation_Text_IngridIntro, StrataFieldStation_Text_IngridDefeat, StrataFieldStation_EventScript_IngridWon
	msgbox StrataFieldStation_Text_IngridAfter, MSGBOX_DEFAULT
	release
	end

StrataFieldStation_EventScript_IngridWon::
	msgbox StrataFieldStation_Text_IngridNote, MSGBOX_DEFAULT
	releaseall
	end

StrataFieldStation_Text_StipendExplain:
	.string "DR. HALVORSEN: One more thing. The\n"
	.string "consortium pays a survey stipend.\p"
	.string "Every new species in your CODEX,\n"
	.string "caught and logged, earns the\l"
	.string "camp a payment. It's yours for\l"
	.string "supplies.\p"
	.string "It grows with every layer the rig\n"
	.string "finishes. Funding follows results.$"

StrataFieldStation_Text_StipendPaid:
	.string "DR. HALVORSEN: {STR_VAR_1} new CODEX entries\n"
	.string "since last time, at ¥{STR_VAR_2} each.\p"
	.string "{PLAYER} received ¥{STR_VAR_3} from the\n"
	.string "survey stipend.$"

StrataFieldStation_Text_StipendNone:
	.string "DR. HALVORSEN: No new CODEX entries\n"
	.string "since the last stipend. Catch and\l"
	.string "log something new, and the\l"
	.string "consortium pays.$"

StrataFieldStation_Text_IngridIntro:
	.string "INGRID: I read tooth enamel with a\n"
	.string "mass spectrometer. The carbon in it\l"
	.string "says what an animal ate, and what\l"
	.string "the air was like.\p"
	.string "Your PETM run has a carbon spike\n"
	.string "in it, doesn't it? Peer review:\l"
	.string "your reconstruction against my\l"
	.string "numbers.$"

StrataFieldStation_Text_IngridDefeat:
	.string "INGRID: Your animals are the right\n"
	.string "sizes for a hot world. Good.$"

StrataFieldStation_Text_IngridNote:
	.string "INGRID: Field note.\p"
	.string "At the PETM, carbon came out over\n"
	.string "thousands of years and the world\l"
	.string "warmed by several degrees.\p"
	.string "Today we're adding carbon roughly\n"
	.string "ten times faster, give or take.\l"
	.string "Check the paper; I'm careful about\l"
	.string "the number, not the direction.$"

StrataFieldStation_Text_IngridAfter:
	.string "INGRID: The horses shrank in the\n"
	.string "heat, too. Heat leaves a body-size\l"
	.string "signature in the teeth.$"

StrataFieldStation_EventScript_LateWaterGear::
	msgbox StrataFieldStation_Text_WaterGear, MSGBOX_DEFAULT
	call Strata_EventScript_GiveWaterGear
	return

@ The rig only ever loads the next layer up: time in Strata moves forward.
StrataFieldStation_EventScript_Rig::
	lockall
	special Strata_RigQuery
	goto_if_eq VAR_RESULT, RIG_IDLE, StrataFieldStation_EventScript_RigIdle
	goto_if_eq VAR_RESULT, RIG_COMPLETE, StrataFieldStation_EventScript_RigComplete
	goto_if_eq VAR_RESULT, RIG_REENTER, StrataFieldStation_EventScript_RigReenter
	goto_if_eq VAR_RESULT, RIG_FIRST, StrataFieldStation_EventScript_RigFirst
	@ RIG_NEXT: one-way, and the extinction filter applies.
	msgbox StrataFieldStation_Text_NextWarning, MSGBOX_DEFAULT
	@ The forecast (src/strata_forecast.c): what the load does to each lineage.
	msgbox StrataFieldStation_Text_Forecast, MSGBOX_DEFAULT
	closemessage
	special Strata_RigForecast
	waitstate
	msgbox StrataFieldStation_Text_LoadLayer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, StrataFieldStation_EventScript_RigCancel
	playse SE_M_EXPLOSION
	special Strata_RigLoadNext
	goto_if_eq VAR_0x8005, 0, StrataFieldStation_EventScript_NoLosses
	@ Every lost animal and why (data/scripts/strata_fossils.inc).
	call Strata_EventScript_ShowLosses
	goto StrataFieldStation_EventScript_AfterLoad

StrataFieldStation_EventScript_NoLosses::
	msgbox StrataFieldStation_Text_NoLosses, MSGBOX_DEFAULT
StrataFieldStation_EventScript_AfterLoad::
	@ The present has no reconstruction to step into: the epilogue happens here.
	goto_if_eq VAR_0x8006, TRUE, StrataFieldStation_EventScript_ReachedToday
	goto StrataFieldStation_EventScript_WarpToAct

StrataFieldStation_EventScript_RigFirst::
	msgbox StrataFieldStation_Text_EnterLayer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, StrataFieldStation_EventScript_RigCancel
	special Strata_RigLoadNext
	goto StrataFieldStation_EventScript_WarpToAct

StrataFieldStation_EventScript_RigReenter::
	msgbox StrataFieldStation_Text_EnterLayer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, StrataFieldStation_EventScript_RigCancel
StrataFieldStation_EventScript_WarpToAct::
	playse SE_WARP_IN
	special Strata_SpecialGetCurrentAct
	switch VAR_RESULT
	case ERA_HELL_CREEK, StrataFieldStation_EventScript_WarpHellCreek
	case ERA_IMPACT_WINTER, StrataFieldStation_EventScript_WarpImpactWinter
	case ERA_CORRAL_BLUFFS, StrataFieldStation_EventScript_WarpCorralBluffs
	case ERA_BIGHORN_PETM, StrataFieldStation_EventScript_WarpBighorn
	case ERA_GREEN_RIVER, StrataFieldStation_EventScript_WarpGreenRiver
	case ERA_WHITE_RIVER, StrataFieldStation_EventScript_WarpWhiteRiver
	case ERA_ASHFALL, StrataFieldStation_EventScript_WarpAshfall
	case ERA_TRAP_CAVE, StrataFieldStation_EventScript_WarpTrapCave
	releaseall
	end

StrataFieldStation_EventScript_WarpHellCreek::
	warp MAP_STRATA_LEVEE, 18, 30
	waitstate
	end

StrataFieldStation_EventScript_WarpImpactWinter::
	warp MAP_STRATA_LEVEE_WINTER, 18, 30
	waitstate
	end

StrataFieldStation_EventScript_WarpCorralBluffs::
	warp MAP_STRATA_PALM_FOREST, STRATA_ARRIVAL_PALM_FOREST
	waitstate
	end

StrataFieldStation_EventScript_WarpBighorn::
	warp MAP_STRATA_RED_BEDS, STRATA_ARRIVAL_RED_BEDS
	waitstate
	end

StrataFieldStation_EventScript_WarpGreenRiver::
	warp MAP_STRATA_LAKE_FOREST, STRATA_ARRIVAL_LAKE_FOREST
	waitstate
	end

StrataFieldStation_EventScript_WarpWhiteRiver::
	warp MAP_STRATA_WHITE_RIVER, STRATA_ARRIVAL_WHITE_RIVER
	waitstate
	end

StrataFieldStation_EventScript_WarpAshfall::
	warp MAP_STRATA_GRASSLAND, STRATA_ARRIVAL_GRASSLAND
	waitstate
	end

StrataFieldStation_EventScript_WarpTrapCave::
	warp MAP_STRATA_STEPPE, STRATA_ARRIVAL_STEPPE
	waitstate
	end

StrataFieldStation_EventScript_ReachedToday::
	msgbox StrataFieldStation_Text_ReachedToday, MSGBOX_DEFAULT
	releaseall
	end

StrataFieldStation_EventScript_RigIdle::
	msgbox StrataFieldStation_Text_RigIdle, MSGBOX_DEFAULT
	releaseall
	end

StrataFieldStation_EventScript_RigComplete::
	msgbox StrataFieldStation_Text_RigComplete, MSGBOX_DEFAULT
	releaseall
	end

StrataFieldStation_EventScript_RigCancel::
	releaseall
	end

@ Shared by every layer's arrival point: the edge of the reconstruction.
StrataFieldStation_EventScript_Anchor::
	lockall
	msgbox StrataFieldStation_Text_Anchor, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, StrataFieldStation_EventScript_RigCancel
	playse SE_WARP_OUT
	warp MAP_STRATA_FIELD_STATION, 10, 8
	waitstate
	releaseall
	end

StrataFieldStation_Text_Welcome:
	.string "DR. HALVORSEN: {PLAYER}! You made it\n"
	.string "out to Hell Creek.\p"
	.string "These badlands are river mud and\n"
	.string "sand, laid down 66 million years\l"
	.string "ago, in the last days of the\l"
	.string "dinosaurs.\p"
	.string "This rig is our STRATA unit. Load a\n"
	.string "rock layer's fossils, and it\l"
	.string "reconstructs that world, alive.\p"
	.string "This week we pulled three specimens\n"
	.string "from the same layer: a small mammal\l"
	.string "jaw, a ground bird and a snapping\l"
	.string "turtle shell.\p"
	.string "Choose one. The rig will rebuild it\n"
	.string "as your field partner.$"

StrataFieldStation_Text_Lineages:
	.string "Good choice. Now, remember this:\p"
	.string "Individuals don't evolve.\n"
	.string "Populations do, over generations.\p"
	.string "When the rig moves up to a younger\n"
	.string "layer, your partner's lineage moves\l"
	.string "with it, shaped by how it lived.$"

StrataFieldStation_Text_Capsules:
	.string "Here, take some specimen capsules.$"

StrataFieldStation_Text_WaterGear:
	.string "DALE left you some field gear,\n"
	.string "too: waders and a fishing kit.\p"
	.string "Half the life down there is in\n"
	.string "the rivers. Don't skip them.$"

StrataFieldStation_Text_Codex:
	.string "Your FIELD CODEX will log every\n"
	.string "species you meet.\p"
	.string "When you're ready, use the rig to\n"
	.string "enter the Hell Creek layer.\p"
	.string "But first, find DALE at the outcrop\n"
	.string "in the badlands, south of camp.\p"
	.string "He'll show you where your partner\n"
	.string "came out of the rock.$"

StrataFieldStation_Text_Rest:
	.string "DR. HALVORSEN: Let's patch up your\n"
	.string "team first.$"

StrataFieldStation_Text_NextWarning:
	.string "DR. HALVORSEN: Before you go…\p"
	.string "The rig only moves up. Once we load\n"
	.string "the next layer, this one is behind\l"
	.string "us for good.\p"
	.string "And any lineage that can't survive\n"
	.string "the change won't come with you.$"

StrataFieldStation_Text_Forecast:
	.string "STRATA RIG: Running the forecast\n"
	.string "for every lineage you carry…$"

StrataFieldStation_Text_LoadLayer:
	.string "STRATA RIG: {STR_VAR_1}.\n"
	.string "Load the layer?$"

StrataFieldStation_Text_EnterLayer:
	.string "STRATA RIG: {STR_VAR_1}.\n"
	.string "Enter the reconstruction?$"

StrataFieldStation_Text_NoLosses:
	.string "The rig shudders as the new layer\n"
	.string "loads…\p"
	.string "Every lineage you carry made it\n"
	.string "through.$"

StrataFieldStation_Text_ReachedToday:
	.string "The rig powers down. There is no\n"
	.string "layer above this one.\p"
	.string "Talk to DR. HALVORSEN.$"

StrataFieldStation_Text_RigIdle:
	.string "The rig hums quietly. DR. HALVORSEN\n"
	.string "should explain it first.$"

StrataFieldStation_Text_RigComplete:
	.string "STRATA RIG: Today.\n"
	.string "You're standing on the top layer.$"

StrataFieldStation_Text_Anchor:
	.string "The air shimmers at the edge of the\n"
	.string "reconstruction. Return to camp?$"

@ Run by the whiteout cutscene (src/field_screen_effect.c) after respawning here.
StrataFieldStation_EventScript_AfterWhiteOut::
	lockall
	msgbox StrataFieldStation_Text_AfterWhiteOut, MSGBOX_DEFAULT
	call Common_EventScript_OutOfCenterPartyHeal
	msgbox StrataFieldStation_Text_AfterWhiteOutHealed, MSGBOX_DEFAULT
	fadedefaultbgm
	releaseall
	end

StrataFieldStation_Text_AfterWhiteOut:
	.string "DR. HALVORSEN: There you are! Let's\n"
	.string "get your team patched up.$"

StrataFieldStation_Text_AfterWhiteOutHealed:
	.string "Out there, nothing is tame. Pick\n"
	.string "your fights.$"

@ ---------------------------------------------------------------------------
@ Station services: the specimen database (PC), the healing cot and the rig's
@ behaviour archive (the move relearner). Halvorsen still patches the team up
@ when you talk to her.
@ ---------------------------------------------------------------------------

@ The lab's desk computers. They carry no PC-screen metatile, so there is no
@ boot-up flicker; the stock PC menu does the rest.
StrataFieldStation_EventScript_PC::
	lockall
	setvar VAR_0x8004, PC_LOCATION_OTHER
	playse SE_PC_ON
	msgbox StrataFieldStation_Text_BootUpPC, MSGBOX_DEFAULT
	goto EventScript_PCMainMenu
	end

StrataFieldStation_EventScript_Cot::
	lockall
	msgbox StrataFieldStation_Text_Cot, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, StrataFieldStation_EventScript_RigCancel
	call Common_EventScript_OutOfCenterPartyHeal
	msgbox StrataFieldStation_Text_CotRested, MSGBOX_DEFAULT
	releaseall
	end

@ Free, any time: level-up moves only, for party and PC mons alike.
StrataFieldStation_EventScript_Relearner::
	lockall
	faceplayer
	msgbox StrataFieldStation_Text_RelearnerHello, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, StrataFieldStation_EventScript_RelearnerBye
StrataFieldStation_EventScript_RelearnerChooseMon::
	msgbox StrataFieldStation_Text_RelearnerWhichMon, MSGBOX_DEFAULT
	setmoverelearnerstate MOVE_RELEARNER_LEVEL_UP_MOVES
	chooseboxmon SELECT_PC_MON_MOVE_RELEARNER
	waitstate
	goto_if_eq VAR_0x8004, PARTY_NOTHING_CHOSEN, StrataFieldStation_EventScript_RelearnerBye
	special IsSelectedMonEgg
	goto_if_eq VAR_RESULT, TRUE, StrataFieldStation_EventScript_RelearnerEgg
	special Special_HasMoveToRelearn
	goto_if_eq VAR_RESULT, FALSE, StrataFieldStation_EventScript_RelearnerNothing
	msgbox StrataFieldStation_Text_RelearnerWhichMove, MSGBOX_DEFAULT
	special TeachMoveRelearnerMove
	goto StrataFieldStation_EventScript_RelearnerChooseMon

StrataFieldStation_EventScript_RelearnerNothing::
	msgbox StrataFieldStation_Text_RelearnerNothing, MSGBOX_DEFAULT
	goto StrataFieldStation_EventScript_RelearnerChooseMon

StrataFieldStation_EventScript_RelearnerEgg::
	msgbox StrataFieldStation_Text_RelearnerEgg, MSGBOX_DEFAULT
	goto StrataFieldStation_EventScript_RelearnerChooseMon

StrataFieldStation_EventScript_RelearnerBye::
	msgbox StrataFieldStation_Text_RelearnerBye, MSGBOX_DEFAULT
	releaseall
	end

@ The rig's in-fiction rules (outline §1.2), pinned over the back desk.
StrataFieldStation_EventScript_RigRules::
	msgbox StrataFieldStation_Text_RigRules, MSGBOX_SIGN
	end

StrataFieldStation_Text_RigRules:
	.string "STRATA RIG: OPERATING RULES\n"
	.string "(pinned up in DR. HALVORSEN's hand)\p"
	.string "1. It's a model, not a time machine.\n"
	.string "It only loads where the record is\l"
	.string "rich.\p"
	.string "2. It runs forward only, each layer\n"
	.string "built on the one below.\p"
	.string "3. It must match the record. What\n"
	.string "the rock says died out, dies out.\p"
	.string "4. Where the record is silent, your\n"
	.string "choices steer the run.\p"
	.string "5. Colors, calls and behavior are\n"
	.string "best guesses.\p"
	.string "6. People appear only as traces:\n"
	.string "tools, cut marks. Never as people.$"

StrataFieldStation_Text_BootUpPC:
	.string "The specimen database wakes up.\n"
	.string "Your sample boxes are on file.$"

StrataFieldStation_Text_Cot:
	.string "A camp cot, made up with a rough\n"
	.string "wool blanket. Rest a while?$"

StrataFieldStation_Text_CotRested:
	.string "A short nap, and the whole team is\n"
	.string "back on its feet.$"

StrataFieldStation_Text_RelearnerHello:
	.string "WREN, STATION TECH: The rig keeps a\n"
	.string "behaviour archive for every lineage.\p"
	.string "I can re-derive a move your partner\n"
	.string "has forgotten. No charge.\p"
	.string "Want me to look through the archive?$"

StrataFieldStation_Text_RelearnerWhichMon:
	.string "Whose behaviours should I pull up?$"

StrataFieldStation_Text_RelearnerWhichMove:
	.string "Which behaviour should I re-derive?$"

StrataFieldStation_Text_RelearnerNothing:
	.string "Nothing missing there. It already\n"
	.string "knows everything it's old enough to.$"

StrataFieldStation_Text_RelearnerEgg:
	.string "That's a sample that hasn't\n"
	.string "hatched. It has no behaviours yet.$"

StrataFieldStation_Text_RelearnerBye:
	.string "WREN: Come back whenever the archive\n"
	.string "can help.$"

@ ---------------------------------------------------------------------------
@ Interludes in the field station (S1; the beat table is in src/strata_story.c). They start
@ on the trigger row between the rig and the door (y 10) while VAR_TEMP_3 is 1, which
@ special Strata_StoryPrepareMap sets when a station beat is due. Visitors appear just inside
@ the door (row 11), Dr. Halvorsen comes down from her desk, and everyone goes back after.
@ ---------------------------------------------------------------------------
StrataFieldStation_EventScript_Interlude::
	lockall
	setvar VAR_TEMP_3, 0
	switch VAR_TEMP_2
	case SUBPLOT_KESSLER_OFFER, StrataFieldStation_EventScript_KesslerOffer
	case SUBPLOT_JOSIE_PIT, StrataFieldStation_EventScript_JosiePit
	case SUBPLOT_HALVORSEN_REFUSAL, StrataFieldStation_EventScript_Refusal
	case SUBPLOT_CONSORTIUM, StrataFieldStation_EventScript_Consortium
	releaseall
	end

@ The next beat may be due here too (a save that skipped some): check again after each one.
StrataFieldStation_EventScript_InterludeEnd::
	special Strata_StoryPrepareMap
	releaseall
	end

StrataFieldStation_EventScript_MentorDown::
	applymovement LOCALID_STRATA_MENTOR, StrataFieldStation_Movement_MentorDown
	waitmovement 0
	return

StrataFieldStation_EventScript_MentorBack::
	applymovement LOCALID_STRATA_MENTOR, StrataFieldStation_Movement_MentorBack
	waitmovement 0
	return

@ Act 1 done: Kessler offers a "partnership" (rig output for prospecting). Halvorsen says no,
@ and Theo calls the rig a fancy diorama.
StrataFieldStation_EventScript_KesslerOffer::
	playse SE_DOOR
	clearflag FLAG_TEMP_9
	addobject LOCALID_STRATA_STATION_KESSLER
	applymovement OBJ_EVENT_ID_PLAYER, StrataFieldStation_Movement_FaceDown
	waitmovement 0
	msgbox StrataFieldStation_Text_StoryKessler1, MSGBOX_DEFAULT
	call StrataFieldStation_EventScript_MentorDown
	msgbox StrataFieldStation_Text_StoryKessler2, MSGBOX_DEFAULT
	msgbox StrataFieldStation_Text_StoryKessler3, MSGBOX_DEFAULT
	applymovement LOCALID_STRATA_STATION_KESSLER, StrataFieldStation_Movement_KesslerLeave
	waitmovement 0
	playse SE_EXIT
	removeobject LOCALID_STRATA_STATION_KESSLER
	setflag FLAG_TEMP_9
	playse SE_DOOR
	clearflag FLAG_TEMP_A
	addobject LOCALID_STRATA_STATION_THEO
	msgbox StrataFieldStation_Text_StoryKessler4, MSGBOX_DEFAULT
	applymovement LOCALID_STRATA_STATION_THEO, StrataFieldStation_Movement_TheoLeave
	waitmovement 0
	playse SE_EXIT
	removeobject LOCALID_STRATA_STATION_THEO
	setflag FLAG_TEMP_A
	msgbox StrataFieldStation_Text_StoryKessler5, MSGBOX_DEFAULT
	call StrataFieldStation_EventScript_MentorBack
	setvar VAR_STRATA_SUBPLOT, SUBPLOT_KESSLER_OFFER
	goto StrataFieldStation_EventScript_InterludeEnd

@ Act 3 done: Josie found a fresh pit on BLM land, in Sand Arroyo.
StrataFieldStation_EventScript_JosiePit::
	playse SE_DOOR
	clearflag FLAG_TEMP_B
	addobject LOCALID_STRATA_STATION_JOSIE
	applymovement OBJ_EVENT_ID_PLAYER, StrataFieldStation_Movement_FaceDown
	waitmovement 0
	msgbox StrataFieldStation_Text_StoryJosie1, MSGBOX_DEFAULT
	call StrataFieldStation_EventScript_MentorDown
	msgbox StrataFieldStation_Text_StoryJosie2, MSGBOX_DEFAULT
	applymovement LOCALID_STRATA_STATION_JOSIE, StrataFieldStation_Movement_JosieLeave
	waitmovement 0
	playse SE_EXIT
	removeobject LOCALID_STRATA_STATION_JOSIE
	setflag FLAG_TEMP_B
	call StrataFieldStation_EventScript_MentorBack
	setvar VAR_STRATA_SUBPLOT, SUBPLOT_JOSIE_PIT
	goto StrataFieldStation_EventScript_InterludeEnd

@ Act 4 done: Kessler offers to fund the rig after Halvorsen retires, for a first look at the
@ crew's surveys. She refuses; Theo, whose grant is ending, nearly takes it.
StrataFieldStation_EventScript_Refusal::
	playse SE_DOOR
	clearflag FLAG_TEMP_9
	addobject LOCALID_STRATA_STATION_KESSLER
	clearflag FLAG_TEMP_A
	addobject LOCALID_STRATA_STATION_THEO
	applymovement OBJ_EVENT_ID_PLAYER, StrataFieldStation_Movement_FaceDown
	waitmovement 0
	msgbox StrataFieldStation_Text_StoryRefusal1, MSGBOX_DEFAULT
	call StrataFieldStation_EventScript_MentorDown
	msgbox StrataFieldStation_Text_StoryRefusal2, MSGBOX_DEFAULT
	msgbox StrataFieldStation_Text_StoryRefusal3, MSGBOX_DEFAULT
	applymovement LOCALID_STRATA_STATION_KESSLER, StrataFieldStation_Movement_KesslerLeave
	waitmovement 0
	playse SE_EXIT
	removeobject LOCALID_STRATA_STATION_KESSLER
	setflag FLAG_TEMP_9
	msgbox StrataFieldStation_Text_StoryRefusal4, MSGBOX_DEFAULT
	applymovement LOCALID_STRATA_STATION_THEO, StrataFieldStation_Movement_TheoLeave
	waitmovement 0
	playse SE_EXIT
	removeobject LOCALID_STRATA_STATION_THEO
	setflag FLAG_TEMP_A
	call StrataFieldStation_EventScript_MentorBack
	setvar VAR_STRATA_SUBPLOT, SUBPLOT_HALVORSEN_REFUSAL
	goto StrataFieldStation_EventScript_InterludeEnd

@ Act 7 done, after the citation: Halvorsen proposes a museum consortium. The research case
@ is the player's Codex (STR_VAR_1 = species caught).
StrataFieldStation_EventScript_Consortium::
	applymovement OBJ_EVENT_ID_PLAYER, StrataFieldStation_Movement_FaceUp
	waitmovement 0
	call StrataFieldStation_EventScript_MentorDown
	call StrataFieldStation_EventScript_ConsortiumTalk
	call StrataFieldStation_EventScript_MentorBack
	goto StrataFieldStation_EventScript_InterludeEnd

StrataFieldStation_EventScript_MentorConsortium::
	setvar VAR_TEMP_3, 0
	call StrataFieldStation_EventScript_ConsortiumTalk
	special Strata_StoryPrepareMap
	goto StrataFieldStation_EventScript_MentorServices

StrataFieldStation_EventScript_ConsortiumTalk::
	special Strata_StoryBufferCaseCount
	msgbox StrataFieldStation_Text_StoryConsortium1, MSGBOX_DEFAULT
	msgbox StrataFieldStation_Text_StoryConsortium2, MSGBOX_DEFAULT
	setvar VAR_STRATA_SUBPLOT, SUBPLOT_CONSORTIUM
	return

@ The visitors only stand in the station during their scene.
StrataFieldStation_EventScript_VisitorKessler::
	msgbox StrataFieldStation_Text_VisitorKessler, MSGBOX_NPC
	end

StrataFieldStation_EventScript_VisitorTheo::
	msgbox StrataFieldStation_Text_VisitorTheo, MSGBOX_NPC
	end

StrataFieldStation_EventScript_VisitorJosie::
	msgbox StrataFieldStation_Text_VisitorJosie, MSGBOX_NPC
	end

StrataFieldStation_Movement_FaceDown:
	face_down
	step_end

StrataFieldStation_Movement_FaceUp:
	face_up
	step_end

StrataFieldStation_Movement_MentorDown:
	walk_down
	walk_down
	walk_down
	step_end

StrataFieldStation_Movement_MentorBack:
	walk_up
	walk_up
	walk_up
	face_down
	step_end

@ From (8, 11) out through the door at (7, 12).
StrataFieldStation_Movement_KesslerLeave:
	walk_left
	walk_down
	step_end

@ From (4, 11) out through the door at (6, 12).
StrataFieldStation_Movement_TheoLeave:
	walk_right
	walk_right
	walk_down
	step_end

@ From (9, 11) out through the door at (7, 12).
StrataFieldStation_Movement_JosieLeave:
	walk_left
	walk_left
	walk_down
	step_end

StrataFieldStation_Text_StoryKessler1::
	.string "KESSLER: DR. HALVORSEN. Forgive the\n"
	.string "intrusion. WADE KESSLER, Kessler\l"
	.string "Natural History.\p"
	.string "I hear your rig rebuilds a whole\n"
	.string "landscape from what's in the rock.$"

StrataFieldStation_Text_StoryKessler2::
	.string "KESSLER: Picture it pointed at a\n"
	.string "hillside before anyone digs. Which\l"
	.string "layer, what lived there, where.\p"
	.string "A partnership. Your rig's maps, my\n"
	.string "crews. I pay well, and I hear the\l"
	.string "station could use the money.\p"
	.string "DR. HALVORSEN: It could. The answer\n"
	.string "is still no, MR. KESSLER.\p"
	.string "What the rig makes is published,\n"
	.string "for anyone, once it's been checked.\l"
	.string "It isn't for sale first.\p"
	.string "And it rebuilds animals, not bones.\n"
	.string "It can't tell you where to dig. I'm\l"
	.string "not sure anything can.$"

StrataFieldStation_Text_StoryKessler3::
	.string "KESSLER: Every spring the rain takes\n"
	.string "bones nobody came to collect,\l"
	.string "Doctor. That's not a theory.\p"
	.string "My door stays open.$"

StrataFieldStation_Text_StoryKessler4::
	.string "THEO: Was that a fossil dealer?\n"
	.string "He wants to prospect with a fancy\l"
	.string "diorama?\p"
	.string "DR. HALVORSEN: THEO.\p"
	.string "THEO: I'm only saying. A toy can't\n"
	.string "find a fossil. It can barely find\l"
	.string "its own mistakes.$"

StrataFieldStation_Text_StoryKessler5::
	.string "DR. HALVORSEN: He's half right about\n"
	.string "the rain, {PLAYER}. Bones do erode\l"
	.string "away if nobody collects them.\p"
	.string "But a bone sold without its layer\n"
	.string "has lost most of what it could\l"
	.string "tell us. Remember that.$"

StrataFieldStation_Text_StoryJosie1::
	.string "JOSIE: {PLAYER}! There you are.\p"
	.string "I took the short way home, across\n"
	.string "SAND ARROYO. The BLM ground.\p"
	.string "There's a pit dug into the slope.\n"
	.string "Fresh pick marks. A plaster jacket\l"
	.string "cracked open and left behind.\p"
	.string "No stakes, no field numbers,\n"
	.string "nothing written down.$"

StrataFieldStation_Text_StoryJosie2::
	.string "DR. HALVORSEN: Then whatever came\n"
	.string "out of it has lost its layer, and\l"
	.string "its date with it.\p"
	.string "Nobody touches it. {PLAYER}, you have\n"
	.string "the permit. Go and look, and take\l"
	.string "careful notes.\p"
	.string "JOSIE: I'll call RANGER ORTIZ. She\n"
	.string "said to, if we ever saw a hole that\l"
	.string "shouldn't be there.$"

StrataFieldStation_Text_StoryRefusal1::
	.string "KESSLER: Doctor. I'll be brief this\n"
	.string "time.\p"
	.string "Word in JORDAN is that you retire\n"
	.string "at the end of the season, and the\l"
	.string "university means to sell the rig.$"

StrataFieldStation_Text_StoryRefusal2::
	.string "KESSLER: I'll fund it instead. Five\n"
	.string "years: staff, power, repairs.\p"
	.string "In return, a first look at every\n"
	.string "survey your crew runs on private\l"
	.string "land. Nothing illegal in that.\p"
	.string "DR. HALVORSEN: No. Nothing illegal.\p"
	.string "But a first look means everyone\n"
	.string "else looks second. Data sold first\l"
	.string "is data someone can bend.\p"
	.string "Thank you, MR. KESSLER. No.$"

StrataFieldStation_Text_StoryRefusal3::
	.string "KESSLER: Your student may see it\n"
	.string "differently. MR. OKAFOR, your grant\l"
	.string "ends in the spring, I believe?\p"
	.string "THEO: …It does.\p"
	.string "KESSLER: My card. The offer is for\n"
	.string "whoever runs the rig next.$"

StrataFieldStation_Text_StoryRefusal4::
	.string "THEO: Three more years of funding.\n"
	.string "I won't pretend I don't want it.\p"
	.string "DR. HALVORSEN: It's your choice,\n"
	.string "THEO. I won't think less of you.\p"
	.string "THEO: I'm keeping the card. That's\n"
	.string "all. I'm just keeping the card.$"

StrataFieldStation_Text_StoryConsortium1::
	.string "DR. HALVORSEN: {PLAYER}, a moment.\n"
	.string "RANGER ORTIZ told me about the\l"
	.string "citation.\p"
	.string "The sale is legal. We can't stop it,\n"
	.string "and I don't think we should try.\p"
	.string "But we can make BEA a better offer\n"
	.string "than a dealer's auction.\p"
	.string "Three museums and the county have\n"
	.string "agreed to pool what they have. A\l"
	.string "consortium.$"

StrataFieldStation_Text_StoryConsortium2::
	.string "It will probably be less money than\n"
	.string "the top bid. I won't pretend\l"
	.string "otherwise.\p"
	.string "What it buys is a Pair that stays\n"
	.string "together, in public, where anyone\l"
	.string "can study it and check our work.\p"
	.string "The museums want a research case:\n"
	.string "proof this crew does work worth\l"
	.string "funding. That's your CODEX.\p"
	.string "{STR_VAR_1} species so far, each tied to\n"
	.string "its layer. Keep catching and\l"
	.string "logging. I'll take it to the\l"
	.string "auction.$"

StrataFieldStation_Text_VisitorKessler::
	.string "KESSLER: Don't mind me. I was just\n"
	.string "leaving.$"

StrataFieldStation_Text_VisitorTheo::
	.string "THEO: Not now.$"

StrataFieldStation_Text_VisitorJosie::
	.string "JOSIE: Come on, come on…$"
