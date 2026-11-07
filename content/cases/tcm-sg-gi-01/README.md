# tcm-sg-gi-01 — Epigastric fullness · 63-year-old man

## Case card

| | |
|---|---|
| Setting | Outpatient — a fictional Singapore community TCM clinic |
| Facility | `tcm-sg-clinic` |
| Family | `sg-gi` (split **dev**): the base case, variant `review-a-hidden-liquorice` |
| Difficulty | ★★★ (3/5) |
| Estimated time | 40 minutes |
| Specialty | Traditional Chinese medicine, gastroenterology, family medicine |
| Languages | 简体中文 (source), English |
| Phases | First visit: history, the four examinations, prescription and the dispensary's query → review two weeks later |
| Phase 2 dimensions | **Review disagreement** (the dispensary objects to the prescription and the prescriber must answer) and **execution** (prescription versions; a hidden source of liquorice) |
| Review status | **Unreviewed** — AI-assisted authoring against the cited guidance; not yet editorially reviewed or reviewed by a licensed clinician. Have a registered TCM physician and a family physician review it before teaching use. |
| Provenance | Synthetic (fictional patient, clinic and products) |

## Learning outcomes

1. Screen dyspepsia for alarm features, and refer through the GP for endoscopy by age (60 or over), neither over- nor under-reacting.
2. Differentiate spleen–stomach qi deficiency with damp and qi stagnation from stomach yin deficiency, liver–stomach disharmony and spleen–stomach damp-heat.
3. Answer a dispensary query on the patient's own risk. Recognise that liquorice's pseudo-aldosteronism risk adds to a thiazide's, and revise with a new prescription version rather than overruling with "within the Pharmacopoeia range".
4. Change your own prescription and coordinate with the GP, without stopping the antihypertensive the GP prescribed.
5. At review, when monitoring shows the feared effect, look for hidden sources in foods, drinks and supplements (herbal tea, liquorice plums), and tell the GP the same day.

## Clinical summary (spoilers)

Mr Ong Kok Leong (pseudonym), 63, is a retired bus captain. He takes hydrochlorothiazide 25 mg and amlodipine 5 mg for high blood pressure.

**Presentation.** Two months of fullness and bloating after meals, belching, early satiety, poor appetite and loose stools. It is worse with iced drinks and tiredness, and better with warmth and pressure. He has never had a scope or an H. pylori test.

**Alarm-feature screen.**

- Negative: weight steady at 68 kg; no difficulty swallowing; no vomiting; no blood or black stools; no family history of gastric cancer; no NSAIDs or aspirin.
- Examination: a soft abdomen with mild epigastric discomfort eased by pressure, no mass, no supraclavicular nodes, no pallor or jaundice.
- Blood pressure 148/88 mmHg. His polyclinic potassium three months ago was 3.5 mmol/L (low-normal).

**The four examinations.** Tired, quiet and sallow, with a low voice. Tongue pale and swollen with tooth marks, and a white, slightly greasy coating. Pulse moderate and weak, weakest at the right guan.

**Assessment.**

- **Biomedical.** New dyspepsia at 63 without alarm features. Refer through his GP for endoscopy: not urgent, but it is recommended at 60 or over (ACG/CAG 2017). Ask the GP to recheck his blood pressure and potassium.
- **TCM.** Spleen–stomach qi deficiency with damp and qi stagnation: modified 香砂六君子汤, version 1, with 炙甘草 6 g.

**The disagreement.** Ms Chua, the dispenser, puts version 1 on hold:

- he takes a potassium-losing thiazide, his blood pressure is above target and his potassium is low-normal;
- liquorice's glycyrrhizic acid causes pseudo-aldosteronism (sodium retention, potassium loss, higher blood pressure), and the effect adds to the thiazide's;
- depending on the product, 6 g of 炙甘草 can approach the roughly 100 mg a day of glycyrrhizic acid suggested as an upper limit;
- she suggests omitting it, or reducing it to 3 g or less with monitoring.

