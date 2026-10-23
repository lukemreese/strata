@ Strata field gear: waders (surf without a badge or HM) and the fishing kit
@ (the Old Rod, renamed; upgraded to the Good and Super Rod). See src/strata_field.c.

@ Pressing A at the water's edge with the waders (GetInteractedWaterScript).
EventScript_StrataWade::
	lockall
	msgbox Text_StrataWantToWade, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EventScript_StrataWadeEnd
	msgbox Text_StrataWadedIn, MSGBOX_DEFAULT
	@ PARTY_SIZE: no mon to show; see SurfFieldEffect_Init.
	setfieldeffectargument 0, PARTY_SIZE
	dofieldeffect FLDEFF_USE_SURF
EventScript_StrataWadeEnd::
	releaseall
	end

@ call Strata_EventScript_GiveWaterGear
@ Gives the waders and the first fishing kit, each only if the player lacks it,
@ with the usual "obtained" messages. Safe to call more than once.
Strata_EventScript_GiveWaterGear::
	checkitem ITEM_WADERS
	call_if_eq VAR_RESULT, FALSE, Strata_EventScript_GiveWaders
	checkitem ITEM_OLD_ROD
	goto_if_eq VAR_RESULT, TRUE, Strata_EventScript_GiveWaterGearDone
	checkitem ITEM_GOOD_ROD
	goto_if_eq VAR_RESULT, TRUE, Strata_EventScript_GiveWaterGearDone
	checkitem ITEM_SUPER_ROD
	goto_if_eq VAR_RESULT, TRUE, Strata_EventScript_GiveWaterGearDone
	giveitem ITEM_OLD_ROD
	msgbox Text_StrataFishingKitHelp, MSGBOX_DEFAULT
Strata_EventScript_GiveWaterGearDone::
	return

Strata_EventScript_GiveWaders::
	giveitem ITEM_WADERS
	msgbox Text_StrataWadersHelp, MSGBOX_DEFAULT
	return

@ call Strata_EventScript_UpgradeFishingKit
@ Swaps the fishing kit for the next one up (Old -> Good -> Super Rod).
@ Output: VAR_RESULT = the new kit, or ITEM_NONE if it was already the best.
Strata_EventScript_UpgradeFishingKit::
	special Strata_SpecialUpgradeFishingKit
	goto_if_eq VAR_RESULT, ITEM_NONE, Strata_EventScript_UpgradeFishingKitDone
	playfanfare MUS_OBTAIN_ITEM
	msgbox Text_StrataFishingKitUpgraded, MSGBOX_DEFAULT
	waitfanfare
Strata_EventScript_UpgradeFishingKitDone::
	return

Text_StrataWantToWade:
	.string "The water looks deep.\n"
	.string "Wade in?$"

Text_StrataWadedIn:
	.string "{PLAYER} waded in.\n"
	.string "The rig handles the depth.$"

Text_StrataWadersHelp:
	.string "Face deep water and press A to\n"
	.string "wade in. Time spent in and by the\l"
	.string "water shapes your lineages too.$"

Text_StrataFishingKitHelp:
	.string "Use the FISHING KIT facing water\n"
	.string "to see what lives below.$"

Text_StrataFishingKitUpgraded:
	.string "{PLAYER}'s fishing kit became\n"
	.string "the {STR_VAR_1}!$"
