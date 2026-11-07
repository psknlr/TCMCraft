# tcm-sg-lbp-03 — Recurrent low back pain · 52-year-old man · review C

## Case card

| | |
|---|---|
| Setting | Outpatient — a fictional Singapore community TCM clinic |
| Facility | `tcm-sg-clinic` |
| Family | `sg-lbp` (split **dev**): variant `review-c-execution-discrepancy` of [`tcm-sg-lbp-01`](../tcm-sg-lbp-01/README.md) |
| Difficulty | ★★★ (3/5) |
| Estimated time | 45 minutes |
| Specialty | Traditional Chinese medicine, acupuncture, musculoskeletal |
| Languages | 简体中文 (source), English |
| Phases | Same first visit as `tcm-sg-lbp-01` → review one week later |
| Review status | **Unreviewed** — AI-assisted authoring against the cited guidance; not yet editorially reviewed or reviewed by a licensed clinician. Have a registered TCM physician review it before teaching use. |
| Provenance | Synthetic |

## Learning outcomes

Outcomes 1–5 are those of `tcm-sg-lbp-01` (the shared first visit). Outcome 6:

6. At review, compare the prescription, the dispensing record and label, and what the patient actually took. Recognise a labelling error as a system problem, report it without blame, correct it and disclose it to the patient, without changing a sound assessment.

## Clinical summary (spoilers)

**The first visit is identical to `tcm-sg-lbp-01`'s** (built from it by `tools/content-gen/lbp_family.py`).

**Review C.** Mr Tan is a little better, at 5/10 with shorter morning stiffness. He did everything he was told in writing:

- one sachet every morning after breakfast, never missed;
- the stretches morning and evening;
- sitting breaks and a jacket in the control room.

The cause of the limited response is in the records.

- **Prescription version 2:** 1 sachet **twice** daily after meals, for 7 days (14 sachets).
- **Label as printed** (dispensing record and the bag he brought): 1 sachet **once** daily, 14 sachets.
- **Sachet count:** 7 of 14 left; one every morning for 7 days, as the label says.
- **Counselling at supply:** recorded as "as per label". He remembers a mention of the evening, but trusted the print.

His symptoms, tongue and pulse are as at the first visit, with no danger signs and no adverse effects beyond the fading bruise. This is an **execution discrepancy**: he received half the intended dose. The right course:

- report it as a no-blame dispensing incident (the dispensary finds a label template that defaulted to once daily, and adds a second-person label check before supply);
- have the label corrected and explain to him with an apology (open disclosure);
- continue the course at the prescribed dose;
- keep the assessment.

## Scenario timeline

| Phase | Opens | Where | What happens |
|---|---|---|---|
| `consult`, `treatment` | as in `tcm-sg-lbp-01` | consulting room, dispensary, treatment room | the shared first visit |
| `followup` — review one week later | as in `tcm-sg-lbp-01` | consulting room | status; how exactly he took the granules; the dispensing record, the bag's label and the sachet count; the decision; incident report, relabelling, continuation |

## Decisions and assessment

### Objective 6 — "One-week review: check what was actually done and revise the plan"

The objective completes when four things are done: `d-followup` answered correctly, a valid `relabel-explain`, a valid `incident-report`, and `continue-course`.

### Decision `d-followup` (single)

It opens once the learner has done four things:

- asked exactly how he took the granules;
- re-checked the danger signs;
- repeated the neurological examination;
- compared the dispensing record with the bag's label or the sachet count.

The correct option is the **execution discrepancy, with incident report, correction, disclosure and continuation**. The distractors are:

- adherence counselling;
- changing the formula;
- two sachets at once;
- stopping the herbs.

### Actions specific to this variant

| Intervention | Rule |
|---|---|
| `incident-report`, `relabel-explain` | Checklist steps, valid only once the records have been compared (`COMPARED`: the dispensing record read, and the bag or the sachet count read) |
| `adherence-counsel` | Neutral, but its response shows the misattribution ("But the label says once a day…"); scored by `r-no-blame` |
| `switch-damp-heat`, `double-dose` | Always contraindicated, with harm texts specific to this branch |
| `continue-course` | As in the base case |

### Rubric (first visit as in `tcm-sg-lbp-01` without its review items; review items below)

| Item | Domain | Weight | Notes |
|---|---|---|---|
| `r-execution-check` | investigations | 3 | asked how he took them; compared the records |
| `r-followup` | management | 3 | `d-followup` first try, no formula change, no doubling; scored once the review opens |
| `r-relabel` | safety | 3 | **critical**: a valid `relabel-explain` |
| `r-incident` | safety | 2 | a valid `incident-report` |
| `r-no-blame` | management | 1 | avoided-harm: no `adherence-counsel` |
| `r-comm-disclosure` | communication | 1 | examiner-judged: open disclosure |

There are 19 deterministic items in all, 42 points.

### Safety gates

| Gate | Verdict | When |
|---|---|---|
| `g-label-left-wrong` | complication | the course continued without a valid relabel |
| `tcm-sg-lbp-01`'s first-visit gates | as there | the shared first visit |

