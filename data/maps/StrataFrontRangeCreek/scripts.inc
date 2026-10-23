@ Act 3: Front Range Creek, Denver Basin, ~65.5 Ma. Field notes only; the water is for
@ waders and the fishing kit (water pressure, the bird and turtle lineages).
StrataFrontRangeCreek_MapScripts::
	.byte 0

StrataFrontRangeCreek_EventScript_NoteRockies::
	msgbox StrataFrontRangeCreek_Text_NoteRockies, MSGBOX_SIGN
	end

StrataFrontRangeCreek_EventScript_NoteTurtles::
	msgbox StrataFrontRangeCreek_Text_NoteTurtles, MSGBOX_SIGN
	end

StrataFrontRangeCreek_EventScript_NoteChampsosaur::
	msgbox StrataFrontRangeCreek_Text_NoteChampsosaur, MSGBOX_SIGN
	end

StrataFrontRangeCreek_Text_NoteRockies:
	.string "FIELD NOTE: Front Range Creek.\n"
	.string "Upstream, the Rocky Mountains are\l"
	.string "rising (the Laramide uplift).\p"
	.string "The sand and mud of the Denver Fm\n"
	.string "was washed down from those young\l"
	.string "mountains onto this plain.$"

StrataFrontRangeCreek_Text_NoteTurtles:
	.string "FIELD NOTE: Turtles.\n"
	.string "Snapping turtles are common in this\l"
	.string "creek. Water softened the blow of\l"
	.string "the extinction: turtles and\l"
	.string "crocodile kin came through it.\p"
	.string "Which of their relatives survive\n"
	.string "today is up to the next filters.$"

StrataFrontRangeCreek_Text_NoteChampsosaur:
	.string "FIELD NOTE: Champsosaurs.\n"
	.string "These gharial-like reptiles crossed\l"
	.string "the impact and lasted many millions\l"
	.string "of years more, until the Eocene\l"
	.string "cooled.\p"
	.string "Their long, toothy snouts suggest\n"
	.string "a diet of fish. (inferred)$"
