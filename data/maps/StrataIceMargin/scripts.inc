@ Act 8: the Ice Margin, ~20,000 years ago. A pale basin of outwash silt under rock ridges, at the
@ edge of the glaciers. Field notes only; wild tables and forage in maps/.
StrataIceMargin_MapScripts::
	.byte 0

StrataIceMargin_EventScript_NoteIce::
	msgbox StrataIceMargin_Text_NoteIce, MSGBOX_SIGN
	end

StrataIceMargin_EventScript_NoteSeaLevel::
	msgbox StrataIceMargin_Text_NoteSeaLevel, MSGBOX_SIGN
	end

StrataIceMargin_EventScript_NoteEdge::
	msgbox StrataIceMargin_Text_NoteEdge, MSGBOX_SIGN
	end

StrataIceMargin_Text_NoteIce:
	.string "FIELD NOTE: The ice\p"
	.string "The Laurentide Ice Sheet buried\n"
	.string "most of Canada and the northern\l"
	.string "US, kilometres thick near its\l"
	.string "centre.\p"
	.string "At this latitude it ended hundreds\n"
	.string "of km north of the cave. The rig\l"
	.string "draws it close, for the story. The\l"
	.string "ice nearby is mountain glaciers.$"

StrataIceMargin_Text_NoteSeaLevel:
	.string "FIELD NOTE: Locked-up water\p"
	.string "So much water sat in the ice that\n"
	.string "the sea stood about 120 m lower.\p"
	.string "The Bering Strait was dry land, and\n"
	.string "animals crossed it.\p"
	.string "People reached the Americas by some\n"
	.string "route. Some sites hint at 20,000\l"
	.string "years ago or earlier; those dates\l"
	.string "are still debated.$"

StrataIceMargin_Text_NoteEdge:
	.string "FIELD NOTE: Odd neighbours\p"
	.string "Musk oxen and bighorn favour cold,\n"
	.string "broken ground. Mammoths and horses\l"
	.string "prefer open grass.\p"
	.string "The ice edge squeezes them into the\n"
	.string "same valleys. A mixed bone bed is\l"
	.string "not always a mixed herd.$"
