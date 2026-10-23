@ Act 7: the Waterhole, before the ash (its ash version is StrataWaterholeAsh). The boss
@ is here: a Teleoceras bull and cow (a wild double, Lv 46/42), with the first ash falling
@ during the intro. Winning starts the ashfall for good: the screen fades out and the
@ player wakes up in the ash version, weeks later.
StrataWaterhole_MapScripts::
	.byte 0

@ Triggered by the line across the shore, or by talking to either rhino.
@ Only the bull (the first foe, Lv 46) gets the totem boost.
StrataWaterhole_EventScript_Teleoceras::
	lockall
	msgbox StrataWaterhole_Text_Waterhole, MSGBOX_DEFAULT
	setweather WEATHER_VOLCANIC_ASH
	doweather
	playmoncry SPECIES_TELEOCERAS, CRY_MODE_ENCOUNTER
	msgbox StrataWaterhole_Text_TeleocerasAppear, MSGBOX_DEFAULT
	waitmoncry
	strata_boss_prep def=1
	setwildbattle SPECIES_TELEOCERAS, 46, ITEM_NONE, SPECIES_TELEOCERAS, 42
	dowildbattle
	strata_boss_done
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, StrataWaterhole_EventScript_Ran
	setvar VAR_STRATA_STORY, 15
	setvar VAR_STRATA_ACT7, 2
	msgbox StrataWaterhole_Text_TeleocerasDone, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_WHITE
	delay 90
	warp MAP_STRATA_WATERHOLE_ASH, STRATA_ARRIVAL_WATERHOLE_ASH
	waitstate
	releaseall
	end

StrataWaterhole_EventScript_Ran::
	setweather WEATHER_SHADE
	doweather
	msgbox StrataWaterhole_Text_Ran, MSGBOX_DEFAULT
	releaseall
	end

StrataWaterhole_EventScript_Herd::
	msgbox StrataWaterhole_Text_Herd, MSGBOX_NPC
	end

StrataWaterhole_EventScript_Camel::
	msgbox StrataWaterhole_Text_Camel, MSGBOX_NPC
	end

StrataWaterhole_EventScript_NoteWaterhole::
	msgbox StrataWaterhole_Text_NoteWaterhole, MSGBOX_SIGN
	end

StrataWaterhole_Text_Waterhole:
	.string "The sky over the waterhole has gone\n"
	.string "grey. The first flakes of ash drift\l"
	.string "down, soft as snow.\p"
	.string "They come from a volcano 1,600 km\n"
	.string "away, in what is now Idaho.\p"
	.string "Animals crowd the water. A few are\n"
	.string "already coughing.$"

StrataWaterhole_Text_TeleocerasAppear:
	.string "A TELEOCERAS bull and cow stand\n"
	.string "between you and the water, ash\l"
	.string "dusting their hides!$"

StrataWaterhole_Text_TeleocerasDone:
	.string "The bull staggers back to the herd,\n"
	.string "the cow at his side.\p"
	.string "The ash keeps falling. It will fall\n"
	.string "for days.$"

StrataWaterhole_Text_Ran:
	.string "You back away from the water.\n"
	.string "The bull and cow still guard it.$"

StrataWaterhole_Text_Herd:
	.string "A TELEOCERAS stands knee-deep in\n"
	.string "the water, drinking. Its short legs\l"
	.string "and barrel body make it look like a\l"
	.string "hippo. It ignores you.$"

StrataWaterhole_Text_Camel:
	.string "A PROCAMELUS lifts its head from\n"
	.string "the water. Its ears flick toward the\l"
	.string "west, where the sky is grey.$"

StrataWaterhole_Text_NoteWaterhole:
	.string "FIELD NOTE: One waterhole\p"
	.string "In a dry season animals crowd the\n"
	.string "last water: grazers, browsers,\l"
	.string "predators and scavengers together.\p"
	.string "Bone beds like Ashfall form when\n"
	.string "many die in one place at once. Here\l"
	.string "the cause was ash from far away.$"
