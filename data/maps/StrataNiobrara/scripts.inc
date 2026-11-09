@ Act 7: the Niobrara River, before the ash: a wide river with a gravel bar across it.
@ Rhinos on the banks, turtles in the water. Its ash version is StrataNiobraraAsh.
StrataNiobrara_MapScripts::
	.byte 0

StrataNiobrara_EventScript_NoteRiver::
	msgbox StrataNiobrara_Text_NoteRiver, MSGBOX_SIGN
	end

StrataNiobrara_EventScript_NoteTurtles::
	msgbox StrataNiobrara_Text_NoteTurtles, MSGBOX_SIGN
	end

StrataNiobrara_EventScript_NoteRhinos::
	msgbox StrataNiobrara_Text_NoteRhinos, MSGBOX_SIGN
	end

StrataNiobrara_Text_NoteRiver:
	.string "FIELD NOTE: A river valley\p"
	.string "The Ashfall site lies in a river\n"
	.string "valley in northeast Nebraska. The\l"
	.string "rig calls this the Niobrara after\l"
	.string "where the river flows today.\p"
	.string "Ash fell on the valley, and the\n"
	.string "river later reworked some of it.$"

StrataNiobrara_Text_NoteTurtles:
	.string "FIELD NOTE: Snapping turtles\p"
	.string "MACROCHELYS, the alligator snapping\n"
	.string "turtle, is known from the Miocene\l"
	.string "of Nebraska: M. schmidti, about 18\l"
	.string "to 16 million years old.\p"
	.string "No snapping turtle is known from\n"
	.string "the Ashfall bed, so the rig uses\l"
	.string "this older animal as a stand-in.\p"
	.string "Today it lives only in the\n"
	.string "southeastern US.$"

StrataNiobrara_Text_NoteRhinos:
	.string "FIELD NOTE: Two kinds of rhino\p"
	.string "TELEOCERAS was short-legged and\n"
	.string "barrel-bodied. APHELOPS was longer-\l"
	.string "legged and rarer in the bed.\p"
	.string "Old reconstructions made Teleoceras\n"
	.string "a river wader like a hippo. Limbs\l"
	.string "and isotopes disagree on how much\l"
	.string "time it spent in water.$"
