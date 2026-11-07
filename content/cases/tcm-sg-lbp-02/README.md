# tcm-sg-lbp-02 — Recurrent low back pain · 52-year-old man · review B

## Case card

| | |
|---|---|
| Setting | Outpatient — a fictional Singapore community TCM clinic |
| Facility | `tcm-sg-clinic` |
| Family | `sg-lbp` (split **dev**): variant `review-b-escalation` of [`tcm-sg-lbp-01`](../tcm-sg-lbp-01/README.md) |
| Difficulty | ★★★ (3/5) |
| Estimated time | 45 minutes |
| Specialty | Traditional Chinese medicine, acupuncture, musculoskeletal |
| Languages | 简体中文 (source), English |
| Phases | Same first visit as `tcm-sg-lbp-01` → review one week later |
| Review status | **Unreviewed** — AI-assisted authoring against the cited guidance; not yet editorially reviewed or reviewed by a licensed clinician. Have a registered TCM physician and a doctor who manages back pain review it before teaching use. |
| Provenance | Synthetic |

## Learning outcomes

Outcomes 1–5 are those of `tcm-sg-lbp-01` (the shared first visit). Outcome 6:

6. At review, recognise new signs of suspected cauda equina syndrome, stop TCM treatment and arrange immediate emergency transfer with a complete written handover. The handover includes antiplatelet and analgesic medicines and their last doses.

## Clinical summary (spoilers)

**The first visit is identical to `tcm-sg-lbp-01`'s**: the same patient, history, examinations, records, prescription versions, dispensary query and acupuncture session. `tools/content-gen/lbp_family.py` builds it from the base case, and `tools/pack_check.py` checks that the shared facts agree across the family.

**Review B.** Two days before the review, Mr Tan lifted a carton at work and felt something "go".

- **Symptoms since then.** Pain down both legs, worse on the left, to the sole of the foot, now 8/10. Both feet are numb and his left foot drags. Since about 16:00 yesterday he has had numbness "like cotton wool" around the back passage when wiping. Since this morning he has had to strain to pass a thin stream. There is no incontinence; his bowels last opened yesterday morning.
- **Medicines.** Aspirin at 07:00 today, the granules this morning, and ibuprofen 400 mg last night, bought at a pharmacy.
- **Examination.**
  - Left ankle dorsiflexion and great-toe extension 4/5.
  - Left ankle reflex absent and right reduced.
  - Reduced light touch over the left foot and both soles, and over both inner buttocks.
  - Straight-leg raise 35° on the left and 50° on the right, with pain below the knee.
  - The clinic has no bladder scanner.
- **Assessment.** Suspected cauda equina syndrome, with symptoms of incomplete urinary dysfunction and no retention.
- **Right course.** Stop TCM treatment. Phone the Emergency Department and send him there now, by ambulance (995) because he can barely walk. Send a written handover with the symptoms and their times, the signs, his medicines with their last doses, and the herbs and acupuncture already given.

## Scenario timeline

| Phase | Opens | Where | What happens |
|---|---|---|---|
| `consult`, `treatment` | as in `tcm-sg-lbp-01` | consulting room, dispensary, treatment room | the shared first visit |
| `followup` — review one week later | automatically once the medicine was validly supplied, the needles validly withdrawn and counted, and the review booked | consulting room | what has changed; the danger signs again; neurological re-examination; the decision; stopping TCM; transfer; handover |

Static clock; no physiology model.

## Decisions and assessment

### Objective 6 — "One-week review: reassess and act on what has changed"

The objective completes when three things are done: `d-followup` answered correctly, a valid `refer-ed`, and a valid `handover-letter`.

### Decision `d-followup` (single)

It opens once the learner has asked how the week went and about the danger signs, and has repeated the neurological examination. The correct option is **suspected cauda equina syndrome: stop TCM, immediate transfer with a written handover**. The distractors, each with its own feedback, are:

- needle today and review in three days;
- a routine polyclinic MRI while continuing the herbs;
- a stronger blood-activating formula for "stasis";
- bed rest until he cannot pass urine at all.

### Actions specific to this variant

