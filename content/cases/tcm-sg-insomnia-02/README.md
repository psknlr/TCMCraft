# tcm-sg-insomnia-02 — Difficulty sleeping · 47-year-old woman · review B

## Case card

| | |
|---|---|
| Setting | Outpatient — a fictional Singapore community TCM clinic |
| Facility | `tcm-sg-clinic` |
| Family | `sg-insomnia` (split **dev**): variant `review-b-conflicting-evidence` of [`tcm-sg-insomnia-01`](../tcm-sg-insomnia-01/README.md) |
| Difficulty | ★★★★ (4/5 at review; the shared first visit is rated 3) |
| Estimated time | 45 minutes |
| Specialty | Traditional Chinese medicine, sleep medicine, family medicine |
| Languages | 简体中文 (source), English |
| Phases | Same first visit as `tcm-sg-insomnia-01` → review two weeks later |
| Phase 2 dimensions | **Uncertain evidence** (a watch and a diary that disagree) and a **herb–drug review** (a new hypnotic taken with calming herbs) |
| Review status | **Unreviewed** — AI-assisted authoring against the cited guidance; not yet editorially reviewed or reviewed by a licensed clinician. Have a registered TCM physician and a family physician review it before teaching use. |
| Provenance | Synthetic |

## Learning outcomes

Outcomes 1–4 are those of `tcm-sg-insomnia-01` (the shared first visit). Outcome 5:

5. At review, weigh conflicting sleep evidence (a watch against a diary) and review a newly prescribed hypnotic taken with calming herbs. Change your own prescription, give safety advice and contact the prescriber the same day, rather than stopping another prescriber's medicine or adding sedation.

## Clinical summary (spoilers)

**The first visit is identical to `tcm-sg-insomnia-01`'s** (built from it by `tools/content-gen/insomnia_family.py`).

**Review B.** Two weeks later, Ms Lim says she is no better, maybe worse.

- **Week 1.** She kept to the schedule (bed at 00:45, up at 06:30). Her diary shows a sleep efficiency of about 90 %; she says it was her best week.
- **The watch.** A week after the first visit her daughter gave her a smartwatch. Its app reports:
  - about 6 h 50 min asleep;
  - "only 38 minutes of deep sleep";
  - a sleep score of 58, "poor".

  She checks it the moment she wakes.
- **Week 2.** Chasing deep sleep, she went to bed at 23:00 and stayed in bed until 07:30 when she could. Her diary, written each morning before she looks at the watch, shows 5 h 20 min asleep in about 8 hours in bed: an efficiency of about 67 %.
- **The zolpidem.** Worried by the score, she saw a private GP near her office (Dr Rahman). He prescribed zolpidem 10 mg at bedtime, 14 tablets. She has taken it for six nights, with the bedtime sachet of the calming granules. She does not mention it until asked about new medicines or other doctors.
- **The nights.** Twice, getting up at 3 a.m. for her mother-in-law, she was very unsteady. Once she walked into the door frame and bruised her left shoulder. There have been no complex sleep behaviours.
- **The mornings.** She is groggy until about ten, and she drives to work at 07:40.
- **Iron.** Her polyclinic GP found iron-deficiency anaemia, as in review A. This time she takes the iron correctly.

**Examination.** She is tired and slower than before, with a 3 cm bruise on the left shoulder (full movement). Gait and Romberg's test are normal at 11 a.m. Tongue and pulse are unchanged.

**Assessment.**

- **The evidence.** The diary, kept the same way each morning before she sees the watch, is the working measure. The watch infers sleep from movement and heart rate: it counts quiet waking as sleep and stages sleep unreliably, and it is not a medical device. Neither source is ground truth, and the 1 h 30 min gap is itself informative. The watch's real harm is behavioural: it has lengthened her time in bed.
- **The herb–drug review.** Zolpidem 10 mg (the US FDA recommends 5 mg for women) taken with sedating herbs has been followed by night-time unsteadiness while caring, and morning grogginess while driving. The label asks for 7–8 hours in bed after a dose, which clashes with sleep restriction.

**Plan.**

