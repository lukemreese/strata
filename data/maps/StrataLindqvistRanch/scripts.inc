@ Lindqvist Ranch (present day): Bea Lindqvist's land, between camp and Jordan.
@ The Pair (a Triceratops and a Tyrannosaurus buried together) lies under a tarp in
@ the cottonwood ring. Wade Kessler and one of his crew are here pitching Bea until
@ the Hell Creek act is done (FLAG_TEMP_1F hides them after that).
StrataLindqvistRanch_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, StrataLindqvistRanch_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, StrataLindqvistRanch_OnFrame
	.byte 0

@ Interludes (S1, src/strata_story.c): the fern spike, the auction date and auction day play here
@ on arrival. Their cast waits by the road in from camp (Josie and Halvorsen are hidden under
@ FLAG_TEMP_9 and FLAG_TEMP_A otherwise; Bea, Priya and Kessler are moved there).
StrataLindqvistRanch_OnTransition:
	call_if_ge VAR_STRATA_STORY, STORY_ACT_DONE(ERA_HELL_CREEK), StrataLindqvistRanch_EventScript_KesslerGone
	special Strata_HideLockedReviewers
	special Strata_StoryPrepareMap
	setflag FLAG_TEMP_9
	setflag FLAG_TEMP_A
	switch VAR_TEMP_2
	case SUBPLOT_FERN_SPIKE, StrataLindqvistRanch_EventScript_SetupFernSpike
	case SUBPLOT_AUCTION_DATE, StrataLindqvistRanch_EventScript_SetupAuctionDate
	case SUBPLOT_AUCTION_DAY, StrataLindqvistRanch_EventScript_SetupAuctionDay
	end

StrataLindqvistRanch_OnFrame:
	map_script_2 VAR_TEMP_3, 1, StrataLindqvistRanch_EventScript_Interlude
	.2byte 0

StrataLindqvistRanch_EventScript_SetupBea::
	setobjectxyperm LOCALID_STRATA_RANCH_BEA, 55, 7
	setobjectmovementtype LOCALID_STRATA_RANCH_BEA, MOVEMENT_TYPE_FACE_RIGHT
	return

StrataLindqvistRanch_EventScript_SetupFernSpike::
	call StrataLindqvistRanch_EventScript_SetupBea
	setobjectxyperm LOCALID_STRATA_RANCH_PRIYA, 56, 9
	setobjectmovementtype LOCALID_STRATA_RANCH_PRIYA, MOVEMENT_TYPE_FACE_RIGHT
	end

StrataLindqvistRanch_EventScript_SetupAuctionDate::
	call StrataLindqvistRanch_EventScript_SetupBea
	clearflag FLAG_TEMP_9
	end

StrataLindqvistRanch_EventScript_SetupAuctionDay::
	call StrataLindqvistRanch_EventScript_SetupBea
	clearflag FLAG_TEMP_9
	clearflag FLAG_TEMP_A
	clearflag FLAG_TEMP_1F
	setobjectxyperm LOCALID_STRATA_RANCH_KESSLER, 56, 6
	setobjectmovementtype LOCALID_STRATA_RANCH_KESSLER, MOVEMENT_TYPE_FACE_DOWN
	end

StrataLindqvistRanch_EventScript_Interlude::
	lockall
	setvar VAR_TEMP_3, 0
	switch VAR_TEMP_2
	case SUBPLOT_FERN_SPIKE, StrataLindqvistRanch_EventScript_FernSpike
	case SUBPLOT_AUCTION_DATE, StrataLindqvistRanch_EventScript_AuctionDate
	case SUBPLOT_AUCTION_DAY, StrataLindqvistRanch_EventScript_AuctionDay
	releaseall
	end

StrataLindqvistRanch_EventScript_InterludeEnd::
	special Strata_StoryPrepareMap
	releaseall
	end

