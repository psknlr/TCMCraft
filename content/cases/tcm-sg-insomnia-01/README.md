# tcm-sg-insomnia-01 — Difficulty sleeping · 47-year-old woman · review A

## Case card

| | |
|---|---|
| Setting | Outpatient — a fictional Singapore community TCM clinic |
| Facility | `tcm-sg-clinic` |
| Family | `sg-insomnia` (split **dev**): the base case, variant `review-a-iron`. [`tcm-sg-insomnia-02`](../tcm-sg-insomnia-02/README.md) (review B) shares this first visit. |
| Difficulty | ★★★ (3/5) |
| Estimated time | 40 minutes |
| Specialty | Traditional Chinese medicine, sleep medicine, family medicine |
| Languages | 简体中文 (source), English |
| Phases | First visit: history, the four examinations, the senior's note, the plan → review two weeks later |
| Phase 2 dimension | **Review disagreement**: the senior physician, having read only the intake form, proposes a different pattern and formula |
| Review status | **Unreviewed** — AI-assisted authoring against the cited guidance; not yet editorially reviewed or reviewed by a licensed clinician. Have a registered TCM physician and a family physician review it before teaching use. |
| Provenance | Synthetic (fictional patient, clinic and products) |

## Learning outcomes

1. Screen insomnia as a symptom — heavy periods and anaemia, mood and self-harm, sleep apnoea, thyroid and medicines — and refer to the GP accordingly.
2. Make CBT-I the first-line treatment for chronic insomnia, with a concrete rising time, stimulus control and sleep restriction.
3. Differentiate heart–spleen deficiency with liver qi stagnation from liver fire, heart–kidney non-communication and phlegm-heat, using the four examinations.
4. Resolve a senior's differing view with evidence — discuss, agree and record — rather than defer to seniority or avoid the conversation.
5. At review, check how herbs and medicines are actually taken, space iron from tea and herbs, and never let herbs replace iron.

## Clinical summary (spoilers)

Ms Lim Hui Min (pseudonym), 47, an accounts executive, has slept badly for five months. Six months ago her mother-in-law was diagnosed with dementia; she lives with the family and wanders at night.

**Sleep.**

- Four or five nights a week she takes over an hour to fall asleep, wakes two or three times, and is awake for good by half past four.
- She is tired all day and has made two mistakes in the accounts.
- She scrolls on her phone in bed until midnight, lies in at weekends, and drinks coffee at three in the afternoon.
- She takes pharmacy antihistamine sleeping tablets about two nights a week.

**What the screen finds.**

- Her periods have been very heavy for six months, with flooding and clots.
- She looks pale, with pale lips, conjunctivae and nail beds, and has palpitations when she lies awake.
- Her mother has thyroid disease. Her thyroid is not enlarged and there is no tremor.
- Her mood is low on some days. She still enjoys things, and she has no thoughts of self-harm (PHQ-9 6, item 9 = 0).
- She does not snore (STOP-Bang 1).

**The four examinations.**

- Poor appetite, bloating after meals and loose stools.
- Many dreams, palpitations and being easily startled.
- A soft, low voice with the occasional sigh. She feels the cold.
- Tongue pale, slightly swollen, tooth-marked, with a thin white coating.
- Pulse thready and weak.

**Assessment.**

- Biomedical: chronic insomnia disorder, with a work-up her history requires. She is referred to her GP for a blood count, ferritin and thyroid function, and for assessment of the heavy periods. CBT-I comes first.
- TCM: heart–spleen deficiency (心脾两虚), with some liver qi stagnation from the stress, and no sign of fire.

**The disagreement.** Dr Ho, the senior physician, read the intake form before the consultation: caring stress, irritability, sighing, and poor sleep with many dreams. His note proposes liver depression turning to fire (肝郁化火) and 丹栀逍遥散, and asks the learner to discuss once she has been seen.

