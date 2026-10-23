@ Act 4: Clarks Fork Crossing, Clarks Fork Basin, Wyoming (~56 Ma).
@ Set piece: an Oxyaena stalks the gravel bar across the river (Lv 26, once).
@ VAR_STRATA_ACT4: 0 = not met yet, 1 = met (the triggers stop). The object itself is
@ hidden by FLAG_STRATA_ACT4_OXYAENA once it is beaten or caught, so a player who ran
@ can talk to it again.
StrataClarksFork_MapScripts::
	.byte 0

StrataClarksFork_EventScript_OxyaenaStalksWest::
	lockall
	turnobject LOCALID_STRATA_CLARKS_OXYAENA, DIR_WEST
	call StrataClarksFork_EventScript_OxyaenaFight
	releaseall
	end

StrataClarksFork_EventScript_OxyaenaStalksEast::
	lockall
	turnobject LOCALID_STRATA_CLARKS_OXYAENA, DIR_EAST
	call StrataClarksFork_EventScript_OxyaenaFight
	releaseall
	end

StrataClarksFork_EventScript_Oxyaena::
	lock
	faceplayer
	call StrataClarksFork_EventScript_OxyaenaFight
	release
	end

StrataClarksFork_EventScript_OxyaenaFight::
	playmoncry SPECIES_OXYAENA, CRY_MODE_ENCOUNTER
	msgbox StrataClarksFork_Text_OxyaenaAppears, MSGBOX_DEFAULT
	waitmoncry
	strata_boss_prep
	setwildbattle SPECIES_OXYAENA, 26
	dowildbattle
	strata_boss_done
	call StrataClarksFork_EventScript_ResolveOxyaena
	goto_if_eq VAR_RESULT, TRUE, StrataClarksFork_EventScript_OxyaenaBeaten
	msgbox StrataClarksFork_Text_OxyaenaRan, MSGBOX_DEFAULT
	return

@ The set piece's state after the battle, free of messages so the test can run it.
@ The stalking triggers stop for good; the Oxyaena itself goes away only if it was beaten
@ or caught. Output: VAR_RESULT = TRUE if it is gone.
StrataClarksFork_EventScript_ResolveOxyaena::
	setvar VAR_STRATA_ACT4, 1
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, StrataClarksFork_EventScript_OxyaenaGone
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, StrataClarksFork_EventScript_OxyaenaGone
	setvar VAR_RESULT, FALSE
	return

StrataClarksFork_EventScript_OxyaenaGone::
	setflag FLAG_STRATA_ACT4_OXYAENA
	setvar VAR_RESULT, TRUE
	return

StrataClarksFork_EventScript_OxyaenaBeaten::
	removeobject LOCALID_STRATA_CLARKS_OXYAENA
	msgbox StrataClarksFork_Text_OxyaenaBeaten, MSGBOX_DEFAULT
	giveitem ITEM_CARRION
	return

StrataClarksFork_EventScript_BasinNote::
	msgbox StrataClarksFork_Text_BasinNote, MSGBOX_SIGN
	end

StrataClarksFork_EventScript_GastornisNote::
	msgbox StrataClarksFork_Text_GastornisNote, MSGBOX_SIGN
	end

StrataClarksFork_Text_OxyaenaAppears:
	.string "Something low and long watches you\n"
	.string "from the gravel bar, a dead\l"
	.string "champsosaur at its feet.\p"
	.string "An OXYAENA, a wolverine-sized\n"
	.string "hunter with short, strong jaws!$"

StrataClarksFork_Text_OxyaenaRan:
	.string "You back off along the bar. The\n"
	.string "OXYAENA doesn't follow, but it\l"
	.string "doesn't leave its kill either.$"

StrataClarksFork_Text_OxyaenaBeaten:
	.string "The OXYAENA bolts, leaving its\n"
	.string "kill behind.\p"
	.string "It is no cat and no dog: oxyaenids\n"
	.string "were an older, extinct branch of\l"
	.string "meat eaters.$"

StrataClarksFork_Text_BasinNote:
	.string "FIELD NOTE: CLARKS FORK BASIN\p"
	.string "Rivers laid these beds one flood\n"
	.string "after another, and a century of\l"
	.string "collecting has put the fossils in\l"
	.string "order.\p"
	.string "The carbon dip fixes the PETM in\n"
	.string "the stack. That is how arrivals\l"
	.string "like the first horses are dated.$"

StrataClarksFork_Text_GastornisNote:
	.string "FIELD NOTE: GASTORNIS\p"
	.string "A flightless bird taller than a\n"
	.string "person, with a huge beak. It was\l"
	.string "drawn as a predator for a century.\p"
	.string "Its blunt, hoof-like claws and a\n"
	.string "bone-chemistry study now point to\l"
	.string "a plant eater. That is still\l"
	.string "debated. Fruit and greens may\l"
	.string "steer a bird lineage.$"
