@ Act 5: Fossil Lake, Wyoming, ~52 Ma (the Fossil Butte Member of the Green River Formation).
@ The lagerstaette: whole fish, the oldest bats, birds. Walking onto the east shore for the first
@ time plays the mass-mortality scene (VAR_STRATA_ACT5 0 -> 1). No battle; it is a labelled
@ hypothesis, and the scene says so.
StrataFossilLake_MapScripts::
	.byte 0

StrataFossilLake_EventScript_Turnover::
	lockall
	setvar VAR_STRATA_ACT5, 1
	msgbox StrataFossilLake_Text_TurnoverSchool, MSGBOX_DEFAULT
	fadescreen FADE_TO_BLACK
	playse SE_M_BUBBLE
	delay 40
	fadescreen FADE_FROM_BLACK
	msgbox StrataFossilLake_Text_TurnoverStill, MSGBOX_DEFAULT
	msgbox StrataFossilLake_Text_TurnoverHypothesis, MSGBOX_DEFAULT
	releaseall
	end

StrataFossilLake_Text_TurnoverSchool:
	.string "A school of KNIGHTIA flickers just\n"
	.string "under the surface, thousands of\l"
	.string "silver fish moving as one.$"

StrataFossilLake_Text_TurnoverStill:
	.string "...Then the water goes still.\p"
	.string "The fish roll over and sink, a\n"
	.string "whole school at once, into the\l"
	.string "quiet mud on the bottom.$"

StrataFossilLake_Text_TurnoverHypothesis:
	.string "RIG: This is a reconstruction of one\n"
	.string "hypothesis, not a record.\p"
	.string "Many layers here hold thousands of\n"
	.string "fish, side by side. Cold or\l"
	.string "oxygen-poor water welling up from\l"
	.string "below (a lake turnover) is one\l"
	.string "explanation. Toxic algae, or ash\l"
	.string "from far-off volcanoes, are others.\p"
	.string "Debated. The mud kept them whole.$"

@ ---- field notes -----------------------------------------------------------------

StrataFossilLake_EventScript_NoteFish::
	msgbox StrataFossilLake_Text_NoteFish, MSGBOX_SIGN
	end

StrataFossilLake_EventScript_NoteBats::
	msgbox StrataFossilLake_Text_NoteBats, MSGBOX_SIGN
	end

StrataFossilLake_EventScript_NoteBirds::
	msgbox StrataFossilLake_Text_NoteBirds, MSGBOX_SIGN
	end

StrataFossilLake_Text_NoteFish:
	.string "FIELD NOTE: FOSSIL LAKE\p"
	.string "Whole schools of KNIGHTIA, a small\n"
	.string "herring relative, lie in single\l"
	.string "layers with fins and scales intact.\p"
	.string "Fish died by the thousand, again\n"
	.string "and again. Why is still debated.\p"
	.string "Stingrays and gars are here too.$"

StrataFossilLake_Text_NoteBats:
	.string "FIELD NOTE: ONYCHONYCTERIS\p"
	.string "One of the oldest bats known,\n"
	.string "about 52 million years old. It flew,\l"
	.string "but still had claws on all five\l"
	.string "fingers.\p"
	.string "Its ear bones suggest it probably\n"
	.string "could not echolocate. Debated.$"

StrataFossilLake_Text_NoteBirds:
	.string "FIELD NOTE: SHORE BIRDS\p"
	.string "PRESBYORNIS was a long-legged,\n"
	.string "flamingo-like wader, an early\l"
	.string "relative of ducks and geese. Its\l"
	.string "bones are common in lake shore\l"
	.string "beds.\p"
	.string "GALLINULOIDES, a small ground bird,\n"
	.string "is an early relative of fowl.$"
