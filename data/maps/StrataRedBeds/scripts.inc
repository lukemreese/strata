@ Act 4: Bighorn Basin, Wyoming, ~56 Ma: the Paleocene-Eocene Thermal Maximum.
StrataRedBeds_MapScripts::
	.byte 0

@ The Coryphodon waits on the natural land bridge (y = 26), so it is met from either end.
@ The boss is a wild double with a calf (Lv 28 + Lv 24); the +1 Defense totem boost goes
@ to the adult only. A player with a single mon gets the adult alone: scripted doubles
@ are buggy with one party member.
StrataRedBeds_EventScript_Coryphodon::
	lockall
	playmoncry SPECIES_CORYPHODON, CRY_MODE_ENCOUNTER
	msgbox StrataRedBeds_Text_CoryphodonAppears, MSGBOX_DEFAULT
	waitmoncry
	strata_boss_prep def=1
	getpartysize
	goto_if_ge VAR_RESULT, 2, StrataRedBeds_EventScript_CoryphodonAndCalf
	setwildbattle SPECIES_CORYPHODON, 28
	goto StrataRedBeds_EventScript_CoryphodonBattle

StrataRedBeds_EventScript_CoryphodonAndCalf::
	msgbox StrataRedBeds_Text_CalfAppears, MSGBOX_DEFAULT
	setwildbattle SPECIES_CORYPHODON, 28, ITEM_NONE, SPECIES_CORYPHODON, 24
StrataRedBeds_EventScript_CoryphodonBattle::
	dowildbattle
	strata_boss_done
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, StrataRedBeds_EventScript_Ran
	call StrataRedBeds_EventScript_ResolveCoryphodon
	msgbox StrataRedBeds_Text_CoryphodonDone, MSGBOX_DEFAULT
	goto_if_eq VAR_0x8004, FALSE, StrataRedBeds_EventScript_ReportBack
	msgbox StrataRedBeds_Text_KitRecalibrated, MSGBOX_DEFAULT
	call Strata_EventScript_UpgradeFishingKit
StrataRedBeds_EventScript_ReportBack::
	msgbox StrataRedBeds_Text_ReportBack, MSGBOX_DEFAULT
	releaseall
	end

@ The story state after the battle, free of messages so the test can run it. Any way out
@ of the fight but running finishes the act. Output: VAR_0x8004 = TRUE the first time only,
@ when the fishing kit is still to be recalibrated (Old -> Good), once, after this act.
StrataRedBeds_EventScript_ResolveCoryphodon::
	setvar VAR_STRATA_STORY, STORY_ACT_DONE(ERA_BIGHORN_PETM)
	setvar VAR_0x8004, FALSE
	goto_if_set FLAG_STRATA_ACT4_KIT_UPGRADED, StrataRedBeds_EventScript_ResolveCoryphodonDone
	setflag FLAG_STRATA_ACT4_KIT_UPGRADED
	setvar VAR_0x8004, TRUE
StrataRedBeds_EventScript_ResolveCoryphodonDone::
	return

StrataRedBeds_EventScript_Ran::
	msgbox StrataRedBeds_Text_Ran, MSGBOX_DEFAULT
	releaseall
	end

StrataRedBeds_EventScript_RedBedsNote::
	msgbox StrataRedBeds_Text_RedBedsNote, MSGBOX_SIGN
	end

StrataRedBeds_EventScript_HeatNote::
	msgbox StrataRedBeds_Text_HeatNote, MSGBOX_SIGN
	end

StrataRedBeds_EventScript_DwarfingNote::
	msgbox StrataRedBeds_Text_DwarfingNote, MSGBOX_SIGN
	end

StrataRedBeds_EventScript_LandBridgeNote::
	msgbox StrataRedBeds_Text_LandBridgeNote, MSGBOX_SIGN
	end

StrataRedBeds_Text_CoryphodonAppears:
	.string "The heat is fierce. A huge shape\n"
	.string "heaves itself out of the shallows.\p"
	.string "A CORYPHODON, the largest animal\n"
	.string "in this hothouse world!$"

StrataRedBeds_Text_CalfAppears:
	.string "A calf splashes out of the reeds\n"
	.string "and plants itself at her side!$"

StrataRedBeds_Text_CoryphodonDone:
	.string "The CORYPHODON wallows back into\n"
	.string "the cool mud, calf in tow.\p"
	.string "The soils here are banded red: old\n"
	.string "ground baked in the PETM heat.$"

StrataRedBeds_Text_KitRecalibrated:
	.string "The rig has logged all your time\n"
	.string "in and beside the water.\p"
	.string "It recalibrates your FISHING KIT\n"
	.string "for deeper water.$"

StrataRedBeds_Text_ReportBack:
	.string "Report back to DR. HALVORSEN.$"

StrataRedBeds_Text_Ran:
	.string "You retreat up the bank. The\n"
	.string "CORYPHODON still blocks the way.$"

StrataRedBeds_Text_RedBedsNote:
	.string "FIELD NOTE: RED BEDS\p"
	.string "The purple, red and yellow bands\n"
	.string "are fossil soils from a floodplain.\p"
	.string "Iron minerals give them their\n"
	.string "colour. Stacks of soils like these\l"
	.string "record floods and long dry spells.$"

StrataRedBeds_Text_HeatNote:
	.string "RIG NOTE: HOT LAYER\p"
	.string "This is the warmest layer you will\n"
	.string "visit. Every step builds heat in\l"
	.string "the lineages in your party.\p"
	.string "Hot layers push a lineage toward\n"
	.string "heat-tolerant branches. Keep a\l"
	.string "lineage in the PC if you don't\l"
	.string "want it to change.$"

StrataRedBeds_Text_DwarfingNote:
	.string "FIELD NOTE: SIFRHIPPUS\p"
	.string "The first horse was cat-sized.\n"
	.string "Its teeth show it shrank by about\l"
	.string "30% as the PETM warmed, then grew\l"
	.string "back (Secord et al. 2012).\p"
	.string "Smaller bodies shed heat more\n"
	.string "easily. The cause is still\l"
	.string "debated: heat, or poorer plants.$"

StrataRedBeds_Text_LandBridgeNote:
	.string "FIELD NOTE: LAND BRIDGES\p"
	.string "In the PETM, warm northern land\n"
	.string "linked North America, Europe and\l"
	.string "Asia.\p"
	.string "Horses, primates and even-toed\n"
	.string "hoofed mammals all appear here\l"
	.string "about now. Where each group came\l"
	.string "from first is debated.$"
