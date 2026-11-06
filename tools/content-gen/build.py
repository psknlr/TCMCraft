#!/usr/bin/env python3
"""Write the TCMCraft content pack (`content/`) from its sources in this folder.

    python3 tools/content-gen/build.py           # rewrite content/
    python3 tools/content-gen/build.py --check   # exit 1 if content/ is out of date

The output is deterministic (sorted nothing, insertion order kept, 2-space JSON), so a second run is a no-op.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import case_lbp  # noqa: E402
import clinic  # noqa: E402
from common import CONTENT, write  # noqa: E402


def main() -> int:
    check = "--check" in sys.argv[1:]
    ok = True
    ok &= write(CONTENT / "cases" / case_lbp.CASE_ID / "case.json", case_lbp.build(), check)
    ok &= write(CONTENT / "catalogs" / f"{clinic.CATALOG_ID}.json", clinic.catalog(), check)
    for template in clinic.templates():
        ok &= write(CONTENT / "templates" / f"{template['id']}.json", template, check)
    ok &= write(CONTENT / "facilities" / f"{clinic.FACILITY_ID}.json", clinic.facility(), check)
    if check:
        print("content/ is up to date" if ok else "content/ is out of date: run python3 tools/content-gen/build.py")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