| Intervention | Rule |
|---|---|
| `refer-ed` | A checklist step. It is valid only once review evidence of the new signs exists (the status or danger-sign questions, or the neurological re-examination). At the first visit it is intercepted with the base case's teaching that nothing then needs emergency care. |
| `handover-letter` | A checklist step, valid only at the review. Its dose text lists what the handover must contain. |
| `stop-tcm` | A checklist step, valid only at the review. |
| `acu-review-session`, `continue-course`, `wait-and-see`, `herbs-stasis` | Always contraindicated: each delays emergency care. |
| `refer-imaging` | Neutral at the first visit. Contraindicated at the review, where a routine referral is too slow. |
| `tuina` | As in the base case, and also refused at the review. |

### Rubric (first visit as in `tcm-sg-lbp-01` without its review items; review items below)

| Item | Domain | Weight | Notes |
|---|---|---|---|
| `r-review-assessment` | history | 3 | danger signs, onset times, medicines and last doses; neurological re-examination and straight-leg raise |
| `r-recognise` | diagnosis | 3 | **critical**: `d-followup` first try |
| `r-transfer` | management | 3 | **critical**: a valid `refer-ed` |
| `r-handover` | management | 2 | a valid `handover-letter` |
| `r-stop-tcm` | safety | 2 | a valid `stop-tcm` |
| `r-no-delay` | safety | 3 | avoided-harm: none of the delaying acts; scored once the review opens or a delaying act is taken |
| `r-comm-escalation` | communication | 1 | examiner-judged |

There are 20 deterministic items in all, 46 points. That is more than the 8–15 the content standard suggests, because the case covers two visits; the lint only enforces the minimum.

### Safety gates

| Gate | Verdict | When |
|---|---|---|
| `g-delayed-emergency-care` | safety-critical (cap 40 %) | any delaying act, or a routine MRI referral at the review |
| `g-transfer-without-handover` | complication | a valid transfer without a valid handover |
| `tcm-sg-lbp-01`'s first-visit gates | as there | the shared first visit |

### Paths and their expected outcomes

These are checked by `python3 tools/pack_check.py --paths`, which fails when an outcome differs. The paths are in `tools/paths/tcm-sg-lbp-02.json`.

| Path | Score | Can finish | Critical missed | Gates |
|---|---|---|---|---|
| Reference path | 46/46 = 100 % | yes | — | — |
| Needles the leg pain before deciding | 40 % (capped) | yes | — | `g-delayed-emergency-care` |
| Routine MRI referral at the review, then transfer | 40 % (capped) | yes | — | `g-delayed-emergency-care` |
| Sends him home to wait for retention, then corrects | 40 % (capped) | yes | — | `g-delayed-emergency-care` |
| Reads it as a sciatica flare first | 93 % | yes | `r-recognise` | — |
| Transfers without a written handover | 96 % | **no** (objective open) | — | `g-transfer-without-handover` |
| Tries to send him to the ED at the first visit (intercepted) | 100 % | yes | — | — |
| Stops after booking the review | 72 % | no | `r-recognise`, `r-transfer` | — |
| Does nothing | 0 % | no | `r-redflags`, `r-rx-version`, `r-recognise`, `r-transfer` | — |

## Reference path (`solution`)

The first 69 steps are `tcm-sg-lbp-01`'s first visit. The review then runs:

1. Ask about status, danger signs, onset times, bowels, medicines and last doses, and adverse effects.
2. Re-examine: general appearance, neurological examination, straight-leg raise, lower abdomen and lower back.
3. `d-followup` (`transfer`).
4. `stop-tcm`, `refer-ed`, `handover-letter`, then `finish`.

There are 85 steps in all.

## Clinical numbers check

- **Pain.** 6/10 at the first visit; 8/10 at review, now radiating to both legs.
- **Times.** Saddle numbness from about 16:00 yesterday; difficulty passing urine from this morning. Aspirin 100 mg at 07:00 today; ibuprofen 2 × 200 mg = 400 mg last night.
- **Straight-leg raise.** 35° on the left, 50° on the right; both positive below the knee.