- Explain the watch: no watch at night, or the score hidden, for four weeks.
- Restart the schedule at 6 hours in bed (00:30–06:30), the 15-minute step her first week had earned.
- Hold the bedtime sachet and keep the after-lunch one. This is the learner's own prescription to change.
- Safety: no driving while drowsy, no alcohol, her husband takes the night duty on nights she takes the tablet, a nightlight, get up slowly.
- Contact Dr Rahman the same day with the herb list, the night events, the morning grogginess and the sleep schedule.

**The prescriber decides.** Dr Rahman reduces the zolpidem to 5 mg as needed, only on nights her husband is on duty, stopping within two weeks.

**Refused.** Stopping his medicine yourself in favour of the herbs; adding cinnabar (朱砂, mercury sulphide); extending her time in bed.

## Scenario timeline

| Phase | Opens | Where | What happens |
|---|---|---|---|
| `consult` | at start | consulting room | the shared first visit |
| `review` — two weeks later | as in `tcm-sg-insomnia-01` | consulting room | the review history (watch, diary method, new medicines, nights, mornings), examination, four records, two decisions, five actions |

## Decisions and assessment

### Objective `o-review`

It completes when:

- `d-sleep-evidence` and `d-review` are decided;
- `watch-explain`, `restriction-reset`, `hold-evening-sachet`, `night-safety` and `prescriber-letter` are all valid.

### Decisions

| Decision | Opens when | Correct | Distractors |
|---|---|---|---|
| `d-sleep-evidence` | the review diary and the watch report read; the watch and the diary method asked | `diary`: the diary is the working measure; read the watch with caution; neither is ground truth; the watch has changed her behaviour | "the watch is objective: sleep-state misperception, wind down"; polysomnography; average the two |
| `d-review` | new medicines, night events and mornings asked; the label read | `coordinate`: hold the bedtime sachet, safety advice, contact the prescriber today, don't change his medicine, restart the schedule | stop the zolpidem for herbs; add cinnabar; carry on unchanged |

### Actions specific to this variant

| Intervention | Rule |
|---|---|
| `watch-explain` | Checklist; valid at review once the watch has been asked about |
| `restriction-reset` | Checklist; valid only at review |
| `hold-evening-sachet`, `night-safety`, `prescriber-letter` | Checklist; valid at review once new medicines have been asked about (`h-rv-meds`) |
| `stop-zolpidem` | Contraindicated; complication gate `g-hypnotic-substitution` |
| `add-cinnabar` | Contraindicated; safety-critical gate `g-cinnabar` |
| `extend-bed` | Contraindicated; `r-no-harm-review` |

Phase twins at the review:

- `h-rv-status` supersedes `h-presenting`, `h-sleep-pattern` and `h-daytime`;
- `h-rv-meds` supersedes `h-meds`;
- `h-rv-mood` supersedes `h-mood` and `h-suicide`.

### Rubric (first visit as in `tcm-sg-insomnia-01` without its review items; review items below)

| Item | Domain | Weight | Notes |
|---|---|---|---|
| `r-review-inquiry` | history | 3 | sleep, watch, plan, diary method, new medicines, night events, mornings, mood |
| `r-review-records` | investigations | 1 | diary, watch report, label |
| `r-evidence` | diagnosis | 3 | **critical**: `d-sleep-evidence` first try |
| `r-hypnotic-review` | management | 3 | **critical**: `d-review` first try, and a valid `prescriber-letter` |
| `r-own-herbs` | safety | 2 | a valid `hold-evening-sachet` |
| `r-night-safety` | safety | 2 | a valid `night-safety` |
| `r-reset` | management | 2 | a valid `watch-explain` and `restriction-reset` |
| `r-no-harm-review` | safety | 2 | avoided-harm: no `stop-zolpidem`, `add-cinnabar` or `extend-bed` |
| `r-comm-review` | communication | 1 | examiner-judged |

There are 20 deterministic items in all, 42 points.

### Safety gates

| Gate | Verdict | When |
|---|---|---|
| `g-cinnabar` | safety-critical (cap 40 %) | `add-cinnabar` |
| `g-hypnotic-substitution` | complication | `stop-zolpidem` (refused) |
| `tcm-sg-insomnia-01`'s first-visit gates | as there | the shared first visit |

### Paths and their expected outcomes

These are checked by `python3 tools/pack_check.py --paths`. The paths are in `tools/paths/tcm-sg-insomnia-02.json`.

