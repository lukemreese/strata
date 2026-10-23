@ Hell Creek Badlands (present day): Dale's tutorial dig at the outcrop, the K-Pg
@ boundary, and the BLM boundary south of it (Sand Arroyo needs the collecting permit).
StrataBadlands_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, StrataBadlands_OnTransition
	.byte 0

StrataBadlands_OnTransition:
	call_if_set FLAG_STRATA_BLM_PERMIT, StrataBadlands_EventScript_OpenBoundary
	end

@ The boundary triggers fire only while VAR_TEMP_1 is 0.
StrataBadlands_EventScript_OpenBoundary::
	setvar VAR_TEMP_1, 1
	return

StrataBadlands_EventScript_BlmFence::
	lockall
	msgbox StrataBadlands_Text_BlmFence, MSGBOX_DEFAULT
	applymovement OBJ_EVENT_ID_PLAYER, StrataBadlands_Movement_StepBack
	waitmovement 0
	releaseall
	end

StrataBadlands_Movement_StepBack:
	walk_up
	step_end

@ ---------------------------------------------------------------------------
@ The tutorial dig. Dale sends the player to the three survey stakes where the
@ starter specimens came out of the rock; each stake logs one site's layer.
@ ---------------------------------------------------------------------------
StrataBadlands_EventScript_Digger::
	lock
	faceplayer
	goto_if_set FLAG_STRATA_DIG_DONE, StrataBadlands_EventScript_DiggerAfter
	goto_if_unset FLAG_STRATA_DIG_STARTED, StrataBadlands_EventScript_DigIntro
	goto_if_unset FLAG_STRATA_DIG_JAW, StrataBadlands_EventScript_DigRemind
	goto_if_unset FLAG_STRATA_DIG_BIRD, StrataBadlands_EventScript_DigRemind
	goto_if_unset FLAG_STRATA_DIG_SHELL, StrataBadlands_EventScript_DigRemind
	msgbox StrataBadlands_Text_DigDone, MSGBOX_DEFAULT
	giveitem ITEM_POTION, 3
	setflag FLAG_STRATA_DIG_DONE
	msgbox StrataBadlands_Text_DigDoneBoundary, MSGBOX_DEFAULT
	release
	end

StrataBadlands_EventScript_DigIntro::
	msgbox StrataBadlands_Text_DigIntro, MSGBOX_DEFAULT
	setflag FLAG_STRATA_DIG_STARTED
	release
	end

StrataBadlands_EventScript_DigRemind::
	msgbox StrataBadlands_Text_DigRemind, MSGBOX_DEFAULT
	release
	end

StrataBadlands_EventScript_DiggerAfter::
	goto_if_ge VAR_STRATA_STORY, STORY_IN_ACT(ERA_HELL_CREEK), StrataBadlands_EventScript_DiggerLater
	msgbox StrataBadlands_Text_Digger, MSGBOX_DEFAULT
	release
	end

StrataBadlands_EventScript_DiggerLater::
	msgbox StrataBadlands_Text_DiggerLater, MSGBOX_DEFAULT
	release
	end

StrataBadlands_EventScript_StakeJaw::
	lockall
	goto_if_unset FLAG_STRATA_DIG_STARTED, StrataBadlands_EventScript_StakeIdle
	goto_if_set FLAG_STRATA_DIG_JAW, StrataBadlands_EventScript_StakeLogged
	msgbox StrataBadlands_Text_StakeJaw, MSGBOX_DEFAULT
	setflag FLAG_STRATA_DIG_JAW
	goto StrataBadlands_EventScript_StakeCheckAll

StrataBadlands_EventScript_StakeBird::
	lockall
	goto_if_unset FLAG_STRATA_DIG_STARTED, StrataBadlands_EventScript_StakeIdle
	goto_if_set FLAG_STRATA_DIG_BIRD, StrataBadlands_EventScript_StakeLogged
	msgbox StrataBadlands_Text_StakeBird, MSGBOX_DEFAULT
	setflag FLAG_STRATA_DIG_BIRD
	goto StrataBadlands_EventScript_StakeCheckAll

StrataBadlands_EventScript_StakeShell::
	lockall
	goto_if_unset FLAG_STRATA_DIG_STARTED, StrataBadlands_EventScript_StakeIdle
	goto_if_set FLAG_STRATA_DIG_SHELL, StrataBadlands_EventScript_StakeLogged
	msgbox StrataBadlands_Text_StakeShell, MSGBOX_DEFAULT
	setflag FLAG_STRATA_DIG_SHELL
	goto StrataBadlands_EventScript_StakeCheckAll

StrataBadlands_EventScript_StakeCheckAll::
	goto_if_unset FLAG_STRATA_DIG_JAW, StrataBadlands_EventScript_StakeEnd
	goto_if_unset FLAG_STRATA_DIG_BIRD, StrataBadlands_EventScript_StakeEnd
	goto_if_unset FLAG_STRATA_DIG_SHELL, StrataBadlands_EventScript_StakeEnd
	goto_if_set FLAG_STRATA_DIG_DONE, StrataBadlands_EventScript_StakeEnd
	msgbox StrataBadlands_Text_StakesAllLogged, MSGBOX_DEFAULT
StrataBadlands_EventScript_StakeEnd::
	releaseall
	end

StrataBadlands_EventScript_StakeIdle::
	msgbox StrataBadlands_Text_StakeIdle, MSGBOX_DEFAULT
	releaseall
	end

StrataBadlands_EventScript_StakeLogged::
	msgbox StrataBadlands_Text_StakeLogged, MSGBOX_DEFAULT
	releaseall
	end

