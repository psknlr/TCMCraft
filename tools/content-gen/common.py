"""Shared helpers for the TCMCraft content generator.

Every learner-facing string is bilingual (zh-CN first, the source language, then en), as
ClinicalCraft requires (docs/CASE_AUTHORING.md §1.4). The generator writes plain JSON that
ClinicalCraft loads through `contentDirs`; the JSON in `content/` is the artifact, these
modules are its source.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / "content"


def L(zh: str, en: str) -> dict[str, str]:
    """A LocalizedText: Simplified Chinese first, then British English."""
    return {"zh-CN": zh, "en": en}


def KW(zh: list[str], en: list[str]) -> dict[str, list[str]]:
    """A LocalizedList (keywords, aliases)."""
    return {"zh-CN": zh, "en": en}


def dump(data: Any) -> str:
    """Deterministic JSON text (2-space indent, UTF-8, trailing newline)."""
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def write(path: Path, data: Any, check: bool) -> bool:
    """Write `data` to `path`; with `check`, only report whether the file is up to date."""
    text = dump(data)
    if check:
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current != text:
            print(f"out of date: {path.relative_to(ROOT)}")
            return False
        return True
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(f"wrote {path.relative_to(ROOT)}")
    return True


# The date of this revision of the pack's content (docs/AUDIT_2026-11-12.md).
LAST_REVISED = "2026-11-12"


def dates(authored: str) -> dict:
    """Content creation, technical verification and clinical sign-off, kept apart (`extensions.tcmcraft.dates`).

    `provenance.review.reviewedAt` is reserved for a review that really happened, so an unreviewed case has none.
    """
    return {
        "authored": authored,
        "lastRevised": LAST_REVISED,
        "technicalVerification": "every commit: tools/check.sh against the pinned ClinicalCraft (tools/clinicalcraft.rev), in CI",
        "clinicalSignOff": None,
    }
