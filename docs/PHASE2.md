# Phase 2 — the 12-case prototype

DESIGN §10, phase 2: "Add uncertain evidence, review disagreements, execution discrepancies and alternative
follow-up branches."

**Acceptance criterion:** each case has reviewed rules, reference trajectories and defined failure conditions.

This page is the plan and the running status. The cases follow the same content standard as phase 1
(ClinicalCraft CASE_AUTHORING §9) and the same checks (`tools/check.sh`, CI against the pinned engine).

## What "done" means for one case

| Criterion | How it is shown |
|---|---|
| **Reference trajectory** | `solution` replays to every objective and decision; `cases verify` passes at 100 % on the pinned engine (CI) |
| **Defined failure conditions** | `tools/paths/<id>.json` lists the wrong and alternative paths with their **expected outcome** (score bounds, safety gates, critical items missed, whether the case can finish). `pack_check.py --paths` fails when a path's outcome differs from what is written, so failure conditions are tested rather than described. |
| **Reviewed rules** | `provenance.review.status` raised from `unreviewed` only after a review that really happened. An `editorial` review against the cited guidance can be done here; `clinician-reviewed` needs a registered TCM physician and, where the case touches conventional care, a doctor of that specialty. Until then the case says so, and its README lists what is "to verify". |
| **Family and split** | `extensions.tcmcraft.caseFamily`, `variant` and `split`. Every case of a family is in one split (DESIGN §7, §9.2). `pack_check.py` checks that cases of one family agree on the split and on every shared first-visit item. |

## The twelve cases

Case families keep variants of one underlying patient together. **dev** cases are for building and tuning;
**test** cases are held out for the phase 4 comparisons and are adapted from real reports.

| # | Case | Family · split | Phase 2 dimension | Source | Status |
|---:|---|---|---|---|---|
| 1 | `tcm-sg-lbp-01` — recurrent LBP; review A: partial response from missed doses and continuing exposure | `sg-lbp` · dev | Uncertain evidence (stained kiosk photo); execution (dispensary query, versions); follow-up branch A | Synthetic | **Done** (phase 1) |
| 2 | `tcm-sg-lbp-02` — same first visit; review B: new bilateral sciatica, saddle numbness, urinary hesitancy | `sg-lbp` · dev | **Alternative follow-up branch: escalation** (suspected cauda equina syndrome → stop TCM, immediate transfer, handover) | Synthetic | **Built** |
| 3 | `tcm-sg-lbp-03` — same first visit; review C: took everything exactly as labelled, the label was wrong | `sg-lbp` · dev | **Execution discrepancy** (label ≠ prescription version 2) → incident, relabel, open disclosure, no blame | Synthetic | **Built** |
| 4 | `tcm-sg-lbp-04` — same first visit; review D: the pattern has transformed (heat), with a genuine yellow coating | `sg-lbp` · dev | Follow-up branch: **changed condition** → assessment revised and a new prescription version | Synthetic | **Built** (this round) |
| 5 | `tcm-sg-insomnia-01` — chronic insomnia; the senior physician disagrees with the learner's pattern | `sg-insomnia` · dev | **Review disagreement** (resolved by evidence, recorded, not by seniority) | Synthetic | **Built** (this round) |
| 6 | `tcm-sg-insomnia-02` — same patient; sleep diary and a wearable's data disagree; a hypnotic in use | `sg-insomnia` · dev | **Uncertain evidence** (conflicting sources); herb–drug review | Synthetic | Planned |
| 7 | `tcm-sg-gi-01` — epigastric fullness; the dispensary objects to a liquorice dose in a patient on a diuretic | `sg-gi` · dev | **Review disagreement** (dispensary objection the prescriber must answer); execution | Synthetic | Planned |
| 8 | `cmcr-1599800` — refractory low back and leg pain | `cmcr-1599800` · test | MSK pathway on a real course | CMCR adaptation | Planned |
| 9 | `cmcr-1571923` — low back pain first labelled disc herniation, later brucellosis | `cmcr-1571923` · test | Uncertain evidence + escalation (a biomedical cause behind the presentation) | CMCR adaptation | Planned |
| 10 | `cmcr-1477723` — epigastric fullness, spleen–stomach deficiency-cold, TCM nursing techniques | `cmcr-1477723` · test | Execution of external techniques; GI generalisation | CMCR adaptation | Planned |
| 11 | `cmcr-1666233` — shoulder-hand syndrome after stroke; herbs, acupuncture and TMS | `cmcr-1666233` · test | AcuCraft planning; coordination with rehabilitation | CMCR adaptation | Planned |
| 12 | `cmcr-1526660` — integrative care after PCI | `cmcr-1526660` · test | Review disagreement with cardiology; antiplatelet–herb interactions | CMCR adaptation | Planned |