@ Act 2 done: Priya explains the fern spike from her spore counts; Bea mentions the drought
@ and sends the player to Ranger Ortiz for a permit.
StrataLindqvistRanch_EventScript_FernSpike::
	applymovement OBJ_EVENT_ID_PLAYER, StrataLindqvistRanch_Movement_FaceLeft
	waitmovement 0
	msgbox StrataLindqvistRanch_Text_StoryFern1, MSGBOX_DEFAULT
	msgbox StrataLindqvistRanch_Text_StoryFern2, MSGBOX_DEFAULT
	setvar VAR_STRATA_SUBPLOT, SUBPLOT_FERN_SPIKE
	goto StrataLindqvistRanch_EventScript_InterludeEnd

@ Act 6 done: Bea has set an auction date with Kessler; Josie argues with her.
StrataLindqvistRanch_EventScript_AuctionDate::
	applymovement OBJ_EVENT_ID_PLAYER, StrataLindqvistRanch_Movement_FaceLeft
	waitmovement 0
	msgbox StrataLindqvistRanch_Text_StoryDate1, MSGBOX_DEFAULT
	msgbox StrataLindqvistRanch_Text_StoryDate2, MSGBOX_DEFAULT
	setvar VAR_STRATA_SUBPLOT, SUBPLOT_AUCTION_DATE
	goto StrataLindqvistRanch_EventScript_InterludeEnd

@ Act 8 done: auction day. Halvorsen brings the consortium's offer and the research case
@ (STR_VAR_1 = Codex species); Bea picks the consortium. Kessler loses gracefully.
StrataLindqvistRanch_EventScript_AuctionDay::
	applymovement OBJ_EVENT_ID_PLAYER, StrataLindqvistRanch_Movement_FaceLeft
	waitmovement 0
	special Strata_StoryBufferCaseCount
	msgbox StrataLindqvistRanch_Text_StoryAuction1, MSGBOX_DEFAULT
	msgbox StrataLindqvistRanch_Text_StoryAuction2, MSGBOX_DEFAULT
	msgbox StrataLindqvistRanch_Text_StoryAuction3, MSGBOX_DEFAULT
	applymovement LOCALID_STRATA_RANCH_KESSLER, StrataLindqvistRanch_Movement_KesslerLeave
	waitmovement 0
	removeobject LOCALID_STRATA_RANCH_KESSLER
	msgbox StrataLindqvistRanch_Text_StoryAuction4, MSGBOX_DEFAULT
	setvar VAR_STRATA_SUBPLOT, SUBPLOT_AUCTION_DAY
	goto StrataLindqvistRanch_EventScript_InterludeEnd

StrataLindqvistRanch_Movement_FaceLeft:
	face_left
	step_end

@ From (56, 6) west along the fence.
StrataLindqvistRanch_Movement_KesslerLeave:
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	step_end

@ The cast between scenes (they stand by the road until the next map load).
StrataLindqvistRanch_EventScript_Josie::
	lock
	faceplayer
	goto_if_ge VAR_STRATA_SUBPLOT, SUBPLOT_AUCTION_DAY, StrataLindqvistRanch_EventScript_JosieAfter
	msgbox StrataLindqvistRanch_Text_JosieDate, MSGBOX_DEFAULT
	release
	end

StrataLindqvistRanch_EventScript_JosieAfter::
	msgbox StrataLindqvistRanch_Text_JosieAfter, MSGBOX_DEFAULT
	release
	end

StrataLindqvistRanch_EventScript_Halvorsen::
	msgbox StrataLindqvistRanch_Text_Halvorsen, MSGBOX_NPC
	end

StrataLindqvistRanch_Text_StoryFern1::
	.string "PRIYA: {PLAYER}! Over here. I've\n"
	.string "counted the spores from your\l"
	.string "impact layer.\p"
	.string "Below the boundary clay: mostly\n"
	.string "pollen from flowering plants.\p"
	.string "Just above it, fern spores take\n"
	.string "over. In some samples, nearly\l"
	.string "everything is fern.\p"
	.string "Fern spores are tiny and tough.\n"
	.string "They ride the wind onto bare\l"
	.string "ground and sprout first.\p"
	.string "That's the fern spike. It tells us\n"
	.string "the forests fell, and how slowly\l"
	.string "they came back.$"

