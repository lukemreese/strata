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

@ Field notes (signposts). The Levee opens east into the Fern Glade.
StrataLevee_EventScript_NoteFlora::
	msgbox StrataLevee_Text_NoteFlora, MSGBOX_SIGN
	end

StrataLevee_EventScript_NoteTriceratops::
	msgbox StrataLevee_Text_NoteTriceratops, MSGBOX_SIGN
	end

StrataLevee_EventScript_NoteSmall::
	msgbox StrataLevee_Text_NoteSmall, MSGBOX_SIGN
	end

StrataLevee_Text_NoteFlora:
	.string "FIELD NOTE: Flora\p"
	.string "Flowering trees and shrubs, with\n"
	.string "ferns and conifers beneath.\p"
	.string "Grasses exist, but they are rare.\n"
	.string "The prairies are still millions of\l"
	.string "years away.$"

StrataLevee_Text_NoteTriceratops:
	.string "FIELD NOTE: Triceratops\p"
	.string "The most common large dinosaur in\n"
	.string "the Hell Creek Formation.\p"
	.string "By some counts it makes up a big\n"
	.string "share of all the dinosaur bones\l"
	.string "found in these beds.$"

StrataLevee_Text_NoteSmall:
	.string "FIELD NOTE: Size\p"
	.string "Nearly every mammal here weighs\n"
	.string "less than a kilogram.\p"
	.string "The largest, Didelphodon, was about\n"
	.string "possum-sized (estimated 5 kg).\p"
	.string "Small bodies will matter soon.$"
