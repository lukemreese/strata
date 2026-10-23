@ Act 8: Natural Trap Cave, Wyoming. A sinkhole that trapped animals for a very long time
@ (the fill may span over 100,000 years; its bones record the Ice Age fauna of the region).
@ The boss, the rope out, and the field notes. The sinkhole is on the Ice Age Steppe.
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

StrataTrapCave_EventScript_NoteTrap::
	msgbox StrataTrapCave_Text_NoteTrap, MSGBOX_SIGN
	end

StrataTrapCave_EventScript_NoteBlur::
	msgbox StrataTrapCave_Text_NoteBlur, MSGBOX_SIGN
	end

StrataTrapCave_EventScript_NotePredators::
	msgbox StrataTrapCave_Text_NotePredators, MSGBOX_SIGN
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
	.string "Within ten thousand years it and\n"
	.string "most of the giants here will be\l"
	.string "gone. Why is still argued: climate,\l"
	.string "hunting, or both.\p"
	.string "Climb out. Up top, the rig has\n"
	.string "opened a later sub-layer by the\l"
	.string "anchor.\l"
	.string "Worth a look before you report back\l"
	.string "to DR. HALVORSEN.$"

StrataTrapCave_Text_Ran:
	.string "You back away into the dark. The\n"
	.string "bear's breathing echoes after you.$"

StrataTrapCave_Text_NoteTrap:
	.string "FIELD NOTE: One-way trap\p"
	.string "The floor lies some 25 m below the\n"
	.string "surface, under sheer walls. Animals\l"
	.string "that fell in were often hurt and\l"
	.string "could not climb out.\p"
	.string "It works like a pitfall that never\n"
	.string "empties. The fill may span well\l"
	.string "over 100,000 years; dates are still\l"
	.string "being refined.$"

StrataTrapCave_Text_NoteBlur:
	.string "FIELD NOTE: A blurred snapshot\p"
	.string "Bones of many ages are mixed here,\n"
	.string "so the rig shows an average: the\l"
	.string "Last Glacial Maximum, ~20,000 years\l"
	.string "ago, with earlier and later animals.\p"
	.string "Time averaging makes neighbours of\n"
	.string "animals that never met.$"

StrataTrapCave_Text_NotePredators:
	.string "FIELD NOTE: Hunters in the pit\p"
	.string "Predators turn up too: lions, a\n"
	.string "cheetah-like cat, a short-faced\l"
	.string "bear, wolves. Some fell in chasing\l"
	.string "prey; some may have been lured by\l"
	.string "trapped animals.\p"
	.string "Species lists differ between\n"
	.string "reports. Treat this one as\l"
	.string "provisional.$"