## Facilitator notes

### Debrief questions (PEARLS)

1. **Reactions.** What went through your mind when he mentioned the numbness "down there"?
2. **Description.** Which findings made this an emergency, and which were distractors (the tongue, the pulse)?
3. **Analysis.**
   - Why is "come back if you can't pass urine at all" the wrong safety net?
   - What does the Emergency Department need from you, and why do the aspirin and ibuprofen matter?
   - What would you have done if he had phoned instead of attending?
4. **Summary.** Write your own one-line rule for danger signs at a follow-up visit.

### Common learner errors

| Error | How the case surfaces it |
|---|---|
| Treating the new pain as a TCM pattern change (stasis) | `d-followup` feedback; `herbs-stasis` refused and gated |
| "Needle the sciatica, review in a few days" | `acu-review-session` refused and gated; the decision's feedback |
| A routine MRI referral | `refer-imaging` contraindicated at the review and gated |
| Transferring without a handover | The objective stays open; the complication gate; `r-handover` |
| Never re-asking the danger signs because they were negative last week | `d-followup` cannot open without them; `r-review-assessment` |

## Embodied mode

The first visit is as in `tcm-sg-lbp-01`. The review takes place in a consulting room (`location: {"roomKind": "consult"}`). The transfer is narrated: the patient leaves by ambulance, and nothing moves him to another facility. The handover requires `records`, available at the records terminal in every consulting room.

## Fidelity limits

- The bladder cannot be assessed in the clinic (no scanner), and a rectal examination is outside the clinic's scope; both are stated as being for the Emergency Department.
- What happens after transfer is unknown in this case. Facts after the handover are not simulated.
- The ambulance call is narrative: there is no transport or timing model.

## Matcher notes

- Review twins:
  - `h-fu-status` supersedes `h-presenting`, `h-severity` and `h-character`;
  - `h-fu-redflags` supersedes `h-redflag-neuro` and `h-redflag-ce`;
  - `h-fu-meds-last` supersedes `h-meds` and `h-antithrombotic` (at review, the current medicines with their last doses);
  - `h-fu-adverse` supersedes `h-bruising`.
- `h-fu-onset-time` is declared before `h-fu-redflags`, so "when did the numbness start?" reaches it first. Each such utterance lists `h-fu-redflags` in `alsoOk`.
- The base case's onset keyword `start` became `whendiditstart` / `howdiditstart` (tcm-sg-lbp-01 0.1.1). Otherwise "when did the numbness start?" selected the first-visit onset item.

## References

The references of `tcm-sg-lbp-01`, plus:

9. Getting It Right First Time (NHS England). National suspected cauda equina syndrome (CES) pathway. London: GIRFT; 2023.

### To verify

Everything listed for `tcm-sg-lbp-01`, and:

- the title, issuer and year of reference 9, and that teaching point 6 matches its wording. The point says "see" and does not quote it.

## Changelog

- **0.1.0 (2026-11-07).** First version: phase 2, case 2 (docs/PHASE2.md).

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

**病例概要。** 初诊与 `tcm-sg-lbp-01` 完全相同。复诊时，陈先生两天前上班搬货后出现：

- 双下肢放射痛（左重）；
- 足部麻木、左足无力；
- 昨天下午起鞍区麻木，今晨起排尿费力，无尿失禁。

查体：左踝背屈与拇背伸4级、左踝反射消失、鞍区感觉减退，直腿抬高左35°、右50°。

**学习目标（第6条）。** 复诊时识别疑似马尾综合征的新征象，停止中医治疗，立即转急诊并附完整书面交接。

**关键决策。**

- 疑似马尾综合征：今天停中医治疗，致电急诊并以救护车（995）转送，当天急诊MRI。
- 交接内容：症状及时间、体征、阿司匹林与布洛芬的最后剂量、已用中药与针灸。

**复盘要点。**

- 每次复诊都要重新筛查危险信号。
- 危险信号出现时，要决定的是照护转移，而不是证候。
- 不能等到完全尿潴留。
- 交接中的抗血小板药与止痛药信息直接影响后续手术。
