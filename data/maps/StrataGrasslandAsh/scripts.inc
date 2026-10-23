@ Act 7: the Grassland after the ash (the same layout as StrataGrassland).
StrataGrasslandAsh_MapScripts::
	.byte 0

StrataGrassland_EventScript_NoteAshDepth::
	msgbox StrataGrassland_Text_NoteAshDepth, MSGBOX_SIGN
	end

StrataGrassland_EventScript_NoteOrder::
	msgbox StrataGrassland_Text_NoteOrder, MSGBOX_SIGN
	end

StrataGrassland_Text_NoteAshDepth:
	.string "FIELD NOTE: How deep?\p"
	.string "Where the real ash bed is thickest,\n"
	.string "it is a few metres deep.\p"
	.string "Layers inside it show it arrived\n"
	.string "over days to weeks, and wind and\l"
	.string "water moved it around afterward.\p"
	.string "The rig's “weeks” is an estimate.$"

StrataGrassland_Text_NoteOrder:
	.string "FIELD NOTE: Who dies first?\p"
	.string "The skeletons suggest an order:\n"
	.string "small animals and birds, then\l"
	.string "horses and camels, rhinos last.\p"
	.string "The order is inferred from how the\n"
	.string "bones lie in the ash layers. No\l"
	.string "one saw it happen.$"
