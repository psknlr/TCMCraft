# tcm-sg-lbp-04 — Recurrent low back pain · 52-year-old man · review D

## Case card

| | |
|---|---|
| Setting | Outpatient — a fictional Singapore community TCM clinic |
| Facility | `tcm-sg-clinic` |
| Family | `sg-lbp` (split **dev**): variant `review-d-changed-pattern` of [`tcm-sg-lbp-01`](../tcm-sg-lbp-01/README.md) |
| Difficulty | ★★★★ (4/5 in practice; the shared first visit is rated 3) |
| Estimated time | 45 minutes |
| Specialty | Traditional Chinese medicine, acupuncture, musculoskeletal |
| Languages | 简体中文 (source), English |
| Phases | Same first visit as `tcm-sg-lbp-01` → review one week later |
| Review status | **Unreviewed** — AI-assisted authoring against the cited guidance; not yet editorially reviewed or reviewed by a licensed clinician. Have a registered TCM physician review it before teaching use. |
| Provenance | Synthetic |

## Learning outcomes

Outcomes 1–5 are those of `tcm-sg-lbp-01` (the shared first visit). Outcome 6:

6. At review, recognise from consistent, good-quality evidence that the pattern has changed (cold-damp turning to damp-heat). Exclude infection and other danger signs, stop what is adding heat, and issue a new prescription version.

## Clinical summary (spoilers)

**The first visit is identical to `tcm-sg-lbp-01`'s** (built from it by `tools/content-gen/lbp_family.py`).

**Review D.** Over the week, Mr Tan:

- took every sachet of the warming formula (version 2);
- wore a heat patch all day, every day;
- took very hot showers;
- ate durian twice, and had beer and fried food at a wedding, in hot weather.

**Now.**

- **Symptoms.** A hot, heavy, distending pain, worse in the heat and in the afternoon, better with a cool rinse (5/10). He feels the heat and wakes with a bitter, sticky mouth, thirsty but unable to drink much. His urine is darker and scantier, without pain, and his stools are sticky.
- **Tongue.** He had only porridge and water before coming. Rinsed and seen in daylight, and under the standard light, the edges are red, with a thin **yellow** greasy coating at the root that **stays yellow**.
- **Pulse.** Slippery and slightly rapid (86/min).
- **Danger signs excluded.** Temperature 36.8 °C; no chills, sweats, weight loss or urinary pain; renal angles painless; neurological examination normal.
- **Skin.** Two faint red patches where the heat patches sat, without blisters.

**Assessment.** Cold-damp has turned to damp-heat. The plan changes:

- stop the heat patches and the very hot showers;
- diet advice: no durian or alcohol for now, less fried food;
- **prescription version 3**: modified 四妙丸, clearing heat and draining damp, with version 2 cancelled;
- supply version 3 and review in a week.

**The evidence-quality inversion.** At the first visit, the disciplined learner set aside a yellow coating because it was stained and badly lit. Here the same discipline accepts one: he rinsed, had no coffee, the coating stays yellow in daylight and under standard light, and it agrees with everything else.

## Scenario timeline

| Phase | Opens | Where | What happens |
|---|---|---|---|
| `consult`, `treatment` | as in `tcm-sg-lbp-01` | consulting room, dispensary, treatment room | the shared first visit |
| `followup` — review one week later | as in `tcm-sg-lbp-01` | consulting room | the four examinations again; temperature, renal angles, the skin; the decision; stop heat, diet, version 3, supply |

## Decisions and assessment

### Objective 6 — "One-week review: re-differentiate the pattern and revise the plan"

The objective completes when four things are done: `d-followup` answered correctly, a valid `dispense-v3`, a valid `stop-heat`, and a valid `diet-advice`.

### Decision `d-followup` (single)

It opens once the learner has asked about the week, heat and cold, and fever and urinary symptoms; taken his temperature; and re-examined the pulse and the tongue (directly or by standard capture). The correct option is **cold-damp turned to damp-heat; danger signs absent; revise**. The distractors are:

