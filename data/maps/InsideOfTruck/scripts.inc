@ Strata: the new game starts here, in the back of the crew truck (new_game.c WarpToTruck). The
@ stock truck sequence (src/field_special_scene.c) plays: black, the rumble, the stop and the door
@ opening. When the player has control the frame script below says where they are and sets the
@ exit's dynamic warp: the Hell Creek camp (StrataFieldCamp's arrival script walks them on to
@ Dr. Halvorsen, whose station script is the unchanged start of the game).
@ VAR_LITTLEROOT_INTRO_STATE is the stock var of this scene, reused as its once-only guard: it is
@ 0 on a new game and nothing else in Strata reads it.

InsideOfTruck_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, InsideOfTruck_OnLoad
	map_script MAP_SCRIPT_ON_RESUME, InsideOfTruck_OnResume
	map_script MAP_SCRIPT_ON_FRAME_TABLE, InsideOfTruck_OnFrame
	.byte 0

InsideOfTruck_OnLoad:
	setmetatile 4, 1, METATILE_InsideOfTruck_ExitLight_Top, FALSE
	setmetatile 4, 2, METATILE_InsideOfTruck_ExitLight_Mid, FALSE
	setmetatile 4, 3, METATILE_InsideOfTruck_ExitLight_Bottom, FALSE
	end

InsideOfTruck_OnResume:
	setstepcallback STEP_CB_TRUCK
	end

InsideOfTruck_OnFrame:
	map_script_2 VAR_LITTLEROOT_INTRO_STATE, 0, InsideOfTruck_EventScript_Arrival
	.2byte 0

InsideOfTruck_EventScript_Arrival::
	lockall
	msgbox InsideOfTruck_Text_Arrival, MSGBOX_DEFAULT
	setvar VAR_LITTLEROOT_INTRO_STATE, 1
	setdynamicwarp MAP_STRATA_FIELD_CAMP, 26, 20
	releaseall
	end

InsideOfTruck_EventScript_MovingBox::
	msgbox InsideOfTruck_Text_Crate, MSGBOX_SIGN
	end

InsideOfTruck_Text_Arrival::
	.string "The truck lurches, then stops. You\n"
	.string "dozed off on the dirt road out of\l"
	.string "Jordan.\p"
	.string "Dry, bright air rolls in through\n"
	.string "the open door: the Hell Creek\l"
	.string "badlands.$"

InsideOfTruck_Text_Crate::
	.string "The crate is stamped FIELD GEAR:\n"
	.string "plaster jackets, sieves and\l"
	.string "survey stakes.$"
