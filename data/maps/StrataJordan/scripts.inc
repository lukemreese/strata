@ Jordan (present day): the county seat, a ranch road west of camp. General store,
@ café, and the BLM field office (Ranger Ortiz). The highway west leads to the
@ prairie once the present layer is loaded (the epilogue).
StrataJordan_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, StrataJordan_OnTransition
	.byte 0

StrataJordan_OnTransition:
	special Strata_HideLockedReviewers
	end

@ Visiting researchers (peer review, C13): the ichnologist (act 6) and the volcanologist
@ (act 7). One battle each.
StrataJordan_EventScript_Oskar::
	lock
	faceplayer
	trainerbattle_single TRAINER_STRATA_REVIEW_ACT6, StrataJordan_Text_OskarIntro, StrataJordan_Text_OskarDefeat, StrataJordan_EventScript_OskarWon
	msgbox StrataJordan_Text_OskarAfter, MSGBOX_DEFAULT
	release
	end

StrataJordan_EventScript_OskarWon::
	msgbox StrataJordan_Text_OskarNote, MSGBOX_DEFAULT
	releaseall
	end

StrataJordan_EventScript_Hollis::
	lock
	faceplayer
	trainerbattle_single TRAINER_STRATA_REVIEW_ACT7, StrataJordan_Text_HollisIntro, StrataJordan_Text_HollisDefeat, StrataJordan_EventScript_HollisWon
	msgbox StrataJordan_Text_HollisAfter, MSGBOX_DEFAULT
	release
	end

StrataJordan_EventScript_HollisWon::
	msgbox StrataJordan_Text_HollisNote, MSGBOX_DEFAULT
	releaseall
	end

StrataJordan_Text_OskarIntro:
	.string "OSKAR: Ichnology: I study tracks,\n"
	.string "burrows and bite marks. What the\l"
	.string "animals did, not the animals.\p"
	.string "A bone can be moved. A track stays\n"
	.string "where it was made. The White River\l"
	.string "trackways are the real record.\p"
	.string "Peer review: your animals against\n"
	.string "my footprints.$"

StrataJordan_Text_OskarDefeat:
	.string "OSKAR: You move the way the tracks\n"
	.string "say. Good.$"

StrataJordan_Text_OskarNote:
	.string "OSKAR: Field note.\p"
	.string "A trace fossil is a behaviour.\n"
	.string "A burrow is a burrow, whoever dug\l"
	.string "it. A trackway shows speed, and\l"
	.string "company.\p"
	.string "Parallel tracks mean a herd, all\n"
	.string "heading the same way.$"

StrataJordan_Text_OskarAfter:
	.string "OSKAR: Bones tell you what lived\n"
	.string "there. Tracks tell you what it was\l"
	.string "doing.$"

StrataJordan_Text_HollisIntro:
	.string "HOLLIS: Volcanologist. The ash at\n"
	.string "Ashfall blew in from a vent over\l"
	.string "1,600 kilometres away, and it\l"
	.string "buried a waterhole.\p"
	.string "Your run sat under that haze,\n"
	.string "didn't it? Let's compare\l"
	.string "reconstructions. Peer review.$"

StrataJordan_Text_HollisDefeat:
	.string "HOLLIS: Your animals handled the\n"
	.string "ash better than my models do.$"

StrataJordan_Text_HollisNote:
	.string "HOLLIS: Field note.\p"
	.string "Nothing died in the eruption.\n"
	.string "They died weeks later, slowly, at\l"
	.string "the water, breathing fine ash.\p"
	.string "Small animals went first, rhinos\n"
	.string "last. The bones lie in that order.$"

StrataJordan_Text_HollisAfter:
	.string "HOLLIS: A thin ash fall, far from\n"
	.string "the vent. Still enough to end a\l"
	.string "waterhole.$"

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
