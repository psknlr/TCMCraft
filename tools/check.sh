#!/usr/bin/env bash
# Check the TCMCraft content pack against a ClinicalCraft checkout:
#   1. content/ is what tools/content-gen writes (build.py --check);
#   2. the offline pack checks (tools/pack_check.py: schema shape, integrity, content lints, the reference path
#      replayed, the matcher corpus, catalogs, templates, the facility) and the alternative paths' scores;
#   3. ClinicalCraft itself, with the pack in contentDirs: `facilities validate --all`, `cases validate --strict`
#      and `cases verify` for every pack case, and the offline demonstration (`exec --autopilot`) of each case in
#      standard mode and in embodied mode (distance and equipment enforced in the clinic), each required to finish,
#      complete every objective and score 100 %.
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
  for mode in standard embodied; do
    flags=()
    if [ "$mode" = embodied ]; then flags=(--embodied); fi
    # `|| true`: the exit code of an incomplete autopilot run is reported by the check below, with its reason
    { cc exec --case "$id" --autopilot ${flags[@]+"${flags[@]}"} --approval bypass --provider offline --output-format json --lang en || true; } \
      | python3 -c 'import json, sys
mode = sys.argv[1]
lines = [l for l in sys.stdin.read().strip().splitlines() if l.strip().startswith("{")]
if not lines:
    print("  demonstration (%s): no result" % mode); sys.exit(1)
r = json.loads(lines[-1])
score = r.get("assessment", {}).get("report", {}).get("score", {}).get("percent")
prog = r.get("progress", {})
done, total = prog.get("done"), prog.get("total")
print("  demonstration (%s): finished=%s completed=%s objectives=%s/%s score=%s%%" % (mode, r.get("finished"), r.get("completed"), done, total, score))
ok = r.get("finished") and r.get("completed") and done == total and score == 100
if not ok:
    print("    " + str(r.get("result")))
sys.exit(0 if ok else 1)' "$mode"
  done
done
echo "== all checks passed"