StrataLindqvistRanch_Text_StoryFern2::
	.string "BEA: Ferns on bare ground. Sounds\n"
	.string "like my south pasture.\p"
	.string "No real rain since May. If the\n"
	.string "pond goes, I sell the herd or I\l"
	.string "sell the bones.\p"
	.string "Josie says you want to look at the\n"
	.string "BLM ground south of your dig. Then\l"
	.string "you need a permit.\p"
	.string "RANGER ORTIZ hands them out at the\n"
	.string "BLM office in JORDAN, just west.$"

StrataLindqvistRanch_Text_StoryDate1::
	.string "JOSIE: Gran, you can't! A private\n"
	.string "buyer could lock it in a vault.\l"
	.string "Nobody would ever study it again.\p"
	.string "BEA: Or they might lend it to a\n"
	.string "museum. Some do.\p"
	.string "MR. KESSLER has set the date: the\n"
	.string "last day of the dig season. Sealed\l"
	.string "bids, here at the ranch.\p"
	.string "JOSIE: It's not just bones, Gran.\n"
	.string "It's the only Pair. Two animals in\l"
	.string "one layer, and how they got there.$"

StrataLindqvistRanch_Text_StoryDate2::
	.string "BEA: And the hay bill is the only\n"
	.string "hay bill. I've done the sums,\l"
	.string "Josie. Four times.\p"
	.string "Don't look at me like that,\n"
	.string "{PLAYER}. I'd take a fair offer from\l"
	.string "a museum.\p"
	.string "Nobody's made one.$"

StrataLindqvistRanch_Text_StoryAuction1::
	.string "KESSLER: The sealed bids are in,\n"
	.string "MRS. LINDQVIST. The top one would\l"
	.string "carry this ranch for ten years.\p"
	.string "DR. HALVORSEN: BEA, before you open\n"
	.string "it. The consortium's offer.\p"
	.string "It's less. I won't pretend it\n"
	.string "isn't.$"

StrataLindqvistRanch_Text_StoryAuction2::
	.string "DR. HALVORSEN: But the Pair goes on\n"
	.string "show in a public museum, as one\l"
	.string "specimen, with your family's name\l"
	.string "on the case.\p"
	.string "And here is the crew's research\n"
	.string "case: {STR_VAR_1} species, each tied to\l"
	.string "its layer.\p"
	.string "The museums want more work like it,\n"
	.string "here, on your land. Paid work.\p"
	.string "JOSIE: Gran…$"

StrataLindqvistRanch_Text_StoryAuction3::
	.string "BEA: Four generations on this place,\n"
	.string "and the thing that lasts is a pile\l"
	.string "of bones.\p"
	.string "Might as well be where people can\n"
	.string "see it.\p"
	.string "Doctor, you have a deal. MR. KESSLER,\n"
	.string "I'm sorry for your trouble.\p"
	.string "KESSLER: Don't be. Losing gracefully\n"
	.string "is part of the job.\p"
	.string "There's always another ranch.$"

StrataLindqvistRanch_Text_StoryAuction4::
	.string "JOSIE: {PLAYER}, did you hear? It's\n"
	.string "going to a museum!\p"
	.string "And I've decided. I'm switching my\n"
	.string "major to paleontology.\p"
	.string "Don't tell Gran yet. Let her enjoy\n"
	.string "the money first.$"

StrataLindqvistRanch_Text_JosieDate::
	.string "JOSIE: She's not wrong about the\n"
	.string "hay. That's the worst part.\p"
	.string "There has to be an offer that\n"
	.string "doesn't make her choose.$"

StrataLindqvistRanch_Text_JosieAfter::
	.string "JOSIE: A museum, with our name on\n"
	.string "the case. Gran's pretending she\l"
	.string "isn't proud.$"

StrataLindqvistRanch_Text_Halvorsen::
	.string "DR. HALVORSEN: We kept the Pair, and\n"
	.string "its layer. That was the part worth\l"
	.string "keeping.$"

