@ Sand Arroyo (present day, BLM land): reached across the badlands' south boundary
@ once Ranger Ortiz has issued the collecting permit. Someone has dug a pit here
@ without a permit. Josie finds it after act 3 (the field station interlude); after act 5
@ the player documents it with Ortiz (S1, src/strata_story.c): she asks for three records,
@ the pit, the broken jacket and the tire tracks, logged at the pit sign, the jacket and the
@ spoil heap (FLAG_STRATA_STORY_EVIDENCE_*).
StrataSandArroyo_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, StrataSandArroyo_OnTransition
	.byte 0

StrataSandArroyo_OnTransition:
	special Strata_StoryPrepareMap
	setflag FLAG_TEMP_9
	call_if_eq VAR_TEMP_2, SUBPLOT_PIT_DOCUMENTED, StrataSandArroyo_EventScript_OrtizHere
	end

StrataSandArroyo_EventScript_OrtizHere::
	clearflag FLAG_TEMP_9
	return

StrataSandArroyo_EventScript_ContextNote::
	msgbox StrataSandArroyo_Text_ContextNote, MSGBOX_SIGN
	end

@ Act 5 done: Ranger Ortiz, documenting the pit.
StrataSandArroyo_EventScript_Ortiz::
	lock
	faceplayer
	goto_if_ge VAR_STRATA_SUBPLOT, SUBPLOT_PIT_DOCUMENTED, StrataSandArroyo_EventScript_OrtizDone
	goto_if_unset FLAG_STRATA_STORY_EVIDENCE_STARTED, StrataSandArroyo_EventScript_OrtizBrief
	goto_if_unset FLAG_STRATA_STORY_EVIDENCE_PIT, StrataSandArroyo_EventScript_OrtizRemind
	goto_if_unset FLAG_STRATA_STORY_EVIDENCE_JACKET, StrataSandArroyo_EventScript_OrtizRemind
	goto_if_unset FLAG_STRATA_STORY_EVIDENCE_TRACKS, StrataSandArroyo_EventScript_OrtizRemind
	msgbox StrataSandArroyo_Text_StoryOrtizReport, MSGBOX_DEFAULT
	setvar VAR_STRATA_SUBPLOT, SUBPLOT_PIT_DOCUMENTED
	special Strata_StoryPrepareMap
	release
	end

StrataSandArroyo_EventScript_OrtizBrief::
	msgbox StrataSandArroyo_Text_StoryOrtizBrief, MSGBOX_DEFAULT
	setflag FLAG_STRATA_STORY_EVIDENCE_STARTED
	release
	end

StrataSandArroyo_EventScript_OrtizRemind::
	msgbox StrataSandArroyo_Text_StoryOrtizRemind, MSGBOX_DEFAULT
	release
	end

StrataSandArroyo_EventScript_OrtizDone::
	msgbox StrataSandArroyo_Text_StoryOrtizDone, MSGBOX_DEFAULT
	release
	end

@ True while Ortiz's records are being made (VAR_RESULT).
StrataSandArroyo_EventScript_Documenting::
	setvar VAR_RESULT, FALSE
	goto_if_ne VAR_STRATA_SUBPLOT, SUBPLOT_HALVORSEN_REFUSAL, StrataSandArroyo_EventScript_DocumentingEnd
	goto_if_unset FLAG_STRATA_STORY_EVIDENCE_STARTED, StrataSandArroyo_EventScript_DocumentingEnd
	setvar VAR_RESULT, TRUE
StrataSandArroyo_EventScript_DocumentingEnd::
	return

StrataSandArroyo_EventScript_Pit::
	lockall
	msgbox StrataSandArroyo_Text_Pit, MSGBOX_DEFAULT
	@ Josie's find (the field log moves on once the player has seen it).
	call_if_ge VAR_STRATA_SUBPLOT, SUBPLOT_JOSIE_PIT, StrataSandArroyo_EventScript_SawPit
	call StrataSandArroyo_EventScript_Documenting
	goto_if_eq VAR_RESULT, FALSE, StrataSandArroyo_EventScript_SignEnd
	goto_if_set FLAG_STRATA_STORY_EVIDENCE_PIT, StrataSandArroyo_EventScript_Logged
	playse SE_CLICK
	msgbox StrataSandArroyo_Text_StoryLogPit, MSGBOX_DEFAULT
	setflag FLAG_STRATA_STORY_EVIDENCE_PIT
	goto StrataSandArroyo_EventScript_SignEnd

StrataSandArroyo_EventScript_SawPit::
	goto_if_set FLAG_STRATA_STORY_SAW_PIT, StrataSandArroyo_EventScript_SawPitEnd
	msgbox StrataSandArroyo_Text_StoryJosiesPit, MSGBOX_DEFAULT
	setflag FLAG_STRATA_STORY_SAW_PIT
StrataSandArroyo_EventScript_SawPitEnd::
	return

