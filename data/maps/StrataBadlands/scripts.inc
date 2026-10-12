StrataBadlands_MapScripts::
	.byte 0

StrataBadlands_EventScript_Digger::
	msgbox StrataBadlands_Text_Digger, MSGBOX_NPC
	end

StrataBadlands_EventScript_BoundarySign::
	msgbox StrataBadlands_Text_BoundarySign, MSGBOX_SIGN
	end

StrataBadlands_Text_Digger:
	.string "See this thin, pale line in the\n"
	.string "rock? That's the boundary clay.\p"
	.string "It's rich in iridium: rare in Earth's\n"
	.string "crust, but common in asteroids.\p"
	.string "Below it, dinosaurs. Above it, none,\n"
	.string "except the birds.$"

StrataBadlands_Text_BoundarySign:
	.string "K-PG BOUNDARY\n"
	.string "The end of the Cretaceous, 66 Ma.$"