- The learner who has examined her owes him the evidence: no red tongue, yellow coating, bitter taste or wiry, rapid pulse; instead a pale tooth-marked tongue, a thready weak pulse, loose stools, cold intolerance and heavy periods.
- Dr Ho's point about stress is fair, and 合欢皮 addresses it.
- Both views go into the notes, so that the review can test them.
- Deferring to seniority, or bolting both formulas together, is refused. The formula's bitter-cold herbs would weaken her spleen further.

**The plan.**

- CBT-I.
- Stop the pharmacy sleeping tablets.
- Modified 归脾汤 with 合欢皮 (version 1), dispensed.
- The GP referral.
- Review in two weeks with the sleep diary and the GP's results.

**Review.**

- Her GP found iron-deficiency anaemia (Hb 109 g/L, MCV 76 fL, ferritin 8 µg/L), probably from the heavy bleeding. Thyroid function is normal (TSH 1.9 mIU/L).
- Her GP started ferrous fumarate once daily and referred her to gynaecology.
- She takes the iron with her breakfast milk tea and mixes the granules at the same time.
- Her sleep is better: sleep efficiency has risen from about 69 % to about 92 %.
- Her mood is better and she has no thoughts of self-harm.
- The right move is to continue the plan, keep the iron exactly as the GP prescribed (the herbs do not replace it), take the iron at least two hours apart from tea, milk tea and the granules, and support the gynaecology referral.

## Scenario timeline

| Phase | Opens | Where | What happens |
|---|---|---|---|
| `consult` — first visit | at start | consulting room | history and the screen, the four examinations, the questionnaire and sleep diary, two decisions, Dr Ho's note, the disagreement, the plan |
| `review` — two weeks later | a valid `dispense`, `gp-referral` and `arrange-review` | consulting room | the review history and examination, the GP's results, the new diary, the decision, iron spacing, continue |

## Decisions and assessment

### Objectives (task list)

| Objective | Completes when |
|---|---|
| `o-inquiry` | `h-presenting`, `h-sleep-pattern`, `h-daytime`, `h-periods`, `h-mood`, `h-suicide`, `h-snoring` and `h-meds` asked |
| `o-exam` | `e-general`, `e-tongue`, `e-pulse`, `e-voice` and `e-neck` examined |
| `o-assess` | `d-medical` and `d-pattern` decided |
| `o-plan` | `d-disagreement` decided; a valid `case-discussion` and `dispense`; `cbti`, `gp-referral` and `arrange-review` done |
| `o-review` | `d-review` decided; a valid `iron-spacing` and `continue-plan` |

### Decisions

| Decision | Opens when | Correct | Distractors |
|---|---|---|---|
| `d-medical` | periods, mood, self-harm and snoring asked; questionnaire read; complexion inspected | `work-up`: chronic insomnia with features needing a GP work-up; no urgent risk; CBT-I first | sleep apnoea; major depression; "simple insomnia, no work-up" |
| `d-pattern` | tongue, pulse, digestion, dreams and palpitations; `d-medical` decided | `heart-spleen` (with liver qi stagnation) | liver fire; heart–kidney non-communication; phlegm-heat |
| `d-disagreement` | Dr Ho's note read; `d-pattern` decided | `discuss`: set out the evidence for and against both patterns, agree a plan that also addresses the stress, record both views | defer to the senior; ignore the note; combine both formulas |
| `d-review` | the GP's results read at review; iron, status and mood asked | `continue-spaced` | stop the iron; stop the herbs; "the anaemia shows the pattern was wrong" |

### The disagreement as state

- **Dr Ho's note** (`senior-note`) is a record in the notes, dated before the consultation, and says it rests on the questionnaire alone.
- **`case-discussion`** is a checklist step. It is valid only after the note has been read and the learner has reached a pattern of their own (`d-pattern`). A discussion with nothing to bring is recorded as invalid.
- **`rx-guipi`** is indicated once `d-disagreement` is decided. `r-disagreement` requires the discussion **before** the prescription (`inOrder`). Prescribing first and talking afterwards misses it.
- **`defer-to-senior` and `combine-formulas`** are always contraindicated. They are refused with the evidence, and they record the complication gate `g-deferred-against-evidence`.
- **The record.** `extensions.tcmcraft.disagreement` holds both views, their basis and the resolution. The engine does not read it yet (docs/ENGINE_EXTENSIONS.md).

