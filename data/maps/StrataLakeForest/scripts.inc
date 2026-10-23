@ Act 5: the Green River lakes and Bridger Basin, Wyoming, ~52-46 Ma.
@ Bridger Shore (this map): the rig's arrival point, the lake, and the Uintatherium boss on
@ the south beach. The bull is an object hidden by FLAG_STRATA_A5_BULL_HIDDEN (set on every
@ map load); crossing the boss line clears the flag, spawns the bull at the edge of the
@ screen's reach and has it charge along the shore to the player, then the battle starts.
StrataLakeForest_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, StrataLakeForest_OnTransition
	.byte 0

StrataLakeForest_OnTransition:
	setflag FLAG_STRATA_A5_BULL_HIDDEN
	end

@ The boss line. Two lanes cross y = 61: the beach lane west of the cliff (x 14-20) and
@ the grass lane east of it (x 24-39). The bull comes along row 62 from the east edge
@ for the grass lane (a run of 39 - x steps), and up the beach from row 65 (3 steps) for
@ the beach lane. VAR_0x8004 = player x, VAR_0x8006 = steps left.
StrataLakeForest_EventScript_Uintatherium::
	lockall
	getplayerxy VAR_0x8004, VAR_0x8005
	setvar VAR_0x8006, 39
	subvar VAR_0x8006, VAR_0x8004
	setobjectxyperm LOCALID_STRATA_A5_BULL, 39, 62
	clearflag FLAG_STRATA_A5_BULL_HIDDEN
	addobject LOCALID_STRATA_A5_BULL
	playmoncry SPECIES_UINTATHERIUM, CRY_MODE_ENCOUNTER
	msgbox StrataLakeForest_Text_BullCharges, MSGBOX_DEFAULT
	waitmoncry
StrataLakeForest_EventScript_BullChargeEast:
	goto_if_eq VAR_0x8006, 0, StrataLakeForest_EventScript_BullArrives
	applymovement LOCALID_STRATA_A5_BULL, StrataLakeForest_Movement_ChargeLeft
	waitmovement 0
	subvar VAR_0x8006, 1
	goto StrataLakeForest_EventScript_BullChargeEast

StrataLakeForest_EventScript_UintatheriumWest::
	lockall
	getplayerxy VAR_0x8004, VAR_0x8005
	setobjectxyperm LOCALID_STRATA_A5_BULL, VAR_0x8004, 65
	clearflag FLAG_STRATA_A5_BULL_HIDDEN
	addobject LOCALID_STRATA_A5_BULL
	playmoncry SPECIES_UINTATHERIUM, CRY_MODE_ENCOUNTER
	msgbox StrataLakeForest_Text_BullCharges, MSGBOX_DEFAULT
	waitmoncry
	applymovement LOCALID_STRATA_A5_BULL, StrataLakeForest_Movement_ChargeUp
	waitmovement 0
	goto StrataLakeForest_EventScript_BullArrives

StrataLakeForest_EventScript_BullArrives::
	applymovement LOCALID_STRATA_A5_BULL, StrataLakeForest_Movement_FaceUp
	waitmovement 0
	msgbox StrataLakeForest_Text_UintatheriumAppears, MSGBOX_DEFAULT
	strata_boss_prep atk=1
	setwildbattle SPECIES_UINTATHERIUM, 34
	dowildbattle
	strata_boss_done
	specialvar VAR_RESULT, GetBattleOutcome
	removeobject LOCALID_STRATA_A5_BULL
	setflag FLAG_STRATA_A5_BULL_HIDDEN
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, StrataLakeForest_EventScript_Ran
	setvar VAR_STRATA_STORY, 11
	msgbox StrataLakeForest_Text_UintatheriumDone, MSGBOX_DEFAULT
	releaseall
	end

StrataLakeForest_EventScript_Ran::
	msgbox StrataLakeForest_Text_Ran, MSGBOX_DEFAULT
	releaseall
	end

@ The bull is only on screen during the charge; nothing to say to it.
StrataLakeForest_EventScript_BullTalk::
	end

StrataLakeForest_Movement_ChargeLeft:
	walk_fast_left
	step_end

StrataLakeForest_Movement_ChargeUp:
	walk_fast_up
	walk_fast_up
	walk_fast_up
	step_end

StrataLakeForest_Movement_FaceUp:
	face_up
	step_end

@ ---- field notes -----------------------------------------------------------------

StrataLakeForest_EventScript_NoteLake::
	msgbox StrataLakeForest_Text_NoteLake, MSGBOX_SIGN
	end

StrataLakeForest_EventScript_NoteClimate::
	msgbox StrataLakeForest_Text_NoteClimate, MSGBOX_SIGN
	end

StrataLakeForest_EventScript_NoteShallows::
	msgbox StrataLakeForest_Text_NoteShallows, MSGBOX_SIGN
	end

StrataLakeForest_EventScript_NoteUintatheres::
	msgbox StrataLakeForest_Text_NoteUintatheres, MSGBOX_SIGN
	end

StrataLakeForest_Text_NoteLake:
	.string "FIELD NOTE: LAKE GOSIUTE\p"
	.string "A broad, shallow lake lay across\n"
	.string "southwest Wyoming. Its mud became\l"
	.string "the Green River Formation.\p"
	.string "The lake muds here are about 53 to\n"
	.string "48 million years old. The Bridger\l"
	.string "beds beside them: about 50 to 46.$"

StrataLakeForest_Text_NoteClimate:
	.string "FIELD NOTE: THE LONG COOLING\p"
	.string "Leaf shapes and isotopes in these\n"
	.string "beds point to a warm, frost-free\l"
	.string "forest (about 20 C a year; the\l"
	.string "estimates vary).\p"
	.string "The peak of the warmth was near 52\n"
	.string "million years ago. After that the\l"
	.string "world cooled, slowly, for 20 million\l"
	.string "years.$"

StrataLakeForest_Text_NoteShallows:
	.string "FIELD NOTE: THE SHALLOWS\p"
	.string "Gars, stingrays and crocodilians\n"
	.string "crowd these shallows.\p"
	.string "A lineage that wades, fishes or\n"
	.string "stands at the water's edge takes\l"
	.string "on the water's habits.$"

StrataLakeForest_Text_NoteUintatheres:
	.string "FIELD NOTE: UINTATHERES\p"
	.string "Six bony knobs on the skull, and\n"
	.string "long upper canines in the males.\l"
	.string "Probably for display and sparring.\p"
	.string "About a rhino's size: estimates run\n"
	.string "to 2 tonnes. The brain was tiny.$"

@ ---- the boss --------------------------------------------------------------------

StrataLakeForest_Text_BullCharges:
	.string "Hooves pound the gravel. Something\n"
	.string "big is charging along the shore!$"

StrataLakeForest_Text_UintatheriumAppears:
	.string "A bull with six bony knobs on its\n"
	.string "head and long upper tusks skids to\l"
	.string "a halt.\p"
	.string "A UINTATHERIUM!$"

StrataLakeForest_Text_UintatheriumDone:
	.string "The UINTATHERIUM lumbers away into\n"
	.string "the forest.\p"
	.string "Fish die in schools here and sink\n"
	.string "into the still lake mud. Millions\l"
	.string "of years from now, they'll be found\l"
	.string "whole.\p"
	.string "Report back to DR. HALVORSEN.$"

StrataLakeForest_Text_Ran:
	.string "You back away along the shore. The\n"
	.string "UINTATHERIUM stamps, wheels around\l"
	.string "and lumbers off. For now.$"
