@ Jordan café: coffee, pie and gossip about fossil prices.
StrataJordanCafe_MapScripts::
	.byte 0

@ Coffee for the dig crew: heals the party.
StrataJordanCafe_EventScript_Owner::
	lock
	faceplayer
	msgbox StrataJordanCafe_Text_Owner, MSGBOX_DEFAULT
	call Common_EventScript_OutOfCenterPartyHeal
	msgbox StrataJordanCafe_Text_OwnerHealed, MSGBOX_DEFAULT
	release
	end

StrataJordanCafe_EventScript_OldTimer::
	msgbox StrataJordanCafe_Text_OldTimer, MSGBOX_NPC
	end

StrataJordanCafe_EventScript_Tourist::
	msgbox StrataJordanCafe_Text_Tourist, MSGBOX_NPC
	end

StrataJordanCafe_Text_Owner:
	.string "Dig crew drinks free. Halvorsen's\n"
	.string "been coming here thirty summers.\p"
	.string "Sit down, all of you. You look like\n"
	.string "the badlands chewed you up.$"

StrataJordanCafe_Text_OwnerHealed:
	.string "Coffee and a slice of pie. Everyone\n"
	.string "perked right up.$"

StrataJordanCafe_Text_OldTimer:
	.string "My granddad homesteaded out here.\n"
	.string "He plowed up a bone the size of a\l"
	.string "fence post once.\p"
	.string "Used it to prop the barn door for\n"
	.string "twenty years. Nobody knew what it\l"
	.string "was, or where it came from.$"

StrataJordanCafe_Text_Tourist:
	.string "I paid a ranch near here to dig for\n"
	.string "a day. Found a gar scale! It's mine.\p"
	.string "Private land, private fossils. The\n"
	.string "rancher said that's the law here.$"
