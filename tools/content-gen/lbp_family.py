"""Case family `sg-lbp`: one first visit, several one-week reviews (docs/PHASE2.md).

`tcm-sg-lbp-01` (case_lbp.py) is the base. A variant keeps its first visit unchanged — the same patient, history,
examination, records, prescription and acupuncture session — removes the base's review, and adds its own. Only
the actions that are appropriate at the review differ, so a variant may also replace a first-visit intervention
whose wording or appropriateness would be wrong in its review (a variant lists those replacements explicitly).

Variants of one family stay in one split (DESIGN §7, §9.2); `tools/pack_check.py` checks that the cases of a
family agree on the split and on every shared first-visit history item, examination finding and record.
"""

from __future__ import annotations

import copy

import case_lbp as base

FAMILY = "sg-lbp"
SPLIT = "dev"

# What belongs to the base case's review (removed from a variant before its own review is added).
REVIEW_INVESTIGATIONS = {"sachet-count"}
REVIEW_INTERVENTIONS = {"adherence-plan", "continue-course", "switch-damp-heat", "double-dose"}
REVIEW_DECISIONS = {"d-followup"}
REVIEW_OBJECTIVES = {"o-followup"}
REVIEW_RUBRIC = {"r-followup", "r-comm-review"}
FIRST_VISIT_END = {"type": "intervene", "interventionId": "arrange-followup"}


def is_review_history(item: dict) -> bool:
    return item["id"].startswith("h-fu-")


def is_review_exam(item: dict) -> bool:
    return item["id"].startswith("e-fu-")


def first_visit() -> dict:
    """The base case without its review: everything up to booking the review."""
    c = copy.deepcopy(base.build())
    c["history"] = [h for h in c["history"] if not is_review_history(h)]
    c["exam"] = [e for e in c["exam"] if not is_review_exam(e)]
    c["investigations"] = [i for i in c["investigations"] if i["id"] not in REVIEW_INVESTIGATIONS]
    c["interventions"] = [i for i in c["interventions"] if i["id"] not in REVIEW_INTERVENTIONS]
    c["decisions"] = [d for d in c["decisions"] if d["id"] not in REVIEW_DECISIONS]
    c["objectives"] = [o for o in c["objectives"] if o["id"] not in REVIEW_OBJECTIVES]
    c["rubric"] = [r for r in c["rubric"] if r["id"] not in REVIEW_RUBRIC]
    end = c["solution"].index(FIRST_VISIT_END)
    c["solution"] = c["solution"][: end + 1]
    ext = c["extensions"]
    ext["testUtterances"] = [u for u in ext["testUtterances"] if not any(x.startswith("h-fu-") for x in u["expect"])]
    return c


def upsert(items: list[dict], new: list[dict]) -> list[dict]:
    """Replace items by id, append the others (order: existing first, then new ones)."""
    by_id = {x["id"]: x for x in new}
    out = [by_id.pop(x["id"], x) for x in items]
    return out + [x for x in new if x["id"] in by_id]


def variant(*, case_id: str, version: str, variant_id: str, title, outcome, review: dict, debrief: dict, tcmcraft: dict) -> dict:
    """Compose a family case: the shared first visit plus `review`.

    `review` keys (all optional): history, exam, investigations, interventions, decisions, objectives, rubric,
    safetyGates, unknowns — upserted by id — and `solution` (the steps after booking the review, `finish` last) and
    `utterances` (the review's matcher corpus). `outcome` replaces the base's review learning outcome; `debrief`
    replaces debrief keys; `tcmcraft` replaces keys of `extensions.tcmcraft`.
    """
    c = first_visit()
    c["id"] = case_id
    c["version"] = version
    c["title"] = title
    c["learningOutcomes"] = c["learningOutcomes"][:-1] + [outcome]
    for key in ("history", "exam", "investigations", "interventions", "decisions", "objectives", "rubric", "safetyGates", "unknowns"):
        if key in review:
            c[key] = upsert(c[key], review[key]) if key != "unknowns" else c[key] + review[key]
    c["solution"] = c["solution"] + review.get("solution", [{"type": "finish"}])
    c["extensions"]["testUtterances"] = c["extensions"]["testUtterances"] + review.get("utterances", [])
    c["debrief"] = {**c["debrief"], **debrief}
    known = {i["id"] for i in c["investigations"]}
    for npc in c["npcs"]:
        npc["interprets"] = [x for x in npc["interprets"] if x in known]
    c["extensions"]["tcmcraft"] = {**c["extensions"]["tcmcraft"], "caseFamily": FAMILY, "variant": variant_id, "split": SPLIT,
                                   "variantOf": base.CASE_ID, **tcmcraft}
    return c