@ Visiting researchers (peer review, C13): the palynologist (act 2), the ichthyologist at the
@ stock pond (act 5) and the Quaternary ecologist (act 8). One battle each.
StrataLindqvistRanch_EventScript_Priya::
	lock
	faceplayer
	trainerbattle_single TRAINER_STRATA_REVIEW_ACT2, StrataLindqvistRanch_Text_PriyaIntro, StrataLindqvistRanch_Text_PriyaDefeat, StrataLindqvistRanch_EventScript_PriyaWon
	msgbox StrataLindqvistRanch_Text_PriyaAfter, MSGBOX_DEFAULT
	release
	end

StrataLindqvistRanch_EventScript_PriyaWon::
	msgbox StrataLindqvistRanch_Text_PriyaNote, MSGBOX_DEFAULT
	releaseall
	end

StrataLindqvistRanch_EventScript_Keola::
	lock
	faceplayer
	trainerbattle_single TRAINER_STRATA_REVIEW_ACT5, StrataLindqvistRanch_Text_KeolaIntro, StrataLindqvistRanch_Text_KeolaDefeat, StrataLindqvistRanch_EventScript_KeolaWon
	msgbox StrataLindqvistRanch_Text_KeolaAfter, MSGBOX_DEFAULT
	release
	end

StrataLindqvistRanch_EventScript_KeolaWon::
	msgbox StrataLindqvistRanch_Text_KeolaNote, MSGBOX_DEFAULT
	releaseall
	end

StrataLindqvistRanch_EventScript_Asha::
	lock
	faceplayer
	trainerbattle_single TRAINER_STRATA_REVIEW_ACT8, StrataLindqvistRanch_Text_AshaIntro, StrataLindqvistRanch_Text_AshaDefeat, StrataLindqvistRanch_EventScript_AshaWon
	msgbox StrataLindqvistRanch_Text_AshaAfter, MSGBOX_DEFAULT
	release
	end

StrataLindqvistRanch_EventScript_AshaWon::
	msgbox StrataLindqvistRanch_Text_AshaNote, MSGBOX_DEFAULT
	releaseall
	end

StrataLindqvistRanch_Text_PriyaIntro:
	.string "PRIYA: Palynologist. I count pollen\n"
	.string "and spores: dust, basically, from\l"
	.string "the bottom of a lake.\p"
	.string "Right above the boundary clay my\n"
	.string "counts go strange. Your impact\l"
	.string "winter run should show it too.\p"
	.string "Let's compare. Peer review.$"

StrataLindqvistRanch_Text_PriyaDefeat:
	.string "PRIYA: Your animals fit my spore\n"
	.string "counts better than I expected.$"

StrataLindqvistRanch_Text_PriyaNote:
	.string "PRIYA: Field note: the fern spike.\p"
	.string "Just above the boundary clay, fern\n"
	.string "spores jump to nearly everything\l"
	.string "and flowering-plant pollen falls\l"
	.string "away.\p"
	.string "Ferns are first back after a\n"
	.string "disaster. Forests took a long\l"
	.string "time to return.$"

StrataLindqvistRanch_Text_PriyaAfter:
	.string "PRIYA: A spike of fern spores marks\n"
	.string "a disaster zone. Volcanic slopes\l"
	.string "today show the same pattern.$"

StrataLindqvistRanch_Text_KeolaIntro:
	.string "KEOLA: Ichthyologist. Fish, mostly\n"
	.string "dead ones: the best-preserved fish\l"
	.string "in the world.\p"
	.string "Green River limestone keeps every\n"
	.string "scale and fin. Your rig rendered\l"
	.string "it sharp, didn't it?\p"
	.string "Peer review: my fossils against\n"
	.string "your reconstruction.$"

StrataLindqvistRanch_Text_KeolaDefeat:
	.string "KEOLA: Your reconstruction held. I\n"
	.string "have a whole drawer of herring\l"
	.string "that agree.$"