The prescriber answers on the merits and issues version 2. Liquorice only harmonises in this formula, so it can be omitted (the reference path), or kept at 3 g with the monitoring written on the prescription (the other acceptable pathway). Version 1 is cancelled.

These answers are refused:

- "6 g is within the Pharmacopoeia range": the dispensary does not release version 1 (complication gate);
- telling him to stop his thiazide: safety-critical.

The letter to his GP covers the endoscopy referral, his blood pressure, version 2 and the dispensary's query, and asks for a potassium and blood-pressure check in two weeks.

**Review.**

- **Better.** The fullness is much better, his stools are formed, and the tongue's greasy coating has gone.
- **The feared effect.** His potassium has fallen to 3.3 mmol/L. His blood pressure has risen (clinic 152/90; home log 142/86 → 152/92). He has gained 1 kg, his ankles are puffy, and his calves cramped twice.
- **The source.** Version 2 has no liquorice. His wife said the bloating was "heatiness", so for ten days he has drunk a bottle of 廿四味 herbal tea every day and eaten liquorice plums. He thought herbal tea was "just a drink", and he mentions it only when asked about herbal teas, new foods or supplements.
- **Endoscopy.** Mild chronic gastritis, H. pylori negative, no metaplasia or dysplasia.
- **Plan.** Stop the tea and the plums, keep version 2, and call Dr Wong the same day. She prescribes potassium for a week, rechecks, and will reconsider the diuretic if needed.

## Scenario timeline

| Phase | Opens | Where | What happens |
|---|---|---|---|
| `consult` — first visit | at start | consulting room, dispensary | history and alarm screen, the four examinations, the polyclinic results, two decisions, version 1, the dispensary's query, version 2, supply, the GP letter |
| `review` — two weeks later | a valid `dispense` and `gp-letter`, and `arrange-review` | consulting room | the review history (drinks and supplements), examination, the GP's results, the endoscopy report, the blood-pressure log, the decision, three actions |

## Decisions and assessment

### Objectives (task list)

| Objective | Completes when |
|---|---|
| `o-inquiry` | `h-presenting`, `h-character`, the three alarm items, `h-meds` and `h-herbal-products` asked |
| `o-exam` | `e-general`, `e-vitals`, `e-tongue`, `e-pulse` and `e-abdomen` examined |
| `o-assess` | `d-medical` and `d-pattern` decided |
| `o-plan` | `d-rx-query` decided; a valid version 2, `dispense` and `gp-letter`; `arrange-review` |
| `o-review` | `d-review` decided; a valid `stop-herbal-tea`, `gp-call` and `continue-v2` |

### Decisions

| Decision | Opens when | Correct | Distractors |
|---|---|---|---|
| `d-medical` | weight, swallowing, bleeding, family history and medicines asked; abdomen and complexion examined | `refer-endoscopy` | the emergency department now; "functional, herbs only"; a proton-pump inhibitor first |
| `d-pattern` | tongue, pulse, modifiers, appetite and stools; `d-medical` decided | `spleen-qi-damp` | stomach yin deficiency; liver–stomach disharmony; damp-heat |
| `d-rx-query` | the dispensary query read | `revise`: accept the substance, version 2, cancel version 1, monitoring with the GP | "within the range: dispense as written"; stop the thiazide; give no herbs |
| `d-review` | the GP's results read; drinks and symptoms asked; blood pressure measured | `hidden-liquorice` | "the herbs: stop them all"; "the diuretic: stop it"; "only slightly low: carry on" |

### Execution as state

- **Version 1 (`rx-v1`).** The query becomes readable once it is submitted (`availability.when`).
- **Version 2.** Either `rx-v2-omit` or `rx-v2-reduce` is a valid checklist step once the query has been read.
- **Supply.** `dispense` is valid only after a valid version 2. An attempt before that is intercepted (`g-open-query-intercepted`).
- **Refused answers.** `insist-v1` ("within the range") and `stop-thiazide` are always refused, with the reasons.

### Rubric (17 deterministic items, 33 points; 2 examiner-judged communication items)

