@ Hell Creek Camp (present day): the hub. The ranch road runs west to the Lindqvist
@ Ranch and Jordan; the badlands dig is south; the field station door is east.
@
@ Peer review (C13, src/strata_review.c): Theo Okafor's four reviews and two of the visiting
@ researchers (the ornithologist after act 1, the mammalogist after act 3) are here.
StrataFieldCamp_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, StrataFieldCamp_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, StrataFieldCamp_OnFrame
	.byte 0

@ The new game's arrival (docs/strata_outline.md, Act 0): the truck (data/maps/InsideOfTruck) lets
@ the player out in front of the station at story 0. Halvorsen calls from the door and the script
@ walks them in, so nobody wanders off before the starter is chosen (the station's intro script,
@ unchanged, is the next thing that happens).
StrataFieldCamp_OnFrame:
	map_script_2 VAR_STRATA_STORY, 0, StrataFieldCamp_EventScript_Arrival
	.2byte 0

StrataFieldCamp_EventScript_Arrival::
	lockall
	delay 20
	msgbox StrataFieldCamp_Text_Arrival, MSGBOX_DEFAULT
	applymovement OBJ_EVENT_ID_PLAYER, StrataFieldCamp_Movement_ToStation
	waitmovement 0
	@ By coordinates (just inside the door), not by warp id: a one-argument `warp` writes the dummy
	@ x = -1 and ScrCmd_warp then VarGets 0xFFFF, a read past gSpecialVars.
	warp MAP_STRATA_FIELD_STATION, 6, 11
	waitstate
	end

StrataFieldCamp_Movement_ToStation:
	walk_up
	walk_up
	step_end

StrataFieldCamp_Text_Arrival::
	.string "DR. HALVORSEN: {PLAYER}! Over here!\n"
	.string "Come in to the station.$"

StrataFieldCamp_OnTransition:
	special Strata_HideLockedReviewers
	@ Josie is at the ranch while a ranch interlude is due there (S1, src/strata_story.c).
	special Strata_StoryPrepareMap
	call_if_eq VAR_TEMP_4, SUBPLOT_AUCTION_DATE, StrataFieldCamp_EventScript_JosieAway
	call_if_eq VAR_TEMP_4, SUBPLOT_AUCTION_DAY, StrataFieldCamp_EventScript_JosieAway
	end

StrataFieldCamp_EventScript_JosieAway::
	setflag FLAG_TEMP_9
	return

@ Theo Okafor, PhD student and the rival. Peer review #0 once the starter is chosen (his animal
@ is the next starter in the cycle mammal -> bird -> turtle), then #1 after Corral Bluffs, #2
@ after White River and #3 (a double battle with Josie) after the Ice Age. He offers the
@ earliest review the player hasn't had yet, so none is missed.
StrataFieldCamp_EventScript_Theo::
	lock
	faceplayer
	goto_if_lt VAR_STRATA_STORY, 1, StrataFieldCamp_EventScript_TheoNoStarter
	goto_if_eq VAR_STARTER_MON, 0, StrataFieldCamp_EventScript_TheoAct0Bird
	goto_if_eq VAR_STARTER_MON, 1, StrataFieldCamp_EventScript_TheoAct0Turtle
	goto StrataFieldCamp_EventScript_TheoAct0Mammal

StrataFieldCamp_EventScript_TheoNoStarter::
	msgbox StrataFieldCamp_Text_TheoAct0, MSGBOX_DEFAULT
	release
	end

StrataFieldCamp_EventScript_TheoAct0Bird::
	goto_if_defeated TRAINER_STRATA_THEO_ACT0_BIRD, StrataFieldCamp_EventScript_TheoAct3
	trainerbattle_single TRAINER_STRATA_THEO_ACT0_BIRD, StrataFieldCamp_Text_Theo0Intro, StrataFieldCamp_Text_Theo0Defeat, StrataFieldCamp_EventScript_TheoWon0