StrataLindqvistRanch_Text_KeolaNote:
	.string "KEOLA: Field note.\p"
	.string "The lake layers are seasonal: one\n"
	.string "pale band a year, like tree rings.\p"
	.string "A mass die-off of fish is one band\n"
	.string "thick. That's how we know it was\l"
	.string "one bad year, not a slow decline.$"

StrataLindqvistRanch_Text_KeolaAfter:
	.string "KEOLA: Count the bands. Each pair\n"
	.string "of layers is a year. The rock keeps\l"
	.string "a calendar.$"

StrataLindqvistRanch_Text_AshaIntro:
	.string "ASHA: Quaternary ecologist: the\n"
	.string "last two million years. I study\l"
	.string "what the Ice Age left standing.\p"
	.string "Mammoths, giant bears, lions, and\n"
	.string "then, within a few thousand years,\l"
	.string "almost none of them.\p"
	.string "Peer review: your last layer\n"
	.string "against my survey data.$"

StrataLindqvistRanch_Text_AshaDefeat:
	.string "ASHA: Your survivors are the right\n"
	.string "survivors. I'll cite that.$"

StrataLindqvistRanch_Text_AshaNote:
	.string "ASHA: Field note.\p"
	.string "The big animals vanished while the\n"
	.string "climate changed and while people\l"
	.string "arrived. We don't know how much\l"
	.string "each one mattered.\p"
	.string "The honest answer is both, with\n"
	.string "error bars. I distrust anyone with\l"
	.string "a single cause.$"

StrataLindqvistRanch_Text_AshaAfter:
	.string "ASHA: Bison, pronghorn, wolves.\n"
	.string "Everything out on the prairie today\l"
	.string "made it through the last filter.$"

StrataLindqvistRanch_EventScript_KesslerGone::
	setflag FLAG_TEMP_1F
	return

StrataLindqvistRanch_EventScript_Bea::
	lock
	faceplayer
	goto_if_ge VAR_STRATA_STORY, STORY_ACT_DONE(ERA_HELL_CREEK), StrataLindqvistRanch_EventScript_BeaLater
	msgbox StrataLindqvistRanch_Text_BeaAct0, MSGBOX_DEFAULT
	release
	end

StrataLindqvistRanch_EventScript_BeaLater::
	goto_if_ge VAR_STRATA_SUBPLOT, SUBPLOT_AUCTION_DAY, StrataLindqvistRanch_EventScript_BeaSold
	goto_if_ge VAR_STRATA_SUBPLOT, SUBPLOT_AUCTION_DATE, StrataLindqvistRanch_EventScript_BeaDate
	msgbox StrataLindqvistRanch_Text_BeaLater, MSGBOX_DEFAULT
	release
	end

StrataLindqvistRanch_EventScript_BeaDate::
	msgbox StrataLindqvistRanch_Text_BeaDate, MSGBOX_DEFAULT
	release
	end

StrataLindqvistRanch_EventScript_BeaSold::
	msgbox StrataLindqvistRanch_Text_BeaSold, MSGBOX_DEFAULT
	release
	end

StrataLindqvistRanch_Text_BeaDate::
	.string "BEA: Last day of the season. Sealed\n"
	.string "bids. Then it's done, one way or\l"
	.string "the other.\p"
	.string "I keep telling Josie it's only\n"
	.string "bones. She keeps not believing me.$"

StrataLindqvistRanch_Text_BeaSold::
	.string "BEA: The consortium paid. Not what\n"
	.string "the dealer bid, but the hay's\l"
	.string "bought, and the bones stay public.\p"
	.string "Josie tells everyone in JORDAN.\n"
	.string "Twice.$"

StrataLindqvistRanch_EventScript_Kessler::
	lock
	faceplayer
	msgbox StrataLindqvistRanch_Text_Kessler, MSGBOX_DEFAULT
	setflag FLAG_STRATA_MET_KESSLER
	release
	end

StrataLindqvistRanch_EventScript_KesslerHand::
	msgbox StrataLindqvistRanch_Text_KesslerHand, MSGBOX_NPC
	end