StrataSandArroyo_EventScript_Jacket::
	lockall
	msgbox StrataSandArroyo_Text_Jacket, MSGBOX_DEFAULT
	call StrataSandArroyo_EventScript_Documenting
	goto_if_eq VAR_RESULT, FALSE, StrataSandArroyo_EventScript_SignEnd
	goto_if_set FLAG_STRATA_STORY_EVIDENCE_JACKET, StrataSandArroyo_EventScript_Logged
	playse SE_CLICK
	msgbox StrataSandArroyo_Text_StoryLogJacket, MSGBOX_DEFAULT
	setflag FLAG_STRATA_STORY_EVIDENCE_JACKET
	goto StrataSandArroyo_EventScript_SignEnd

StrataSandArroyo_EventScript_Spoil::
	lockall
	msgbox StrataSandArroyo_Text_Spoil, MSGBOX_DEFAULT
	call StrataSandArroyo_EventScript_Documenting
	goto_if_eq VAR_RESULT, FALSE, StrataSandArroyo_EventScript_SignEnd
	goto_if_set FLAG_STRATA_STORY_EVIDENCE_TRACKS, StrataSandArroyo_EventScript_Logged
	playse SE_CLICK
	msgbox StrataSandArroyo_Text_StoryLogTracks, MSGBOX_DEFAULT
	setflag FLAG_STRATA_STORY_EVIDENCE_TRACKS
	goto StrataSandArroyo_EventScript_SignEnd

StrataSandArroyo_EventScript_Logged::
	msgbox StrataSandArroyo_Text_StoryLogged, MSGBOX_DEFAULT
StrataSandArroyo_EventScript_SignEnd::
	releaseall
	end

StrataSandArroyo_Text_ContextNote:
	.string "FIELD NOTE: Context is data. The\n"
	.string "layer dates a fossil. Its position\l"
	.string "shows how it died and was buried.\p"
	.string "Dig a bone out with no notes, and\n"
	.string "most of its science goes with it.$"

StrataSandArroyo_Text_Pit:
	.string "A pit cut into the slope with picks\n"
	.string "and a shovel. The tool marks are\l"
	.string "fresh.\p"
	.string "No stakes. No field numbers. No\n"
	.string "flagging tape.\p"
	.string "Whatever came out of here has lost\n"
	.string "its layer.$"

StrataSandArroyo_Text_Jacket:
	.string "A plaster jacket, cracked open and\n"
	.string "left behind. Bone splinters inside.\p"
	.string "There's no field number written on\n"
	.string "it. Nobody can say which layer it\l"
	.string "came from now.$"

StrataSandArroyo_Text_Spoil:
	.string "A heap of grey spoil from the pit.\p"
	.string "Tire tracks run from here toward\n"
	.string "the private-land fence.$"

StrataSandArroyo_Text_StoryJosiesPit::
	.string "This is the pit JOSIE found. You\n"
	.string "note the time and the place, and\l"
	.string "leave everything as it is.$"

StrataSandArroyo_Text_StoryOrtizBrief::
	.string "RANGER ORTIZ: Thanks for coming.\n"
	.string "JOSIE's report checks out.\p"
	.string "I need this pit documented the way\n"
	.string "you'd record a find: photos, GPS,\l"
	.string "and the layer.\p"
	.string "Three records. The pit itself, the\n"
	.string "broken jacket, and the tire tracks\l"
	.string "by the spoil heap.\p"
	.string "Don't move anything. A record is\n"
	.string "only good if someone else could\l"
	.string "stand here and check it.$"

StrataSandArroyo_Text_StoryOrtizRemind::
	.string "RANGER ORTIZ: Three records: the pit,\n"
	.string "the jacket, the tracks by the spoil\l"
	.string "heap. Bring them back to me.$"

StrataSandArroyo_Text_StoryOrtizReport::
	.string "RANGER ORTIZ: Let's see. Time, place,\n"
	.string "layer, photos. Good.\p"
	.string "The pick marks cut the same layer\n"
	.string "your crew digs in the badlands.\l"
	.string "This is federal ground.\p"
	.string "Fossils on BLM land are public.\n"
	.string "Digging them without a permit is\l"
	.string "against federal law.\p"
	.string "And those tracks run to the fence\n"
	.string "of the lease KESSLER's crew works.\p"
	.string "I'll take it from here. Thank you,\n"
	.string "{PLAYER}. This is what notes are for.$"

StrataSandArroyo_Text_StoryOrtizDone::
	.string "RANGER ORTIZ: The file's with my\n"
	.string "office now. Go on, you've got a rig\l"
	.string "to run.$"

StrataSandArroyo_Text_StoryLogPit::
	.string "You photograph the pit wall and log\n"
	.string "its GPS position.\p"
	.string "The pick marks cut grey mudstone\n"
	.string "above a sandstone channel. You\l"
	.string "write down the layer.$"

StrataSandArroyo_Text_StoryLogJacket::
	.string "You photograph the jacket and note\n"
	.string "the missing field number.\p"
	.string "Inside: splinters of limb bone, too\n"
	.string "broken to name.$"

StrataSandArroyo_Text_StoryLogTracks::
	.string "You photograph the tire tracks and\n"
	.string "log the line they take.\p"
	.string "They run straight to the private-\n"
	.string "land fence, toward the next lease.$"

StrataSandArroyo_Text_StoryLogged::
	.string "That record is already in your\n"
	.string "notebook.$"