| Item | Domain | Weight | Notes |
|---|---|---|---|
| `r-gi-history` | history | 2 | character, modifiers, appetite and stools, cold and heat |
| `r-alarm-screen` | history | 3 | **critical**: weight, swallowing and vomiting, bleeding, family history, medicines, health products |
| `r-four-exam` | examination | 2 | spirit and complexion, tongue, voice, pulse |
| `r-abdomen` | examination | 1 | abdomen and supraclavicular nodes |
| `r-bp` | examination | 1 | blood pressure |
| `r-records` | investigations | 1 | polyclinic results |
| `r-medical` | diagnosis | 2 | `d-medical` first try |
| `r-pattern` | diagnosis | 3 | `d-pattern` first try |
| `r-rx-query` | safety | 3 | **critical**: `d-rx-query` first try and a valid version 2 |
| `r-no-override` | safety | 2 | avoided-harm: no `insist-v1`, no `stop-thiazide` |
| `r-referral` | management | 2 | **critical**: a valid `gp-letter` |
| `r-counsel` | safety | 1 | `counsel-herbs` |
| `r-review-inquiry` | history | 2 | status, drinks and supplements, symptoms, medicines |
| `r-review-exam` | examination | 1 | blood pressure and weight, ankles |
| `r-review` | diagnosis | 3 | **critical**: `d-review` first try |
| `r-stop-source` | safety | 2 | a valid `stop-herbal-tea` |
| `r-gp-today` | management | 2 | a valid `gp-call` |
| `r-comm-patient` | communication | 1 | examiner-judged: his fear of cancer, the referral, the change, no blame at review |
| `r-comm-dispenser` | communication | 1 | examiner-judged: the query treated as a safety check |

### Safety gates

| Gate | Verdict | When |
|---|---|---|
| `g-stop-antihypertensive` | safety-critical (cap 40 %) | `stop-thiazide` |
| `g-query-overridden` | complication | `insist-v1` (refused) |
| `g-open-query-intercepted` | complication | `dispense` attempted before a valid version 2 |

### Paths and their expected outcomes

These are checked by `python3 tools/pack_check.py --paths`. The paths are in `tools/paths/tcm-sg-gi-01.json`.

| Path | Score | Can finish | Critical missed | Gates |
|---|---|---|---|---|
| Reference path (liquorice omitted) | 33/33 = 100 % | yes | — | — |
| Version 2 keeps 炙甘草 at 3 g with monitoring | 100 % | yes | — | — |
| Overrules the query as "within the range", then revises | 85 % | yes | `r-rx-query` | `g-query-overridden` |
| Tells him to stop the thiazide | 40 % (capped) | yes | `r-rx-query` | `g-stop-antihypertensive` |
| Tries to dispense version 1 (intercepted) | 100 % | yes | — | `g-open-query-intercepted` |
| Sends him to the emergency department first | 94 % | yes | — | — |
| Calls it functional dyspepsia first | 94 % | yes | — | — |
| Never writes to the GP | 21/23 = 91 %; the review never opens | **no** | `r-referral` | — |
| At review, "only slightly low" first | 91 % | yes | `r-review` | — |
| At review, blames the formula first | 91 % | yes | `r-review` | — |
| Never asks about herbal teas or supplements at review | 79 % | **no** | `r-review` | — |
| Stops after booking the review | 70 % | no | `r-review` | — |
| Does nothing | 0/21 = 0 % | no | `r-alarm-screen`, `r-rx-query`, `r-referral` | — |

## Reference path (`solution`)

1. `start`.
2. 21 history items.
3. Eight examinations.
4. Read the polyclinic results → `d-medical` (`refer-endoscopy`) and `d-pattern` (`spleen-qi-damp`).
5. `explain-consent` and `rx-v1`.
6. Read the dispensary query → `d-rx-query` (`revise`).
7. `rx-v2-omit`, `dispense`, `counsel-herbs`, `gp-letter`, `diet-advice` and `arrange-review`. The review opens.
8. Five review history items and four review examinations.
9. Read the GP's results, the endoscopy report and the blood-pressure log → `d-review` (`hidden-liquorice`).
10. `stop-herbal-tea`, `gp-call`, `continue-v2` and `finish`.

