@ Jordan (present day): the county seat, a ranch road west of camp. General store,
@ café, and the BLM field office (Ranger Ortiz). The highway west leads to the
@ prairie once the present layer is loaded (the epilogue).
StrataJordan_MapScripts::
	.byte 0

StrataJordan_EventScript_Highway::
	lockall
	goto_if_lt VAR_STRATA_STORY, STORY_IN_ACT(ERA_EPILOGUE), StrataJordan_EventScript_HighwayClosed
	warp MAP_STRATA_PRAIRIE, STRATA_ARRIVAL_PRAIRIE
	waitstate
	releaseall
	end

StrataJordan_EventScript_HighwayClosed::
	msgbox StrataJordan_Text_HighwayClosed, MSGBOX_DEFAULT
	applymovement OBJ_EVENT_ID_PLAYER, StrataJordan_Movement_StepBack
	waitmovement 0
	releaseall
	end

StrataJordan_Movement_StepBack:
	walk_right
	step_end

StrataJordan_EventScript_Rancher::
	lock
	faceplayer
	goto_if_ge VAR_STRATA_STORY, STORY_ACT_DONE(ERA_HELL_CREEK), StrataJordan_EventScript_RancherLater
	msgbox StrataJordan_Text_Rancher, MSGBOX_DEFAULT
	release
	end

StrataJordan_EventScript_RancherLater::
	msgbox StrataJordan_Text_RancherLater, MSGBOX_DEFAULT
	release
	end

StrataJordan_EventScript_Local::
	msgbox StrataJordan_Text_Local, MSGBOX_NPC
	end

StrataJordan_EventScript_TownSign::
	msgbox StrataJordan_Text_TownSign, MSGBOX_SIGN
	end

StrataJordan_EventScript_OfficeSign::
	msgbox StrataJordan_Text_OfficeSign, MSGBOX_SIGN
	end

StrataJordan_EventScript_LawNote::
	msgbox StrataJordan_Text_LawNote, MSGBOX_SIGN
	end

StrataJordan_Text_HighwayClosed:
	.string "The highway west. It's a long way to\n"
	.string "anywhere from here.\p"
	.string "The dig season isn't over yet.$"

StrataJordan_Text_Rancher:
	.string "You're with the college dig? Heard\n"
	.string "a fella say a good T. REX tooth\l"
	.string "sells for more than a steer.\p"
	.string "And there's a dealer's truck parked\n"
	.string "at the LINDQVIST place every day\l"
	.string "this week. Folks talk.$"

StrataJordan_Text_RancherLater:
	.string "Still no rain. Half the stock ponds\n"
	.string "in the county are mud.\p"
	.string "Can't blame a rancher for listening\n"
	.string "when money comes knocking.$"

StrataJordan_Text_Local:
	.string "Jordan's small, but we've got a café,\n"
	.string "a store, and more dinosaurs than\l"
	.string "people, if you count the dead ones.$"

StrataJordan_Text_TownSign:
	.string "JORDAN\n"
	.string "Garfield County seat. Ranch country.$"

StrataJordan_Text_OfficeSign:
	.string "BUREAU OF LAND MANAGEMENT\n"
	.string "Field office. Permits inside.$"

StrataJordan_Text_LawNote:
	.string "FIELD NOTE: In Montana, fossils on\n"
	.string "private land go with the surface\l"
	.string "land, and the owner may sell them.\p"
	.string "On federal land they're public\n"
	.string "property. Digging vertebrate fossils\l"
	.string "there needs a permit, and the finds\l"
	.string "go to a public museum.$"
