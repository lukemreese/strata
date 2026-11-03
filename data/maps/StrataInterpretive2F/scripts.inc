@ Epilogue: the Hall of Lost Lineages. One case per extinction filter of src/data/lineages.h
@ (sExtinctions_*), and the two statues at the door (the end-Pleistocene filter, and the case
@ that is not written yet).
@
@ Each filter plaque reads: its title, then the lineages the player carried and lost to that
@ filter (fossil flags, special Strata_BufferHallCase in src/strata_fossils.c), then why the
@ filter took them. A player who lost none there reads the generic list of every lineage the
@ rig drops at that filter instead.
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

@ Each case: VAR_0x8004 = the filter's era, then the three plaque texts.
StrataInterpretive2F_EventScript_CaseKPg::
	lockall
	setvar VAR_0x8004, ERA_IMPACT_WINTER
	msgbox StrataInterpretive2F_Text_CaseKPg_Title, MSGBOX_DEFAULT
	call StrataInterpretive2F_EventScript_OwnFossils
	goto_if_ne VAR_RESULT, 0, StrataInterpretive2F_EventScript_CaseKPgWhy
	msgbox StrataInterpretive2F_Text_CaseKPg_List, MSGBOX_DEFAULT
StrataInterpretive2F_EventScript_CaseKPgWhy:
	msgbox StrataInterpretive2F_Text_CaseKPg_Why, MSGBOX_DEFAULT
	goto StrataInterpretive2F_EventScript_CaseEnd

StrataInterpretive2F_EventScript_CasePaleocene::
	lockall
	setvar VAR_0x8004, ERA_BIGHORN_PETM
	msgbox StrataInterpretive2F_Text_CasePaleocene_Title, MSGBOX_DEFAULT
	call StrataInterpretive2F_EventScript_OwnFossils
	goto_if_ne VAR_RESULT, 0, StrataInterpretive2F_EventScript_CasePaleoceneWhy
	msgbox StrataInterpretive2F_Text_CasePaleocene_List, MSGBOX_DEFAULT
StrataInterpretive2F_EventScript_CasePaleoceneWhy:
	msgbox StrataInterpretive2F_Text_CasePaleocene_Why, MSGBOX_DEFAULT
	goto StrataInterpretive2F_EventScript_CaseEnd

StrataInterpretive2F_EventScript_CaseEocene::
	lockall
	setvar VAR_0x8004, ERA_WHITE_RIVER
	msgbox StrataInterpretive2F_Text_CaseEocene_Title, MSGBOX_DEFAULT
	call StrataInterpretive2F_EventScript_OwnFossils
	goto_if_ne VAR_RESULT, 0, StrataInterpretive2F_EventScript_CaseEoceneWhy
	msgbox StrataInterpretive2F_Text_CaseEocene_List, MSGBOX_DEFAULT
StrataInterpretive2F_EventScript_CaseEoceneWhy:
	msgbox StrataInterpretive2F_Text_CaseEocene_Why, MSGBOX_DEFAULT
	goto StrataInterpretive2F_EventScript_CaseEnd

StrataInterpretive2F_EventScript_CaseMiocene::
	lockall
	setvar VAR_0x8004, ERA_ASHFALL
	msgbox StrataInterpretive2F_Text_CaseMiocene_Title, MSGBOX_DEFAULT
	call StrataInterpretive2F_EventScript_OwnFossils
	goto_if_ne VAR_RESULT, 0, StrataInterpretive2F_EventScript_CaseMioceneWhy
	msgbox StrataInterpretive2F_Text_CaseMiocene_List, MSGBOX_DEFAULT
StrataInterpretive2F_EventScript_CaseMioceneWhy:
	msgbox StrataInterpretive2F_Text_CaseMiocene_Why, MSGBOX_DEFAULT
	goto StrataInterpretive2F_EventScript_CaseEnd

