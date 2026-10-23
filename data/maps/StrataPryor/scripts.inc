@ Epilogue: the Pryor Mountains (optional). Red limestone foothills on the Montana-Wyoming
@ line, with a herd of feral horses: Equus came back with the Spanish, in the 1500s. North edge:
@ the Montana Prairie.
StrataPryor_MapScripts::
	.byte 0

StrataPryor_EventScript_Horse::
	lock
	faceplayer
	playmoncry SPECIES_EQUUS, CRY_MODE_NORMAL
	msgbox StrataPryor_Text_Horse, MSGBOX_DEFAULT
	waitmoncry
	release
	end

StrataPryor_EventScript_NoteLimestone::
	msgbox StrataPryor_Text_NoteLimestone, MSGBOX_SIGN
	end

StrataPryor_EventScript_NoteHorses::
	msgbox StrataPryor_Text_NoteHorses, MSGBOX_SIGN
	end

StrataPryor_EventScript_NotePronghorn::
	msgbox StrataPryor_Text_NotePronghorn, MSGBOX_SIGN
	end

StrataPryor_Text_Horse:
	.string "A feral horse studies you, ears\n"
	.string "forward, then goes back to\l"
	.string "grazing. Its ancestors were\l"
	.string "brought here by the Spanish.$"

StrataPryor_Text_NoteLimestone:
	.string "FIELD NOTE: Pryor Mountains.\p"
	.string "The grey and red rock here is\n"
	.string "mostly limestone laid down in a\l"
	.string "shallow sea, then lifted by\l"
	.string "mountain-building. Limestone\l"
	.string "dissolves, and the range is full\l"
	.string "of caves.\p"
	.string "Natural Trap Cave, where the Ice\n"
	.string "Age animals fell, is cut into the\l"
	.string "same kind of rock in the Bighorn\l"
	.string "Mountains to the south.$"

StrataPryor_Text_NoteHorses:
	.string "FIELD NOTE: Wild horses.\p"
	.string "Horses evolved in North America,\n"
	.string "spread to Asia, and died out here\l"
	.string "about 12,000 years ago. Spanish\l"
	.string "colonists brought them back in the\l"
	.string "1500s.\p"
	.string "The Pryor herd traces to Spanish\n"
	.string "colonial stock, and its range was\l"
	.string "set aside in 1968. Is Equus native\l"
	.string "here? The lineage is, the current\l"
	.string "herd is not. People still argue\l"
	.string "the point.$"

StrataPryor_Text_NotePronghorn:
	.string "FIELD NOTE: Pronghorn.\p"
	.string "The pronghorn is the fastest land\n"
	.string "animal in the Americas, far faster\l"
	.string "than any predator alive here now.\p"
	.string "One leading hypothesis: it evolved\n"
	.string "its speed running from predators\l"
	.string "that are gone, such as the\l"
	.string "American cheetah, Miracinonyx.\l"
	.string "Chasers and runners shape each\l"
	.string "other. It is a hypothesis, not a\l"
	.string "proof.$"