### Paths and their expected outcomes

These are checked by `python3 tools/pack_check.py --paths`. The paths are in `tools/paths/tcm-sg-lbp-03.json`.

| Path | Score | Can finish | Critical missed | Gates |
|---|---|---|---|---|
| Reference path | 42/42 = 100 % | yes | — | — |
| Reads it as missed doses and counsels him first | 90 % | yes | — | — |
| Switches to a damp-heat formula | 93 % | yes | — | — |
| Two sachets at once each morning | 93 % | yes | — | — |
| Continues without correcting the label | 93 % | **no** | `r-relabel` | `g-label-left-wrong` |
| Corrects the label but never reports it | 95 % | **no** | — | — |
| Tries to relabel before comparing the records (intercepted) | 100 % | yes | — | — |
| Stops after booking the review | 74 % | no | `r-relabel` | — |
| Does nothing | 0 % | no | `r-redflags`, `r-rx-version`, `r-relabel` | — |

## Reference path (`solution`)

The first 69 steps are `tcm-sg-lbp-01`'s first visit. The review then runs:

1. Seven history items, including `h-fu-how-taken`.
2. Five examinations.
3. Read the dispensing record, the medicine bag, the sachet count and the session record.
4. `d-followup` (`label-error`).
5. `incident-report`, `relabel-explain`, `continue-course`, then `finish`.

There are 94 steps in all.

## Clinical numbers check

- **Pain.** 6/10 at the first visit, 5/10 at review.
- **Sachets.** Prescribed 2 a day × 7 days = 14. Label: 1 a day. Taken: 7, one each morning. Left: 7.

## Facilitator notes

### Debrief questions (PEARLS)

1. **Reactions.** When he said "I did everything you said", what did you expect to find?
2. **Description.** Which three documents did you compare, and what did each say?
3. **Analysis.**
   - Why is reporting the incident not "blaming the dispenser"?
   - What would have happened next week without the correction?
   - How does a verbal "twice a day" lose to a printed "once daily"?
4. **Summary.** Which question at review would have found this fastest?

### Common learner errors

| Error | How the case surfaces it |
|---|---|
| "He forgot the evening dose" | `d-followup` feedback; `adherence-counsel`'s response; `r-no-blame` |
| Relabelling the pattern because the response is limited | `switch-damp-heat` refused; `r-followup` |
| Doubling the morning dose | `double-dose` refused; `r-followup` |
| Fixing the label quietly without telling him or reporting it | the review objective stays open; `r-incident`; the examiner-judged disclosure item |

## Embodied mode

As in `tcm-sg-lbp-01`. The bag check (`medicine-bag`) and the sachet count are bedside studies at the patient's side. The dispensing record is read at a records terminal.

## Fidelity limits

- The label is a record's text, not an object. The engine cannot yet compare a supplied item with the prescription version line by line (docs/ENGINE_EXTENSIONS.md §2).
- The dispensary's root-cause finding and its fix are narrated in the incident report's response.

## Matcher notes

- `h-fu-how-taken` is declared before `h-fu-adherence`, so "how many sachets a day?" reaches it first.
- Review twins are as in `tcm-sg-lbp-01`, plus `h-fu-adverse` superseding `h-bruising`.

## References

The references of `tcm-sg-lbp-01`, plus:

9. World Health Organization. Medication without harm: WHO global patient safety challenge on medication safety. Geneva: WHO; 2017.

### To verify

Everything listed for `tcm-sg-lbp-01`, and:

- the title and year of reference 9. Teaching point 6 refers to it with "see" and does not quote it.
- how open disclosure and incident reporting are framed for TCM clinics in Singapore.

## Changelog

- **0.1.0 (2026-11-07).** First version: phase 2, case 3 (docs/PHASE2.md).

## Validation

```bash
python3 tools/content-gen/build.py --check
```

```bash
python3 tools/pack_check.py --paths
```

```bash
tools/check.sh ../ClinicalCraft
```

## 中文摘要

**病例概要。** 初诊与 `tcm-sg-lbp-01` 相同。复诊时，陈先生完全照药袋标签每天早上吃一包，也坚持了伸展、起身活动和穿外套，但只好了一点（5分）。对照记录发现：

- 第2版处方是每日2次；
- 标签印的是每日1次；
- 剩余7包。

他只服了一半剂量。

**学习目标（第6条）。** 把处方、调剂记录与标签、实际服药三者对照，识别标签差错这一系统问题，按无责原则上报、更正并开放披露，不改变站得住脚的评估。

**关键决策。** 这是执行差错，不是依从性问题，也不是辨证错误。

- 上报调剂差错；
- 更正标签；
- 向患者说明并致歉；
- 按处方剂量继续疗程。

**复盘要点。**

- 归因于患者或证候之前，先核对“开了什么、发了什么、写了什么、吃了什么”。
- 印在纸上的用法往往胜过口头交代。
- 上报是为了修正系统，开放披露是对患者的责任。
