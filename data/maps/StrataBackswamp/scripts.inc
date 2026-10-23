StrataBackswamp_MapScripts::
	.byte 0

@ Field notes (signposts).
StrataBackswamp_EventScript_NoteDetritus::
	msgbox StrataBackswamp_Text_NoteDetritus, MSGBOX_SIGN
	end

StrataBackswamp_EventScript_NoteShallows::
	msgbox StrataBackswamp_Text_NoteShallows, MSGBOX_SIGN
	end

StrataBackswamp_Text_NoteDetritus:
	.string "FIELD NOTE: What eats dead leaves?\p"
	.string "Swamp mud is full of rotting\n"
	.string "plants, and of the insects, snails\l"
	.string "and worms that eat them.\p"
	.string "A food web built on dead matter\n"
	.string "keeps running when green things\l"
	.string "stop growing. Remember this.$"

StrataBackswamp_Text_NoteShallows:
	.string "FIELD NOTE: Crowded shallows\p"
	.string "Gars, champsosaurs, turtles and\n"
	.string "crocodile relatives share this\l"
	.string "water.\p"
	.string "Freshwater animals lost fewer\n"
	.string "species at the boundary than\l"
	.string "land animals did.$"
