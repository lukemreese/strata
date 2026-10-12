StrataFieldCamp_MapScripts::
	.byte 0

StrataFieldCamp_EventScript_Crew::
	msgbox StrataFieldCamp_Text_Crew, MSGBOX_NPC
	end

StrataFieldCamp_EventScript_Student::
	msgbox StrataFieldCamp_Text_Student, MSGBOX_NPC
	end

StrataFieldCamp_EventScript_CampSign::
	msgbox StrataFieldCamp_Text_CampSign, MSGBOX_SIGN
	end

StrataFieldCamp_EventScript_StationSign::
	msgbox StrataFieldCamp_Text_StationSign, MSGBOX_SIGN
	end

StrataFieldCamp_Text_Crew:
	.string "The badlands erode a little every\n"
	.string "rain, so new bones turn up each\l"
	.string "spring.\p"
	.string "Mostly we find turtle shell and gar\n"
	.string "scales. A T. rex is the jackpot!$"

StrataFieldCamp_Text_Student:
	.string "See the stripes in the hills? Each\n"
	.string "band is old floodplain mud.\p"
	.string "Lower is older. Climbing the hill is\n"
	.string "climbing forward in time!$"

StrataFieldCamp_Text_CampSign:
	.string "HELL CREEK FIELD CAMP\n"
	.string "Garfield County, Montana$"

StrataFieldCamp_Text_StationSign:
	.string "FIELD STATION\n"
	.string "STRATA reconstruction rig inside.$"