StrataLindqvistRanch_EventScript_Tarp::
	lockall
	msgbox StrataLindqvistRanch_Text_Tarp, MSGBOX_DEFAULT
	setflag FLAG_STRATA_SAW_PAIR
	releaseall
	end

StrataLindqvistRanch_EventScript_RanchSign::
	msgbox StrataLindqvistRanch_Text_RanchSign, MSGBOX_SIGN
	end

StrataLindqvistRanch_EventScript_HouseDoor::
	msgbox StrataLindqvistRanch_Text_HouseDoor, MSGBOX_SIGN
	end

StrataLindqvistRanch_EventScript_SplitEstateNote::
	msgbox StrataLindqvistRanch_Text_SplitEstateNote, MSGBOX_SIGN
	end

StrataLindqvistRanch_EventScript_DroughtNote::
	msgbox StrataLindqvistRanch_Text_DroughtNote, MSGBOX_SIGN
	end

StrataLindqvistRanch_Text_BeaAct0:
	.string "BEA: You're one of Halvorsen's kids.\n"
	.string "I'm BEA LINDQVIST. This is my land.\p"
	.string "Four generations of cattle, and now\n"
	.string "the most valuable thing on the place\l"
	.string "is a pile of bones.\p"
	.string "This gentleman wants to sell them\n"
	.string "for me. Says he'll get a price that\l"
	.string "would carry us through the drought.\p"
	.string "I haven't said yes. I haven't said\n"
	.string "no, either.$"

StrataLindqvistRanch_Text_BeaLater:
	.string "BEA: Pond's down another foot.\n"
	.string "I'm selling heifers I'd rather keep.\p"
	.string "Josie wants the Pair in a museum.\n"
	.string "Museums want it for free.\p"
	.string "Somebody tell me how that pays for\n"
	.string "hay.$"

StrataLindqvistRanch_Text_Kessler:
	.string "WADE KESSLER, Kessler Natural\n"
	.string "History. A pleasure.\p"
	.string "Every spring the rain breaks up\n"
	.string "bones nobody came to collect.\p"
	.string "Museums can't afford them, and the\n"
	.string "badlands won't wait. I can, and I do.\p"
	.string "Everything I sell comes off private\n"
	.string "land, legally. Tell your director\l"
	.string "my door is open.$"

StrataLindqvistRanch_Text_KesslerHand:
	.string "Boss says we stay on deeded land.\n"
	.string "Fence line's right there.\p"
	.string "Mostly.$"

StrataLindqvistRanch_Text_Tarp:
	.string "A blue tarp, weighted down with old\n"
	.string "tires.\p"
	.string "Under one corner: the curved edge of\n"
	.string "a TRICERATOPS frill, wide as a wagon\l"
	.string "wheel.\p"
	.string "A hand's width away, the toe bones of\n"
	.string "a TYRANNOSAURUS.\p"
	.string "Two animals, buried together. Josie\n"
	.string "calls it the Pair.$"

StrataLindqvistRanch_Text_RanchSign:
	.string "LINDQVIST RANCH\n"
	.string "Homesteaded 1911. Shut the gate.$"

StrataLindqvistRanch_Text_HouseDoor:
	.string "The ranch house. The door's shut;\n"
	.string "BEA's out with the stock.$"

StrataLindqvistRanch_Text_SplitEstateNote:
	.string "FIELD NOTE: Out West, the land's\n"
	.string "surface and the minerals under it\l"
	.string "can have different owners.\p"
	.string "Montana counts fossils as part of\n"
	.string "the surface, not the minerals. So\l"
	.string "the Pair is BEA's to sell.$"

StrataLindqvistRanch_Text_DroughtNote:
	.string "FIELD NOTE: Stock ponds catch spring\n"
	.string "snowmelt and rain for the cattle.\p"
	.string "In a dry year they shrink to mud,\n"
	.string "and a rancher has to sell animals\l"
	.string "or buy hay and water.$"
