---
name: strata-playtest
description: Playtesting Strata in mGBA with computer use — launching, input timing, save states, the debug menu (warps, story var, no-collision), and catching crashes with mGBA's log viewer, a watchpoint and addr2line. Use when asked to test or reproduce something in game.
---

# Playtesting Strata in mGBA

Build a debug ROM first (strata-build-test skill). mGBA: `C:\Program Files\mGBA\mGBA.exe`.
ROMs and saves: `C:\Projects\pokemon-custom\build\` (`strata-debug.gba` + `.sav`). Close mGBA
before overwriting the ROM. Set an old save aside (rename to `.sav.old`) instead of deleting it.

## Input

- Request access to `mGBA`, then click the game window before keys (keys fail if Claude's window
  has focus). Keys: X = A, Z = B, Enter = Start, arrows.
- Use `hold_key`, not `key`: about 0.1 s for buttons, about 0.27 s per tile of walking. A tap of
  ≤ 0.1 s on an arrow only turns the player.
- Text is slow: ~1.8–2.5 s per box. Pressing A too early skips to the end of the box; extra A
  presses can land on a YES/NO prompt.
- Batch predictable sequences (`computer_batch`) and screenshot at 0.4–0.5 scale; zoom on the text box.
- If another app (e.g. Edge) is in front, `open_application mGBA` brings mGBA forward but also opens
  a second, empty mGBA window; ignore it and click the window running the game.
- A long batch that assumes a menu state drifts badly if one press is missed (you end up deep in the
  team menu). After any menu batch, screenshot before continuing, and back out with several B presses.
- Turn encounters off (debug menu) before walking anywhere you aren't testing battles; tall grass
  near the Act 1 arrival triggers a battle every few steps.
- A new game takes ~3 minutes of input (intro + station). Save a state right after it (slot 1) and
  reuse it; save states don't survive a rebuilt ROM, so rebuild only between test sessions.

## Save states (huge time saver)

Shift+F1..F9 saves a state to a slot, F1..F9 loads it. Save one right after the new-game intro and
before each test so a crash or a long walk can be retried instantly.

## Debug menu (Start → DEBUG)

- Main list: Utilities, PC/Bag, Party, Give X, Player, Scripts, Trainers, Encounters, Flags & Vars.
  The cursor doesn't wrap upward; count downs from the top.
- **Warp:** Utilities → Warp to map warp. Strata maps are map group **75**. The number entry
  uses up/down to change and left/right to pick the digit (+1/+10/+100). The map order is
  `data/maps/map_groups.json`.
- **Story:** Flags & Vars → Set Var. `VAR_STRATA_STORY` = **0x408B** (0x4000 + 139). Select the
  var, then set the value.
- **Walk anywhere:** Flags & Vars → Toggle Collision OFF (index 13) and Encounter OFF (14). Coord
  triggers still fire. Signs you would normally face from a blocked tile can now be walked onto.
- Interactions have facing rules (e.g. the rig only from below, facing north).

## When the game resets or freezes

1. Tools → View logs; enable Debug and Game Error and disable Info (DMA spam). "Bad memory" or
   "Bad BIOS" lines every frame mean a NULL or garbage pointer.
2. Tools → Open debugger console: `watch/r 0x8` (or the bad address), then `c`. Note `r15` (PC)
   and `r14` (LR).
3. Map them: `arm-none-eabi-addr2line -f -e ~/strata-debug.elf <pc> <lr>` (from the same build as
   the ROM you ran).

Example: `UpdateObjectEventOffscreen` reading NULL+8 meant an object with no graphics
(FRLG-only `OBJ_EVENT_GFX_WORKER_F`).

## Known quirks

- Present-day maps follow the real clock, so they look dark at night. Deep-time maps use fixed light.
- Creature objects show the substitute placeholder until their species has overworld sprites.
