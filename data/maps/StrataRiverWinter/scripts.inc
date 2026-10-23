StrataRiverWinter_MapScripts::
	.byte 0

StrataRiverWinter_EventScript_Bluff::
	msgbox StrataRiverWinter_Text_Bluff, MSGBOX_SIGN
	end

StrataRiverWinter_Text_Bluff:
	.string "The bluff is silent. A huge skull\n"
	.string "lies half-buried in grey ash.\p"
	.string "Nothing up here is big enough to\n"
	.string "rule it now.$"

StrataRiverWinter_EventScript_NoteFreshwater::
	msgbox StrataRiverWinter_Text_NoteFreshwater, MSGBOX_SIGN
	end

StrataRiverWinter_Text_NoteFreshwater:
	.string "FIELD NOTE: Water is a refuge\p"
	.string "Rivers and swamps kept a food\n"
	.string "supply: dead leaves, insects,\l"
	.string "snails.\p"
	.string "Turtles, champsosaurs and crocodile\n"
	.string "relatives mostly came through.\l"
	.string "Animals that can go months without\l"
	.string "food had the best odds.$"
