@ Act 5: Bridger Forest, Wyoming, ~50-47 Ma (the Bridger Formation). Canopy primates and early
@ rodents. Field notes only; the forage and the tall grass do the work.
StrataBridgerForest_MapScripts::
	.byte 0

StrataBridgerForest_EventScript_NotePrimates::
	msgbox StrataBridgerForest_Text_NotePrimates, MSGBOX_SIGN
	end

StrataBridgerForest_EventScript_NoteFlora::
	msgbox StrataBridgerForest_Text_NoteFlora, MSGBOX_SIGN
	end

StrataBridgerForest_EventScript_NoteRodents::
	msgbox StrataBridgerForest_Text_NoteRodents, MSGBOX_SIGN
	end

StrataBridgerForest_Text_NotePrimates:
	.string "FIELD NOTE: CANOPY PRIMATES\p"
	.string "NOTHARCTUS was lemur-like: a big,\n"
	.string "leaf-eating climber. OMOMYS was\l"
	.string "tiny and big-eyed, more like a\l"
	.string "tarsier, and ate fruit and insects.\p"
	.string "Both are relatives of the first\n"
	.string "primates. Neither is known to be\l"
	.string "our direct ancestor.$"

StrataBridgerForest_Text_NoteFlora:
	.string "FIELD NOTE: THE FOREST\p"
	.string "Palms, ferns and legumes grew in\n"
	.string "this frost-free forest, and\l"
	.string "crocodiles lived in its streams.\p"
	.string "Eating plants steers a lineage\n"
	.string "toward plant-eating. Look for fruit\l"
	.string "and leaves among the trunks.$"

StrataBridgerForest_Text_NoteRodents:
	.string "FIELD NOTE: EARLY RODENTS\p"
	.string "PARAMYS was squirrel-like, with\n"
	.string "gnawing front teeth that never stop\l"
	.string "growing.\p"
	.string "The first rodents in North America\n"
	.string "turn up about 57 million years ago,\l"
	.string "just before the PETM. By now they\l"
	.string "are common in the forest.$"
