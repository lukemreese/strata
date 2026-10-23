@ Act 8: Natural Trap Cave, Wyoming. A sinkhole that trapped animals for over
@ 100,000 years; its bones record the Ice Age fauna of the region.
StrataTrapCave_MapScripts::
	.byte 0

StrataTrapCave_EventScript_Rope::
	lockall
	msgbox StrataTrapCave_Text_Rope, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, StrataTrapCave_EventScript_Stay
	warp MAP_STRATA_STEPPE, 66, 13
	waitstate
	releaseall
	end

StrataTrapCave_EventScript_Stay::
	releaseall
	end

StrataTrapCave_EventScript_Arctodus::
	lockall
	msgbox StrataTrapCave_Text_Bones, MSGBOX_DEFAULT
	playmoncry SPECIES_ARCTODUS, CRY_MODE_ENCOUNTER
	msgbox StrataTrapCave_Text_ArctodusAppears, MSGBOX_DEFAULT
	waitmoncry
	strata_boss_prep atk=1
	setwildbattle SPECIES_ARCTODUS, 52
	dowildbattle
	strata_boss_done
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, StrataTrapCave_EventScript_Ran
	setvar VAR_STRATA_STORY, 17
	msgbox StrataTrapCave_Text_ArctodusDone, MSGBOX_DEFAULT
	releaseall
	end

StrataTrapCave_EventScript_Ran::
	msgbox StrataTrapCave_Text_Ran, MSGBOX_DEFAULT
	releaseall
	end

StrataTrapCave_Text_Rope:
	.string "Your rope hangs from the opening far\n"
	.string "above. Climb back out?$"

StrataTrapCave_Text_Bones:
	.string "The cave floor is thick with bones:\n"
	.string "horses, a cheetah, a young mammoth.\p"
	.string "Something living has fallen in too.$"

StrataTrapCave_Text_ArctodusAppears:
	.string "A giant short-faced bear rears up,\n"
	.string "trapped and furious! ARCTODUS!$"

StrataTrapCave_Text_ArctodusDone:
	.string "Exhausted, the bear slumps against\n"
	.string "the cave wall.\p"
	.string "Within a few thousand years, it and\n"
	.string "most of the giants here will be\l"
	.string "gone forever.\p"
	.string "Climb out and report back to\n"
	.string "DR. HALVORSEN.$"

StrataTrapCave_Text_Ran:
	.string "You back away into the dark. The\n"
	.string "bear's breathing echoes after you.$"
