StrataBackswampWinter_MapScripts::
	.byte 0

@ The impact winter's "boss" is the environment: three hungry survivors in a row,
@ with no chance to heal between them. Losing whites out and leaves the story
@ at 4, so the gauntlet is waiting on the next visit. Smart wild AI (strata_boss_prep)
@ for all three fights; the old crocodylian that ends it also gets a +1 Attack totem boost.
StrataBackswampWinter_EventScript_Gauntlet::
	lockall
	msgbox StrataBackswampWinter_Text_Approach, MSGBOX_DEFAULT
	playmoncry SPECIES_CHAMPSOSAUR, CRY_MODE_ENCOUNTER
	waitmoncry
	strata_boss_prep
	setwildbattle SPECIES_CHAMPSOSAUR, 13
	dowildbattle
	call StrataBackswampWinter_EventScript_CheckFled
	msgbox StrataBackswampWinter_Text_SecondSurvivor, MSGBOX_DEFAULT
	playmoncry SPECIES_BOREALOSUCH, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_BOREALOSUCH, 14
	dowildbattle
	call StrataBackswampWinter_EventScript_CheckFled
	msgbox StrataBackswampWinter_Text_OldCroc, MSGBOX_DEFAULT
	playmoncry SPECIES_BOREALOSUCH, CRY_MODE_ENCOUNTER
	waitmoncry
	strata_boss_prep atk=1
	setwildbattle SPECIES_BOREALOSUCH, 16
	dowildbattle
	call StrataBackswampWinter_EventScript_CheckFled
	strata_boss_done
	setvar VAR_STRATA_STORY, 5
	msgbox StrataBackswampWinter_Text_FernSpike, MSGBOX_DEFAULT
	releaseall
	end

StrataBackswampWinter_EventScript_CheckFled::
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, StrataBackswampWinter_EventScript_Fled
	return

StrataBackswampWinter_EventScript_Fled::
	strata_boss_done
	msgbox StrataBackswampWinter_Text_Fled, MSGBOX_DEFAULT
	releaseall
	end

StrataBackswampWinter_Text_Approach:
	.string "The last open water in the swamp.\n"
	.string "Low shapes slide out of the mud.\p"
	.string "Nothing here has eaten in months.$"

StrataBackswampWinter_Text_SecondSurvivor:
	.string "Before you can catch your breath,\n"
	.string "another one surfaces!$"

StrataBackswampWinter_Text_OldCroc:
	.string "The water heaves. The biggest of\n"
	.string "them all, an old crocodylian, has\l"
	.string "waited out the dark!$"

StrataBackswampWinter_Text_Fled:
	.string "You scramble back. The survivors\n"
	.string "still guard the water.$"

StrataBackswampWinter_Text_FernSpike:
	.string "The swamp falls quiet.\p"
	.string "Through the ash at your feet, tiny\n"
	.string "green coils are unfurling.\p"
	.string "Ferns. The first plants to return.\n"
	.string "Life is starting over.\p"
	.string "Better tell DR. HALVORSEN.$"