StrataFieldCamp_EventScript_TheoAct0Turtle::
	goto_if_defeated TRAINER_STRATA_THEO_ACT0_TURTLE, StrataFieldCamp_EventScript_TheoAct3
	trainerbattle_single TRAINER_STRATA_THEO_ACT0_TURTLE, StrataFieldCamp_Text_Theo0Intro, StrataFieldCamp_Text_Theo0Defeat, StrataFieldCamp_EventScript_TheoWon0

StrataFieldCamp_EventScript_TheoAct0Mammal::
	goto_if_defeated TRAINER_STRATA_THEO_ACT0_MAMMAL, StrataFieldCamp_EventScript_TheoAct3
	trainerbattle_single TRAINER_STRATA_THEO_ACT0_MAMMAL, StrataFieldCamp_Text_Theo0Intro, StrataFieldCamp_Text_Theo0Defeat, StrataFieldCamp_EventScript_TheoWon0

StrataFieldCamp_EventScript_TheoWon0::
	msgbox StrataFieldCamp_Text_Theo0After, MSGBOX_DEFAULT
	releaseall
	end

StrataFieldCamp_EventScript_TheoAct3::
	goto_if_lt VAR_STRATA_STORY, STORY_ACT_DONE(ERA_CORRAL_BLUFFS), StrataFieldCamp_EventScript_TheoIdle0
	goto_if_defeated TRAINER_STRATA_THEO_ACT3, StrataFieldCamp_EventScript_TheoAct6
	trainerbattle_single TRAINER_STRATA_THEO_ACT3, StrataFieldCamp_Text_Theo3Intro, StrataFieldCamp_Text_Theo3Defeat, StrataFieldCamp_EventScript_TheoWon3

StrataFieldCamp_EventScript_TheoWon3::
	msgbox StrataFieldCamp_Text_Theo3After, MSGBOX_DEFAULT
	releaseall
	end

StrataFieldCamp_EventScript_TheoAct6::
	goto_if_lt VAR_STRATA_STORY, STORY_ACT_DONE(ERA_WHITE_RIVER), StrataFieldCamp_EventScript_TheoIdle3
	goto_if_defeated TRAINER_STRATA_THEO_ACT6, StrataFieldCamp_EventScript_TheoAct8
	trainerbattle_single TRAINER_STRATA_THEO_ACT6, StrataFieldCamp_Text_Theo6Intro, StrataFieldCamp_Text_Theo6Defeat, StrataFieldCamp_EventScript_TheoWon6

StrataFieldCamp_EventScript_TheoWon6::
	msgbox StrataFieldCamp_Text_Theo6After, MSGBOX_DEFAULT
	releaseall
	end

@ Review #3 is a double battle: Josie lends Theo a second pair, so the player needs two animals.
StrataFieldCamp_EventScript_TheoAct8::
	goto_if_lt VAR_STRATA_STORY, STORY_ACT_DONE(ERA_TRAP_CAVE), StrataFieldCamp_EventScript_TheoIdle6
	goto_if_defeated TRAINER_STRATA_THEO_ACT8, StrataFieldCamp_EventScript_TheoIdle8
	trainerbattle_double TRAINER_STRATA_THEO_ACT8, StrataFieldCamp_Text_Theo8Intro, StrataFieldCamp_Text_Theo8Defeat, StrataFieldCamp_Text_Theo8NeedTwo, StrataFieldCamp_EventScript_TheoWon8

StrataFieldCamp_EventScript_TheoWon8::
	msgbox StrataFieldCamp_Text_Theo8After, MSGBOX_DEFAULT
	releaseall
	end

StrataFieldCamp_EventScript_TheoIdle0::
	msgbox StrataFieldCamp_Text_TheoLater, MSGBOX_DEFAULT
	release
	end

StrataFieldCamp_EventScript_TheoIdle3::
	@ After Kessler's funding offer (S1) he still has the card.
	goto_if_ge VAR_STRATA_SUBPLOT, SUBPLOT_HALVORSEN_REFUSAL, StrataFieldCamp_EventScript_TheoCard
	msgbox StrataFieldCamp_Text_TheoIdle3, MSGBOX_DEFAULT
	release
	end

StrataFieldCamp_EventScript_TheoCard::
	msgbox StrataFieldCamp_Text_TheoCard, MSGBOX_DEFAULT
	release
	end

