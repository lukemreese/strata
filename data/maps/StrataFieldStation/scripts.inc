@ Field station at the Hell Creek camp: the STRATA reconstruction rig.
@ VAR_STRATA_STORY: 0 new game, 1 starter chosen, 2 entered Hell Creek, 3 tyrannosaur met

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
	goto_if_eq VAR_STRATA_STORY, 3, StrataFieldStation_EventScript_MentorAfterTyrannosaur
	goto_if_eq VAR_STRATA_STORY, 2, StrataFieldStation_EventScript_MentorInHellCreek
	msgbox StrataFieldStation_Text_RigReady, MSGBOX_DEFAULT
	release
	end

StrataFieldStation_EventScript_MentorInHellCreek::
	msgbox StrataFieldStation_Text_InHellCreek, MSGBOX_DEFAULT
	release
	end

StrataFieldStation_EventScript_MentorAfterTyrannosaur::
	msgbox StrataFieldStation_Text_AfterTyrannosaur, MSGBOX_DEFAULT
	release
	end

StrataFieldStation_EventScript_Rig::
	lockall
	goto_if_eq VAR_STRATA_STORY, 0, StrataFieldStation_EventScript_RigIdle
	msgbox StrataFieldStation_Text_EnterHellCreek, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, StrataFieldStation_EventScript_RigCancel
	call_if_eq VAR_STRATA_STORY, 1, StrataFieldStation_EventScript_FirstEntry
	playse SE_WARP_IN
	warp MAP_STRATA_LEVEE, 18, 30
	waitstate
	releaseall
	end

StrataFieldStation_EventScript_FirstEntry::
	setvar VAR_0x8004, ERA_HELL_CREEK
	special Strata_AdvanceEra
	setvar VAR_STRATA_STORY, 2
	return

StrataFieldStation_EventScript_RigIdle::
	msgbox StrataFieldStation_Text_RigIdle, MSGBOX_DEFAULT
	releaseall
	end

StrataFieldStation_EventScript_RigCancel::
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

StrataFieldStation_Text_RigReady:
	.string "The rig is calibrated to the Hell\n"
	.string "Creek layer, 66.04 million years ago.$"

StrataFieldStation_Text_InHellCreek:
	.string "You saw tyrannosaur tracks by the\n"
	.string "river? Be careful up on that bluff.$"

StrataFieldStation_Text_AfterTyrannosaur:
	.string "You stood your ground against a\n"
	.string "TYRANNOSAURUS! Remarkable.\p"
	.string "The next layer up holds the\n"
	.string "impact. We're still calibrating\l"
	.string "the rig for it.$"

StrataFieldStation_Text_EnterHellCreek:
	.string "STRATA RIG: Hell Creek Fm, 66.04 Ma.\n"
	.string "Enter the reconstruction?$"

StrataFieldStation_Text_RigIdle:
	.string "The rig hums quietly. DR. HALVORSEN\n"
	.string "should explain it first.$"
