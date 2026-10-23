@ Act 6: the Toadstool Trackways, a floodplain of damp sand and ash that kept footprints. A
@ Hyaenodon (the act's mini-boss, Lv 38) hunts across the way east; step into its line of sight
@ or talk to it. Once, whatever the outcome. Winning (or catching) leaves a scrap of its kill.
StrataToadstool_MapScripts::
	.byte 0

StrataToadstool_EventScript_Hyaenodon::
	lockall
	playmoncry SPECIES_HYAENODON, CRY_MODE_ENCOUNTER
	msgbox StrataToadstool_Text_HyaenodonAppears, MSGBOX_DEFAULT
	waitmoncry
	strata_boss_prep atk=1
	setwildbattle SPECIES_HYAENODON, 38
	dowildbattle
	strata_boss_done
	setvar VAR_STRATA_ACT6, 1
	setflag FLAG_STRATA_A6_HYAENODON_GONE
	removeobject LOCALID_STRATA_TT_HYAENODON
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, StrataToadstool_EventScript_RanFromHyaenodon
	msgbox StrataToadstool_Text_HyaenodonGone, MSGBOX_DEFAULT
	giveitem ITEM_CARRION
	releaseall
	end

StrataToadstool_EventScript_RanFromHyaenodon::
	msgbox StrataToadstool_Text_RanFromHyaenodon, MSGBOX_DEFAULT
	releaseall
	end

StrataToadstool_EventScript_NoteTrackway::
	msgbox StrataToadstool_Text_NoteTrackway, MSGBOX_SIGN
	end

StrataToadstool_EventScript_NoteCreodont::
	msgbox StrataToadstool_Text_NoteCreodont, MSGBOX_SIGN
	end

StrataToadstool_EventScript_NoteBurial::
	msgbox StrataToadstool_Text_NoteBurial, MSGBOX_SIGN
	end

StrataToadstool_Text_HyaenodonAppears:
	.string "Something long-jawed lifts its head\n"
	.string "from a kill in the grass.\p"
	.string "A HYAENODON, with a mouthful of\n"
	.string "shearing teeth. It has seen you!$"

StrataToadstool_Text_HyaenodonGone:
	.string "The HYAENODON slinks off through\n"
	.string "the grass, favouring one leg.\p"
	.string "It leaves a scrap of its kill\n"
	.string "behind.$"

StrataToadstool_Text_RanFromHyaenodon:
	.string "You back away. The HYAENODON\n"
	.string "snarls, then drags its kill off\l"
	.string "into the grass.$"

StrataToadstool_Text_NoteTrackway:
	.string "FIELD NOTE: Trackways\p"
	.string "Footprints in the Brule are rare\n"
	.string "but real. Sites like Toadstool Park\l"
	.string "in Nebraska keep prints left on\l"
	.string "damp sand and ash.\p"
	.string "Toes and stride show who passed:\n"
	.string "hoofed browsers, small carnivores,\l"
	.string "birds. Naming the maker from a\l"
	.string "print alone is a guess.$"

StrataToadstool_Text_NoteCreodont:
	.string "FIELD NOTE: Creodont\p"
	.string "HYAENODON is no hyena and no dog.\n"
	.string "It belongs to the creodonts, an\l"
	.string "older group of meat eaters with\l"
	.string "shearing teeth far back in the\l"
	.string "jaw.\p"
	.string "It lived through much of the\n"
	.string "Oligocene. Later, dogs and cats\l"
	.string "seem to have taken over its work.$"

StrataToadstool_Text_NoteBurial:
	.string "FIELD NOTE: Why tracks last\p"
	.string "A print survives only if the mud\n"
	.string "sets before the next herd or flood\l"
	.string "wipes it, then gets buried gently\l"
	.string "and turns to stone.\p"
	.string "Each print is a few seconds of one\n"
	.string "animal's day, and many are worn\l"
	.string "away before anyone finds them.$"