### Rubric (14 deterministic items, 29 points; 2 examiner-judged communication items)

| Item | Domain | Weight | Notes |
|---|---|---|---|
| `r-sleep-history` | history | 2 | sleep pattern, daytime effects, caffeine, sleep habits |
| `r-medical-screen` | history | 3 | **critical**: periods, mood, self-harm, snoring, medicines |
| `r-four-exam` | examination | 2 | spirit and complexion, tongue, voice, pulse |
| `r-thyroid-exam` | examination | 1 | thyroid and tremor |
| `r-records` | investigations | 1 | questionnaire and sleep diary |
| `r-medical` | diagnosis | 2 | `d-medical` first try |
| `r-pattern` | diagnosis | 3 | `d-pattern` first try |
| `r-disagreement` | management | 3 | **critical**: `d-disagreement` first try, and `case-discussion` before `rx-guipi` |
| `r-no-deference` | safety | 2 | avoided-harm: neither `defer-to-senior` nor `combine-formulas` |
| `r-gp` | management | 2 | **critical**: `gp-referral` |
| `r-cbti` | management | 2 | `cbti` |
| `r-otc` | safety | 1 | stop the pharmacy sleeping tablets; no `stronger-sleeper` |
| `r-review` | management | 3 | at review: `d-review` first try and a valid `iron-spacing` |
| `r-no-stop-iron` | safety | 2 | avoided-harm, scored at review or on a `stop-iron` attempt |
| `r-comm-patient` | communication | 1 | examiner-judged: her strain as a carer, her fears, the plan explained |
| `r-comm-colleague` | communication | 1 | examiner-judged: the disagreement handled professionally and recorded |

### Safety gates

| Gate | Verdict | When |
|---|---|---|
| `g-stop-iron` | safety-critical (cap 40 %) | `stop-iron`: herbs offered in place of iron for iron-deficiency anaemia |
| `g-deferred-against-evidence` | complication | `defer-to-senior` or `combine-formulas` attempted (both are refused) |
| `g-hypnotic-escalation` | complication | `stronger-sleeper` attempted (refused) |

### Paths and their expected outcomes

These are checked by `python3 tools/pack_check.py --paths`. The paths are in `tools/paths/tcm-sg-insomnia-01.json`.

| Path | Score | Can finish | Critical missed | Gates |
|---|---|---|---|---|
| Reference path | 29/29 = 100 % | yes | — | — |
| Prescribes Dr Ho's formula as it stands, then corrects | 83 % | yes | `r-disagreement` | `g-deferred-against-evidence` |
| Combines both formulas, then corrects | 83 % | yes | `r-disagreement` | `g-deferred-against-evidence` |
| Prescribes 归脾汤, then discusses it with Dr Ho | 90 % | yes | `r-disagreement` | — |
| Calls it liver fire from the questionnaire, then corrects | 90 % | yes | — | — |
| Sleep study and urgent psychiatry first | 93 % | yes | — | — |
| Advises nightly, stronger sleeping tablets | 97 % | yes | — | `g-hypnotic-escalation` |
| Never refers her to her GP | 22/24 = 92 %; the review never opens | **no** | `r-gp` | — |
| Tells her at review that the herbs replace the iron | 40 % (capped) | yes | — | `g-stop-iron` |
| Leaves the iron with the milk tea and the granules | 90 % | **no** | — | — |
| Stops after booking the review | 90 % | no | — | — |
| Does nothing | 0/22 = 0 % | no | `r-medical-screen`, `r-disagreement`, `r-gp` | — |

A path that cannot finish shows only the items that could be scored. The review items count once the review opens, so "never refers her to her GP" is out of 24 points, not 29. Its failure is the critical miss and the unfinished case, not the percentage.