| Path | Score | Can finish | Critical missed | Gates |
|---|---|---|---|---|
| Reference path | 42/42 = 100 % | yes | — | — |
| Trusts the watch first | 93 % | yes | `r-evidence` | — |
| Orders polysomnography first | 93 % | yes | `r-evidence` | — |
| Averages the two first | 93 % | yes | `r-evidence` | — |
| Stops the zolpidem for herbs (refused), then coordinates | 88 % | yes | `r-hypnotic-review` | `g-hypnotic-substitution` |
| Adds cinnabar | 40 % (capped) | yes | `r-hypnotic-review` | `g-cinnabar` |
| Lets her stay in bed longer (refused) | 95 % | yes | — | — |
| Never contacts the prescriber | 93 % | **no** | `r-hypnotic-review` | — |
| Leaves the bedtime sachet as it is | 95 % | **no** | — | — |
| Never asks about new medicines | 76 % | **no** | `r-hypnotic-review` | — |
| Stops after booking the review | 62 % | no | `r-evidence`, `r-hypnotic-review` | — |
| Does nothing | 0 % | no | the three first-visit critical items, `r-evidence`, `r-hypnotic-review` | — |

## Reference path (`solution`)

The first 51 steps are `tcm-sg-insomnia-01`'s first visit. The review then runs:

1. Nine history items.
2. Four examinations.
3. Read the review diary, the watch report, the label and the GP's results.
4. `d-sleep-evidence` (`diary`), then `d-review` (`coordinate`).
5. `watch-explain`, `restriction-reset`, `hold-evening-sachet`, `night-safety`, `prescriber-letter`, then `finish`.

There are 80 steps in all.

## Clinical numbers check

- **Week 1 diary.** 5 h 45 min in bed = 345 min; 310 min asleep (5 h 10 min). Efficiency 310/345 = 90 %.
- **Week 2 diary.** About 8 h in bed (23:00 to about 07:00) = 480 min, minus 25 min to fall asleep and 135 min awake in the night = 320 min asleep (5 h 20 min). Efficiency 320/480 = 67 %.
- **Watch (the same week).** In bed 7 h 55 min = 475 min = 410 asleep + 65 awake. "Asleep" = 38 deep + 292 light + 80 REM = 410 min (6 h 50 min). The watch reports 410 − 320 = 90 min more sleep than the diary.
- **Zolpidem.** 10 mg, 14 tablets, prescribed seven days ago; six nights taken, eight left.
- **Restarted schedule.** 6 h in bed, 00:30–06:30: week 1's 5 h 45 min plus the 15-minute step its 90 % efficiency earned.
- **GP results.** As in `tcm-sg-insomnia-01`.

## Facilitator notes

### Debrief questions (PEARLS)

1. **Reactions.** When the watch said 6 h 50 min, what was your first thought?
2. **Description.** How was each number produced, and what does that tell you about each?
3. **Analysis.**
   - What harm has the watch already done, whatever its accuracy?
   - Whose decision is the zolpidem, and whose is the bedtime sachet?
   - What makes the night-time unsteadiness more than a side effect for her?
4. **Summary.** What will you ask at every review now that you would not have asked before?

### Common learner errors

| Error | How the case surfaces it |
|---|---|
| "The watch is objective" | `d-sleep-evidence` feedback; the app's own notice says it is not a medical device |
| Polysomnography to settle it | `d-sleep-evidence` feedback: not indicated, would not change the plan |
| Never asking about new medicines or other doctors | `d-review` stays closed; she does not volunteer the zolpidem |
| Stopping the other doctor's medicine for herbs | Refused; `g-hypnotic-substitution`; Dr Rahman's reply shows what coordination achieves |
| "More sedation" (cinnabar) | Refused; gated safety-critical |
| Letting her lie in to "catch up" | Refused with her own diary (90 % → 67 %) |
| Forgetting driving | `r-night-safety`; the objective stays open |

## Embodied mode

As in `tcm-sg-insomnia-01`, with these additions:

- She brings the tablet bag: `zolpidem-label` is a bedside look.
- The watch report and the review diary are records, read at a records terminal.
- Mr Lim, the dispenser, can explain zolpidem and interprets the label.
- Dr Ho interprets the watch report.

## Fidelity limits

