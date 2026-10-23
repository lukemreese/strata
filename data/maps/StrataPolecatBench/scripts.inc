@ Act 4: Polecat Bench, Clarks Fork Basin, Wyoming (~56 Ma). Field notes only.
StrataPolecatBench_MapScripts::
	.byte 0

StrataPolecatBench_EventScript_CarbonNote::
	msgbox StrataPolecatBench_Text_CarbonNote, MSGBOX_SIGN
	end

StrataPolecatBench_EventScript_ImmigrantsNote::
	msgbox StrataPolecatBench_Text_ImmigrantsNote, MSGBOX_SIGN
	end

StrataPolecatBench_EventScript_ReleaseRateNote::
	msgbox StrataPolecatBench_Text_ReleaseRateNote, MSGBOX_SIGN
	end

StrataPolecatBench_Text_CarbonNote:
	.string "FIELD NOTE: CARBON ISOTOPES\p"
	.string "In these beds the carbon in fossil\n"
	.string "soils and teeth turns lighter, by\l"
	.string "roughly 4 to 6 parts per thousand.\p"
	.string "That dip is the PETM's signature,\n"
	.string "and it fades over 100,000 years or\l"
	.string "more. Where the carbon came from\l"
	.string "is still debated.$"

StrataPolecatBench_Text_ImmigrantsNote:
	.string "FIELD NOTE: IMMIGRANTS\p"
	.string "At the base of the Eocene, horses,\n"
	.string "primates and even-toed hoofed\l"
	.string "mammals first appear in North\l"
	.string "America.\p"
	.string "The Arctic was warm enough to\n"
	.string "cross on land. The exact route is\l"
	.string "debated. Early rodents arrived a\l"
	.string "little before the PETM.$"

StrataPolecatBench_Text_ReleaseRateNote:
	.string "RIG NOTE: HOW FAST?\p"
	.string "The PETM carbon release took\n"
	.string "thousands of years: at most about\l"
	.string "1 billion tons of carbon a year\l"
	.string "(Zeebe et al. 2016).\p"
	.string "People now add about 10 billion\n"
	.string "tons a year: roughly ten times\l"
	.string "faster. Both figures are\l"
	.string "estimates.$"
