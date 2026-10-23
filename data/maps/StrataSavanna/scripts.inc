@ Act 7: the Savanna Woodland, before the ash: meadow with scattered trees, browsers and
@ grazers side by side. A bone-cracking dog (EPICYON, Lv 44) guards a carcass (a mini-boss,
@ once). Its ash version is StrataSavannaAsh.
StrataSavanna_MapScripts::
	.byte 0

@ Talk to the dog (once, whatever the outcome).
StrataSavanna_EventScript_Epicyon::
	lockall
	playmoncry SPECIES_EPICYON, CRY_MODE_ENCOUNTER
	msgbox StrataSavanna_Text_EpicyonAppears, MSGBOX_DEFAULT
	waitmoncry
	setwildbattle SPECIES_EPICYON, 44
	dowildbattle
	setflag FLAG_STRATA_A7_EPICYON_GONE
	removeobject LOCALID_STRATA_SAVANNA_EPICYON
	msgbox StrataSavanna_Text_EpicyonGone, MSGBOX_DEFAULT
	giveitem ITEM_CARRION
	releaseall
	end

StrataSavanna_EventScript_NoteBrowsers::
	msgbox StrataSavanna_Text_NoteBrowsers, MSGBOX_SIGN
	end

StrataSavanna_EventScript_NoteDogs::
	msgbox StrataSavanna_Text_NoteDogs, MSGBOX_SIGN
	end

StrataSavanna_Text_EpicyonAppears:
	.string "A big, heavy-headed dog crouches\n"
	.string "over a carcass, cracking a bone.\p"
	.string "An EPICYON! It bares its teeth and\n"
	.string "won't give up its meal!$"

StrataSavanna_Text_EpicyonGone:
	.string "The EPICYON drags what is left of\n"
	.string "the carcass into the long grass.\p"
	.string "It leaves a scrap of meat behind.$"

StrataSavanna_Text_NoteBrowsers:
	.string "FIELD NOTE: Leaves or grass?\p"
	.string "HYPOHIPPUS had low-crowned teeth, a\n"
	.string "leaf-eater's teeth, in a horse. It\l"
	.string "lived in woodland while other\l"
	.string "horses took to the grass.\p"
	.string "It is known from the Miocene of the\n"
	.string "Great Plains, but not from the\l"
	.string "Ashfall bed itself. The rig lets it\l"
	.string "stand here for contrast.$"

StrataSavanna_Text_NoteDogs:
	.string "FIELD NOTE: Bone-crushing dogs\p"
	.string "EPICYON was a large, heavy-jawed\n"
	.string "dog with thick premolars. Dogs of\l"
	.string "its group are known from the\l"
	.string "Ashfall beds.\p"
	.string "Hunter or scavenger? Probably both.\n"
	.string "Tooth wear and bite marks on bones\l"
	.string "can't settle it.$"
