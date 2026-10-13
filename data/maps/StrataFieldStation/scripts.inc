@ Field station at the Hell Creek camp: the STRATA reconstruction rig.
@ VAR_STRATA_STORY and the acts are described in include/strata_acts.h and
@ src/strata_acts.c, which also holds Dr. Halvorsen's lines for each stage.

StrataFieldStation_MapScripts::
	map_script MAP_SCRIPT_ON_FRAME_TABLE, StrataFieldStation_OnFrame
	.byte 0

StrataFieldStation_OnFrame:
	map_script_2 VAR_STRATA_STORY, 0, StrataFieldStation_EventScript_Intro
	.2byte 0

StrataFieldStation_EventScript_Intro::
	lockall
	msgbox StrataFieldStation_Text_Welcome, MSGBOX_DEFAULT
	special ChooseStarter
	msgbox StrataFieldStation_Text_Lineages, MSGBOX_DEFAULT
	giveitem ITEM_POKE_BALL, 5
	setflag FLAG_SYS_POKEMON_GET
	setflag FLAG_SYS_POKEDEX_GET
	setflag FLAG_SYS_B_DASH
	special EnableNationalPokedex
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
	special Strata_BufferMentorText
	msgbox gStringVar4, MSGBOX_DEFAULT
	release
	end

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
	msgbox StrataFieldStation_Text_LoadLayer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, StrataFieldStation_EventScript_RigCancel
	playse SE_M_EXPLOSION
	special Strata_RigLoadNext
	goto_if_eq VAR_0x8005, 0, StrataFieldStation_EventScript_NoLosses
	goto_if_eq VAR_0x8005, 1, StrataFieldStation_EventScript_OneLoss
	msgbox StrataFieldStation_Text_ManyLosses, MSGBOX_DEFAULT
	goto StrataFieldStation_EventScript_AfterLoad

StrataFieldStation_EventScript_OneLoss::
	msgbox StrataFieldStation_Text_OneLoss, MSGBOX_DEFAULT
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
	.string "with it, shaped by how it lived.\p"
	.string "Here, take some specimen capsules.$"

StrataFieldStation_Text_Codex:
	.string "Your FIELD CODEX will log every\n"
	.string "species you meet.\p"
	.string "When you're ready, use the rig to\n"
	.string "enter the Hell Creek layer.$"

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

StrataFieldStation_Text_LoadLayer:
	.string "STRATA RIG: {STR_VAR_1}.\n"
	.string "Load the layer?$"

StrataFieldStation_Text_EnterLayer:
	.string "STRATA RIG: {STR_VAR_1}.\n"
	.string "Enter the reconstruction?$"

StrataFieldStation_Text_ManyLosses:
	.string "The rig shudders as the new layer\n"
	.string "loads…\p"
	.string "{STR_VAR_1} and {STR_VAR_2} other\n"
	.string "specimens could not survive. Their\l"
	.string "lineages end here.\p"
	.string "That is what extinction means.$"

StrataFieldStation_Text_OneLoss:
	.string "The rig shudders as the new layer\n"
	.string "loads…\p"
	.string "{STR_VAR_1} could not survive. Its\n"
	.string "lineage ends here.\p"
	.string "That is what extinction means.$"

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
