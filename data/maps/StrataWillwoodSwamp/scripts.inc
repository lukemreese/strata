@ Act 4: Willwood Swamp, Willwood Formation, Wyoming (~56 Ma). Field notes only.
StrataWillwoodSwamp_MapScripts::
	.byte 0

StrataWillwoodSwamp_EventScript_WallowNote::
	msgbox StrataWillwoodSwamp_Text_WallowNote, MSGBOX_SIGN
	end

StrataWillwoodSwamp_EventScript_LeafDamageNote::
	msgbox StrataWillwoodSwamp_Text_LeafDamageNote, MSGBOX_SIGN
	end

StrataWillwoodSwamp_EventScript_WarmWaterNote::
	msgbox StrataWillwoodSwamp_Text_WarmWaterNote, MSGBOX_SIGN
	end

StrataWillwoodSwamp_Text_WallowNote:
	.string "FIELD NOTE: CORYPHODON\p"
	.string "A tusked plant eater about as\n"
	.string "heavy as a cow (roughly 500 kg, an\l"
	.string "estimate), and the biggest animal\l"
	.string "of its world.\p"
	.string "Its bones turn up in swampy beds,\n"
	.string "so it is drawn as a wallower.\l"
	.string "Whether it really lived like a\l"
	.string "hippo is debated.$"

StrataWillwoodSwamp_Text_LeafDamageNote:
	.string "FIELD NOTE: LEAVES\p"
	.string "Fossil leaves from the warmest\n"
	.string "layer carry more insect chew marks\l"
	.string "than leaves from just before it\l"
	.string "(Currano et al. 2008).\p"
	.string "More grubs means more food for\n"
	.string "small mammals. Try the mud.$"

StrataWillwoodSwamp_Text_WarmWaterNote:
	.string "FIELD NOTE: COLD-BLOODED\p"
	.string "Gars, turtles, champsosaurs and\n"
	.string "crocodile relatives need warm\l"
	.string "water all year.\p"
	.string "Their bones turn up in Eocene beds\n"
	.string "on Ellesmere Island, far inside\l"
	.string "the Arctic Circle.$"
