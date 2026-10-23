@ Act 7: the Waterhole after the ash (the same layout as StrataWaterhole). The player
@ arrives here from the boss battle; the first frame shows the "weeks later" text.
StrataWaterholeAsh_MapScripts::
	map_script MAP_SCRIPT_ON_FRAME_TABLE, StrataWaterholeAsh_OnFrame
	.byte 0

StrataWaterholeAsh_OnFrame:
	map_script_2 VAR_STRATA_ACT7, 2, StrataWaterholeAsh_EventScript_Weeks
	.2byte 0

StrataWaterholeAsh_EventScript_Weeks::
	lockall
	setvar VAR_STRATA_ACT7, 3
	msgbox StrataWaterhole_Text_Weeks, MSGBOX_DEFAULT
	releaseall
	end

StrataWaterhole_EventScript_AshRhino::
	msgbox StrataWaterhole_Text_AshRhino, MSGBOX_NPC
	end

StrataWaterhole_EventScript_NoteBarn::
	msgbox StrataWaterhole_Text_NoteBarn, MSGBOX_SIGN
	end

StrataWaterhole_EventScript_NoteGlass::
	msgbox StrataWaterhole_Text_NoteGlass, MSGBOX_SIGN
	end

StrataWaterhole_Text_Weeks:
	.string "Weeks later.\p"
	.string "The waterhole is half-buried in grey.\n"
	.string "Breathing the glassy ash made them\l"
	.string "sick. The small animals died first,\l"
	.string "then the horses and camels, the\l"
	.string "rhinos last.\p"
	.string "Their skeletons will be found here,\n"
	.string "still lying as they fell.\p"
	.string "Report back to DR. HALVORSEN.$"

StrataWaterhole_Text_AshRhino:
	.string "A TELEOCERAS stands in the ash, head\n"
	.string "low. Its breathing is slow and\l"
	.string "rough. It doesn't look up.$"

StrataWaterhole_Text_NoteBarn:
	.string "FIELD NOTE: The rhino barn\p"
	.string "At the real site a shelter, the\n"
	.string "“rhino barn”, covers part of the\l"
	.string "dig. The skeletons still lie where\l"
	.string "they died, adults with young.\p"
	.string "Teleoceras bones here carry damage\n"
	.string "linked to lung disease. The order\l"
	.string "of deaths is partly inference.$"

StrataWaterhole_Text_NoteGlass:
	.string "FIELD NOTE: Glass, not ash\p"
	.string "Volcanic ash is not burnt wood. It\n"
	.string "is tiny, sharp shards of volcanic\l"
	.string "glass.\p"
	.string "Breathed in, they scar the lungs.\n"
	.string "Settled on grass, they wear teeth\l"
	.string "and clog the gut. Grazers suffer\l"
	.string "most.$"
