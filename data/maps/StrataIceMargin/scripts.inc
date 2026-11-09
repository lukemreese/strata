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
	.string "US, up to about 3 km thick at its\l"
	.string "centre, thinner here at the edge.\p"
	.string "At this latitude the real edge lay\n"
	.string "hundreds of km north of the cave.\l"
	.string "The rig draws it close, for the\l"
	.string "story. The ice nearby is mountain\l"
	.string "glaciers.$"

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
	.string "Bighorn favour steep, broken\n"
	.string "ground. Mammoths, horses and\l"
	.string "helmeted musk oxen prefer open\l"
	.string "country.\p"
	.string "The ice edge squeezes them into the\n"
	.string "same valleys. A mixed bone bed is\l"
	.string "not always a mixed herd.$"
