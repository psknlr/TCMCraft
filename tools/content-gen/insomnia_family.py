"""Case family `sg-insomnia`: one first visit, several two-week reviews (docs/PHASE2.md, family.py).

`tcm-sg-insomnia-01` (case_insomnia.py) is the base. A variant keeps its first visit unchanged — the same patient,
screen, four examinations, the senior's note and its resolution, and the plan — removes the base's review, and adds
its own.
"""

from __future__ import annotations

import case_insomnia as base
from family import Family

FAMILY = Family(
    family="sg-insomnia",
    split="dev",
    base_id=base.CASE_ID,
    history_prefix="h-rv-",
    exam_prefix="e-rv-",
    first_visit_end={"type": "intervene", "interventionId": "arrange-review"},
    investigations=frozenset({"gp-results", "sleep-diary-review"}),
    interventions=frozenset({"iron-spacing", "continue-plan", "stop-iron"}),
    decisions=frozenset({"d-review"}),
    objectives=frozenset({"o-review"}),
    rubric=frozenset({"r-review", "r-no-stop-iron"}),
    gates=frozenset({"g-stop-iron"}),
)


def first_visit() -> dict:
    """The base case without its review: everything up to booking the review."""
    return FAMILY.first_visit(base.build())


def variant(**kwargs) -> dict:
    """Compose a family case: the shared first visit plus a review (family.Family.variant)."""
    return FAMILY.variant(base.build(), **kwargs)