- "staining again";
- spinal infection;
- adding aconite;
- "herbs take time".

### Actions specific to this variant

| Intervention | Rule |
|---|---|
| `rx-v3-damp-heat` | A checklist step, valid only at the review. At the first visit it is intercepted (`g-revision-intercepted`, complication). |
| `dispense-v3` | A checklist step, valid only after a valid version 3 |
| `stop-heat`, `diet-advice` | Checklist steps, valid only at the review |
| `continue-course` | Contraindicated: the warming formula keeps adding heat |
| `add-fuzi` | Contraindicated; safety-critical gate |
| `tongue-recapture` | The first visit's standard capture, with a result for the review too |

Phase twins at the review:

- `h-fu-heat` supersedes `h-coldheat` and `h-appetite`;
- `h-fu-urine-stool` supersedes `h-urine-stool`;
- `h-fu-fever` supersedes `h-redflag-systemic`;
- `h-fu-diet` supersedes `h-food-before`;
- `h-fu-status` supersedes `h-presenting`, `h-severity` and `h-character`;
- `h-fu-redflags` supersedes `h-redflag-neuro` and `h-redflag-ce`;
- `h-fu-adverse` supersedes `h-bruising`.

### Rubric (first visit as in `tcm-sg-lbp-01` without its review items; review items below)

| Item | Domain | Weight | Notes |
|---|---|---|---|
| `r-review-inquiry` | history | 3 | heat and cold, taste, urine and stools, fever and urinary symptoms, diet, heat patches |
| `r-review-exam` | examination | 2 | temperature, pulse, tongue, skin, renal angles |
| `r-revise` | diagnosis | 3 | **critical**: `d-followup` first try |
| `r-new-version` | safety | 3 | a valid `dispense-v3` (only the current version supplied) |
| `r-stop-heat` | safety | 2 | a valid `stop-heat` |
| `r-diet` | management | 1 | a valid `diet-advice` |
| `r-no-more-warming` | safety | 2 | avoided-harm: no `continue-course`, no `add-fuzi` |
| `r-comm-change` | communication | 1 | examiner-judged |

There are 21 deterministic items in all, 46 points.

### Safety gates

| Gate | Verdict | When |
|---|---|---|
| `g-aconite-into-heat` | safety-critical (cap 40 %) | `add-fuzi` |
| `g-revision-intercepted` | complication | an invalid `rx-v3-damp-heat` attempt (at the first visit) |
| `tcm-sg-lbp-01`'s first-visit gates | as there | the shared first visit |

### Paths and their expected outcomes

These are checked by `python3 tools/pack_check.py --paths`. The paths are in `tools/paths/tcm-sg-lbp-04.json`.

| Path | Score | Can finish | Critical missed | Gates |
|---|---|---|---|---|
| Reference path | 46/46 = 100 % | yes | — | — |
| Dismisses the coating as staining first | 93 % | yes | `r-revise` | — |
| Calls it a spinal infection first | 93 % | yes | `r-revise` | — |
| Adds aconite | 40 % (capped) | yes | — | `g-aconite-into-heat` |
| Keeps version 2 unchanged before revising | 96 % | yes | — | — |
| Never stops the heat patches | 96 % | **no** | — | — |
| Tries the heat-clearing formula at the first visit (intercepted) | 100 % | yes | — | `g-revision-intercepted` (complication) |
| Stops after booking the review | 70 % | no | `r-revise` | — |
| Does nothing | 0 % | no | `r-redflags`, `r-rx-version`, `r-revise` | — |

## Reference path (`solution`)

The first 69 steps are `tcm-sg-lbp-01`'s first visit. The review then runs:

1. Nine history items.
2. Seven examinations.
3. The standard tongue capture and the sachet count.
4. `d-followup` (`heat`).
5. `stop-heat`, `diet-advice`, `rx-v3-damp-heat`, `dispense-v3`, then `finish`.

