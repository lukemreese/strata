@ Act 8: Meltwater River, ~20,000 years ago. Braided glacial outwash east of the steppe, with a
@ sand-bar ford across the main channel. Field notes only; wild tables and forage in maps/.
StrataMeltwater_MapScripts::
	.byte 0

StrataMeltwater_EventScript_NoteBraided::
	msgbox StrataMeltwater_Text_NoteBraided, MSGBOX_SIGN
	end

StrataMeltwater_EventScript_NoteTurtle::
	msgbox StrataMeltwater_Text_NoteTurtle, MSGBOX_SIGN
	end

StrataMeltwater_EventScript_NoteMuskOx::
	msgbox StrataMeltwater_Text_NoteMuskOx, MSGBOX_SIGN
	end

StrataMeltwater_Text_NoteBraided:
	.string "FIELD NOTE: Braided river\p"
	.string "Rivers fed by glaciers carry more\n"
	.string "gravel and sand than they can move.\p"
	.string "The channel splits around bars and\n"
	.string "shifts after each melt-season\l"
	.string "flood. Flow was low in winter and\l"
	.string "big in summer.$"

StrataMeltwater_Text_NoteTurtle:
	.string "FIELD NOTE: Snapping turtle?\p"
	.string "CHELYDRA is a warm-water turtle. We\n"
	.string "can't cite a record of one in a\l"
	.string "cold, glacier-fed river in Wyoming\l"
	.string "at this time.\p"
	.string "The rig keeps your turtle lineage\n"
	.string "here as a stand-in. It marks a\l"
	.string "limit of the model, not a find.$"

StrataMeltwater_Text_NoteMuskOx:
	.string "FIELD NOTE: Musk oxen south of ice\p"
	.string "Several musk-ox forms lived south of\n"
	.string "the ice sheets. Which species\l"
	.string "reached Wyoming, and when, is still\l"
	.string "being sorted out.\p"
	.string "The rig uses OVIBOS, today's Arctic\n"
	.string "species, as the stand-in.$"
