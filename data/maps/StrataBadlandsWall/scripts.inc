@ Act 6: the Badlands Wall. Open red-soil flats under a banded cliff: the Chadron / Brule
@ contact (the Eocene-Oligocene boundary is near it) is in the wall at the north-west corner.
@ Oreodont herds, early rabbits and tortoises on the flats. Field notes only; no set piece.
StrataBadlandsWall_MapScripts::
	.byte 0

StrataBadlandsWall_EventScript_Herd::
	msgbox StrataBadlandsWall_Text_Herd, MSGBOX_NPC
	end

StrataBadlandsWall_EventScript_NoteContact::
	msgbox StrataBadlandsWall_Text_NoteContact, MSGBOX_SIGN
	end

StrataBadlandsWall_EventScript_NoteOreodonts::
	msgbox StrataBadlandsWall_Text_NoteOreodonts, MSGBOX_SIGN
	end

StrataBadlandsWall_EventScript_NoteRabbit::
	msgbox StrataBadlandsWall_Text_NoteRabbit, MSGBOX_SIGN
	end

StrataBadlandsWall_Text_Herd:
	.string "A MERYCOIDODON grazes with the\n"
	.string "herd, snuffling at the dry ground.\l"
	.string "It ignores you.$"

StrataBadlandsWall_Text_NoteContact:
	.string "FIELD NOTE: The contact\p"
	.string "The banded clays low in the cliff\n"
	.string "are the Chadron Formation (late\l"
	.string "Eocene). The paler, siltier layers\l"
	.string "above are the Brule Formation\l"
	.string "(Oligocene).\p"
	.string "The Eocene-Oligocene boundary lies\n"
	.string "near this contact, give or take.\l"
	.string "Its exact place varies from site\l"
	.string "to site.$"

StrataBadlandsWall_Text_NoteOreodonts:
	.string "FIELD NOTE: Oreodonts\p"
	.string "MERYCOIDODON is among the most\n"
	.string "common fossils in the Brule: a\l"
	.string "stocky, sheep-sized plant eater.\p"
	.string "Many skeletons lie together, which\n"
	.string "hints at herds. Floods or drought\l"
	.string "could have gathered them instead.\l"
	.string "The bones can't tell us.$"

StrataBadlandsWall_Text_NoteRabbit:
	.string "FIELD NOTE: Early rabbits\p"
	.string "PALAEOLAGUS is one of the commonest\n"
	.string "small mammals in the Brule. Long\l"
	.string "hind legs fit a runner in open\l"
	.string "country, though its habits are\l"
	.string "inferred.\p"
	.string "This genus died out in the Miocene.\n"
	.string "Rabbits as a group did not.$"