StrataInterpretive2F_EventScript_CaseIceAge::
	lockall
	setvar VAR_0x8004, ERA_TRAP_CAVE
	msgbox StrataInterpretive2F_Text_CaseIceAge_Title, MSGBOX_DEFAULT
	call StrataInterpretive2F_EventScript_OwnFossils
	goto_if_ne VAR_RESULT, 0, StrataInterpretive2F_EventScript_CaseIceAgeWhy
	msgbox StrataInterpretive2F_Text_CaseIceAge_List, MSGBOX_DEFAULT
StrataInterpretive2F_EventScript_CaseIceAgeWhy:
	msgbox StrataInterpretive2F_Text_CaseIceAge_Why, MSGBOX_DEFAULT
	goto StrataInterpretive2F_EventScript_CaseEnd

StrataInterpretive2F_EventScript_StatueLast::
	lockall
	setvar VAR_0x8004, ERA_EPILOGUE
	msgbox StrataInterpretive2F_Text_StatueLast_Title, MSGBOX_DEFAULT
	call StrataInterpretive2F_EventScript_OwnFossils
	goto_if_ne VAR_RESULT, 0, StrataInterpretive2F_EventScript_StatueLastWhy
	msgbox StrataInterpretive2F_Text_StatueLast_List, MSGBOX_DEFAULT
StrataInterpretive2F_EventScript_StatueLastWhy:
	msgbox StrataInterpretive2F_Text_StatueLast_Why, MSGBOX_DEFAULT
	goto StrataInterpretive2F_EventScript_CaseEnd

@ Input VAR_0x8004 = era. Shows the player's own lost lineages from that filter, if any.
@ Output VAR_RESULT = how many.
StrataInterpretive2F_EventScript_OwnFossils:
	special Strata_BufferHallCase
	goto_if_eq VAR_RESULT, 0, StrataInterpretive2F_EventScript_OwnFossilsNone
	msgbox gStringVar4, MSGBOX_DEFAULT
	setvar VAR_RESULT, 1
StrataInterpretive2F_EventScript_OwnFossilsNone:
	return

StrataInterpretive2F_EventScript_CaseEnd:
	closemessage
	releaseall
	end

StrataInterpretive2F_EventScript_StatueNow::
	msgbox StrataInterpretive2F_Text_StatueNow, MSGBOX_SIGN
	end

StrataInterpretive2F_Text_Docent:
	.string "Welcome to the Hall of Lost\n"
	.string "Lineages. Each case is one filter\l"
	.string "in the record: who was there\l"
	.string "before it, and who was gone after.\p"
	.string "Some of these were in your team\n"
	.string "once. Their cases hold your own\l"
	.string "fossils. The rig can carry a\l"
	.string "lineage only as far as the record\l"
	.string "lets it go.$"

StrataInterpretive2F_Text_Student:
	.string "The cases list who died out, not\n"
	.string "who deserved to. Size, diet,\l"
	.string "habitat and luck. That's what the\l"
	.string "rock says.\p"
	.string "I keep wanting to put a case here\n"
	.string "for the animals on the prairie.\l"
	.string "The curator says not yet.$"

StrataInterpretive2F_Text_CaseKPg_Title:
	.string "THE END OF THE CRETACEOUS, 66\n"
	.string "million years ago.$"

StrataInterpretive2F_Text_CaseKPg_List:
	.string "Gone above the boundary clay:\n"
	.string "TYRANNOSAURUS, TRICERATOPS,\l"
	.string "EDMONTOSAURUS, ANKYLOSAURUS,\l"
	.string "PACHYCEPHALOSAURUS,\l"
	.string "THESCELOSAURUS, ACHERORAPTOR,\l"
	.string "ANZU, DIDELPHODON and AVISAURUS.$"

StrataInterpretive2F_Text_CaseKPg_Why:
	.string "Every dinosaur that was not a\n"
	.string "bird, and the tree-perching birds.\l"
	.string "The survivors were small, or\l"
	.string "burrowed, or lived in water, or\l"
	.string "ate detritus.$"

