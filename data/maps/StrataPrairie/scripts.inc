@ Epilogue: the Montana prairie today.
StrataPrairie_MapScripts::
	.byte 0

StrataPrairie_EventScript_TrailToCamp::
	lockall
	msgbox StrataPrairie_Text_TrailToCamp, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, StrataPrairie_EventScript_Stay
	warp MAP_STRATA_FIELD_CAMP, 2, 8
	waitstate
	releaseall
	end

StrataPrairie_EventScript_Stay::
	releaseall
	end

StrataPrairie_Text_TrailToCamp:
	.string "The ranch road back to the Hell\n"
	.string "Creek camp. Head back?$"
