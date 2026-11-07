"""Case family `sg-lbp`: one first visit, several one-week reviews (docs/PHASE2.md, family.py).

`tcm-sg-lbp-01` (case_lbp.py) is the base. A variant keeps its first visit unchanged — the same patient, history,
examination, records, prescription and acupuncture session — removes the base's review, and adds its own.
"""

from __future__ import annotations

import case_lbp as base
from family import Family, upsert  # noqa: F401  (upsert re-exported for the variants)

FAMILY = Family(
    family="sg-lbp",
    split="dev",
    base_id=base.CASE_ID,
    history_prefix="h-fu-",
    exam_prefix="e-fu-",
    first_visit_end={"type": "intervene", "interventionId": "arrange-followup"},
    investigations=frozenset({"sachet-count"}),
    interventions=frozenset({"adherence-plan", "continue-course", "switch-damp-heat", "double-dose"}),
    decisions=frozenset({"d-followup"}),
    objectives=frozenset({"o-followup"}),
    rubric=frozenset({"r-followup", "r-comm-review"}),
)


def first_visit() -> dict:
    """The base case without its review: everything up to booking the review."""
    return FAMILY.first_visit(base.build())


def variant(**kwargs) -> dict:
    """Compose a family case: the shared first visit plus a review (family.Family.variant)."""
    return FAMILY.variant(base.build(), **kwargs)