StrataFieldCamp_Text_TheoCard::
	.string "THEO: Kessler's card is still in my\n"
	.string "wallet. I haven't called.\p"
	.string "If the rig is sold, my thesis goes\n"
	.string "with it. I'd like a better reason\l"
	.string "than that to say no.$"

StrataFieldCamp_EventScript_TheoIdle6::
	msgbox StrataFieldCamp_Text_TheoIdle6, MSGBOX_DEFAULT
	release
	end

StrataFieldCamp_EventScript_TheoIdle8::
	msgbox StrataFieldCamp_Text_TheoIdle8, MSGBOX_DEFAULT
	release
	end

@ The ornithologist (act 1) and the mammalogist (act 3): visiting researchers, one battle each.
StrataFieldCamp_EventScript_Arlo::
	lock
	faceplayer
	trainerbattle_single TRAINER_STRATA_REVIEW_ACT1, StrataFieldCamp_Text_ArloIntro, StrataFieldCamp_Text_ArloDefeat, StrataFieldCamp_EventScript_ArloWon
	msgbox StrataFieldCamp_Text_ArloAfter, MSGBOX_DEFAULT
	release
	end

StrataFieldCamp_EventScript_ArloWon::
	msgbox StrataFieldCamp_Text_ArloNote, MSGBOX_DEFAULT
	releaseall
	end

StrataFieldCamp_EventScript_Tomas::
	lock
	faceplayer
	trainerbattle_single TRAINER_STRATA_REVIEW_ACT3, StrataFieldCamp_Text_TomasIntro, StrataFieldCamp_Text_TomasDefeat, StrataFieldCamp_EventScript_TomasWon
	msgbox StrataFieldCamp_Text_TomasAfter, MSGBOX_DEFAULT
	release
	end

StrataFieldCamp_EventScript_TomasWon::
	msgbox StrataFieldCamp_Text_TomasNote, MSGBOX_DEFAULT
	releaseall
	end

@ Josie Lindqvist: undergrad on the crew, and Bea's granddaughter.
StrataFieldCamp_EventScript_Student::
	lock
	faceplayer
	@ The subplot (S1): what Josie is worried about after each interlude.
	goto_if_ge VAR_STRATA_SUBPLOT, SUBPLOT_AUCTION_DAY, StrataFieldCamp_EventScript_JosieMuseum
	goto_if_ge VAR_STRATA_SUBPLOT, SUBPLOT_AUCTION_DATE, StrataFieldCamp_EventScript_JosieAuction
	goto_if_ge VAR_STRATA_SUBPLOT, SUBPLOT_JOSIE_PIT, StrataFieldCamp_EventScript_JosiePit
	msgbox StrataFieldCamp_Text_Student, MSGBOX_DEFAULT
	goto_if_set FLAG_STRATA_SAW_PAIR, StrataFieldCamp_EventScript_JosieSawPair
	msgbox StrataFieldCamp_Text_JosieRanch, MSGBOX_DEFAULT
	release
	end

StrataFieldCamp_EventScript_JosieSawPair::
	msgbox StrataFieldCamp_Text_JosieSawPair, MSGBOX_DEFAULT
	release
	end

StrataFieldCamp_EventScript_JosiePit::
	goto_if_ge VAR_STRATA_SUBPLOT, SUBPLOT_PIT_DOCUMENTED, StrataFieldCamp_EventScript_JosieDocumented
	msgbox StrataFieldCamp_Text_JosiePit, MSGBOX_DEFAULT
	release
	end

StrataFieldCamp_EventScript_JosieDocumented::
	msgbox StrataFieldCamp_Text_JosieDocumented, MSGBOX_DEFAULT
	release
	end

StrataFieldCamp_EventScript_JosieAuction::
	msgbox StrataFieldCamp_Text_JosieAuction, MSGBOX_DEFAULT
	release
	end

StrataFieldCamp_EventScript_JosieMuseum::
	msgbox StrataFieldCamp_Text_JosieMuseum, MSGBOX_DEFAULT
	release
	end

