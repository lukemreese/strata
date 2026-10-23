@ Epilogue: the Interpretive Center, ground floor. The Pair (the Triceratops and Tyrannosaurus the
@ summer crew found) in the round case, paleoart murals of the layers the player climbed, and the
@ cast: Halvorsen, Josie, Bea, Dale and Theo. The stairs lead up to the Hall of Lost Lineages.
@
@ C13 (peer-review trainers): Halvorsen's final peer review (Lv 55: Tyrannosaur, Uintatherium,
@ Epicyon, Arctodus, Teleoceras, Chelydra) goes in StrataInterpretive1F_EventScript_Halvorsen, then
@ setflag FLAG_STRATA_EPI_PEER_REVIEW_DONE. S3 (ending text, credits) can hook the same script.
@ Light story hooks only: the present-day wrap-up (Kessler, the museum specimen) is S1/S3.
StrataInterpretive1F_MapScripts::
	.byte 0

StrataInterpretive1F_EventScript_Halvorsen::
	lock
	faceplayer
	goto_if_set FLAG_STRATA_EPI_PEER_REVIEW_DONE, StrataInterpretive1F_EventScript_HalvorsenAfter
	msgbox StrataInterpretive1F_Text_HalvorsenIntro, MSGBOX_DEFAULT
	@ C13: the final peer review goes here (trainerbattle against Halvorsen, Lv 55),
	@ then: setflag FLAG_STRATA_EPI_PEER_REVIEW_DONE, goto StrataInterpretive1F_EventScript_HalvorsenAfter
	release
	end

StrataInterpretive1F_EventScript_HalvorsenAfter::
	msgbox StrataInterpretive1F_Text_HalvorsenAfter, MSGBOX_DEFAULT
	release
	end

StrataInterpretive1F_EventScript_Josie::
	msgbox StrataInterpretive1F_Text_Josie, MSGBOX_NPC
	end

StrataInterpretive1F_EventScript_Bea::
	msgbox StrataInterpretive1F_Text_Bea, MSGBOX_NPC
	end

StrataInterpretive1F_EventScript_Dale::
	msgbox StrataInterpretive1F_Text_Dale, MSGBOX_NPC
	end

StrataInterpretive1F_EventScript_Theo::
	msgbox StrataInterpretive1F_Text_Theo, MSGBOX_NPC
	end

StrataInterpretive1F_EventScript_Pair::
	setflag FLAG_STRATA_EPI_PAIR_SEEN
	msgbox StrataInterpretive1F_Text_Pair, MSGBOX_SIGN
	end

StrataInterpretive1F_EventScript_PairLabel::
	setflag FLAG_STRATA_EPI_PAIR_SEEN
	msgbox StrataInterpretive1F_Text_PairLabel, MSGBOX_SIGN
	end

StrataInterpretive1F_EventScript_Cast::
	msgbox StrataInterpretive1F_Text_Cast, MSGBOX_SIGN
	end

StrataInterpretive1F_EventScript_RigModel::
	msgbox StrataInterpretive1F_Text_RigModel, MSGBOX_SIGN
	end

StrataInterpretive1F_EventScript_MuralHellCreek::
	msgbox StrataInterpretive1F_Text_MuralHellCreek, MSGBOX_SIGN
	end

StrataInterpretive1F_EventScript_MuralCorral::
	msgbox StrataInterpretive1F_Text_MuralCorral, MSGBOX_SIGN
	end

StrataInterpretive1F_EventScript_MuralPetm::
	msgbox StrataInterpretive1F_Text_MuralPetm, MSGBOX_SIGN
	end

StrataInterpretive1F_EventScript_MuralGreenRiver::
	msgbox StrataInterpretive1F_Text_MuralGreenRiver, MSGBOX_SIGN
	end

StrataInterpretive1F_EventScript_MuralWhiteRiver::
	msgbox StrataInterpretive1F_Text_MuralWhiteRiver, MSGBOX_SIGN
	end

StrataInterpretive1F_EventScript_MuralAshfall::
	msgbox StrataInterpretive1F_Text_MuralAshfall, MSGBOX_SIGN
	end

StrataInterpretive1F_EventScript_MuralIceAge::
	msgbox StrataInterpretive1F_Text_MuralIceAge, MSGBOX_SIGN
	end

StrataInterpretive1F_Text_HalvorsenIntro:
	.string "There you are, {PLAYER}. Look at\n"
	.string "it: the Pair, in a public case,\l"
	.string "with its layer, its map and its\l"
	.string "notes.\p"
	.string "Every extinction you saw was\n"
	.string "written in the rock before you got\l"
	.string "there. The one happening now isn't\l"
	.string "written yet.\p"
	.string "One last peer review, if you're\n"
	.string "willing. Two people put their\l"
	.string "reconstructions side by side. Mine\l"
	.string "are the classics. Yours are the\l"
	.string "survivors.$"

StrataInterpretive1F_Text_HalvorsenAfter:
	.string "Two reconstructions, side by side,\n"
	.string "and neither one is the truth. Both\l"
	.string "are useful. That's the job.\p"
	.string "Thank you for the season, {PLAYER}.\n"
	.string "Go and look at the prairie again.\l"
	.string "Everything out there is a lineage\l"
	.string "that made it this far.$"

StrataInterpretive1F_Text_Josie:
	.string "I switched my major to\n"
	.string "paleontology. Grandma says the\l"
	.string "ranch keeps the quarry road, and\l"
	.string "the museum keeps the Pair.\p"
	.string "They let me write some of the\n"
	.string "labels. It turns out I like saying\l"
	.string "exactly how sure we are.$"

