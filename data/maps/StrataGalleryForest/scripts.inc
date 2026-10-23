@ Act 6: the Gallery Forest, north of the White River valley. Strips of forest along a river and
@ its lake in otherwise open country: browsing horses (their forest branch is steered here),
@ the first squirrels, and gars in the water. Field notes only; no set piece.
StrataGalleryForest_MapScripts::
	.byte 0

StrataGalleryForest_EventScript_NoteGallery::
	msgbox StrataGalleryForest_Text_NoteGallery, MSGBOX_SIGN
	end

StrataGalleryForest_EventScript_NoteSquirrel::
	msgbox StrataGalleryForest_Text_NoteSquirrel, MSGBOX_SIGN
	end

StrataGalleryForest_EventScript_NoteHorse::
	msgbox StrataGalleryForest_Text_NoteHorse, MSGBOX_SIGN
	end

StrataGalleryForest_Text_NoteGallery:
	.string "FIELD NOTE: Gallery forest\p"
	.string "In open country, trees hug the\n"
	.string "rivers in strips, like this one.\l"
	.string "Fossil wood and leaves in river\l"
	.string "sands show such strips here.\p"
	.string "Browsers with low-crowned teeth\n"
	.string "can live in them. Time spent under\l"
	.string "the trees pulls a lineage toward\l"
	.string "a forest life.$"

StrataGalleryForest_Text_NoteSquirrel:
	.string "FIELD NOTE: Early squirrels\p"
	.string "DOUGLASSCIURUS was a tree-climbing\n"
	.string "rodent with a squirrel's skeleton.\l"
	.string "The best fossils are from the late\l"
	.string "Eocene of Wyoming, about 36 Ma: a\l"
	.string "little older than this layer.\p"
	.string "The rig places it here as a\n"
	.string "stand-in. Which later squirrels\l"
	.string "come from it is uncertain.$"

StrataGalleryForest_Text_NoteHorse:
	.string "FIELD NOTE: Three-toed horses\p"
	.string "MESOHIPPUS was about the size of a\n"
	.string "big dog, with three toes and low-\l"
	.string "crowned teeth for soft leaves.\p"
	.string "Later horses split into forest\n"
	.string "browsers and grassland runners.\l"
	.string "In this model, which way this\l"
	.string "lineage goes depends on where you\l"
	.string "keep it.$"