### Coverage

| Dimension | Cases |
|---|---|
| Uncertain evidence | 1, 6, 9 |
| Review disagreements | 5, 7, 12 |
| Execution discrepancies | 1, 3, 7, 10 |
| Alternative follow-up branches | 1 → 2, 3, 4 (one first visit, four reviews) |
| Generalisation beyond MSK pain (DESIGN §9.2) | insomnia 5, 6; GI 7, 10; stroke rehabilitation 11; cardiovascular 12 |

## How a family is built

`tools/content-gen/lbp_family.py` takes the first visit of `tcm-sg-lbp-01` unchanged, removes its review, and
adds a variant's review (history, examination, records, decisions, interventions, objective, rubric, gates,
reference path and matcher corpus). The first visit is therefore identical across the family by construction.
`pack_check.py` also compares shared items across the family's cases: a case's last phase is its review, and
everything before it must be identical across the family.

`sg-insomnia` starts with its base case, `tcm-sg-insomnia-01` (`tools/content-gen/case_insomnia.py`), written as a
whole patient. Case 6 will be its first variant. The `sg-lbp` builder is specific to that family's first visit, so
case 6 needs its own family module or a generalised one.

## How the review disagreement is modelled (case 5)

The engine has no notion of a colleague's opinion, so case 5 builds the disagreement from parts it has:

- **The senior's view** is a record (`senior-note`), dated before the consultation, that states what it rests on:
  the intake questionnaire only.
- **The learner's own view comes first.** `d-disagreement` and the `case-discussion` step open only once the note
  has been read and `d-pattern` decided.
- **Discuss before acting.** The critical item `r-disagreement` needs the correct option first time and the
  discussion before the prescription (`inOrder`).
- **Deference and false compromise are refused.** Adopting the senior's formula unexamined, or combining both
  formulas, is always contraindicated: it is refused with the evidence and recorded as a complication gate.
- **Both views are kept.** `extensions.tcmcraft.disagreement` holds both views, their basis and the resolution.
  The engine does not read it yet.
- **The quality of the conversation** is judged only by the examiner item `r-comm-colleague`.

## Real-report adaptations (cases 8–12)

These follow ClinicalCraft's CMCR conventions (its docs/CMCR_CASES.md):

- the report is paraphrased;
- pseudonyms and relative time are used;
- unrecorded facts stay unknown;
- contradictions in the report are kept and labelled;
- the source is shown only once the case is complete.

Before any of them is built:

1. Confirm the permission basis for using, and for keeping in this repository, the PDFs in `CMCR中医案例80篇/`
   (docs/CMCR_CORPUS.md).
2. Take each report's DOI from the article itself: the archive manifests carry one DOI for all 80 rows.
3. Check every page and figure for identifying details, as ClinicalCraft did for its 20.

## Engine work that would sharpen phase 2

From docs/ENGINE_EXTENSIONS.md, in the order phase 2 feels it:

1. Prescriptions as versioned objects (cases 3, 7, 12).
2. Evidence provenance (cases 6, 9).
3. Episodes with simulated time (all follow-up branches).

Phase 2 does not wait for them; each case notes the workaround it uses.