StrataBadlands_EventScript_BoundarySign::
	msgbox StrataBadlands_Text_BoundarySign, MSGBOX_SIGN
	end

StrataBadlands_EventScript_FormationNote::
	msgbox StrataBadlands_Text_FormationNote, MSGBOX_SIGN
	end

StrataBadlands_EventScript_BlmBoundary::
	msgbox StrataBadlands_Text_BlmBoundary, MSGBOX_SIGN
	end

StrataBadlands_Text_DigIntro:
	.string "DALE: So you're the new hand. I'm\n"
	.string "DALE, crew chief. First lesson's\l"
	.string "free.\p"
	.string "A bone without its layer is just\n"
	.string "a rock.\p"
	.string "Your three specimens came out of\n"
	.string "this outcrop. I left a survey stake\l"
	.string "at each spot.\p"
	.string "Go read the rock at all three. Log\n"
	.string "how far below the boundary clay\l"
	.string "each one sat. Then come find me.$"

StrataBadlands_Text_DigRemind:
	.string "DALE: Three stakes, three sites.\n"
	.string "Log every one before you come back.\p"
	.string "Height below the clay, rock type,\n"
	.string "what else is in it. Write it down.$"

StrataBadlands_Text_DigDone:
	.string "DALE: Let's see your notebook…\p"
	.string "Jaw, 2.4 meters down. Bird, 5.1.\n"
	.string "Shell, 0.8. Good, clean notes.\p"
	.string "Now those fossils mean something.\n"
	.string "All three lived right at the end:\l"
	.string "the top few meters of the\l"
	.string "Cretaceous.\p"
	.string "Here. Camp-store quality, but they\n"
	.string "work.$"

StrataBadlands_Text_DigDoneBoundary:
	.string "One more thing. That thin, pale\n"
	.string "line above all three sites?\p"
	.string "That's the boundary clay. Their\n"
	.string "kind made it over that line. The\l"
	.string "tyrannosaurs didn't.\p"
	.string "Figuring out why is the doc's job.\n"
	.string "And now yours.$"

StrataBadlands_Text_Digger:
	.string "DALE: See this thin, pale line in\n"
	.string "the rock? That's the boundary clay.\p"
	.string "It's rich in iridium: rare in\n"
	.string "Earth's crust, but common in\l"
	.string "asteroids.\p"
	.string "Below it, dinosaurs. Above it, none,\n"
	.string "except the birds.$"

StrataBadlands_Text_DiggerLater:
	.string "DALE: Rain last night. Every storm\n"
	.string "washes a little more of this hill\l"
	.string "away.\p"
	.string "Bones come out, and if nobody picks\n"
	.string "them up, the next storm breaks them.\p"
	.string "Collect them with notes, or lose\n"
	.string "them. Those are the two choices.$"

StrataBadlands_Text_StakeIdle:
	.string "A survey stake with orange flagging\n"
	.string "tape. It's one of DALE's. Better ask\l"
	.string "him about it first.$"

StrataBadlands_Text_StakeLogged:
	.string "A survey stake. This site is\n"
	.string "already in your field notebook.$"

StrataBadlands_Text_StakeJaw:
	.string "Stake 1: the mammal jaw site.\p"
	.string "Grey mudstone: old floodplain. The\n"
	.string "boundary clay is 2.4 meters up the\l"
	.string "slope.\p"
	.string "Most Hell Creek mammals are known\n"
	.string "only from teeth and jaws.\p"
	.string "{PLAYER} logged the site: Hell Creek\n"
	.string "Formation, 2.4 m below the K-Pg.$"

StrataBadlands_Text_StakeBird:
	.string "Stake 2: the ground bird site.\p"
	.string "Cross-bedded sandstone: an old river\n"
	.string "channel, 5.1 meters below the clay.\p"
	.string "Bird bones are thin and hollow. Few\n"
	.string "survive a tumble down a river.\p"
	.string "{PLAYER} logged the site: Hell Creek\n"
	.string "Formation, 5.1 m below the K-Pg.$"

StrataBadlands_Text_StakeShell:
	.string "Stake 3: the snapping turtle site.\p"
	.string "Dark mudstone from a quiet pond, full\n"
	.string "of gar scales and shell scraps,\l"
	.string "0.8 meters below the clay.\p"
	.string "Turtle shell is one of the commonest\n"
	.string "fossils in Hell Creek rock.\p"
	.string "{PLAYER} logged the site: Hell Creek\n"
	.string "Formation, 0.8 m below the K-Pg.$"

StrataBadlands_Text_StakesAllLogged:
	.string "That's all three sites logged.\n"
	.string "Time to show DALE the notebook.$"

StrataBadlands_Text_BoundarySign:
	.string "K-PG BOUNDARY\n"
	.string "The end of the Cretaceous, 66 Ma.$"

StrataBadlands_Text_FormationNote:
	.string "FIELD NOTE: These grey and tan bands\n"
	.string "are the Hell Creek Formation.\p"
	.string "River sand and floodplain mud, laid\n"
	.string "down about 67 to 66 million years\l"
	.string "ago.\p"
	.string "Above the boundary clay, the rock\n"
	.string "is Paleocene: the Tullock beds.$"

StrataBadlands_Text_BlmBoundary:
	.string "BLM BOUNDARY: public land beyond.\p"
	.string "Collecting vertebrate fossils on\n"
	.string "federal land needs a permit.$"

StrataBadlands_Text_BlmFence:
	.string "A barbed-wire fence marks the BLM\n"
	.string "boundary.\p"
	.string "No permit, no digging. Better not\n"
	.string "go past it.$"