## Reference path (`solution`)

1. `start`.
2. 25 history items.
3. Eight examinations.
4. Read the questionnaire and the sleep diary.
5. `d-medical` (`work-up`) and `d-pattern` (`heart-spleen`).
6. Read Dr Ho's note → `d-disagreement` (`discuss`).
7. `case-discussion`, `explain-consent`, `gp-referral`, `cbti`, `stop-otc-sleeper`, `rx-guipi`, `dispense` and `arrange-review`. The review opens.
8. Six review history items and three review examinations.
9. Read the GP's results and the new sleep diary → `d-review` (`continue-spaced`).
10. `iron-spacing`, `continue-plan` and `finish`.

There are 68 steps in all. Acupuncture (`explain-consent` then `acupuncture-sleep`, lying down in the treatment room) is an acceptable adjunct, not part of the reference path.

## Clinical numbers check

- **BMI.** 52 kg / (1.58 m)² = 20.8.
- **Observations.** Blood pressure 112/70 mmHg; pulse 84/min, regular; temperature 36.5 °C. At review the pulse is 78/min.
- **Scales.**
  - ISI 17/28: moderate.
  - PHQ-9 6/27: mild, with item 9 = 0.
  - GAD-7 7/21: mild.
  - STOP-Bang 1/8: low risk.
- **First sleep diary (14 nights).** In bed 7 h 30 min = 450 min, minus 70 min to fall asleep and 70 min awake after = 310 min asleep (5 h 10 min). Sleep efficiency 310/450 = 69 %.
- **Sleep restriction.** Time in bed starts at 5 h 45 min: the 5 h 10 min average sleep plus about 30 minutes, and never under 5 hours. She rises at 06:30, so she goes to bed at 00:45. Time in bed lengthens by 15–30 minutes a week while sleep efficiency is 90 % or more.
- **Review diary.** In bed 5 h 45 min in the first week, lengthened to 6 h 15 min in the second. In the second week: 375 min in bed, 20 min to fall asleep and 10 min awake after = 345 min asleep (5 h 45 min). Sleep efficiency 345/375 = 92 %.
- **GP results.** Hb 109 g/L (115–150), MCV 76 fL (80–100), ferritin 8 µg/L (15–150), TSH 1.9 mIU/L (0.4–4.0). The ranges are illustrative.
- **Version 1 (crude-herb equivalent, g/day).** 党参 12, 黄芪 15, 白术 10, 茯苓 12, 酸枣仁 15, 龙眼肉 10, 木香 6, 当归 9, 远志 6, 合欢皮 10, 炙甘草 6, 大枣 10.
  - One sachet after lunch and one an hour before bed, for 14 days: 28 sachets.
  - At review, four weeks are repeated: 56 sachets.
- **Acupuncture (adjunct).** HT7 ×2, PC6 ×2, SP6 ×2, Anmian ×2 and Yintang ×1 = 9 needles in, 9 out.

## Facilitator notes

### Debrief questions (PEARLS)

1. **Reactions.** How did it feel to find that you disagreed with the senior's note?
2. **Description.** What did Dr Ho have to go on, and what did you?
3. **Analysis.**
   - Which findings argued for heart–spleen deficiency, and which for liver fire? Was anything in his view right?
   - Why must heavy periods be worked up before treating "insomnia"?
   - What changes when the disagreement is written into the notes?
   - Why does how she takes the iron matter as much as whether she takes it?
4. **Summary.** How will you raise a disagreement with a senior next time?

### Common learner errors

