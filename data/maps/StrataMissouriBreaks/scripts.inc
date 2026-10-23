@ Epilogue: the Missouri Breaks, central Montana. River badlands cut into the Hell Creek
@ Formation, the same rock as the dig, eroding today. Water habitat: gar and snapping turtles
@ in the river, bighorn sheep and turkeys on the benches. West edge: the Montana Prairie.
StrataMissouriBreaks_MapScripts::
	.byte 0

StrataMissouriBreaks_EventScript_NoteRocks::
	msgbox StrataMissouriBreaks_Text_NoteRocks, MSGBOX_SIGN
	end

StrataMissouriBreaks_EventScript_NoteGar::
	msgbox StrataMissouriBreaks_Text_NoteGar, MSGBOX_SIGN
	end

StrataMissouriBreaks_EventScript_NoteSheep::
	msgbox StrataMissouriBreaks_Text_NoteSheep, MSGBOX_SIGN
	end

StrataMissouriBreaks_Text_NoteRocks:
	.string "FIELD NOTE: The Breaks.\p"
	.string "The Missouri is cutting down\n"
	.string "through the Hell Creek Formation\l"
	.string "here, the same rock as the dig you\l"
	.string "started the season on, 66 million\l"
	.string "years on.\p"
	.string "Erosion is exposing bone faster\n"
	.string "than anyone can collect it. That\l"
	.string "is the best argument for\l"
	.string "collecting, and the best argument\l"
	.string "for recording where each bone came\l"
	.string "from.$"

StrataMissouriBreaks_Text_NoteGar:
	.string "FIELD NOTE: Gar and turtles.\p"
	.string "Shortnose gar still live in the\n"
	.string "Missouri, with hard,\l"
	.string "diamond-shaped scales and a swim\l"
	.string "bladder that works like a lung.\l"
	.string "Gars have lived in North American\l"
	.string "rivers since the Cretaceous, and a\l"
	.string "close relative swam in Hell\l"
	.string "Creek's channels.\p"
	.string "The snapping turtle is another old\n"
	.string "survivor: slow, armoured, and\l"
	.string "happy in muddy water. Water and\l"
	.string "burrows were good places to be\l"
	.string "when the filters ran.$"

StrataMissouriBreaks_Text_NoteSheep:
	.string "FIELD NOTE: Bighorn sheep.\p"
	.string "Native to these breaks, but\n"
	.string "hunting and diseases from domestic\l"
	.string "sheep wiped them out across much\l"
	.string "of the West by the early 1900s.\p"
	.string "Animals trapped elsewhere were\n"
	.string "released back into the Breaks from\l"
	.string "the middle of the 20th century.\l"
	.string "Dates differ by herd. Some herds\l"
	.string "still struggle with disease.$"
