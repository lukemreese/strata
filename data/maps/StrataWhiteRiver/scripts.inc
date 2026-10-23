@ Act 6: the White River badlands, South Dakota, ~34-30 Ma. The arrival valley, the notes on the
@ cooling, and the bone stash on the plateau to the south, where the Archaeotherium (the act's
@ boss) waits. Once it has gone, the stash is carrion for the taking (forage), which is where
@ the player decides whether to push the Hesperocyon line toward Epicyon.
StrataWhiteRiver_MapScripts::
	.byte 0

@ The boss: triggered by the stairs up onto the plateau, or by talking to the hell pig.
@ Winning, catching or being outlasted ends the act; running leaves it standing.
StrataWhiteRiver_EventScript_Archaeotherium::
	lockall
	playmoncry SPECIES_ARCHAEOTHERE, CRY_MODE_ENCOUNTER
	msgbox StrataWhiteRiver_Text_ArchaeotheriumAppears, MSGBOX_DEFAULT
	waitmoncry
	strata_boss_prep atk=1
	setwildbattle SPECIES_ARCHAEOTHERE, 40
	dowildbattle
	strata_boss_done
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, StrataWhiteRiver_EventScript_Ran
	setvar VAR_STRATA_STORY, STORY_ACT_DONE(ERA_WHITE_RIVER)
	setflag FLAG_STRATA_A6_STASH_CLEARED
	removeobject LOCALID_STRATA_WR_ARCHAEOTHERIUM
	msgbox StrataWhiteRiver_Text_ArchaeotheriumDone, MSGBOX_DEFAULT
	releaseall
	end

StrataWhiteRiver_EventScript_Ran::
	msgbox StrataWhiteRiver_Text_Ran, MSGBOX_DEFAULT
	releaseall
	end

StrataWhiteRiver_EventScript_NoteCooling::
	msgbox StrataWhiteRiver_Text_NoteCooling, MSGBOX_SIGN
	end

StrataWhiteRiver_EventScript_NoteDogs::
	msgbox StrataWhiteRiver_Text_NoteDogs, MSGBOX_SIGN
	end

StrataWhiteRiver_EventScript_NoteStash::
	msgbox StrataWhiteRiver_Text_NoteStash, MSGBOX_SIGN
	end

StrataWhiteRiver_Text_ArchaeotheriumAppears:
	.string "A stink of rotting meat. Bones are\n"
	.string "piled against the rocks.\p"
	.string "An ARCHAEOTHERIUM, the hell pig,\n"
	.string "guarding its stash!$"

StrataWhiteRiver_Text_ArchaeotheriumDone:
	.string "The ARCHAEOTHERIUM grunts and\n"
	.string "trots away, leaving its stash.\p"
	.string "The air is cooler and drier than\n"
	.string "in the Eocene. Forest is giving way\l"
	.string "to open woodland.\p"
	.string "Report back to DR. HALVORSEN.$"

StrataWhiteRiver_Text_Ran:
	.string "You leave the hell pig to its\n"
	.string "stash. It's still up there.$"

StrataWhiteRiver_Text_NoteCooling:
	.string "FIELD NOTE: Cooling\p"
	.string "About 34 million years ago the\n"
	.string "world cooled fast and ice grew on\l"
	.string "Antarctica. Here the lush Eocene\l"
	.string "forests thinned into open woodland\l"
	.string "with scattered grasses.\p"
	.string "Fossil soils and leaf shapes show\n"
	.string "it. Long legs and fast feet paid\l"
	.string "off. The change took hundreds of\l"
	.string "thousands of years, not a season.$"

StrataWhiteRiver_Text_NoteDogs:
	.string "FIELD NOTE: Hesperocyon\p"
	.string "A fox-sized early dog: long body,\n"
	.string "short legs, and a bony ear chamber\l"
	.string "like later canids have.\p"
	.string "Its kin split into big bone-\n"
	.string "crushing hunters and light, fast\l"
	.string "omnivores. In this model, which\l"
	.string "way a line goes depends on what it\l"
	.string "eats. Mind the bone pile south of\l"
	.string "here.$"

StrataWhiteRiver_Text_NoteStash:
	.string "FIELD NOTE: The bone pile\p"
	.string "Entelodonts like ARCHAEOTHERIUM had\n"
	.string "huge heads with cheek flanges.\l"
	.string "Bites that fit their jaws have\l"
	.string "been reported on other animals'\l"
	.string "bones.\p"
	.string "Hunter or scavenger? Probably\n"
	.string "both. Teeth that crack bone suit\l"
	.string "a carcass-eater. Whatever feeds\l"
	.string "here tilts toward a meat diet.$"
