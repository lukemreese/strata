@ Fossils (src/strata_fossils.c): the rig's loss list after a jump, the Fossil Case (key item,
@ run from the bag by ItemUseOutOfBattle_FossilCase) and the Gentle Deep Time question.

@ After special Strata_RigLoadNext with VAR_0x8005 != 0: every lost animal, one message each
@ (who, then why that era's filter took it), then the Fossil Case on the first loss.
@ Leaves VAR_0x8006 (the rig's "reached today") alone.
Strata_EventScript_ShowLosses::
	buffernumberstring STR_VAR_1, VAR_0x8005
	goto_if_eq VAR_0x8005, 1, Strata_EventScript_ShowLossesOne
	msgbox Strata_Text_LossHeaderMany, MSGBOX_DEFAULT
	goto Strata_EventScript_ShowLossList
Strata_EventScript_ShowLossesOne:
	msgbox Strata_Text_LossHeaderOne, MSGBOX_DEFAULT
Strata_EventScript_ShowLossList:
	setvar VAR_0x8004, 0
Strata_EventScript_ShowLossNext:
	special Strata_BufferLoss
	goto_if_eq VAR_RESULT, FALSE, Strata_EventScript_ShowLossesDone
	msgbox gStringVar4, MSGBOX_DEFAULT
	addvar VAR_0x8004, 1
	goto Strata_EventScript_ShowLossNext
Strata_EventScript_ShowLossesDone:
	goto_if_set FLAG_STRATA_GENTLE_DEEP_TIME, Strata_EventScript_ShowLossesGentle
	msgbox Strata_Text_LossFooter, MSGBOX_DEFAULT
	goto Strata_EventScript_GiveFossilCase
Strata_EventScript_ShowLossesGentle:
	msgbox Strata_Text_LossFooterGentle, MSGBOX_DEFAULT
Strata_EventScript_GiveFossilCase:
	checkitem ITEM_FOSSIL_CASE
	goto_if_eq VAR_RESULT, TRUE, Strata_EventScript_ShowLossesEnd
	msgbox Strata_Text_FossilCaseGift, MSGBOX_DEFAULT
	giveitem ITEM_FOSSIL_CASE
	msgbox Strata_Text_FossilCaseHowTo, MSGBOX_DEFAULT
Strata_EventScript_ShowLossesEnd:
	return

@ The Fossil Case: a scrolling list of fossils with the animal's icon; A reads one, B closes.
Strata_EventScript_FossilCase::
	lockall
	setvar VAR_0x8005, 0
Strata_EventScript_FossilCaseList:
	special Strata_PushFossilList
	goto_if_eq VAR_RESULT, 0, Strata_EventScript_FossilCaseEmpty
	buffernumberstring STR_VAR_1, VAR_RESULT
	message Strata_Text_FossilCaseHeader
	waitmessage
	dynmultistack 0, 0, FALSE, 6, FALSE, VAR_0x8005, DYN_MULTICHOICE_CB_SHOW_PKMN
	goto_if_eq VAR_RESULT, MULTI_B_PRESSED, Strata_EventScript_FossilCaseClose
	copyvar VAR_0x8005, VAR_RESULT
	copyvar VAR_0x8004, VAR_RESULT
	special Strata_BufferFossil
	msgbox gStringVar4, MSGBOX_DEFAULT
	goto Strata_EventScript_FossilCaseList

Strata_EventScript_FossilCaseEmpty:
	msgbox Strata_Text_FossilCaseEmpty, MSGBOX_DEFAULT
Strata_EventScript_FossilCaseClose:
	closemessage
	releaseall
	end

@ New game: how strictly the rig follows the record (S4). Strict is the default (A on the
@ first row); B can't skip the question.
Strata_EventScript_AskDeepTimeMode::
	msgbox Strata_Text_AskDeepTime, MSGBOX_DEFAULT
	message Strata_Text_AskDeepTimeChoose
	waitmessage
	dynmultichoice 18, 6, TRUE, 2, 0, DYN_MULTICHOICE_CB_NONE, Strata_Text_StrictRecord, Strata_Text_GentleRecord
	goto_if_eq VAR_RESULT, 1, Strata_EventScript_ChoseGentle
	clearflag FLAG_STRATA_GENTLE_DEEP_TIME
	msgbox Strata_Text_ChoseStrict, MSGBOX_DEFAULT
	return
Strata_EventScript_ChoseGentle:
	setflag FLAG_STRATA_GENTLE_DEEP_TIME
	msgbox Strata_Text_ChoseGentle, MSGBOX_DEFAULT
	return

Strata_Text_LossHeaderOne:
	.string "The rig shudders as the new layer\n"
	.string "loads…\p"
	.string "One of your animals could not\n"
	.string "survive it.$"

Strata_Text_LossHeaderMany:
	.string "The rig shudders as the new layer\n"
	.string "loads…\p"
	.string "{STR_VAR_1} of your animals could not\n"
	.string "survive it.$"

Strata_Text_LossFooter:
	.string "Their lineages end here.\n"
	.string "That is what extinction means.$"

Strata_Text_LossFooterGentle:
	.string "The record ends those lineages.\n"
	.string "The gentle record lets their\l"
	.string "relatives carry on in your team.$"

Strata_Text_FossilCaseGift:
	.string "DR. HALVORSEN: I'm sorry. Here,\n"
	.string "this is for what the rock keeps.$"

Strata_Text_FossilCaseHowTo:
	.string "The FOSSIL CASE holds every\n"
	.string "lineage the record takes from you.\p"
	.string "Open it from the KEY ITEMS pocket\n"
	.string "of your BAG.$"

Strata_Text_FossilCaseHeader:
	.string "FOSSIL CASE. Lost lineages: {STR_VAR_1}.\n"
	.string "Which fossil?$"

Strata_Text_FossilCaseEmpty:
	.string "The FOSSIL CASE is empty.\n"
	.string "No lineage you carried is lost.$"

Strata_Text_AskDeepTime:
	.string "One more thing. The rig follows\n"
	.string "the fossil record.\p"
	.string "When a layer's record ends a\n"
	.string "lineage, an animal of it you\l"
	.string "carry is lost. That is the strict\l"
	.string "record.\p"
	.string "In the gentle record, a related\n"
	.string "survivor takes its place instead.\l"
	.string "Its fossil is kept either way.$"

Strata_Text_AskDeepTimeChoose:
	.string "Which record should the rig\n"
	.string "follow? You can't change it later.$"

Strata_Text_StrictRecord:
	.string "Strict record$"

Strata_Text_GentleRecord:
	.string "Gentle record$"

Strata_Text_ChoseStrict:
	.string "The strict record, then. Every\n"
	.string "loss will be real.$"

Strata_Text_ChoseGentle:
	.string "The gentle record, then. The rock\n"
	.string "still keeps what it keeps.$"
