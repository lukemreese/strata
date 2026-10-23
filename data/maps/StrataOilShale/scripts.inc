@ Act 5: Oil-Shale Cliffs, Wyoming, ~50 Ma (Green River Formation varves). The Patriofelis set
@ piece: a visible creature on the sand path. Talk to it, or walk into its line of sight (the
@ row of triggers at y = 20, one per map visit: VAR_TEMP_1) to start a one-time wild battle.
@ Winning or catching it sets FLAG_STRATA_A5_PATRIOFELIS and leaves a kill to eat; running
@ leaves it where it is.
StrataOilShale_MapScripts::
	.byte 0

StrataOilShale_EventScript_PatriofelisSight::
	lockall
	setvar VAR_TEMP_1, 1
	goto_if_set FLAG_STRATA_A5_PATRIOFELIS, StrataOilShale_EventScript_PatriofelisGone
	goto StrataOilShale_EventScript_PatriofelisStart

StrataOilShale_EventScript_PatriofelisGone::
	releaseall
	end

StrataOilShale_EventScript_Patriofelis::
	lockall
	faceplayer
StrataOilShale_EventScript_PatriofelisStart::
	playmoncry SPECIES_PATRIOFELIS, CRY_MODE_ENCOUNTER
	msgbox StrataOilShale_Text_PatriofelisAppears, MSGBOX_DEFAULT
	waitmoncry
	setwildbattle SPECIES_PATRIOFELIS, 32
	dowildbattle
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, StrataOilShale_EventScript_PatriofelisRan
	setflag FLAG_STRATA_A5_PATRIOFELIS
	removeobject LOCALID_STRATA_A5_PATRIOFELIS
	msgbox StrataOilShale_Text_PatriofelisDone, MSGBOX_DEFAULT
	giveitem ITEM_CARRION
	releaseall
	end

StrataOilShale_EventScript_PatriofelisRan::
	msgbox StrataOilShale_Text_PatriofelisRan, MSGBOX_DEFAULT
	releaseall
	end

StrataOilShale_Text_PatriofelisAppears:
	.string "Bones crack on the sand path. A\n"
	.string "heavy, short-faced predator looks\l"
	.string "up from its kill.\p"
	.string "A PATRIOFELIS! Not a cat. It is an\n"
	.string "oxyaenid, a meat-eating mammal from\l"
	.string "an extinct side branch.$"

StrataOilShale_Text_PatriofelisDone:
	.string "The PATRIOFELIS slinks off into the\n"
	.string "ferns, leaving its kill behind.\p"
	.string "Bones and a carcass: meat-eaters\n"
	.string "feed on what the big predators\l"
	.string "leave.$"

StrataOilShale_Text_PatriofelisRan:
	.string "You back off down the path. The\n"
	.string "PATRIOFELIS watches you go and\l"
	.string "returns to its kill.$"

@ ---- field notes -----------------------------------------------------------------

StrataOilShale_EventScript_NoteVarves::
	msgbox StrataOilShale_Text_NoteVarves, MSGBOX_SIGN
	end

StrataOilShale_EventScript_NoteKerogen::
	msgbox StrataOilShale_Text_NoteKerogen, MSGBOX_SIGN
	end

StrataOilShale_EventScript_NoteCreodonts::
	msgbox StrataOilShale_Text_NoteCreodonts, MSGBOX_SIGN
	end

StrataOilShale_Text_NoteVarves:
	.string "FIELD NOTE: ONE STRIPE, ONE YEAR\p"
	.string "The shale is laid down in thin\n"
	.string "pale and dark pairs. Many are read\l"
	.string "as yearly layers, called varves:\l"
	.string "pale for chalky summer, dark for\l"
	.string "winter's organic matter.\p"
	.string "Not all of them are yearly, and\n"
	.string "counts disagree. Volcanic ash\l"
	.string "beds, dated by argon, check the\l"
	.string "count.$"

StrataOilShale_Text_NoteKerogen:
	.string "FIELD NOTE: OIL SHALE\p"
	.string "This is not oil. It is a rock rich\n"
	.string "in kerogen, the remains of algae\l"
	.string "and microbes that rained down into\l"
	.string "the lake's still, oxygen-poor\l"
	.string "bottom water.\p"
	.string "Cooked to about 500 C, it gives off\n"
	.string "oil. That is why it's mined.$"

StrataOilShale_Text_NoteCreodonts:
	.string "FIELD NOTE: PATRIOFELIS\p"
	.string "A creodont, which is not a cat or a\n"
	.string "dog but a branch of meat-eating\l"
	.string "mammals that died out. Heavy-\l"
	.string "boned, short-faced, perhaps 70 kg\l"
	.string "(an estimate).\p"
	.string "Heavy jaws suggest it also crushed\n"
	.string "bone (inferred from the skull).$"
