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
	.string "CHELYDRA has a Pleistocene record,\n"
	.string "and it overwinters under ice today,\l"
	.string "but we can't cite one from a\l"
	.string "glacier-fed Wyoming river at this\l"
	.string "time.\p"
	.string "The rig keeps your turtle lineage\n"
	.string "here as a stand-in. It marks a\l"
	.string "limit of the model, not a find.$"

StrataMeltwater_Text_NoteMuskOx:
	.string "FIELD NOTE: Musk oxen south of ice\p"
	.string "BOOTHERIUM, the helmeted musk ox,\n"
	.string "is on the fossil list from Natural\l"
	.string "Trap Cave. It stood taller and\l"
	.string "leaner than today's Arctic musk ox.\p"
	.string "It lived south of the ice sheets,\n"
	.string "and died out at the end of the\l"
	.string "Ice Age.$"
