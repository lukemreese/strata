@ The Levee a year after the impact. Its south edge uses the same return script
@ as the Hell Creek Levee (StrataLevee_EventScript_ReconstructionEdge).
StrataLeveeWinter_MapScripts::
	.byte 0

@ The way into the Burrow Refuge: the mound at (5..7, 19..21), entered from its south side.
StrataLeveeWinter_EventScript_BurrowMouth::
	lockall
	goto_if_set FLAG_STRATA_A2_BURROW_SEEN, StrataLeveeWinter_EventScript_BurrowAsk
	msgbox StrataLeveeWinter_Text_BurrowFirst, MSGBOX_DEFAULT
	setflag FLAG_STRATA_A2_BURROW_SEEN
StrataLeveeWinter_EventScript_BurrowAsk::
	msgbox StrataLeveeWinter_Text_BurrowMouth, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, StrataLeveeWinter_EventScript_BurrowStay
	playse SE_WARP_IN
	warp MAP_STRATA_BURROW, STRATA_ARRIVAL_BURROW
	waitstate
	releaseall
	end

StrataLeveeWinter_EventScript_BurrowStay::
	applymovement OBJ_EVENT_ID_PLAYER, StrataLeveeWinter_Movement_BurrowStepBack
	waitmovement 0
	releaseall
	end

StrataLeveeWinter_Movement_BurrowStepBack:
	walk_down
	step_end

StrataLeveeWinter_EventScript_NoteDark::
	msgbox StrataLeveeWinter_Text_NoteDark, MSGBOX_SIGN
	end

StrataLeveeWinter_EventScript_NoteBurrows::
	msgbox StrataLeveeWinter_Text_NoteBurrows, MSGBOX_SIGN
	end

StrataLeveeWinter_Text_BurrowFirst:
	.string "A dark hole opens at the foot of the\n"
	.string "mound, sized for something small.\p"
	.string "Tracks of tiny feet lead in.$"

StrataLeveeWinter_Text_BurrowMouth:
	.string "Crawl into the burrow?$"

StrataLeveeWinter_Text_NoteDark:
	.string "FIELD NOTE: Dark at noon\p"
	.string "Dust and soot thrown up by the\n"
	.string "impact blocked much of the sun for\l"
	.string "months, perhaps longer.\p"
	.string "How long, and how dark, is still\n"
	.string "debated.$"

StrataLeveeWinter_Text_NoteBurrows:
	.string "FIELD NOTE: Holes in the ground\p"
	.string "Animals that could dig in, or sleep\n"
	.string "through hard times, seem to have\l"
	.string "done better.\p"
	.string "It fits the pattern, but burrows\n"
	.string "rarely fossilize. A hypothesis,\l"
	.string "not a finding.$"
