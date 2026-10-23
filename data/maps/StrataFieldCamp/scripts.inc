StrataFieldCamp_MapScripts::
	.byte 0

@ The ranch road west to the prairie opens once the present layer is loaded.
StrataFieldCamp_EventScript_PrairieRoad::
	lockall
	goto_if_lt VAR_STRATA_STORY, STORY_IN_ACT(ERA_EPILOGUE), StrataFieldCamp_EventScript_RoadClosed
	warp MAP_STRATA_PRAIRIE, STRATA_ARRIVAL_PRAIRIE
	waitstate
	releaseall
	end

StrataFieldCamp_EventScript_RoadClosed::
	msgbox StrataFieldCamp_Text_RoadClosed, MSGBOX_DEFAULT
	applymovement OBJ_EVENT_ID_PLAYER, StrataFieldCamp_Movement_StepBack
	waitmovement 0
	releaseall
	end

StrataFieldCamp_Movement_StepBack:
	walk_right
	step_end

StrataFieldCamp_Text_RoadClosed:
	.string "The ranch road west is fenced off\n"
	.string "during the dig season.$"

StrataFieldCamp_EventScript_Crew::
	msgbox StrataFieldCamp_Text_Crew, MSGBOX_NPC
	end

StrataFieldCamp_EventScript_Student::
	msgbox StrataFieldCamp_Text_Student, MSGBOX_NPC
	end

StrataFieldCamp_EventScript_CampSign::
	msgbox StrataFieldCamp_Text_CampSign, MSGBOX_SIGN
	end

StrataFieldCamp_EventScript_StationSign::
	msgbox StrataFieldCamp_Text_StationSign, MSGBOX_SIGN
	end

StrataFieldCamp_Text_Crew:
	.string "The badlands erode a little every\n"
	.string "rain, so new bones turn up each\l"
	.string "spring.\p"
	.string "Mostly we find turtle shell and gar\n"
	.string "scales. A T. rex is the jackpot!$"

StrataFieldCamp_Text_Student:
	.string "See the stripes in the hills? Each\n"
	.string "band is old floodplain mud.\p"
	.string "Lower is older. Climbing the hill is\n"
	.string "climbing forward in time!$"

StrataFieldCamp_Text_CampSign:
	.string "HELL CREEK FIELD CAMP\n"
	.string "Garfield County, Montana$"

StrataFieldCamp_Text_StationSign:
	.string "FIELD STATION\n"
	.string "STRATA reconstruction rig inside.$"

@ The camp store: the quartermaster's stock grows with the story. Great Balls and Super
@ Potions come once the Corral Bluffs act (3) is done, Hyper Potions after White River (6).
StrataFieldCamp_EventScript_Quartermaster::
	lock
	faceplayer
	msgbox StrataFieldCamp_Text_QuartermasterWelcome, MSGBOX_DEFAULT
	goto_if_ge VAR_STRATA_STORY, STORY_ACT_DONE(ERA_WHITE_RIVER), StrataFieldCamp_EventScript_StoreTier2
	goto_if_ge VAR_STRATA_STORY, STORY_ACT_DONE(ERA_CORRAL_BLUFFS), StrataFieldCamp_EventScript_StoreTier1
	pokemart StrataFieldCamp_Pokemart_Tier0
	goto StrataFieldCamp_EventScript_StoreBye

StrataFieldCamp_EventScript_StoreTier1::
	pokemart StrataFieldCamp_Pokemart_Tier1
	goto StrataFieldCamp_EventScript_StoreBye

StrataFieldCamp_EventScript_StoreTier2::
	pokemart StrataFieldCamp_Pokemart_Tier2
StrataFieldCamp_EventScript_StoreBye::
	msgbox StrataFieldCamp_Text_QuartermasterBye, MSGBOX_DEFAULT
	release
	end

	.align 2
StrataFieldCamp_Pokemart_Tier0:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	pokemartlistend

	.align 2
StrataFieldCamp_Pokemart_Tier1:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	pokemartlistend

	.align 2
StrataFieldCamp_Pokemart_Tier2:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	pokemartlistend

StrataFieldCamp_Text_QuartermasterWelcome:
	.string "MARGE, QUARTERMASTER: Field supplies\n"
	.string "are on the camp budget. What'll it be?$"

StrataFieldCamp_Text_QuartermasterBye:
	.string "MARGE: Bring back every specimen\n"
	.string "capsule you don't use. They're not\l"
	.string "cheap.$"