| Error | How the case surfaces it |
|---|---|
| Treating the insomnia without the screen (periods, mood, self-harm, snoring) | `d-medical` stays closed; `r-medical-screen` is critical |
| No GP referral | The review never opens; `r-gp` is critical |
| Deferring to seniority, or combining formulas to avoid conflict | Refused with the evidence; `g-deferred-against-evidence`; `r-disagreement` and `r-no-deference` |
| Prescribing and then telling Dr Ho | `r-disagreement` (`inOrder`) |
| Ignoring Dr Ho's note | `d-disagreement` feedback |
| Trusting the questionnaire over the patient | `d-pattern` feedback; Dr Ho's note says what it rests on |
| Over-referral (sleep study, urgent psychiatry) | `d-medical` feedback; the referral responses explain why |
| Escalating sleeping tablets | Refused; `g-hypnotic-escalation`; `r-otc` |
| Stopping the iron, "herbs nourish the blood" | Refused; gated safety-critical; Dr Ho's correction `herbs-replace-iron` |
| Not asking how she takes her medicines | `d-review` stays closed until `h-rv-iron` is asked |

## Embodied mode

- **Grounding.** Everything the patient and staff say comes from the case. The gynaecology result and the long-term outcome are `unknowns`.
- **Where things happen.**
  - She starts seated on the examination couch of a consulting room.
  - Acupuncture, if chosen, moves her to a couch in the acupuncture and tuina room, lying down.
  - The review brings her back to a consulting room.
- **People.**
  - Dr Ho (`attending`) answers in line with his note until the learner brings the evidence. He then agrees, and insists that the stress is addressed. He corrects two misconceptions: "pills first" and "herbs replace iron".
  - Mr Lim (`pharmacist`) explains the formula, the pharmacy antihistamines and iron spacing.
  - Dr Wong (`consultant`) is her polyclinic family physician.
  - Siti (`nurse`) handles reception and bookings.
- **Kit.**
  - Records (`records`) are read at a consulting room's records terminal.
  - Supply (`medications`) is at the herbal dispensary.

## Fidelity limits

- **The disagreement.** It is a decision, an ordered pair of steps and a record. Dr Ho's change of mind is authored, not argued: a learner who brings weak evidence gets the same agreement as one who brings strong evidence. Only the examiner-judged item `r-comm-colleague` sees the quality of the conversation.
- **CBT-I.** It is one step. The sleep restriction schedule, its weekly adjustment and adherence are narrative. The review diary is authored.
- **The iron–tea interaction.** It is taught, not modelled: nothing changes the haemoglobin.
- **The review.** It is a single authored branch. `tcm-sg-insomnia-02` is review B of the same first visit (a watch against the diary, and a new hypnotic). Other reviews (a mood change, no improvement) would be further variants.

## Matcher notes

- **Review twins.**
  - `h-rv-status` supersedes `h-presenting`, `h-sleep-pattern` and `h-daytime`.
  - `h-rv-mood` supersedes `h-mood` and `h-suicide`.
  - `h-rv-gynae` supersedes `h-periods`.
- **Worry questions.** "最担心" and "most worried" belong to `h-ice`.
  - `h-anxiety` keeps "老是担心" and "担心个不停" rather than a bare 担心.
  - `h-stress` dropped "worries".
- **Mood questions at review.** `h-rv-status` excludes mood words, so "这两周心情好吗？" reaches `h-rv-mood`, not the sleep status.
- **The review diary.** An `orderMatching` rule sends "review", "latest", "new" and "这两周" to `sleep-diary-review`, never the first diary.
- **The corpus.** 32 utterances in both languages, with every required item paraphrased. All of them pass the offline matcher.

## References

