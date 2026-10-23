@ Act 3: Concretion Bluffs, the Denver Fm at Corral Bluffs, ~65.4 Ma.
@ A Taeniolabis mini-boss (Lv 20) on the flats; three concretions to crack
@ (VAR_STRATA_ACT3 counts them).
StrataConcretionBluffs_MapScripts::
	.byte 0

StrataConcretionBluffs_EventScript_Taeniolabis::
	lockall
	playmoncry SPECIES_TAENIOLABIS, CRY_MODE_ENCOUNTER
	msgbox StrataConcretionBluffs_Text_TaeniolabisAppears, MSGBOX_DEFAULT
	waitmoncry
	setwildbattle SPECIES_TAENIOLABIS, 20
	dowildbattle
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, StrataConcretionBluffs_EventScript_TaeniolabisRan
	setflag FLAG_STRATA_A3_TAENIOLABIS_DONE
	removeobject LOCALID_STRATA_BLUFFS_TAENIOLABIS
	msgbox StrataConcretionBluffs_Text_TaeniolabisDone, MSGBOX_DEFAULT
	giveitem ITEM_LEGUME_POD
	releaseall
	end

StrataConcretionBluffs_EventScript_TaeniolabisRan::
	msgbox StrataConcretionBluffs_Text_TaeniolabisRan, MSGBOX_DEFAULT
	releaseall
	end

@ Each concretion: crack it, find something, get a small reward. The count in
@ VAR_STRATA_ACT3 makes the third a set.
StrataConcretionBluffs_EventScript_Concretion1::
	lockall
	msgbox StrataConcretionBluffs_Text_Crack, MSGBOX_DEFAULT
	setflag FLAG_STRATA_A3_CONCRETION_1
	removeobject LOCALID_STRATA_BLUFFS_CONCRETION_1
	msgbox StrataConcretionBluffs_Text_FoundJaw, MSGBOX_DEFAULT
	giveitem ITEM_POTION
	call StrataConcretionBluffs_EventScript_Cracked
	releaseall
	end

StrataConcretionBluffs_EventScript_Concretion2::
	lockall
	msgbox StrataConcretionBluffs_Text_Crack, MSGBOX_DEFAULT
	setflag FLAG_STRATA_A3_CONCRETION_2
	removeobject LOCALID_STRATA_BLUFFS_CONCRETION_2
	msgbox StrataConcretionBluffs_Text_FoundShell, MSGBOX_DEFAULT
	giveitem ITEM_POTION
	call StrataConcretionBluffs_EventScript_Cracked
	releaseall
	end

StrataConcretionBluffs_EventScript_Concretion3::
	lockall
	msgbox StrataConcretionBluffs_Text_Crack, MSGBOX_DEFAULT
	setflag FLAG_STRATA_A3_CONCRETION_3
	removeobject LOCALID_STRATA_BLUFFS_CONCRETION_3
	msgbox StrataConcretionBluffs_Text_FoundSkull, MSGBOX_DEFAULT
	giveitem ITEM_GREAT_BALL, 2
	call StrataConcretionBluffs_EventScript_Cracked
	releaseall
	end

@ Counts a cracked concretion; the third gets a closing note.
StrataConcretionBluffs_EventScript_Cracked::
	addvar VAR_STRATA_ACT3, 1
	goto_if_lt VAR_STRATA_ACT3, 3, StrataConcretionBluffs_EventScript_CrackedMore
	msgbox StrataConcretionBluffs_Text_FoundSet, MSGBOX_DEFAULT
StrataConcretionBluffs_EventScript_CrackedMore::
	return

StrataConcretionBluffs_EventScript_NoteSite::
	msgbox StrataConcretionBluffs_Text_NoteSite, MSGBOX_SIGN
	end

StrataConcretionBluffs_EventScript_NoteTaeniolabis::
	msgbox StrataConcretionBluffs_Text_NoteTaeniolabis, MSGBOX_SIGN
	end

StrataConcretionBluffs_EventScript_NoteConcretions::
	msgbox StrataConcretionBluffs_Text_NoteConcretions, MSGBOX_SIGN
	end

StrataConcretionBluffs_Text_TaeniolabisAppears:
	.string "A beaver-sized TAENIOLABIS is\n"
	.string "cracking seeds with its chisel\l"
	.string "teeth. It bristles as you step\l"
	.string "closer!$"

StrataConcretionBluffs_Text_TaeniolabisDone:
	.string "The TAENIOLABIS is done with you.\n"
	.string "It leaves a scatter of gnawed pods\l"
	.string "behind.$"

StrataConcretionBluffs_Text_TaeniolabisRan:
	.string "You back off. The TAENIOLABIS goes\n"
	.string "back to its seeds.$"

StrataConcretionBluffs_Text_Crack:
	.string "A round, hard concretion, half out\n"
	.string "of the slope. You tap it along its\l"
	.string "seam.\p"
	.string "Crack!$"

StrataConcretionBluffs_Text_FoundJaw:
	.string "Inside: a small jaw with broad,\n"
	.string "bumpy back teeth. A plant and insect\l"
	.string "eater, no bigger than a rat.$"

StrataConcretionBluffs_Text_FoundShell:
	.string "Inside: a flattened turtle shell.\n"
	.string "Turtles are common fossils in this\l"
	.string "rock. Water animals handled the\l"
	.string "aftermath better than most.$"

StrataConcretionBluffs_Text_FoundSkull:
	.string "Inside: a skull as long as your\n"
	.string "hand, with huge gnawing front\l"
	.string "teeth. A multituberculate.$"

StrataConcretionBluffs_Text_FoundSet:
	.string "A jaw, a shell and a skull: three\n"
	.string "animals from one bluff, all from\l"
	.string "the first million years after the\l"
	.string "impact.\p"
	.string "This is how we know what lived\n"
	.string "here, and when.$"

StrataConcretionBluffs_Text_NoteSite:
	.string "FIELD NOTE: Corral Bluffs.\n"
	.string "These pale bluffs are the Denver Fm:\l"
	.string "mud and sand left by rivers on a\l"
	.string "wide plain.\p"
	.string "The fossils sit inside hard, round\n"
	.string "concretions that weather out of the\l"
	.string "slope. Crack them open.$"

StrataConcretionBluffs_Text_NoteTaeniolabis:
	.string "FIELD NOTE: Taeniolabis taoensis.\n"
	.string "The largest multituberculate: a\l"
	.string "rodent-like mammal with chisel\l"
	.string "teeth and a big jaw muscle.\p"
	.string "Mass: roughly 30 kg (an estimate,\n"
	.string "and estimates vary). Its teeth are\l"
	.string "worn flat by tough plant food.$"

StrataConcretionBluffs_Text_NoteConcretions:
	.string "FIELD NOTE: Concretions.\n"
	.string "Minerals gather around a bone and\l"
	.string "harden into a ball of rock, which\l"
	.string "protects what is inside.\p"
	.string "Much of what we know about these\n"
	.string "mammals comes from skulls found\l"
	.string "this way.$"
