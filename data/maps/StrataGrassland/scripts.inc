@ Act 7: Ashfall Fossil Beds, Nebraska, ~11.9 Ma. The Grassland, before the ash: the
@ rig arrives here. Its ash version is StrataGrasslandAsh; the boss is at the Waterhole.
StrataGrassland_MapScripts::
	.byte 0

@ The first step away from the arrival point: the plume on the horizon (once).
StrataGrassland_EventScript_Haze::
	lockall
	msgbox StrataGrassland_Text_Haze, MSGBOX_DEFAULT
	setvar VAR_STRATA_ACT7, 1
	releaseall
	end

StrataGrassland_EventScript_NoteTeeth::
	msgbox StrataGrassland_Text_NoteTeeth, MSGBOX_SIGN
	end

StrataGrassland_EventScript_NoteSeeds::
	msgbox StrataGrassland_Text_NoteSeeds, MSGBOX_SIGN
	end

StrataGrassland_EventScript_NoteCranes::
	msgbox StrataGrassland_Text_NoteCranes, MSGBOX_SIGN
	end

StrataGrassland_Text_Haze:
	.string "Grass, as far as you can see, under\n"
	.string "a warm, dry wind.\p"
	.string "On the western horizon hangs a grey\n"
	.string "smudge. It is the plume of a huge\l"
	.string "eruption in what is now Idaho,\l"
	.string "1,600 km away.\p"
	.string "The animals here haven't noticed.$"

StrataGrassland_Text_NoteTeeth:
	.string "FIELD NOTE: Teeth against grit\p"
	.string "CORMOHIPPARION has tall, ridged\n"
	.string "cheek teeth (high-crowned, or\l"
	.string "hypsodont) that wear down slowly.\p"
	.string "Grass is tough and gritty, and so\n"
	.string "is dust. Which of the two drove\l"
	.string "tall teeth is still debated.$"

StrataGrassland_Text_NoteSeeds:
	.string "FIELD NOTE: Seed heads\p"
	.string "Grasslands covered the Great Plains\n"
	.string "by now, mostly cool-season grasses.\l"
	.string "The warm-season kind spread later,\l"
	.string "a few million years on.\p"
	.string "Ancient soil carbon in teeth and\n"
	.string "soil tells the two apart.\p"
	.string "Lineages that feed here are pushed\n"
	.string "toward open ground.$"

StrataGrassland_Text_NoteCranes:
	.string "FIELD NOTE: Cranes on the plain\p"
	.string "A BALEARICA, a crowned crane, has\n"
	.string "been reported from Ashfall. Cranes\l"
	.string "wade for seeds, insects and small\l"
	.string "animals.\p"
	.string "The identification rests on a few\n"
	.string "bones, so treat it as tentative.\l"
	.string "It does suggest wet ground nearby.$"
