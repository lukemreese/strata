@ Lindqvist Ranch (present day): Bea Lindqvist's land, between camp and Jordan.
@ The Pair (a Triceratops and a Tyrannosaurus buried together) lies under a tarp in
@ the cottonwood ring. Wade Kessler and one of his crew are here pitching Bea until
@ the Hell Creek act is done (FLAG_TEMP_1F hides them after that).
StrataLindqvistRanch_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, StrataLindqvistRanch_OnTransition
	.byte 0

StrataLindqvistRanch_OnTransition:
	call_if_ge VAR_STRATA_STORY, STORY_ACT_DONE(ERA_HELL_CREEK), StrataLindqvistRanch_EventScript_KesslerGone
	end

StrataLindqvistRanch_EventScript_KesslerGone::
	setflag FLAG_TEMP_1F
	return

StrataLindqvistRanch_EventScript_Bea::
	lock
	faceplayer
	goto_if_ge VAR_STRATA_STORY, STORY_ACT_DONE(ERA_HELL_CREEK), StrataLindqvistRanch_EventScript_BeaLater
	msgbox StrataLindqvistRanch_Text_BeaAct0, MSGBOX_DEFAULT
	release
	end

StrataLindqvistRanch_EventScript_BeaLater::
	msgbox StrataLindqvistRanch_Text_BeaLater, MSGBOX_DEFAULT
	release
	end

StrataLindqvistRanch_EventScript_Kessler::
	lock
	faceplayer
	msgbox StrataLindqvistRanch_Text_Kessler, MSGBOX_DEFAULT
	setflag FLAG_STRATA_MET_KESSLER
	release
	end

StrataLindqvistRanch_EventScript_KesslerHand::
	msgbox StrataLindqvistRanch_Text_KesslerHand, MSGBOX_NPC
	end

StrataLindqvistRanch_EventScript_Tarp::
	lockall
	msgbox StrataLindqvistRanch_Text_Tarp, MSGBOX_DEFAULT
	setflag FLAG_STRATA_SAW_PAIR
	releaseall
	end

StrataLindqvistRanch_EventScript_RanchSign::
	msgbox StrataLindqvistRanch_Text_RanchSign, MSGBOX_SIGN
	end

StrataLindqvistRanch_EventScript_HouseDoor::
	msgbox StrataLindqvistRanch_Text_HouseDoor, MSGBOX_SIGN
	end

StrataLindqvistRanch_EventScript_SplitEstateNote::
	msgbox StrataLindqvistRanch_Text_SplitEstateNote, MSGBOX_SIGN
	end

StrataLindqvistRanch_EventScript_DroughtNote::
	msgbox StrataLindqvistRanch_Text_DroughtNote, MSGBOX_SIGN
	end

StrataLindqvistRanch_Text_BeaAct0:
	.string "BEA: You're one of Halvorsen's kids.\n"
	.string "I'm BEA LINDQVIST. This is my land.\p"
	.string "Four generations of cattle, and now\n"
	.string "the most valuable thing on the place\l"
	.string "is a pile of bones.\p"
	.string "This gentleman wants to sell them\n"
	.string "for me. Says he'll get a price that\l"
	.string "would carry us through the drought.\p"
	.string "I haven't said yes. I haven't said\n"
	.string "no, either.$"

StrataLindqvistRanch_Text_BeaLater:
	.string "BEA: Pond's down another foot.\n"
	.string "I'm selling heifers I'd rather keep.\p"
	.string "Josie wants the Pair in a museum.\n"
	.string "Museums want it for free.\p"
	.string "Somebody tell me how that pays for\n"
	.string "hay.$"

StrataLindqvistRanch_Text_Kessler:
	.string "WADE KESSLER, Kessler Natural\n"
	.string "History. A pleasure.\p"
	.string "Every spring the rain breaks up\n"
	.string "bones nobody came to collect.\p"
	.string "Museums can't afford them, and the\n"
	.string "badlands won't wait. I can, and I do.\p"
	.string "Everything I sell comes off private\n"
	.string "land, legally. Tell your director\l"
	.string "my door is open.$"

StrataLindqvistRanch_Text_KesslerHand:
	.string "Boss says we stay on deeded land.\n"
	.string "Fence line's right there.\p"
	.string "Mostly.$"

StrataLindqvistRanch_Text_Tarp:
	.string "A blue tarp, weighted down with old\n"
	.string "tires.\p"
	.string "Under one corner: the curved edge of\n"
	.string "a TRICERATOPS frill, wide as a wagon\l"
	.string "wheel.\p"
	.string "A hand's width away, the toe bones of\n"
	.string "a TYRANNOSAURUS.\p"
	.string "Two animals, buried together. Josie\n"
	.string "calls it the Pair.$"

StrataLindqvistRanch_Text_RanchSign:
	.string "LINDQVIST RANCH\n"
	.string "Homesteaded 1911. Shut the gate.$"

StrataLindqvistRanch_Text_HouseDoor:
	.string "The ranch house. The door's shut;\n"
	.string "BEA's out with the stock.$"

StrataLindqvistRanch_Text_SplitEstateNote:
	.string "FIELD NOTE: Out West, the land's\n"
	.string "surface and the minerals under it\l"
	.string "can have different owners.\p"
	.string "Montana counts fossils as part of\n"
	.string "the surface, not the minerals. So\l"
	.string "the Pair is BEA's to sell.$"

StrataLindqvistRanch_Text_DroughtNote:
	.string "FIELD NOTE: Stock ponds catch spring\n"
	.string "snowmelt and rain for the cattle.\p"
	.string "In a dry year they shrink to mud,\n"
	.string "and a rancher has to sell animals\l"
	.string "or buy hay and water.$"
