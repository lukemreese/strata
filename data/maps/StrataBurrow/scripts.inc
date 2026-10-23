@ Act 2: the Burrow Refuge, where small mammals waited the impact winter out. The stock
@ Island Cave chamber, with a seed cache (browse) on the floor.
StrataBurrow_MapScripts::
	.byte 0

@ Stepping down toward the glowing slab offers the climb back into the ash.
StrataBurrow_EventScript_Exit::
	lockall
	msgbox StrataBurrow_Text_Exit, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, StrataBurrow_EventScript_Stay
	playse SE_WARP_OUT
	warp MAP_STRATA_LEVEE_WINTER, 9, 23
	waitstate
	releaseall
	end

StrataBurrow_EventScript_Stay::
	applymovement OBJ_EVENT_ID_PLAYER, StrataBurrow_Movement_StepBack
	waitmovement 0
	releaseall
	end

StrataBurrow_Movement_StepBack:
	walk_up
	step_end

StrataBurrow_EventScript_NoteCache::
	msgbox StrataBurrow_Text_NoteCache, MSGBOX_SIGN
	end

StrataBurrow_EventScript_NoteBurrowers::
	msgbox StrataBurrow_Text_NoteBurrowers, MSGBOX_SIGN
	end

StrataBurrow_Text_Exit:
	.string "Climb back out into the ash?$"

StrataBurrow_Text_NoteCache:
	.string "FIELD NOTE: A seed cache\p"
	.string "Small seed-eating mammals may have\n"
	.string "lived on stored food through the\l"
	.string "dark months.\p"
	.string "Inferred: no hoard is preserved.\n"
	.string "The rig put this one here.$"

StrataBurrow_Text_NoteBurrowers:
	.string "FIELD NOTE: Burrowers\p"
	.string "Small animals, and animals that\n"
	.string "sheltered underground or in water,\l"
	.string "lost the fewest species.\p"
	.string "Burrowing is a leading explanation,\n"
	.string "but it is hard to prove from bones.$"
