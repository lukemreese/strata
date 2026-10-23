@ Epilogue: the Montana prairie today. Open once the present layer is loaded (story 18): the
@ ranch road/highway west of Jordan leads here. A prairie-dog town in the east, with the
@ black-footed ferret that hunts it (a one-time scripted encounter, then it is a rare wild);
@ swift fox, sage-grouse, bison and pronghorn on the open ground. The Interpretive Center is
@ the building in the east half (door warp 0). East edge: Missouri Breaks. South edge: Pryor
@ Mountains. Act state: FLAG_STRATA_EPI_FERRET_MET.
StrataPrairie_MapScripts::
	.byte 0

StrataPrairie_EventScript_TrailToCamp::
	lockall
	msgbox StrataPrairie_Text_TrailToCamp, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, StrataPrairie_EventScript_Stay
	warp MAP_STRATA_FIELD_CAMP, 2, 8
	waitstate
	releaseall
	end

StrataPrairie_EventScript_Stay::
	releaseall
	end

@ The black-footed ferret in the prairie-dog town (a wild battle, once). Triggered by talking to
@ it. After the fight (caught or not) it slips back down its burrow and leaves a meal behind.
StrataPrairie_EventScript_Ferret::
	lockall
	playmoncry SPECIES_MUSTELA, CRY_MODE_ENCOUNTER
	msgbox StrataPrairie_Text_FerretAppears, MSGBOX_DEFAULT
	waitmoncry
	setwildbattle SPECIES_MUSTELA, 48
	dowildbattle
	setflag FLAG_STRATA_EPI_FERRET_MET
	removeobject LOCALID_STRATA_PRAIRIE_FERRET
	msgbox StrataPrairie_Text_FerretGone, MSGBOX_DEFAULT
	giveitem ITEM_CARRION
	releaseall
	end

StrataPrairie_EventScript_Dog::
	lock
	faceplayer
	playmoncry SPECIES_CYNOMYS, CRY_MODE_NORMAL
	msgbox StrataPrairie_Text_Dog, MSGBOX_DEFAULT
	waitmoncry
	release
	end

StrataPrairie_EventScript_NoteDogs::
	msgbox StrataPrairie_Text_NoteDogs, MSGBOX_SIGN
	end

StrataPrairie_EventScript_NoteGrouse::
	msgbox StrataPrairie_Text_NoteGrouse, MSGBOX_SIGN
	end

StrataPrairie_EventScript_NoteFox::
	msgbox StrataPrairie_Text_NoteFox, MSGBOX_SIGN
	end

StrataPrairie_EventScript_NoteBison::
	msgbox StrataPrairie_Text_NoteBison, MSGBOX_SIGN
	end

StrataPrairie_EventScript_CenterSign::
	msgbox StrataPrairie_Text_CenterSign, MSGBOX_SIGN
	end

StrataPrairie_Text_TrailToCamp:
	.string "The ranch road back to the Hell\n"
	.string "Creek camp. Head back?$"

StrataPrairie_Text_FerretAppears:
	.string "A slim, masked face pokes out of a\n"
	.string "prairie-dog burrow. A BLACK-FOOTED\l"
	.string "FERRET!\p"
	.string "It is one of the rarest mammals in\n"
	.string "North America. It spots you, and\l"
	.string "bristles.$"

StrataPrairie_Text_FerretGone:
	.string "The ferret flows back down the\n"
	.string "burrow like water.\p"
	.string "It leaves a scrap of its last meal\n"
	.string "on the mound.$"

StrataPrairie_Text_Dog:
	.string "A prairie dog pops up on its\n"
	.string "mound, barks a warning, and drops\l"
	.string "back into the burrow.$"

StrataPrairie_Text_NoteDogs:
	.string "FIELD NOTE: Prairie-dog town.\p"
	.string "Black-tailed prairie dogs dig\n"
	.string "burrows and clip the grass short.\l"
	.string "Hundreds of other species use the\l"
	.string "town, from burrowing owls to the\l"
	.string "black-footed ferret, which eats\l"
	.string "little else and lives in their\l"
	.string "burrows.\p"
	.string "Ferrets were thought extinct until\n"
	.string "1981, when a ranch dog brought one\l"
	.string "home near Meeteetse, Wyoming.\l"
	.string "Every ferret alive now descends\l"
	.string "from a handful of survivors bred\l"
	.string "in captivity. Releases in Montana\l"
	.string "began in the 1990s.$"

StrataPrairie_Text_NoteGrouse:
	.string "FIELD NOTE: Sage-grouse.\p"
	.string "Each spring the males gather on a\n"
	.string "bare patch, a lek, to display for\l"
	.string "the females. Greater sage-grouse\l"
	.string "need big, unbroken sagebrush for\l"
	.string "nests, chicks and winter food.\p"
	.string "Their range has shrunk by roughly\n"
	.string "44% since settlement (Schroeder et\l"
	.string "al., 2004), as sagebrush was\l"
	.string "ploughed, grazed, burned and built\l"
	.string "over. That is one study's\l"
	.string "estimate; the real loss is hard to\l"
	.string "pin down.$"

StrataPrairie_Text_NoteFox:
	.string "FIELD NOTE: Swift fox.\p"
	.string "A cat-sized fox of the short-grass\n"
	.string "prairie, fast over short\l"
	.string "distances. Trapping, poison baits\l"
	.string "meant for wolves and coyotes, and\l"
	.string "ploughed grassland wiped it out of\l"
	.string "Canada by the 1930s.\p"
	.string "Releases began in Canada in 1983\n"
	.string "and in Montana in the late 1990s.\l"
	.string "Dates vary by source. The fox is\l"
	.string "back because people chose to bring\l"
	.string "it back.$"

StrataPrairie_Text_NoteBison:
	.string "FIELD NOTE: Bison.\p"
	.string "Tens of millions of bison grazed\n"
	.string "the plains before the 1800s.\l"
	.string "Market hunting took nearly all of\l"
	.string "them within decades, and by about\l"
	.string "1890 only hundreds were left in\l"
	.string "the wild.\p"
	.string "Today's herds descend from those\n"
	.string "few survivors, and many carry some\l"
	.string "cattle genes. Several tribal\l"
	.string "nations now manage herds of their\l"
	.string "own.$"

StrataPrairie_Text_CenterSign:
	.string "MONTANA PRAIRIE INTERPRETIVE\n"
	.string "CENTER\p"
	.string "The Pair. The Hall of Lost\n"
	.string "Lineages. Open daily. Please stay\l"
	.string "on the trail.$"