StrataInterpretive2F_Text_CasePaleocene_Title:
	.string "THE PALEOCENE RECOVERY, gone by\n"
	.string "about 56 million years ago.$"

StrataInterpretive2F_Text_CasePaleocene_List:
	.string "PURGATORIUS, LOXOLOPHUS,\n"
	.string "CARSIOPTYCHUS, TAENIOLABIS and\l"
	.string "EOCONODON.$"

StrataInterpretive2F_Text_CasePaleocene_Why:
	.string "The first mammals to fill the\n"
	.string "emptied world were replaced by\l"
	.string "newcomers from other continents.\l"
	.string "Last appearances are approximate.$"

StrataInterpretive2F_Text_CaseEocene_Title:
	.string "THE END OF THE WARM WORLD, about\n"
	.string "34 million years ago.$"

StrataInterpretive2F_Text_CaseEocene_List:
	.string "OMOMYS, OXYAENA, PATRIOFELIS,\n"
	.string "GASTORNIS, PRESBYORNIS,\l"
	.string "CHAMPSOSAURS, BOREALOSUCHUS,\l"
	.string "MESODMA, HYOPSODUS, DIACODEXIS,\l"
	.string "CORYPHODON, ONYCHONYCTERIS,\l"
	.string "HELIOBATIS, KNIGHTIA, NOTHARCTUS\l"
	.string "and UINTATHERIUM.$"

StrataInterpretive2F_Text_CaseEocene_Why:
	.string "The Eocene-Oligocene cooling\n"
	.string "thinned the forests. Some of these\l"
	.string "were gone earlier; the case shows\l"
	.string "where the rig drops them.$"

StrataInterpretive2F_Text_CaseMiocene_Title:
	.string "THE GRASSLAND TURNOVER, gone by\n"
	.string "about 12 million years ago.$"

StrataInterpretive2F_Text_CaseMiocene_List:
	.string "HYAENODON, PALAEOLAGUS,\n"
	.string "ARCHAEOTHERIUM, HOPLOPHONEUS,\l"
	.string "MERYCOIDODON, LEPTOMERYX, STYLEMYS\l"
	.string "and ISCHYROMYS.$"

StrataInterpretive2F_Text_CaseMiocene_Why:
	.string "Cooler, drier grassland favoured\n"
	.string "runners and grazers. Rabbits,\l"
	.string "rodents and tortoises still live\l"
	.string "on through relatives.$"

StrataInterpretive2F_Text_CaseIceAge_Title:
	.string "GONE BY THE ICE AGE, between 5 and\n"
	.string "2 million years ago.$"

StrataInterpretive2F_Text_CaseIceAge_List:
	.string "APHELOPS, TELEOCERAS, HYPOHIPPUS,\n"
	.string "CORMOHIPPARION, EPICYON, BALEARICA\l"
	.string "and ANCHIGYPS.$"

StrataInterpretive2F_Text_CaseIceAge_Why:
	.string "North America's rhinos vanished\n"
	.string "about 5 million years ago, and the\l"
	.string "bone-crushing dogs by about 2\l"
	.string "million. Horses and cranes live on\l"
	.string "elsewhere.$"

StrataInterpretive2F_Text_StatueLast_Title:
	.string "THE LATE PLEISTOCENE, about 13,000\n"
	.string "to 11,000 years ago.$"

StrataInterpretive2F_Text_StatueLast_List:
	.string "AENOCYON, ARCTODUS, MIRACINONYX,\n"
	.string "PANTHERA, MAMMUTHUS and CAMELOPS:\l"
	.string "the dire wolf, short-faced bear,\l"
	.string "American cheetah, lion, mammoth\l"
	.string "and camel.$"

StrataInterpretive2F_Text_StatueLast_Why:
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
