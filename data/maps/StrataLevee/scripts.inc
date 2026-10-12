StrataLevee_MapScripts::
	.byte 0

@ The south edge of the reconstruction, where the player arrives from camp.
StrataLevee_EventScript_ReconstructionEdge::
	lockall
	msgbox StrataLevee_Text_ReturnToCamp, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, StrataLevee_EventScript_StayInLayer
	playse SE_WARP_OUT
	warp MAP_STRATA_FIELD_STATION, 10, 8
	waitstate
	releaseall
	end

StrataLevee_EventScript_StayInLayer::
	applymovement OBJ_EVENT_ID_PLAYER, StrataLevee_Movement_StepBack
	waitmovement 0
	releaseall
	end

StrataLevee_Movement_StepBack:
	walk_up
	step_end

StrataLevee_Text_ReturnToCamp:
	.string "The air shimmers at the edge of the\n"
	.string "reconstruction. Return to camp?$"
