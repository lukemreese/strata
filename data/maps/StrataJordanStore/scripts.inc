@ Jordan general store (the stock Mart layout).
StrataJordanStore_MapScripts::
	.byte 0

StrataJordanStore_EventScript_Clerk::
	lock
	faceplayer
	msgbox StrataJordanStore_Text_ClerkWelcome, MSGBOX_DEFAULT
	pokemart StrataJordanStore_Pokemart
	msgbox StrataJordanStore_Text_ClerkBye, MSGBOX_DEFAULT
	release
	end

	.align 2
StrataJordanStore_Pokemart:
	.2byte ITEM_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_POKE_BALL
	pokemartlistend

StrataJordanStore_EventScript_Shopper::
	msgbox StrataJordanStore_Text_Shopper, MSGBOX_NPC
	end

StrataJordanStore_Text_ClerkWelcome:
	.string "Feed, fencing, first aid. If we\n"
	.string "don't have it, Billings does.$"

StrataJordanStore_Text_ClerkBye:
	.string "Tell DALE his plaster came in.$"

StrataJordanStore_Text_Shopper:
	.string "The dig crew buys plaster and burlap\n"
	.string "by the sack.\p"
	.string "They wrap every bone like a broken\n"
	.string "leg before it leaves the ground.$"