StrataFieldCamp_Text_JosiePit::
	.string "JOSIE: I keep thinking about that\n"
	.string "pit. Somebody stood there with a\l"
	.string "shovel and decided the layer\l"
	.string "didn't matter.\p"
	.string "Dale says a bone without its layer\n"
	.string "is just a rock. Now I get it.$"

StrataFieldCamp_Text_JosieDocumented::
	.string "JOSIE: ORTIZ says your notes are\n"
	.string "good enough for a case file.\p"
	.string "Photos, GPS, the layer. That's all\n"
	.string "it takes? Huh. I'm keeping a\l"
	.string "notebook from now on.$"

StrataFieldCamp_Text_JosieAuction::
	.string "JOSIE: Gran set an auction date.\n"
	.string "Sealed bids. Kessler's running it.\p"
	.string "I yelled at her. She didn't yell\n"
	.string "back. That was worse.\p"
	.string "The ranch is going to be mine one\n"
	.string "day. And this choice with it.$"

StrataFieldCamp_Text_JosieMuseum::
	.string "JOSIE: The Pair's going to a museum,\n"
	.string "and Gran still got paid!\p"
	.string "One day it's my land, and my turn\n"
	.string "to choose. I know what I'll pick.$"

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

StrataFieldCamp_Text_Theo0Intro:
	.string "THEO: You got the rig running?\n"
	.string "Good. Then test it.\p"
	.string "A reconstruction is a hypothesis.\n"
	.string "It has to hold up against another\l"
	.string "one.\p"
	.string "Mine is the next animal in the\n"
	.string "cycle: mammal, bird, turtle. Same\l"
	.string "age and size as yours.\p"
	.string "Peer review. Show me yours.$"

StrataFieldCamp_Text_Theo0Defeat:
	.string "THEO: Hm. Fine, you won this one.\p"
	.string "One round isn't evidence.$"

StrataFieldCamp_Text_Theo0After:
	.string "THEO: Don't get comfortable.\p"
	.string "Run the rig, and write down\n"
	.string "everything it gets wrong. I'll be\l"
	.string "reading your notes.$"

StrataFieldCamp_Text_Theo3Intro:
	.string "THEO: I read the Corral Bluffs data\n"
	.string "again. Palms, then legumes, then\l"
	.string "bigger plant eaters, then the first\l"
	.string "big predator.\p"
	.string "The rig got the order right. That\n"
	.string "could still be luck.\p"
	.string "So: my reconstruction against\n"
	.string "yours. If yours is better, show me\l"
	.string "why.$"

StrataFieldCamp_Text_Theo3Defeat:
	.string "THEO: …It held.\p"
	.string "The order of recovery looks right.\n"
	.string "But 'looks right' isn't a\l"
	.string "mechanism.$"

StrataFieldCamp_Text_Theo3After:
	.string "THEO: Peer review isn't about\n"
	.string "winning. It's about finding the\l"
	.string "weak point.\p"
	.string "Keep going up. I'll keep looking\n"
	.string "for it.$"

StrataFieldCamp_Text_TheoIdle3:
	.string "THEO: The recovery after the\n"
	.string "impact is the part I trust most.\p"
	.string "Everything after that is a longer\n"
	.string "chain of guesses. Check each link.$"

StrataFieldCamp_Text_Theo6Intro:
	.string "THEO: The Eocene-Oligocene\n"
	.string "boundary. I compared your run to\l"
	.string "the cliff contact, species by\l"
	.string "species.\p"
	.string "The losses match. That actually\n"
	.string "worries me: if it's a toy, it\l"
	.string "shouldn't be this good.\p"
	.string "So I'm not here to beat you. I'm\n"
	.string "here to break it. Ready?$"

StrataFieldCamp_Text_Theo6Defeat:
	.string "THEO: It held again.\p"
	.string "Not a diorama, then. A model.\n"
	.string "It's wrong somewhere. I just\l"
	.string "haven't found where.$"

StrataFieldCamp_Text_Theo6After:
	.string "THEO: A model is useful when you\n"
	.string "know how it's wrong.\p"
	.string "Don't tell Halvorsen I said that.\n"
	.string "They'll want it in writing.$"