1. Riemann D, Baglioni C, Bassetti C, Bjorvatn B, Dolenc Groselj L, Ellis JG, et al. European guideline for the diagnosis and treatment of insomnia. J Sleep Res. 2017;26(6):675-700.
2. Qaseem A, Kansagara D, Forciea MA, Cooke M, Denberg TD; Clinical Guidelines Committee of the American College of Physicians. Management of chronic insomnia disorder in adults: a clinical practice guideline from the American College of Physicians. Ann Intern Med. 2016;165(2):125-33.
3. Edinger JD, Arnedt JT, Bertisch SM, Carney CE, Harrington JJ, Lichstein KL, et al. Behavioral and psychological treatments for chronic insomnia disorder in adults: an American Academy of Sleep Medicine clinical practice guideline. J Clin Sleep Med. 2021;17(2):255-62.
4. National Institute for Health and Care Excellence. Heavy menstrual bleeding: assessment and management (NICE guideline NG88). London: NICE; 2018 (updated 2021).
5. Kroenke K, Spitzer RL, Williams JB. The PHQ-9: validity of a brief depression severity measure. J Gen Intern Med. 2001;16(9):606-13.
6. World Health Organization. WHO international standard terminologies on traditional Chinese medicine. Geneva: WHO; 2022.
7. Chinese Pharmacopoeia Commission. Pharmacopoeia of the People's Republic of China, Volume I. 2020 ed. Beijing: China Medical Science Press; 2020.
8. Traditional Chinese Medicine Practitioners Board (Singapore). Ethical code and ethical guidelines for TCM practitioners. Singapore: TCMPB.

### To verify

No DOIs are given: none was verified with a lookup in this session.

- The page ranges and issue numbers of references 1–3 and 5, and the edition and year of reference 8.
- That NICE NG88 recommends a full blood count for every woman with heavy menstrual bleeding, as worded in `d-medical`.
- The sleep-restriction parameters against the European guideline and AASM 2021: the starting time in bed, the 5-hour floor, the weekly step and the efficiency threshold.
- Every herb dose against the 2020 Chinese Pharmacopoeia ranges. Check also whether 当归 should be reduced or withheld during heavy menstrual flow; 归脾汤 is classically used where the spleen fails to control blood.
- The spacing advice for iron and tea, milk tea and herbal granules. The granule interaction rests on limited evidence and is offered as a precaution.
- That the TCMPB ethical code addresses professional collaboration and disagreement, as teaching point 4 says.
- The availability of antihistamine sleeping tablets from Singapore pharmacies.

## Changelog

- **0.1.1 (2026-11-07).** Family metadata (variant `review-a-iron`) and the title suffix "· review A", now that `tcm-sg-insomnia-02` shares the first visit. No scoring change.
- **0.1.0 (2026-11-07).** First version: phase 2, case 5 (docs/PHASE2.md).

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

**病例概要。** 林女士47岁，会计，失眠5个月。半年前婆婆确诊失智症，与家人同住，夜间常起来走动。

- 入睡困难、夜醒、早醒，白天疲乏，工作出错。
- 睡前在床上滑手机，周末补眠，下午喝咖啡，每周约两晚服用药房的抗组胺类安眠药。
- 筛查发现：月经过多半年，面色、唇甲淡白，夜间心悸；母亲有甲状腺病。
- 情绪偶有低落，无自伤念头（PHQ-9 6分，第9题0分）；不打鼾。
- 四诊：纳呆、腹胀、便溏，多梦易惊，语声低弱，怕冷；舌淡胖、有齿痕、苔薄白；脉细弱。

**评估。** 西医：慢性失眠障碍，需转介家庭医生查血常规、铁蛋白和甲状腺功能，并评估月经过多；首选睡眠认知行为治疗。中医：心脾两虚，兼肝气郁结，无火象。

**分歧（第二阶段维度：复核意见分歧）。** 何医生只看过问卷，倾向肝郁化火、丹栀逍遥散。正确做法：

- 拿出证据与他讨论；
- 承认他关于压力的合理观察，用合欢皮兼顾；
- 商定以归脾汤为主；
- 把双方意见记入病历。

照搬上级的方或两方合用都会被拒绝，并记录为并发问题。

**复诊。** 家庭医生证实缺铁性贫血，甲状腺功能正常，已开铁剂并转介妇科。她把铁剂与奶茶、中药颗粒同服。睡眠效率由约69%升至约92%。正确做法：

- 继续原方案；
- 铁剂照服，中药不能代替；
- 铁剂与茶、奶茶及中药颗粒至少间隔两小时；
- 配合妇科转诊。

**复盘要点。**

- 失眠先当作症状来筛查。
- 分歧用证据而不是资历解决，并记录下来。
- 复诊时核对每样药实际怎么服。