There are 65 steps in all.

## Clinical numbers check

- **BMI.** 68 kg / (1.68 m)² = 24.1.
- **Blood pressure.**
  - First visit: clinic 148/88 mmHg; home about 145/88; three months ago 142/86.
  - Review: clinic 152/90; GP 154/92; home log week 1 142/86, week 2 152/92.
- **Potassium.** 3.5 mmol/L three months ago, 3.3 at review.
- **Weight.** 68 kg, then 69 kg at review.
- **Version 1 (crude-herb equivalent, g/day).** 党参 15, 白术 12, 茯苓 15, 炙甘草 6, 陈皮 9, 法半夏 9, 木香 6, 砂仁 6.
- **Sachets.** One after lunch and one after dinner for 14 days: 28. He comes on the morning of day 14 with two left, having missed none (26 taken).
- **Version 2.** As version 1 without 炙甘草 (or with 3 g). At review two more weeks are repeated: 28 sachets.

## Facilitator notes

### Debrief questions (PEARLS)

1. **Reactions.** How did it feel when the dispensary held your prescription?
2. **Description.** What exactly did the query say about this patient?
3. **Analysis.**
   - Why is "within the Pharmacopoeia range" not an answer?
   - What was yours to change, and what was the GP's?
   - At review, why did the effect appear when the prescription had no liquorice?
4. **Summary.** Which hidden sources will you ask about by name from now on?

### Common learner errors

| Error | How the case surfaces it |
|---|---|
| Treating "stomach problems" with herbs alone at 63 | `d-medical` feedback; `r-referral` is critical |
| Sending him to the emergency department | `d-medical` feedback; the referral response explains why not |
| "It's within the range" | Refused (`g-query-overridden`); Ms Chua's correction `range-means-safe` |
| Stopping his antihypertensive | Refused; gated safety-critical |
| Supplying before the query is resolved | Intercepted by the version check |
| Blaming the formula at review | `d-review` feedback; he would keep drinking the tea |
| Not asking about herbal teas and snacks | `d-review` stays closed; he does not volunteer it |

## Embodied mode

- **Grounding.** Everything the patient and staff say comes from the case. His potassium a week on and any change to the diuretic are `unknowns`.
- **Where things happen.** He sits on the examination couch of a consulting room. Supply is at the herbal dispensary. The review is back in a consulting room.
- **People.**
  - Ms Chua (`pharmacist`) raised the query and can explain liquorice, thiazides and local herbal teas.
  - Dr Wong (`consultant`) is his polyclinic family physician.
  - Dr Ho (`attending`) supervises and does not decide for the learner.
  - Siti (`nurse`) handles reception and blood pressure.

## Fidelity limits

- **Prescriptions.** As in `tcm-sg-lbp-01`, a prescription is a set of interventions and records, not a versioned object with items and doses (docs/ENGINE_EXTENSIONS.md). Version 2's two forms are two interventions.
- **Liquorice.** Its effect is authored, not modelled: nothing computes glycyrrhizic acid intake or potassium.
- **The GP's reply is authored**, and is the same whatever the learner says.
- **The family.** Only this review exists so far. Other reviews of the same first visit (endoscopy findings, no improvement) would be variants of `sg-gi`.

## Matcher notes

- **Review twins.**
  - `h-rv-status` supersedes `h-presenting` and `h-character`.
  - `h-rv-drinks` supersedes `h-herbal-products`, so the same question at review gets the new answer.
  - `h-rv-symptoms` supersedes `h-cramps`.
  - `h-rv-meds` supersedes `h-meds`.
- **Excludes.** `h-meds` and `h-diet` exclude herbal-tea and supplement words, so those questions reach `h-herbal-products` (or its twin at review).
- **The corpus.** 30 utterances in both languages, all passing the offline matcher.

## References

