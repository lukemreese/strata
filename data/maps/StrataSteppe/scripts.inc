@ Act 8: Ice Age steppe, Wyoming, ~20,000 years ago.
StrataSteppe_MapScripts::
	.byte 0

StrataSteppe_EventScript_Sinkhole::
	lockall
	msgbox StrataSteppe_Text_Sinkhole, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, StrataSteppe_EventScript_StayOut
	playse SE_FALL
	warp MAP_STRATA_TRAP_CAVE, STRATA_ARRIVAL_TRAP_CAVE
	waitstate
	releaseall
	end

StrataSteppe_EventScript_StayOut::
	applymovement OBJ_EVENT_ID_PLAYER, StrataSteppe_Movement_StepBack
	waitmovement 0
	releaseall
	end

StrataSteppe_Movement_StepBack:
	walk_up
	step_end

StrataSteppe_Text_Sinkhole:
	.string "Snow hides the lip of a deep hole:\n"
	.string "NATURAL TRAP CAVE.\p"
	.string "Animals that stumble in can't climb\n"
	.string "out. Lower yourself in on a rope?$"
