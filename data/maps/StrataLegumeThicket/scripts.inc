@ Act 3: the Legume Thicket and the marsh at its north end, Denver Basin, ~65.4 Ma.
@ Boss: Eoconodon (Lv 22) at its carcass. Triggers on row 13 fire while
@ VAR_STRATA_STORY is STORY_IN_ACT(ERA_CORRAL_BLUFFS); the win sets the done value.
StrataLegumeThicket_MapScripts::
	.byte 0

StrataLegumeThicket_EventScript_Eoconodon::
	lockall
	playmoncry SPECIES_EOCONODON, CRY_MODE_ENCOUNTER
	msgbox StrataLegumeThicket_Text_EoconodonAppears, MSGBOX_DEFAULT
	waitmoncry
	strata_boss_prep atk=1
	setwildbattle SPECIES_EOCONODON, 22
	dowildbattle
	strata_boss_done
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, StrataLegumeThicket_EventScript_Ran
	setvar VAR_STRATA_STORY, STORY_ACT_DONE(ERA_CORRAL_BLUFFS)
	setflag FLAG_STRATA_A3_EOCONODON_GONE
	removeobject LOCALID_STRATA_THICKET_EOCONODON
	msgbox StrataLegumeThicket_Text_EoconodonDone, MSGBOX_DEFAULT
	releaseall
	end

@ Talking to the visible Eoconodon is the same fight.
StrataLegumeThicket_EventScript_EoconodonLook::
	goto StrataLegumeThicket_EventScript_Eoconodon
	end

StrataLegumeThicket_EventScript_Ran::
	msgbox StrataLegumeThicket_Text_Ran, MSGBOX_DEFAULT
	releaseall
	end

StrataLegumeThicket_EventScript_NoteLegumes::
	msgbox StrataLegumeThicket_Text_NoteLegumes, MSGBOX_SIGN
	end

StrataLegumeThicket_EventScript_NoteMarsh::
	msgbox StrataLegumeThicket_Text_NoteMarsh, MSGBOX_SIGN
	end

StrataLegumeThicket_EventScript_NoteCarcass::
	msgbox StrataLegumeThicket_Text_NoteCarcass, MSGBOX_SIGN
	end

StrataLegumeThicket_Text_EoconodonAppears:
	.string "In the marsh beyond the thicket,\n"
	.string "something heavy-jawed is tearing at\l"
	.string "a carcass.\p"
	.string "An EOCONODON! A wolf-sized hunter,\n"
	.string "less than a million years after the\l"
	.string "impact left no big land animals\l"
	.string "of any kind.$"

StrataLegumeThicket_Text_EoconodonDone:
	.string "The EOCONODON slinks off into the\n"
	.string "reeds.\p"
	.string "With the dinosaurs gone, mammals are\n"
	.string "filling the empty roles: big plant\l"
	.string "eaters, and now big hunters.\p"
	.string "Report back to DR. HALVORSEN.$"

StrataLegumeThicket_Text_Ran:
	.string "You back away. The EOCONODON goes\n"
	.string "back to its meal.$"

StrataLegumeThicket_Text_NoteLegumes:
	.string "FIELD NOTE: Legume Thicket.\n"
	.string "About 700,000 years after the impact,\l"
	.string "legume fossils appear here, among the\l"
	.string "oldest known. (Dating and\l"
	.string "identification are still debated.)\p"
	.string "Hypothesis: protein-rich seeds helped\n"
	.string "plant eaters grow bigger. It fits the\l"
	.string "timing, but it is not proven.$"

StrataLegumeThicket_Text_NoteMarsh:
	.string "FIELD NOTE: Marsh.\n"
	.string "Ferns and reeds ring the ponds. Wet\l"
	.string "ground buried leaves and bones\l"
	.string "quickly, which is why so many of\l"
	.string "them reached us.\p"
	.string "Plant diversity was still below\n"
	.string "pre-impact levels. (inferred)$"

StrataLegumeThicket_Text_NoteCarcass:
	.string "FIELD NOTE: A large plant eater,\n"
	.string "stripped to the bone. Gnaw marks and\l"
	.string "tooth scratches on the shafts.\p"
	.string "EOCONODON was a heavy-jawed meat\n"
	.string "eater, among the first big mammal\l"
	.string "predators after the extinction.\l"
	.string "It probably scavenged too.\p"
	.string "There is still meat on the bones.$"
