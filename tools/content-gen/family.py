"""Case families: one first visit, several reviews (docs/PHASE2.md).

A family's base case is a whole episode. A variant keeps the base's first visit unchanged — the same patient,
history, examination, records and plan — removes the base's review, and adds its own. A variant may also replace a
first-visit item whose wording or appropriateness would be wrong in its review (it lists those replacements
explicitly).

Variants of one family stay in one split (DESIGN §7, §9.2); `tools/pack_check.py` checks that the cases of a family
agree on the split and on every shared first-visit history item, examination finding and record.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Family:
    """What belongs to a base case's review, so that a variant can remove it."""

    family: str
    split: str
    base_id: str
    history_prefix: str  # review history items (and the corpus utterances that expect them)
    exam_prefix: str
    first_visit_end: dict  # the solution step that books the review
    investigations: frozenset = field(default_factory=frozenset)
    interventions: frozenset = field(default_factory=frozenset)
    decisions: frozenset = field(default_factory=frozenset)
    objectives: frozenset = field(default_factory=frozenset)
    rubric: frozenset = field(default_factory=frozenset)
    gates: frozenset = field(default_factory=frozenset)

    def first_visit(self, base_case: dict) -> dict:
        """The base case without its review: everything up to booking the review."""
        c = copy.deepcopy(base_case)
        c["history"] = [h for h in c["history"] if not h["id"].startswith(self.history_prefix)]
        c["exam"] = [e for e in c["exam"] if not e["id"].startswith(self.exam_prefix)]
        c["investigations"] = [i for i in c["investigations"] if i["id"] not in self.investigations]
        c["interventions"] = [i for i in c["interventions"] if i["id"] not in self.interventions]
        c["decisions"] = [d for d in c["decisions"] if d["id"] not in self.decisions]
        c["objectives"] = [o for o in c["objectives"] if o["id"] not in self.objectives]
        c["rubric"] = [r for r in c["rubric"] if r["id"] not in self.rubric]
        c["safetyGates"] = [g for g in c["safetyGates"] if g["id"] not in self.gates]
        end = c["solution"].index(self.first_visit_end)
        c["solution"] = c["solution"][: end + 1]
        ext = c["extensions"]
        ext["testUtterances"] = [u for u in ext["testUtterances"] if not any(x.startswith(self.history_prefix) for x in u["expect"])]
        return c

    def variant(self, base_case: dict, *, case_id: str, version: str, variant_id: str, title, outcome, review: dict, debrief: dict,
                tcmcraft: dict) -> dict:
        """Compose a family case: the shared first visit plus `review`.

        `review` keys (all optional): history, exam, investigations, interventions, decisions, objectives, rubric,
        safetyGates, unknowns — upserted by id — and `solution` (the steps after booking the review, `finish` last) and
        `utterances` (the review's matcher corpus). `outcome` replaces the base's review learning outcome; `debrief`
        replaces debrief keys; `tcmcraft` replaces keys of `extensions.tcmcraft`.
        """
        c = self.first_visit(base_case)
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
        c["extensions"]["tcmcraft"] = {**c["extensions"]["tcmcraft"], "caseFamily": self.family, "variant": variant_id,
                                       "split": self.split, "variantOf": self.base_id, **tcmcraft}
        return c


def upsert(items: list[dict], new: list[dict]) -> list[dict]:
    """Replace items by id, append the others (order: existing first, then new ones)."""
    by_id = {x["id"]: x for x in new}
    out = [by_id.pop(x["id"], x) for x in items]
    return out + [x for x in new if x["id"] in by_id]
