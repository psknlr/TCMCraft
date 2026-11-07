#!/usr/bin/env bash
# Check the TCMCraft content pack against a ClinicalCraft checkout:
#   1. content/ is what tools/content-gen writes (build.py --check);
#   2. the offline pack checks (tools/pack_check.py: schema shape, integrity, content lints, the reference path
#      replayed, the matcher corpus, catalogs, templates, the facility) and the alternative paths' scores;
#   3. ClinicalCraft itself, with the pack in contentDirs: `facilities validate --all`, `cases validate --strict`
#      and `cases verify` for every pack case, and the offline demonstration (`exec --autopilot`) finishing each
#      case completed.
# Usage: tools/check.sh [path/to/ClinicalCraft]   (default: ../ClinicalCraft next to this repository)
# CI (.github/workflows/check.yml) runs it against the revision pinned in tools/clinicalcraft.rev.
# Nothing is left behind in the ClinicalCraft checkout.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
PACK="$ROOT/content"
CC="$(cd "${1:-$ROOT/../ClinicalCraft}" && pwd)"
SETTINGS_HOME="$(mktemp -d)"
trap 'rm -rf "$SETTINGS_HOME"' EXIT
printf '{"contentDirs": ["%s"]}\n' "$PACK" > "$SETTINGS_HOME/settings.json"
cc() { (cd "$CC" && CLINICALCRAFT_HOME="$SETTINGS_HOME" npm run -s cc -- "$@"); }

echo "== content/ is up to date with tools/content-gen"
python3 "$HERE/content-gen/build.py" --check

echo "== offline pack checks (tools/pack_check.py)"
python3 "$HERE/pack_check.py" --clinicalcraft "$CC" --paths

echo "== ClinicalCraft at $CC ($(git -C "$CC" rev-parse --short HEAD 2>/dev/null || echo 'not a git checkout'))"
cc facilities validate --all

for case_json in "$PACK"/cases/*/case.json; do
  id="$(basename "$(dirname "$case_json")")"
  echo "== case $id: validate --strict, verify, offline demonstration"
  cc cases validate "$case_json" --strict
  cc cases verify "$id"
  cc exec --case "$id" --autopilot --approval bypass --provider offline --output-format json --lang en \
    | python3 -c 'import json, sys
r = json.loads(sys.stdin.read().strip().splitlines()[-1])
score = r.get("assessment", {}).get("report", {}).get("score", {}).get("percent")
print("  demonstration: finished=%s completed=%s score=%s%%" % (r.get("finished"), r.get("completed"), score))
sys.exit(0 if r.get("finished") and r.get("completed") else 1)'
done
echo "== all checks passed"