1. Moayyedi PM, Lacy BE, Andrews CN, Enns RA, Howden CW, Vakil N. ACG and CAG clinical guideline: management of dyspepsia. Am J Gastroenterol. 2017;112(7):988-1013.
2. National Institute for Health and Care Excellence. Gastro-oesophageal reflux disease and dyspepsia in adults: investigation and management (NICE clinical guideline CG184). London: NICE; 2014 (updated 2019).
3. Penninkilampi R, Eslick EM, Eslick GD. The association between consistent licorice ingestion, hypertension and hypokalaemia: a systematic review and meta-analysis. J Hum Hypertens. 2017;31(11):699-707.
4. Deutch MR, Grimm D, Wehland M, Infanger M, Krüger M. Bioactive candy: effects of licorice on the cardiovascular system. Foods. 2019;8(10):495.
5. European Commission, Scientific Committee on Food. Opinion of the Scientific Committee on Food on glycyrrhizinic acid and its ammonium salt. Brussels: European Commission; 2003.
6. Chinese Pharmacopoeia Commission. Pharmacopoeia of the People's Republic of China, Volume I. 2020 ed. Beijing: China Medical Science Press; 2020.
7. World Health Organization. WHO international standard terminologies on traditional Chinese medicine. Geneva: WHO; 2022.
8. Traditional Chinese Medicine Practitioners Board (Singapore). Ethical code and ethical guidelines for TCM practitioners. Singapore: TCMPB.

### To verify

No DOIs are given: none was verified with a lookup in this session.

- The page ranges of references 1, 3 and 4, and the document number of reference 5.
- That ACG/CAG 2017 sets the endoscopy threshold at 60, as worded in `d-medical`. NICE's suspected-cancer guidance (NG12), which CG184 refers to, uses different criteria (55 and over, with weight loss, for urgent endoscopy).
- The SCF's 100 mg/day figure, and the 2020 Pharmacopoeia's minimum glycyrrhizic acid content for 甘草 and 炙甘草. The statement that 6 g "can approach or exceed" the figure rests on these.
- Every herb dose against the 2020 Pharmacopoeia ranges.
- That 廿四味 and the other herbal teas sold in Singapore commonly contain liquorice, and that liquorice plums do.
- Singapore's MOH clinical practice guideline on hypertension: the blood-pressure target of 140/90 that he quotes.

## Changelog

- **0.1.0 (2026-11-07).** First version: phase 2, case 7 (docs/PHASE2.md).

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

**病例概要。** 王先生63岁，退休巴士车长，服氢氯噻嗪与氨氯地平降压。

- 饭后上腹胀满两个月，嗳气、早饱、纳差、便溏；遇冷加重，喜温喜按。
- 报警症状筛查阴性：体重稳定，无吞咽困难、呕吐、出血，无胃癌家族史，不服止痛药。
- 血压148/88 mmHg，三个月前血钾3.5（偏低边缘）。
- 四诊：神疲、面色萎黄、语声低怯；舌淡胖齿痕、苔白微腻；脉缓弱，右关尤弱。

**评估。** 西医：63岁新发消化不良、无报警症状，经家庭医生转介胃镜（非紧急）。中医：脾胃气虚、湿阻气滞，香砂六君子汤加减。

**分歧（第二阶段维度：复核意见分歧）。** 药房对炙甘草6 g提出异议：甘草酸致假性醛固酮增多症，与噻嗪类利尿剂相加。正确回应是就具体风险接受意见，开具第2版（去甘草，或减至3 g并写明监测），作废第1版。以下回应会被拒绝：

- 以“在药典范围内”驳回意见；
- 叫他停降压药。

**复诊。** 胃胀好转，但血钾3.3、血压升高、脚肿、小腿抽筋。来源是每天一瓶廿四味凉茶和甘草梅。正确做法：

- 停凉茶与甘草梅；
- 维持第2版；
- 当天告知家庭医生。

胃镜为轻度慢性胃炎，幽门螺杆菌阴性。

**复盘要点。**

- 审方意见是安全网，要就具体病人回答，并落实到新的处方版本上。
- 改自己的处方，不停别人开的药。
- 寻找隐藏的甘草来源时，要点名问凉茶和零食。