StrataFieldCamp_Text_TheoIdle6:
	.string "THEO: Grasslands and ash next,\n"
	.string "then the Ice Age. Fewer species,\l"
	.string "bigger animals. Fewer records to\l"
	.string "check, too.$"

StrataFieldCamp_Text_Theo8Intro:
	.string "JOSIE: Theo! You promised me a\n"
	.string "turn. Two reviewers, one\l"
	.string "reconstruction.\p"
	.string "THEO: Josie's lent me her pair.\n"
	.string "Two on two. We'll find every hole\l"
	.string "in the last layer.\p"
	.string "JOSIE: I get to be nice. He\n"
	.string "doesn't.$"

StrataFieldCamp_Text_Theo8Defeat:
	.string "THEO: The model is wrong.\p"
	.string "It's wrong in ways we can name,\n"
	.string "and it's useful anyway. Write that\l"
	.string "down.\p"
	.string "JOSIE: …I'm writing it down.$"

StrataFieldCamp_Text_Theo8NeedTwo:
	.string "THEO: Two on two. You need a second\n"
	.string "animal that can still fight.$"

StrataFieldCamp_Text_Theo8After:
	.string "THEO: My thesis proposal says it:\n"
	.string "the model is wrong, but it's\l"
	.string "useful.\p"
	.string "The committee didn't make me cut\n"
	.string "it. Thanks for the review.$"

StrataFieldCamp_Text_TheoIdle8:
	.string "THEO: Still asking how we know?\n"
	.string "Good. Don't stop.\p"
	.string "Go and see the prairie. That's\n"
	.string "the one layer we can actually\l"
	.string "check.$"

StrataFieldCamp_Text_ArloIntro:
	.string "ARLO: Ornithologist, visiting from\n"
	.string "the university. I came for the\l"
	.string "birds in your Hell Creek run.\p"
	.string "Most birds back then had teeth and\n"
	.string "clawed wings. Your rig rebuilt\l"
	.string "them from a few hollow bones.\p"
	.string "Peer review, then: my notes\n"
	.string "against your animals.$"

StrataFieldCamp_Text_ArloDefeat:
	.string "ARLO: Good. Your reconstruction held\n"
	.string "up where my sketches are guesses.$"

StrataFieldCamp_Text_ArloNote:
	.string "ARLO: Here's my field note.\p"
	.string "The birds that came through the\n"
	.string "impact had toothless beaks, and\l"
	.string "many fed on the ground, on seeds.\p"
	.string "Forest birds went down with the\n"
	.string "forests. Probably. We argue about\l"
	.string "that a lot.$"

StrataFieldCamp_Text_ArloAfter:
	.string "ARLO: Seeds on the ground, no\n"
	.string "teeth. That's my best guess for why\l"
	.string "any of them made it.\p"
	.string "Write down the 'best guess' part.$"

StrataFieldCamp_Text_TomasIntro:
	.string "TOMAS: Mammalogist. Corral Bluffs\n"
	.string "is my favourite site: palms, then\l"
	.string "legumes, then big plant eaters,\l"
	.string "then the first big predator.\p"
	.string "Every step shows up in the rock.\n"
	.string "Let's see what your rig did with\l"
	.string "them. Peer review.$"

StrataFieldCamp_Text_TomasDefeat:
	.string "TOMAS: Not bad. Small mammals\n"
	.string "filling empty niches. You played it\l"
	.string "the way the rock says.$"

StrataFieldCamp_Text_TomasNote:
	.string "TOMAS: Field note.\p"
	.string "After the extinction, mammals got\n"
	.string "much bigger within a million\l"
	.string "years.\p"
	.string "Not because they were better. The\n"
	.string "big dinosaurs were gone, and empty\l"
	.string "niches fill fast.$"

StrataFieldCamp_Text_TomasAfter:
	.string "TOMAS: Size isn't destiny. It's\n"
	.string "whatever the empty niche allows.$"

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
	.string "One visitor comes for each layer\n"
	.string "the rig finishes. They want a peer\l"
	.string "review: your animals against their\l"
	.string "notes. The grant pays for it.$"

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
