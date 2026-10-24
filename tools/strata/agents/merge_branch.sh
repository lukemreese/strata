#!/bin/bash
# Usage: merge_act.sh <branch>   (or merge_act.sh --continue after a manual fix)
# Merge an act branch; generated files are resolved by regenerating, markdown
# table conflicts by resolve_tables.py.
cd ~/projects/strata
BR=$1
if [ "$BR" != "--continue" ]; then
  git merge --no-edit "$BR" > /tmp/merge.log 2>&1
fi
CONFLICTS=$(git diff --name-only --diff-filter=U)
GEN_RE='^(data/maps/map_groups\.json|data/layouts/|data/maps/[^/]+/map\.json|src/data/wild_encounters\.json|include/constants/strata_maps\.h|src/data/strata_map_eras\.h|src/data/heal_locations|data/event_scripts\.s|include/constants/heal_locations|src/data/region_map/region_map_sections\.json|include/constants/layouts)'
OTHER=""
for f in $CONFLICTS; do
  if echo "$f" | grep -Eq "$GEN_RE"; then
    git checkout --theirs -- "$f" 2>/dev/null || git checkout --ours -- "$f"
    git add "$f"
  elif echo "$f" | grep -Eq '\.md$' && python3 tools/strata/agents/resolve_tables.py "$f"; then
    git add "$f"
  else
    OTHER="$OTHER $f"
  fi
done
if [ -n "$OTHER" ]; then
  echo "MANUAL CONFLICTS:$OTHER"
  exit 1
fi
python3 tools/strata/gen_species.py >/dev/null && python3 tools/strata/gen_tilesets.py >/dev/null && python3 tools/strata/gen_maps.py >/dev/null || { echo GENFAIL; exit 1; }
git add -A
if git rev-parse -q --verify MERGE_HEAD >/dev/null; then git commit -q --no-edit; else git diff --cached --quiet || git commit -q -m "Regenerate after merging $BR

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"; fi
git log --oneline -1
python3 tools/strata/mapcheck.py | grep -E "problems|unreach|can't" | head
make -j16 2>&1 | grep -E "error|Error"; echo "build ${PIPESTATUS[0]}"
make check -j16 2>&1 | grep -E "FAILED|Tests|: .*FAIL" | grep -v KNOWN | tail -6