There are 95 steps in all.

## Clinical numbers check

- **Pain.** 6/10 at the first visit, 5/10 at review, but of a different character.
- **Observations.** Temperature 36.8 °C; pulse 86/min; blood pressure 134/82 mmHg.
- **Sachets.** 14 of 14 taken.
- **Version 3 (crude-herb equivalent, g/day).** 苍术 9, 黄柏 9, 牛膝 10, 薏苡仁 30, 秦艽 9, 忍冬藤 15; 7 days, 14 sachets.

## Facilitator notes

### Debrief questions (PEARLS)

1. **Reactions.** Did the yellow coating make you suspicious, after the first visit?
2. **Description.** What made you trust it this time?
3. **Analysis.**
   - What had to be excluded before calling it damp-heat, and why?
   - Which of his own choices added heat, and how do you raise them without blame?
   - Does this mean the first visit's assessment was wrong?
4. **Summary.** Patterns move. What will you re-check at every review?

### Common learner errors

| Error | How the case surfaces it |
|---|---|
| "It's staining again" | `d-followup` feedback; the review's standard capture says the coating is genuine |
| Escalating to the ED for "infection" without danger signs | `d-followup` feedback |
| Keeping the warming formula ("herbs take time") | `continue-course` refused; `r-no-more-warming` |
| More warming (aconite) | Refused and gated safety-critical |
| Forgetting the heat patches and the reddened skin | The objective stays open; `r-stop-heat` |

## Embodied mode

As in `tcm-sg-lbp-01`. The review's standard tongue capture is a bedside study. Version 3 is prescribed at a records terminal and supplied at the dispensary.

## Fidelity limits

- The transformation is authored. Nothing models how warming herbs, heat patches or diet change the pattern over days.
- The dose of the warming formula and the season appear only as history facts.
- Heat-patch skin injury is described, not modelled.

## Matcher notes

- The many phase twins at this review are listed under "Actions specific to this variant".
- `h-fu-heat-patches` uses `allday` (run together). "all day" would reduce to the single token `day`, which matched "every day" in the base case's medication question.

## References

The references of `tcm-sg-lbp-01`. No further guideline is cited for the damp-heat transformation; it follows standard TCM pattern teaching.

### To verify

Everything listed for `tcm-sg-lbp-01`, and:

- the version 3 doses against the 2020 Chinese Pharmacopoeia ranges (苍术, 黄柏, 牛膝, 薏苡仁, 秦艽, 忍冬藤);
- that 防己 is deliberately absent, given the aristolochic-acid history of some 防己 sources;
- the guidance on how long heat patches may be worn (the low-temperature burn risk).

## Changelog

- **0.1.0 (2026-11-07).** First version: phase 2, case 4 (docs/PHASE2.md).

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

**病例概要。** 初诊同 `tcm-sg-lbp-01`。这一周他：

- 按时服完温热方；
- 每天整天贴暖贴，洗很烫的热水澡；
- 吃了两次榴莲，又喝啤酒、吃油炸食物。

复诊时，寒湿已化热：

- 热痛、遇热加重、得凉则舒；
- 口苦黏，尿黄，便黏；
- 舌边红、苔薄黄腻（漱口后、自然光及标准光源下一致），脉滑数。

体温36.8℃，无泌尿和全身症状，肾区叩击痛阴性，神经系统正常；暖贴处皮肤发红。

**学习目标（第6条）。** 依据一致且可靠的证据识别证候已变，排除危险信号，去除助热因素，开具新版本处方。

**关键决策。**

- 停暖贴与过烫热水澡；
- 饮食建议；
- 第3版处方（四妙丸加减），第2版作废；
- 只按现行版本发药，一周后复诊。

**复盘要点。**

- 证候会随治疗、饮食与季节变化，每次复诊都要重新辨证。
- 判断证据质量的标准对两个方向都适用：初诊排除染苔，复诊采信真正的黄苔。
- 修订处方前先排除感染等危险信号。
