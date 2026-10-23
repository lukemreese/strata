@ Epilogue: the Hall of Lost Lineages. Placeholder until F4 (fossil flags): one plaque per
@ extinction filter of src/data/lineages.h (sExtinctions_*), listing every lineage the rig drops
@ at that filter, oldest first, and the two statues at the door (the end-Pleistocene filter, and
@ the case that is not written yet).
@
@ F4/S3 follow-up: when FLAG_STRATA_FOSSIL_<species> exist, each case plaque should list only
@ (or highlight) the lineages the player carried and lost, with "carried from Act N". Plaques are
@ per filter on purpose, so a per-species flag check slots into each case script.
StrataInterpretive2F_MapScripts::
	.byte 0

StrataInterpretive2F_EventScript_Docent::
	lock
	faceplayer
	setflag FLAG_STRATA_EPI_HALL_SEEN
	msgbox StrataInterpretive2F_Text_Docent, MSGBOX_DEFAULT
	release
	end

StrataInterpretive2F_EventScript_Student::
	msgbox StrataInterpretive2F_Text_Student, MSGBOX_NPC
	end

StrataInterpretive2F_EventScript_CaseKPg::
	msgbox StrataInterpretive2F_Text_CaseKPg, MSGBOX_SIGN
	end

StrataInterpretive2F_EventScript_CasePaleocene::
	msgbox StrataInterpretive2F_Text_CasePaleocene, MSGBOX_SIGN
	end

StrataInterpretive2F_EventScript_CaseEocene::
	msgbox StrataInterpretive2F_Text_CaseEocene, MSGBOX_SIGN
	end

StrataInterpretive2F_EventScript_CaseMiocene::
	msgbox StrataInterpretive2F_Text_CaseMiocene, MSGBOX_SIGN
	end

StrataInterpretive2F_EventScript_CaseIceAge::
	msgbox StrataInterpretive2F_Text_CaseIceAge, MSGBOX_SIGN
	end

StrataInterpretive2F_EventScript_StatueLast::
	msgbox StrataInterpretive2F_Text_StatueLast, MSGBOX_SIGN
	end

StrataInterpretive2F_EventScript_StatueNow::
	msgbox StrataInterpretive2F_Text_StatueNow, MSGBOX_SIGN
	end

StrataInterpretive2F_Text_Docent:
	.string "Welcome to the Hall of Lost\n"
	.string "Lineages. Each case is one filter\l"
	.string "in the record: who was there\l"
	.string "before it, and who was gone after.\p"
	.string "Some of these were in your party\n"
	.string "once. The rig can carry a lineage\l"
	.string "only as far as the record lets it\l"
	.string "go.$"

StrataInterpretive2F_Text_Student:
	.string "The cases list who died out, not\n"
	.string "who deserved to. Size, diet,\l"
	.string "habitat and luck. That's what the\l"
	.string "rock says.\p"
	.string "I keep wanting to put a case here\n"
	.string "for the animals on the prairie.\l"
	.string "The curator says not yet.$"

StrataInterpretive2F_Text_CaseKPg:
	.string "THE END OF THE CRETACEOUS, 66\n"
	.string "million years ago.\p"
	.string "Gone above the boundary clay:\n"
	.string "TYRANNOSAURUS, TRICERATOPS,\l"
	.string "EDMONTOSAURUS, ANKYLOSAURUS,\l"
	.string "PACHYCEPHALOSAURUS,\l"
	.string "THESCELOSAURUS, ACHERORAPTOR,\l"
	.string "ANZU, DIDELPHODON and AVISAURUS.\p"
	.string "Every dinosaur that was not a\n"
	.string "bird, and the tree-perching birds.\l"
	.string "The survivors were small, or\l"
	.string "burrowed, or lived in water, or\l"
	.string "ate detritus.$"

StrataInterpretive2F_Text_CasePaleocene:
	.string "THE PALEOCENE RECOVERY, gone by\n"
	.string "about 56 million years ago.\p"
	.string "PURGATORIUS, LOXOLOPHUS,\n"
	.string "CARSIOPTYCHUS, TAENIOLABIS and\l"
	.string "EOCONODON.\p"
	.string "The first mammals to fill the\n"
	.string "emptied world were replaced by\l"
	.string "newcomers from other continents.\l"
	.string "Last appearances are approximate.$"

StrataInterpretive2F_Text_CaseEocene:
	.string "THE END OF THE WARM WORLD, about\n"
	.string "34 million years ago.\p"
	.string "OMOMYS, OXYAENA, PATRIOFELIS,\n"
	.string "GASTORNIS, PRESBYORNIS,\l"
	.string "CHAMPSOSAURS, BOREALOSUCHUS,\l"
	.string "MESODMA, HYOPSODUS, DIACODEXIS,\l"
	.string "CORYPHODON, ONYCHONYCTERIS,\l"
	.string "HELIOBATIS, KNIGHTIA, NOTHARCTUS\l"
	.string "and UINTATHERIUM.\p"
	.string "The Eocene-Oligocene cooling\n"
	.string "thinned the forests. Some of these\l"
	.string "were gone earlier; the case shows\l"
	.string "where the rig drops them.$"

StrataInterpretive2F_Text_CaseMiocene:
	.string "THE GRASSLAND TURNOVER, gone by\n"
	.string "about 12 million years ago.\p"
	.string "HYAENODON, PALAEOLAGUS,\n"
	.string "ARCHAEOTHERIUM, HOPLOPHONEUS,\l"
	.string "MERYCOIDODON, LEPTOMERYX, STYLEMYS\l"
	.string "and ISCHYROMYS.\p"
	.string "Cooler, drier grassland favoured\n"
	.string "runners and grazers. Rabbits,\l"
	.string "rodents and tortoises still live\l"
	.string "on through relatives.$"

StrataInterpretive2F_Text_CaseIceAge:
	.string "GONE BY THE ICE AGE, between 5 and\n"
	.string "2 million years ago.\p"
	.string "APHELOPS, TELEOCERAS, HYPOHIPPUS,\n"
	.string "CORMOHIPPARION, EPICYON, BALEARICA\l"
	.string "and ANCHIGYPS.\p"
	.string "North America's rhinos vanished\n"
	.string "about 5 million years ago, and the\l"
	.string "bone-crushing dogs by about 2\l"
	.string "million. Horses and cranes live on\l"
	.string "elsewhere.$"

StrataInterpretive2F_Text_StatueLast:
	.string "THE LATE PLEISTOCENE, about 13,000\n"
	.string "to 11,000 years ago.\p"
	.string "AENOCYON, ARCTODUS, MIRACINONYX,\n"
	.string "PANTHERA, MAMMUTHUS and CAMELOPS:\l"
	.string "the dire wolf, short-faced bear,\l"
	.string "American cheetah, lion, mammoth\l"
	.string "and camel.\p"
	.string "Horses and musk oxen vanished from\n"
	.string "the lower 48 but live elsewhere,\l"
	.string "and horses came back in the 1500s.\l"
	.string "The cause was climate, people, or\l"
	.string "both. It is still argued.$"

StrataInterpretive2F_Text_StatueNow:
	.string "THE CASE THAT IS NOT WRITTEN YET.\p"
	.string "Black-footed ferret. Swift fox.\n"
	.string "Sage-grouse. Bison. Each one\l"
	.string "nearly entered a case in the last\l"
	.string "150 years, and each one is still\l"
	.string "out on the prairie.\p"
	.string "Every case in this Hall was closed\n"
	.string "by the record. These are still\l"
	.string "open.$"
