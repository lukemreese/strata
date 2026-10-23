@ Act 8: Ice Age steppe, Wyoming, ~20,000 years ago. The hub of the act: the arrival and
@ anchor, a pair of American lions in the corridor to the sinkhole, the sinkhole itself
@ (Natural Trap Cave), the way north to the Ice Margin and east to the Meltwater River, and,
@ once the cave boss is done, the marker for the late-glacial Colby sub-layer.
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

@ The American lion pair (a wild double battle, Lv 48/48), the act's mini-boss. They sit in
@ the corridor to the sinkhole. Triggered by the line across it or by talking to either lion;
@ once, whatever the outcome (running is allowed: they have no quarrel with you).
StrataSteppe_EventScript_Lions::
	lockall
	playmoncry SPECIES_PANTHERA, CRY_MODE_ENCOUNTER
	msgbox StrataSteppe_Text_LionsAppear, MSGBOX_DEFAULT
	waitmoncry
	setwildbattle SPECIES_PANTHERA, 48, ITEM_NONE, SPECIES_PANTHERA, 48
	dowildbattle
	setvar VAR_STRATA_ACT8, 1
	setflag FLAG_STRATA_A8_LIONS_GONE
	removeobject LOCALID_STRATA_STEPPE_LION_A
	removeobject LOCALID_STRATA_STEPPE_LION_B
	msgbox StrataSteppe_Text_LionsGone, MSGBOX_DEFAULT
	giveitem ITEM_CARRION
	releaseall
	end

@ The marker beside the anchor. Locked until the cave boss is done (story value 17).
StrataSteppe_EventScript_SubLayer::
	lockall
	goto_if_ge VAR_STRATA_STORY, STORY_ACT_DONE(ERA_TRAP_CAVE), StrataSteppe_EventScript_SubLayerOpen
	msgbox StrataSteppe_Text_SubLayerLocked, MSGBOX_DEFAULT
	releaseall
	end

StrataSteppe_EventScript_SubLayerOpen::
	msgbox StrataSteppe_Text_SubLayerOpen, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, StrataSteppe_EventScript_SubLayerNo
	playse SE_WARP_IN
	warp MAP_STRATA_COLBY, STRATA_ARRIVAL_COLBY
	waitstate
	releaseall
	end

StrataSteppe_EventScript_SubLayerNo::
	releaseall
	end

StrataSteppe_EventScript_NoteSteppe::
	msgbox StrataSteppe_Text_NoteSteppe, MSGBOX_SIGN
	end

StrataSteppe_EventScript_NotePronghorn::
	msgbox StrataSteppe_Text_NotePronghorn, MSGBOX_SIGN
	end

StrataSteppe_EventScript_NoteWolf::
	msgbox StrataSteppe_Text_NoteWolf, MSGBOX_SIGN
	end

StrataSteppe_EventScript_NoteSinkhole::
	msgbox StrataSteppe_Text_NoteSinkhole, MSGBOX_SIGN
	end

StrataSteppe_Text_Sinkhole:
	.string "Snow hides the lip of a deep hole:\n"
	.string "NATURAL TRAP CAVE.\p"
	.string "Animals that stumble in can't climb\n"
	.string "out. Lower yourself in on a rope?$"

StrataSteppe_Text_LionsAppear:
	.string "Two tawny shapes rise from the\n"
	.string "snow-crusted grass. AMERICAN LIONS,\l"
	.string "bigger than any lion alive today.\p"
	.string "They are between you and the\n"
	.string "sinkhole, and they have seen you!$"

StrataSteppe_Text_LionsGone:
	.string "The pair pad off toward the ice,\n"
	.string "unhurried. Hunting here is a long\l"
	.string "game, and you are not on the menu.\p"
	.string "They leave scraps of an old kill.$"

StrataSteppe_Text_SubLayerLocked:
	.string "A second marker stands by the\n"
	.string "anchor, dark and dusty.\p"
	.string "SUB-LAYER: LATE GLACIAL, ~13,000\n"
	.string "years ago. LOCKED.\p"
	.string "The rig opens it once this layer's\n"
	.string "record is read.$"

StrataSteppe_Text_SubLayerOpen:
	.string "The second marker glows.\p"
	.string "SUB-LAYER: LATE GLACIAL, ~13,000\n"
	.string "years ago. Colby, Bighorn Basin.\p"
	.string "A thin slice with bones and stone,\n"
	.string "and no animals. Load it?$"

StrataSteppe_Text_NoteSteppe:
	.string "FIELD NOTE: Steppe\p"
	.string "Cold, dry ground of grasses,\n"
	.string "sedges, sagebrush and hardy herbs,\l"
	.string "with trees only in sheltered spots.\p"
	.string "Pollen and old packrat nests across\n"
	.string "the interior West show it.\p"
	.string "Many Ice Age plant and animal mixes\n"
	.string "have no match today.$"

StrataSteppe_Text_NotePronghorn:
	.string "FIELD NOTE: Fast for no reason?\p"
	.string "The pronghorn sprints near 90 km/h,\n"
	.string "faster than any predator now alive\l"
	.string "in North America.\p"
	.string "One hypothesis: it is outrunning\n"
	.string "ghosts, such as the cheetah-like\l"
	.string "MIRACINONYX, now gone. Others say\l"
	.string "it is just stamina. Not settled.$"

StrataSteppe_Text_NoteWolf:
	.string "FIELD NOTE: Which wolf?\p"
	.string "Wolf bones from the cave are\n"
	.string "usually reported as gray wolves,\l"
	.string "not dire wolves.\p"
	.string "The dire wolf, AENOCYON, is known\n"
	.string "mostly from farther south, so no\l"
	.string "AENOCYON is wild here. If your dog\l"
	.string "lineage turned meat-hungry, the rig\l"
	.string "builds one as a stand-in.$"

StrataSteppe_Text_NoteSinkhole:
	.string "FIELD NOTE: Natural Trap Cave\p"
	.string "A sinkhole on the west flank of the\n"
	.string "Bighorn Mountains. The opening is\l"
	.string "small; the drop is about 25 m.\p"
	.string "Cold, steady air in the cave keeps\n"
	.string "bone well, and sometimes DNA.$"
