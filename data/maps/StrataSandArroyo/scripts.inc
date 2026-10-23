@ Sand Arroyo (present day, BLM land): reached across the badlands' south boundary
@ once Ranger Ortiz has issued the collecting permit. Someone has dug a pit here
@ without a permit; documenting it with Ortiz is a later interlude (outline §1.5).
StrataSandArroyo_MapScripts::
	.byte 0

StrataSandArroyo_EventScript_ContextNote::
	msgbox StrataSandArroyo_Text_ContextNote, MSGBOX_SIGN
	end

StrataSandArroyo_EventScript_Pit::
	msgbox StrataSandArroyo_Text_Pit, MSGBOX_SIGN
	end

StrataSandArroyo_EventScript_Jacket::
	msgbox StrataSandArroyo_Text_Jacket, MSGBOX_SIGN
	end

StrataSandArroyo_EventScript_Spoil::
	msgbox StrataSandArroyo_Text_Spoil, MSGBOX_SIGN
	end

StrataSandArroyo_Text_ContextNote:
	.string "FIELD NOTE: Context is data. The\n"
	.string "layer dates a fossil. Its position\l"
	.string "shows how it died and was buried.\p"
	.string "Dig a bone out with no notes, and\n"
	.string "most of its science goes with it.$"

StrataSandArroyo_Text_Pit:
	.string "A pit cut into the slope with picks\n"
	.string "and a shovel. The tool marks are\l"
	.string "fresh.\p"
	.string "No stakes. No field numbers. No\n"
	.string "flagging tape.\p"
	.string "Whatever came out of here has lost\n"
	.string "its layer.$"

StrataSandArroyo_Text_Jacket:
	.string "A plaster jacket, cracked open and\n"
	.string "left behind. Bone splinters inside.\p"
	.string "There's no field number written on\n"
	.string "it. Nobody can say which layer it\l"
	.string "came from now.$"

StrataSandArroyo_Text_Spoil:
	.string "A heap of grey spoil from the pit.\p"
	.string "Tire tracks run from here toward\n"
	.string "the private-land fence.$"