StrataInterpretive1F_Text_Bea:
	.string "The dealer's offer was bigger. The\n"
	.string "consortium's was enough, and the\l"
	.string "Pair stays where anyone can see\l"
	.string "it.\p"
	.string "I never thought I'd drive forty\n"
	.string "miles to look at a rock in a case.\l"
	.string "Look at that. It's ours, and it's\l"
	.string "everyone's.$"

StrataInterpretive1F_Text_Dale:
	.string "See the label? Layer, map, notes.\n"
	.string "That's the whole lesson, if you\l"
	.string "boil down the season.\p"
	.string "A bone without its layer is just a\n"
	.string "rock. A bone with its layer is the\l"
	.string "whole day it died.$"

StrataInterpretive1F_Text_Theo:
	.string "I put it in my thesis proposal:\n"
	.string "the model is wrong, but it's\l"
	.string "useful.\p"
	.string "I still ask how we know that,\n"
	.string "every time. Don't let anyone talk\l"
	.string "you out of that question.$"

StrataInterpretive1F_Text_Pair:
	.string "THE PAIR\p"
	.string "A Triceratops and a Tyrannosaurus,\n"
	.string "found together in the Hell Creek\l"
	.string "Formation. They were buried close,\l"
	.string "but the bones can't say whether\l"
	.string "they fought or were washed\l"
	.string "together by one flood.\p"
	.string "The sediment around them can help,\n"
	.string "which is why it was kept.$"

StrataInterpretive1F_Text_PairLabel:
	.string "LOCALITY: Garfield County,\n"
	.string "Montana. Exact site withheld to\l"
	.string "protect the quarry.\p"
	.string "LAYER: Hell Creek Formation, about\n"
	.string "66 million years old.\p"
	.string "FOUND BY: the summer field crew.\n"
	.string "Maps, photographs and field notes\l"
	.string "are archived with the specimen. On\l"
	.string "public display, thanks to the\l"
	.string "Lindqvist family and the museum\l"
	.string "consortium.$"

StrataInterpretive1F_Text_Cast:
	.string "A plaster cast of an Edmontosaurus\n"
	.string "tooth battery. Please touch.\p"
	.string "Hundreds of teeth, packed in rows\n"
	.string "and replaced throughout life: good\l"
	.string "for grinding tough plants.$"

StrataInterpretive1F_Text_RigModel:
	.string "A scale model of the STRATA rig,\n"
	.string "on loan from the field station.\p"
	.string "The card says: a model you can\n"
	.string "walk around in, not a time\l"
	.string "machine. Every rule in it is a\l"
	.string "statement about evidence, and the\l"
	.string "unknowns are labelled as guesses.$"

StrataInterpretive1F_Text_MuralHellCreek:
	.string "MURAL: Hell Creek, 66 million\n"
	.string "years ago.\p"
	.string "A tyrannosaur on a river bluff, a\n"
	.string "Triceratops in the shallows, small\l"
	.string "mammals in the ferns.\p"
	.string "The rock keeps shape far more\n"
	.string "often than colour, so the colours\l"
	.string "are the artist's guess.$"

StrataInterpretive1F_Text_MuralCorral:
	.string "MURAL: Corral Bluffs, about 65.4\n"
	.string "million years ago.\p"
	.string "Palm woods after the impact, and\n"
	.string "the first legumes. Within about a\l"
	.string "million years, forests regrew and\l"
	.string "mammals grew bigger (Lyson et al.,\l"
	.string "2019).$"

StrataInterpretive1F_Text_MuralPetm:
	.string "MURAL: Wyoming at the PETM, about\n"
	.string "56 million years ago.\p"
	.string "A hothouse world: small early\n"
	.string "horses and primates among swamp\l"
	.string "forests. Carbon was released over\l"
	.string "thousands of years, and ours is\l"
	.string "being released many times faster.\l"
	.string "Estimates differ, but not by\l"
	.string "enough to make it comfortable.$"

StrataInterpretive1F_Text_MuralGreenRiver:
	.string "MURAL: Green River, about 50\n"
	.string "million years ago.\p"
	.string "A subtropical lake with palms on\n"
	.string "the shore, schools of fish, and\l"
	.string "bats overhead. The lake mud kept\l"
	.string "every scale and feather, so this\l"
	.string "is the best-preserved layer in the\l"
	.string "Hall.$"

StrataInterpretive1F_Text_MuralWhiteRiver:
	.string "MURAL: White River badlands, about\n"
	.string "33 million years ago.\p"
	.string "After the Eocene-Oligocene\n"
	.string "cooling: open woodland,\l"
	.string "hyaenodonts and pig-like\l"
	.string "archaeotheres, rabbits and\l"
	.string "burrowers. The warm-world forests\l"
	.string "had thinned and the archaic\l"
	.string "mammals had gone.$"

StrataInterpretive1F_Text_MuralAshfall:
	.string "MURAL: Ashfall, about 11.9 million\n"
	.string "years ago.\p"
	.string "A Nebraska waterhole under falling\n"
	.string "ash from a supereruption in Idaho,\l"
	.string "1,600 km away. Animals died over\l"
	.string "weeks, not minutes: small ones\l"
	.string "first, rhinos last.$"

StrataInterpretive1F_Text_MuralIceAge:
	.string "MURAL: the Ice Age steppe, about\n"
	.string "20,000 years ago.\p"
	.string "Mammoth, lion, short-faced bear\n"
	.string "and horses. Within about 10,000\l"
	.string "years most of the giants were\l"
	.string "gone. The climate shifted and\l"
	.string "people arrived. Scientists still\l"
	.string "argue how much each mattered.$"
