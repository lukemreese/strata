@ The descent scene (F3, src/strata_descent.c): after special Strata_RigLoadNext, one evolution
@ style scene for each TEAM animal whose lineage changed, then one line for the PC. Runs before
@ the loss list. Leaves VAR_0x8005 and VAR_0x8006 (the rig's losses and "reached today") alone.
Strata_EventScript_Descents::
	special Strata_GetDescentSceneCount
	goto_if_eq VAR_RESULT, 0, Strata_EventScript_DescentsPc
	@ Strata_StartDescentScenes always ends in ScriptContext_Enable, so it may only run
	@ with a scene waiting (it has an implicit waitstate).
	closemessage
	waitse
	special Strata_StartDescentScenes
Strata_EventScript_DescentsPc:
	special Strata_BufferPcDescents
	goto_if_eq VAR_RESULT, 0, Strata_EventScript_DescentsEnd
	msgbox gStringVar4, MSGBOX_DEFAULT
Strata_EventScript_DescentsEnd:
	return
