@ Hell Creek Camp (present day): the hub. The ranch road runs west to the Lindqvist
@ Ranch and Jordan; the badlands dig is south; the field station door is east.
StrataFieldCamp_MapScripts::
	.byte 0

@ Theo Okafor, PhD student and the rival. His peer-review battles come with C13.
StrataFieldCamp_EventScript_Theo::
	lock
	faceplayer
	goto_if_ge VAR_STRATA_STORY, STORY_ACT_DONE(ERA_HELL_CREEK), StrataFieldCamp_EventScript_TheoLater
	msgbox StrataFieldCamp_Text_TheoAct0, MSGBOX_DEFAULT
	release
	end

StrataFieldCamp_EventScript_TheoLater::
	msgbox StrataFieldCamp_Text_TheoLater, MSGBOX_DEFAULT
	release
	end

@ Josie Lindqvist: undergrad on the crew, and Bea's granddaughter.
StrataFieldCamp_EventScript_Student::
	lock
	faceplayer
	msgbox StrataFieldCamp_Text_Student, MSGBOX_DEFAULT
	goto_if_set FLAG_STRATA_SAW_PAIR, StrataFieldCamp_EventScript_JosieSawPair
	msgbox StrataFieldCamp_Text_JosieRanch, MSGBOX_DEFAULT
	release
	end

StrataFieldCamp_EventScript_JosieSawPair::
	msgbox StrataFieldCamp_Text_JosieSawPair, MSGBOX_DEFAULT
	release
	end

StrataFieldCamp_EventScript_CampSign::
	msgbox StrataFieldCamp_Text_CampSign, MSGBOX_SIGN
	end

StrataFieldCamp_EventScript_StationSign::
	msgbox StrataFieldCamp_Text_StationSign, MSGBOX_SIGN
	end

StrataFieldCamp_EventScript_SuperpositionNote::
	msgbox StrataFieldCamp_Text_SuperpositionNote, MSGBOX_SIGN
	end

@ Where the visiting researcher of each act sets up (peer review, C13).
StrataFieldCamp_EventScript_ResearcherBoard::
	msgbox StrataFieldCamp_Text_ResearcherBoard, MSGBOX_SIGN
	end

StrataFieldCamp_Text_TheoAct0:
	.string "THEO: You're the new field hand?\n"
	.string "THEO OKAFOR. Fourth-year PhD.\p"
	.string "Halvorsen's rig builds a whole world\n"
	.string "from a few bones and some pollen.\p"
	.string "It looks alive. That doesn't make it\n"
	.string "right. How do we know any of it?\p"
	.string "Run your model a few times. Then I'll\n"
	.string "review it. Properly.$"

StrataFieldCamp_Text_TheoLater:
	.string "THEO: Still taking the fancy diorama\n"
	.string "for a walk?\p"
	.string "Every reconstruction is a hypothesis.\n"
	.string "Try to break it before you trust it.$"

StrataFieldCamp_Text_Student:
	.string "JOSIE: See the stripes in the hills?\n"
	.string "Each band is old floodplain mud.\p"
	.string "Lower is older. Climbing the hill is\n"
	.string "climbing forward in time!$"

StrataFieldCamp_Text_JosieRanch:
	.string "My gran's ranch is just west, on the\n"
	.string "road to Jordan.\p"
	.string "She's got something under a tarp out\n"
	.string "there. Go say hi. Tell her I'm\l"
	.string "eating my vegetables.$"

StrataFieldCamp_Text_JosieSawPair:
	.string "You saw the Pair? A TRICERATOPS and\n"
	.string "a TYRANNOSAURUS, buried together.\p"
	.string "It should be in a museum. Gran says\n"
	.string "museums don't pay the feed bill.\p"
	.string "…She's not wrong. That's the worst\n"
	.string "part.$"

StrataFieldCamp_Text_CampSign:
	.string "HELL CREEK FIELD CAMP\n"
	.string "Garfield County, Montana$"

StrataFieldCamp_Text_SuperpositionNote:
	.string "FIELD NOTE: Sediment piles up one\n"
	.string "layer on another, so lower is older.\p"
	.string "That's the law of superposition\n"
	.string "(Steno, 1669).\p"
	.string "Unless the beds were folded or\n"
	.string "faulted. Always check first.$"

StrataFieldCamp_Text_ResearcherBoard:
	.string "VISITING RESEARCHERS: a bench, a\n"
	.string "tent and a plug for a laptop.\p"
	.string "This week: nobody. Next: whoever the\n"
	.string "grant money brings.$"

StrataFieldCamp_Text_StationSign:
	.string "FIELD STATION\n"
	.string "STRATA reconstruction rig inside.$"

@ The camp store: the quartermaster's stock grows with the story. Great Balls and Super
@ Potions come once the Corral Bluffs act (3) is done, Hyper Potions after White River (6).
StrataFieldCamp_EventScript_Quartermaster::
	lock
	faceplayer
	msgbox StrataFieldCamp_Text_QuartermasterWelcome, MSGBOX_DEFAULT
	goto_if_ge VAR_STRATA_STORY, STORY_ACT_DONE(ERA_WHITE_RIVER), StrataFieldCamp_EventScript_StoreTier2
	goto_if_ge VAR_STRATA_STORY, STORY_ACT_DONE(ERA_CORRAL_BLUFFS), StrataFieldCamp_EventScript_StoreTier1
	pokemart StrataFieldCamp_Pokemart_Tier0
	goto StrataFieldCamp_EventScript_StoreBye

StrataFieldCamp_EventScript_StoreTier1::
	pokemart StrataFieldCamp_Pokemart_Tier1
	goto StrataFieldCamp_EventScript_StoreBye

StrataFieldCamp_EventScript_StoreTier2::
	pokemart StrataFieldCamp_Pokemart_Tier2
StrataFieldCamp_EventScript_StoreBye::
	msgbox StrataFieldCamp_Text_QuartermasterBye, MSGBOX_DEFAULT
	release
	end

	.align 2
StrataFieldCamp_Pokemart_Tier0:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	pokemartlistend

	.align 2
StrataFieldCamp_Pokemart_Tier1:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	pokemartlistend

	.align 2
StrataFieldCamp_Pokemart_Tier2:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	pokemartlistend

StrataFieldCamp_Text_QuartermasterWelcome:
	.string "MARGE, QUARTERMASTER: Field supplies\n"
	.string "are on the camp budget. What'll it be?$"

StrataFieldCamp_Text_QuartermasterBye:
	.string "MARGE: Bring back every specimen\n"
	.string "capsule you don't use. They're not\l"
	.string "cheap.$"
