@ BLM field office in Jordan: Ranger Lucia Ortiz. After the impact-winter act she
@ issues the collecting permit (FLAG_STRATA_BLM_PERMIT), which opens the BLM
@ boundary south of the badlands into Sand Arroyo.
StrataBlmOffice_MapScripts::
	.byte 0

StrataBlmOffice_EventScript_Ranger::
	lock
	faceplayer
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
	release
	end

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