- **The disagreement between sources is authored.** Nothing models how a wrist device estimates sleep.
- **The prescriber's reply is authored.** It is the same whatever the letter says. Only the examiner-judged item sees the quality of the communication.
- **The interaction is precautionary.** The herb–zolpidem interaction is taught as a precaution with limited direct evidence, not modelled.
- **The bedtime sachet is held as a recorded instruction**, not as a new prescription version. The engine has no versioned prescription object (docs/ENGINE_EXTENSIONS.md).

## Matcher notes

- **Review twins.** They are listed under "Actions specific to this variant".
- **`h-rv-status`** excludes mood, watch, diary, new-medicine and doctor words. Questions such as "have you seen another doctor since last time?" therefore reach `h-rv-meds`, not the sleep status.
- **`h-rv-cbti`** uses plan phrasings ("有没有照着做", "stick to the plan"), not bedtime words, which belong to the first visit's `h-sleep-habits`.

## References

The references of `tcm-sg-insomnia-01`, and:

1. de Zambotti M, Cellini N, Goldstone A, Colrain IM, Baker FC. Wearable sleep technology in clinical and research settings. Med Sci Sports Exerc. 2019;51(7):1538-57.
2. Baron KG, Abbott S, Jao N, Manalo N, Mullen R. Orthosomnia: are some patients taking the quantified self too far? J Clin Sleep Med. 2017;13(2):351-4.
3. Harvey AG, Tang NK. (Mis)perception of sleep in insomnia: a puzzle and a resolution. Psychol Bull. 2012;138(1):77-101.
4. US Food and Drug Administration. FDA Drug Safety Communication: risk of next-morning impairment after use of insomnia drugs; FDA requires lower recommended doses for certain drugs containing zolpidem. Silver Spring (MD): FDA; 2013.
5. US Food and Drug Administration. FDA adds Boxed Warning for risk of serious injuries caused by sleepwalking with certain prescription insomnia medicines. Silver Spring (MD): FDA; 2019.

### To verify

Everything listed for `tcm-sg-insomnia-01`, and:

- The page ranges of references 1–3, and the exact titles and dates of the two FDA communications.
- **Zolpidem in Singapore.** Its prescribing status and Singapore's Ministry of Health guidance on hypnotic prescribing: duration limits and record-keeping.
- **The label.** The local product's wording on driving and on time in bed after a dose.
- **Herb–drug evidence.** The evidence on interactions between zolpidem and 酸枣仁, 远志 or 合欢皮. The case treats additive sedation as a precaution.
- **Cinnabar.** The 2020 Chinese Pharmacopoeia's cautions on 朱砂, and its status in Singapore: the Health Sciences Authority's heavy-metal limits for Chinese proprietary medicines.
- **Wearables.** That consumer wearables overestimate sleep relative to polysomnography in insomnia specifically, as `d-sleep-evidence` states.

## Changelog

- **0.1.0 (2026-11-07).** First version: phase 2, case 6 (docs/PHASE2.md).

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

**病例概要。** 初诊同 `tcm-sg-insomnia-01`。复诊时：

- 智能手表报告每晚6小时50分、深睡38分钟、分数“差”；
- 每天早上、看手表前写的日记是5小时20分；
- 为了追分数，她提早上床、晚起，睡眠效率由约90%降到约67%；
- 她又去私人诊所，服唑吡坦10毫克，与睡前那包安神中药同服；
- 夜里起来照顾婆婆时站不稳、撞伤肩膀，早上头昏仍开车。

**学习目标（第5条）。** 权衡相互矛盾的睡眠证据；核查新开的催眠药与安神中药同用：改自己的处方，给安全建议，当天联系开药医生。

**关键决策。**

- 以日记为治疗依据，谨慎看待手表，二者都不是“真值”；
- 解释手表，暂时不戴；恢复睡眠时间表（卧床6小时）；
- 暂停睡前那包中药，午饭后那包照服；
- 嗜睡不开车、不喝酒，服药的晚上由先生照顾婆婆；
- 当天联系开药医生，由他决定唑吡坦的剂量与去留。

**不可接受。** 自行停用他人的药改靠中药；加朱砂（含汞）；让她多躺补深睡。

**复盘要点。**

- 证据不一致时，先问每份证据是怎么产生的。
- 每次复诊都问新的药和别的医生。
- 改自己能改的，协调别人的。
