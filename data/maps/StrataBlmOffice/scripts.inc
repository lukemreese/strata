@ BLM field office in Jordan: Ranger Lucia Ortiz. After the impact-winter act she
@ issues the collecting permit (FLAG_STRATA_BLM_PERMIT), which opens the BLM
@ boundary south of the badlands into Sand Arroyo.
StrataBlmOffice_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, StrataBlmOffice_OnTransition
	.byte 0

@ Ortiz is out in the field while the pit and citation interludes are due (S1).
StrataBlmOffice_OnTransition:
	special Strata_StoryPrepareMap
	call_if_eq VAR_TEMP_4, SUBPLOT_PIT_DOCUMENTED, StrataBlmOffice_EventScript_RangerOut
	call_if_eq VAR_TEMP_4, SUBPLOT_CITATION, StrataBlmOffice_EventScript_RangerOut
	end

StrataBlmOffice_EventScript_RangerOut::
	setflag FLAG_TEMP_9
	return

StrataBlmOffice_EventScript_Ranger::
	lock
	faceplayer
	goto_if_ge VAR_STRATA_SUBPLOT, SUBPLOT_CITATION, StrataBlmOffice_EventScript_RangerCited
	goto_if_ge VAR_STRATA_SUBPLOT, SUBPLOT_PIT_DOCUMENTED, StrataBlmOffice_EventScript_RangerCase
	goto_if_set FLAG_STRATA_BLM_PERMIT, StrataBlmOffice_EventScript_RangerPermitted
	goto_if_ge VAR_STRATA_STORY, STORY_ACT_DONE(ERA_IMPACT_WINTER), StrataBlmOffice_EventScript_GivePermit
	msgbox StrataBlmOffice_Text_RangerAct0, MSGBOX_DEFAULT
	release
	end

StrataBlmOffice_EventScript_GivePermit::
	msgbox StrataBlmOffice_Text_RangerOffer, MSGBOX_DEFAULT
	setflag FLAG_STRATA_BLM_PERMIT
	playfanfare MUS_OBTAIN_ITEM
	message StrataBlmOffice_Text_GotPermit
	waitfanfare
	waitmessage
	msgbox StrataBlmOffice_Text_RangerAfterPermit, MSGBOX_DEFAULT
	@ The permit interlude (S1). Out of order (an old save), Strata_StoryPrepareMap catches up.
	call_if_eq VAR_STRATA_SUBPLOT, SUBPLOT_FERN_SPIKE, StrataBlmOffice_EventScript_PermitBeat
	release
	end

StrataBlmOffice_EventScript_PermitBeat::
	setvar VAR_STRATA_SUBPLOT, SUBPLOT_BLM_PERMIT
	return

StrataBlmOffice_EventScript_RangerCase::
	msgbox StrataBlmOffice_Text_RangerCase, MSGBOX_DEFAULT
	release
	end

StrataBlmOffice_EventScript_RangerCited::
	msgbox StrataBlmOffice_Text_RangerCited, MSGBOX_DEFAULT
	release
	end

StrataBlmOffice_Text_RangerCase::
	.string "RANGER ORTIZ: Your notes from the\n"
	.string "pit are in the case file. Photos,\l"
	.string "GPS, layer. Clean work.\p"
	.string "Now I find out whose crew drove\n"
	.string "those tire tracks.$"

StrataBlmOffice_Text_RangerCited::
	.string "RANGER ORTIZ: KESSLER paid the fine\n"
	.string "the day it came. He always does.\p"
	.string "The point was never the money. It's\n"
	.string "a record that the line was crossed.$"

StrataBlmOffice_EventScript_RangerPermitted::
	msgbox StrataBlmOffice_Text_RangerAfterPermit, MSGBOX_DEFAULT
	release
	end

StrataBlmOffice_EventScript_Binder::
	msgbox StrataBlmOffice_Text_Binder, MSGBOX_SIGN
	end

StrataBlmOffice_EventScript_Map::
	msgbox StrataBlmOffice_Text_Map, MSGBOX_SIGN
	end

StrataBlmOffice_Text_RangerAct0:
	.string "RANGER ORTIZ: LUCIA ORTIZ, BLM. I\n"
	.string "look after the fossils on public\l"
	.string "land in this county.\p"
	.string "Out here the land's a patchwork:\n"
	.string "private, state, federal. The bones\l"
	.string "don't care whose they are.\p"
	.string "People do. Keep good notes, and keep\n"
	.string "your GPS on. Notes are evidence.$"

StrataBlmOffice_Text_RangerOffer:
	.string "RANGER ORTIZ: HALVORSEN says you\n"
	.string "keep the best notes on her crew.\p"
	.string "I need eyes on the BLM ground south\n"
	.string "of your badlands. Sand Arroyo.\p"
	.string "Your station's paperwork covers you.\n"
	.string "Here's your collecting permit.$"

StrataBlmOffice_Text_GotPermit:
	.string "{PLAYER} received the BLM collecting\n"
	.string "permit!$"

StrataBlmOffice_Text_RangerAfterPermit:
	.string "RANGER ORTIZ: Anything you find on\n"
	.string "BLM land stays public. It goes to a\l"
	.string "museum, not a mantelpiece.\p"
	.string "And if you see a hole that shouldn't\n"
	.string "be there, don't touch it. Photograph\l"
	.string "it, log it, and call me.$"

StrataBlmOffice_Text_Binder:
	.string "A binder: PALEONTOLOGICAL RESOURCES\n"
	.string "PRESERVATION ACT (2009).\p"
	.string "Fossils on federal land are public.\n"
	.string "Collecting the vertebrate ones needs\l"
	.string "a permit, and the finds stay public,\l"
	.string "in an approved museum repository.$"

StrataBlmOffice_Text_Map:
	.string "A wall map of the county's land:\n"
	.string "yellow for BLM, blue for state,\l"
	.string "white for private.\p"
	.string "The colors make a patchwork. A fence\n"
	.string "is the only way to tell them apart\l"
	.string "on the ground.$"
