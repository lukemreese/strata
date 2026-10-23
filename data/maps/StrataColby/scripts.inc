@ Act 8 coda: the Colby site, Bighorn Basin, ~13,000 years ago (late glacial sub-layer, same
@ era as the cave). No wild encounters. Mammoth bones and a Clovis point; the rig can build
@ the bone and the stone but not the people (rule R-g). Seeing the point sets
@ FLAG_STRATA_COLBY_SEEN, which the epilogue gate (story task S3) can check before the rig
@ offers "Today". The story value is left alone: leaving by the anchor is always allowed.
StrataColby_MapScripts::
	.byte 0

StrataColby_EventScript_Intro::
	lockall
	setvar VAR_TEMP_1, 1
	msgbox StrataColby_Text_Intro, MSGBOX_DEFAULT
	releaseall
	end

StrataColby_EventScript_Bones::
	msgbox StrataColby_Text_Bones, MSGBOX_NPC
	end

StrataColby_EventScript_Point::
	lockall
	msgbox StrataColby_Text_Point, MSGBOX_DEFAULT
	goto_if_set FLAG_STRATA_COLBY_SEEN, StrataColby_EventScript_PointAgain
	setflag FLAG_STRATA_COLBY_SEEN
	msgbox StrataColby_Text_PointLogged, MSGBOX_DEFAULT
	releaseall
	end

StrataColby_EventScript_PointAgain::
	releaseall
	end

StrataColby_EventScript_NoteSite::
	msgbox StrataColby_Text_NoteSite, MSGBOX_SIGN
	end

StrataColby_EventScript_NoteEvidence::
	msgbox StrataColby_Text_NoteEvidence, MSGBOX_SIGN
	end

StrataColby_Text_Intro:
	.string "The layer thins. Less snow, and no\n"
	.string "herds: only what the ground kept.\p"
	.string "About 13,000 years ago. The rig\n"
	.string "renders bone and stone here, and\l"
	.string "nothing that walked on two legs.$"

StrataColby_Text_Bones:
	.string "A heap of mammoth bones: limb\n"
	.string "bones, ribs, parts of skulls, from\l"
	.string "several animals.\p"
	.string "One reading is a pile made by\n"
	.string "people. Another is a chance heap.\l"
	.string "The bones are evidence. The story\l"
	.string "is a guess.$"

StrataColby_Text_Point:
	.string "A fluted stone point lies among the\n"
	.string "bones: a channel flake was struck\l"
	.string "off each face.\p"
	.string "Clovis points turn up with mammoth\n"
	.string "bones at a few sites.\p"
	.string "The rig can build the bone and the\n"
	.string "stone. It can't build whoever made\l"
	.string "it: people are only traces here.\p"
	.string "Someone made this.$"

StrataColby_Text_PointLogged:
	.string "The rig logs the find. Nothing here\n"
	.string "to resolve: this slice is only a\l"
	.string "record of bones with tools.\p"
	.string "The anchor leads back to camp.$"

StrataColby_Text_NoteSite:
	.string "FIELD NOTE: Colby\p"
	.string "A bone bed in the Bighorn Basin,\n"
	.string "near Worland, Wyoming, about 13,000\l"
	.string "years old (calibrated).\p"
	.string "Bones of several mammoths lie in\n"
	.string "one pile, with Clovis stone tools.\p"
	.string "Clovis is a toolmaking tradition,\n"
	.string "known only from its tools.$"

StrataColby_Text_NoteEvidence:
	.string "FIELD NOTE: Hunters, climate, or\n"
	.string "both?\p"
	.string "For a human role: big animals fade\n"
	.string "soon after people arrive; some\l"
	.string "bones show cut marks or points.\p"
	.string "Against: only a few mammoth kill\n"
	.string "sites are known, most lost genera\l"
	.string "have none, and the climate was\l"
	.string "swinging hard (the Younger Dryas).\p"
	.string "This is unresolved. Many\n"
	.string "researchers favour a mix. The game\l"
	.string "does not pick one.$"
