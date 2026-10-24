---
name: strata-shell
description: How to run commands in the Strata repo (WSL ~/projects/strata) from the Windows-side Claude session — the script-file pattern, quoting traps, long builds, and pushing to GitHub. Use before any shell work on Strata.
---

# Running commands in the Strata repo

The repo lives in WSL Ubuntu at `~/projects/strata` (branch `strata`, remote `origin` =
github.com/lukemreese/strata). The Claude session runs on Windows. Files are readable and
editable from Windows at `\\wsl$\Ubuntu\home\lreese\projects\strata\...` with Read/Edit/Write.

## Always use a script file

PowerShell mangles anything non-trivial passed through `wsl -- bash -c "..."`: `$`, quotes,
`(`, `from x import y`, awk `$1`, heredocs. Do this instead:

1. Write the commands to `C:\Users\lukem\AppData\Local\Temp\<task>_x.sh` with the Write tool.
2. Run: `wsl -d Ubuntu -- bash -c "tr -d '\r' < /mnt/c/Users/lukem/AppData/Local/Temp/<task>_x.sh > ~/<task>_x.sh && bash ~/<task>_x.sh"`

The `tr -d '\r'` strips Windows line endings. Use a unique `<task>` name when several agents
run at once. Put Python in a `.py` file next to it and run it from the script.

Only one-liners with no `$`, quotes or parentheses are safe inline.

## Traps

- `pkill -f '<pattern>'` inside `bash -c` matches its own command line and kills itself. Put it
  in a script file, or use a pattern that can't match the script.
- `/tmp` doesn't persist between calls; keep scripts in `~` or the Windows temp folder.
- bash reads a script while it runs: don't rewrite `~/<task>_x.sh` while a background run of it
  is still going; use a second name (`<task>_y.sh`) for anything you run meanwhile.
- Builds and full test runs take minutes, longer when other agents build at the same time. Run
  them with `run_in_background: true` (or a long timeout) and wait for the completion
  notice rather than polling.
- PNG renders meant for Read go under `/mnt/c/Users/lukem/AppData/Local/Temp/...`.
- Copy the ROM for the emulator: `cp pokeemerald.gba /mnt/c/Projects/pokemon-custom/build/strata.gba`
  (fails with "Invalid argument" while mGBA has the file open: close mGBA first).

## Pushing

The user approves each push; ask "Should I push?" unless they already said to. The global git
credential helper points at an old Git-for-Windows path and hangs. Push with:

```bash
timeout 170 git -c credential.helper= -c "credential.helper=/mnt/c/Program\ Files/Git/ucrt64/bin/git-credential-manager.exe" push origin strata
```

End commit messages with the attribution line the session's system reminder gives.
