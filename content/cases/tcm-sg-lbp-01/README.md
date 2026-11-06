# tcm-sg-lbp-01 — Recurrent low back pain · 52-year-old man

## Case card

| | |
|---|---|
| Setting | Outpatient — a fictional Singapore community TCM clinic |
| Facility | `tcm-sg-clinic` (this pack: `content/facilities/tcm-sg-clinic.json`) |
| Difficulty | ★★★ (3/5) |
| Estimated time | 45 minutes |
| Specialty | Traditional Chinese medicine, acupuncture, musculoskeletal |
| Languages | 简体中文 (source), English |
| Phases | First visit: history and four examinations → first visit: prescription, review and acupuncture → review one week later |
| Review status | **Unreviewed** — AI-assisted authoring against the cited guidance; not yet editorially reviewed or reviewed by a licensed clinician. Have a registered TCM physician and a family physician review it before teaching use. |
| Provenance | Synthetic (fictional patient, clinic, prices and products) |

## Learning outcomes

1. Screen recurrent low back pain for danger signs and nerve-root involvement, and decide with reasons that imaging and referral are not needed now (NICE NG59).
2. Judge the quality of multimodal evidence: recognise a stained or poorly lit tongue photo and obtain a reliable view before using it for pattern differentiation.
3. Differentiate cold-damp obstruction with liver–kidney insufficiency from damp-heat and blood-stasis lumbago using all four examinations, stating the evidence for and against.
4. Resolve a dispensary query as a versioned prescription change, and reconcile a concurrent antiplatelet medicine before supply, keeping the patient's doctor informed.
5. Deliver an acupuncture session with consent, clean needle technique, a position that guards against fainting, and needles counted in and out.
6. At review, use the execution record to separate incomplete adherence and continuing exposure from a wrong assessment, without unnecessary escalation.

## Clinical summary (spoilers)

Mr Tan Wee Liang (pseudonym), 52, an operations supervisor who sits for long hours in a cold, air-conditioned control room and works two night shifts a week, has had low back pain on and off for three years. This flare began three weeks ago after he helped his mother move a cupboard.

- **Disease assessment.** Recurrent non-specific (mechanical) low back pain with non-radicular referral to the right buttock. There are no danger signs: no leg numbness or weakness, no bladder, bowel or saddle symptoms, and no fever, weight loss, cancer or steroids. Straight-leg raise is 80° on both sides without leg pain, and the lower-limb neurological examination is normal.
- **Pattern.** TCM disease: lumbago (腰痛). Pattern: cold-damp obstruction (寒湿痹阻) with underlying liver–kidney insufficiency (肝肾不足).
  - Cold-damp: a cold, heavy ache, worse in cold and damp and better with warmth; he feels the cold and prefers hot drinks; his lower back is cool to touch.
  - Liver–kidney insufficiency: three years of recurrence, sore and weak knees, weak chi pulses, and a pale, swollen, tooth-marked tongue with a thin white greasy coating.
- **The evidence trap.** The intake kiosk's tongue photo shows a thick yellow-brown coating. It was taken under warm light without a colour card, twenty minutes after a kopi and kaya toast, and the kiosk itself flagged that the colour check failed. A direct look after a rinse, or a standard recapture, shows a white coating.
- **Medicines.** Amlodipine 5 mg and atorvastatin 20 mg, which he volunteers, and **aspirin 100 mg** taken since a coronary stent four years ago, which he mentions only when asked specifically, or which can be read on the polyclinic printout he brought. He also has a history of **needle syncope**: he nearly fainted sitting up for acupuncture two years ago, on an empty stomach.
- **Plan.**
  - Self-management: stay active, stretches, sitting breaks, keep warm.
  - Herbs: modified 独活寄生汤 as concentrated granules for 7 days.
  - Acupuncture: BL23, BL25 and BL40 bilaterally, right GB30 and local Ashi points; 10 needles, retained for 20 minutes, with him lying prone.
  - Coordination: a letter to his polyclinic and heart-clinic doctors.
- **The dispensary query.** The dispensary holds prescription version 1 because 桑寄生 is out of stock (槲寄生 is offered, but it is a different medicinal) and because the medication field is incomplete. The prescriber issues **version 2** — naming 槲寄生, or leaving 桑寄生 out — and records aspirin. Only then is the medicine supplied.
- **Review at one week.** His pain is down from 6 to 4 out of 10, but the gain has not held. The sachet count shows 6 of 14 left: he missed evening doses on night shifts. He also stopped the stretches and still sits in the cold. There is a small, painless bruise at the BL40 site and no danger signs. The assessment stands; the plan for carrying it out is revised: dosing fitted to his shifts, reminders, a jacket and sitting breaks, and the acupuncture course continued.

## Scenario timeline

Static clock (`clock.mode: "static"`); the phases stand for time.

| Phase | Opens | Where | What happens |
|---|---|---|---|
| `consult` — first visit: history and four examinations | at start | Consulting room 1 (seated on the examination couch) | History, four examinations, the kiosk photo, the polyclinic printout, the tongue recapture, three assessment decisions |
| `treatment` — first visit: prescription, review and acupuncture | automatically once `d-disease` and `d-pattern` are answered correctly | Consulting room, dispensary; the patient moves to the treatment room when positioned for needling | Consent, prescription v1 → dispensary query (a record that exists only after v1 is submitted) → v2 → supply → counselling → acupuncture → documentation → booking |
| `followup` — review one week later | automatically once the medicine was validly supplied, the needles validly withdrawn and counted, and the review booked | Consulting room | Status, adherence, adverse effects, danger signs, the dispensing and session records, the sachet count, the review decision and plan |

No physiology model and no monitor: an outpatient TCM clinic has none. Vital signs are an examination finding.

## Decisions and assessment

### Objectives (task list)

1. Take the history and screen for danger signs.
2. Complete the four examinations and the physical screen.
3. Weigh the evidence and make the diagnosis and pattern assessment (`d-evidence`, `d-disease`, `d-pattern`).
4. Prescribe, resolve the dispensary's query and supply the medicine (`d-rx-review`, valid `dispense`, `counsel-herbs`).
5. Give the first acupuncture session safely and book the review.
6. One-week review: check what was actually done and revise the plan (`d-followup`, `adherence-plan`, `continue-course`).

### Decisions

| Decision | Kind | Opens when | Correct |
|---|---|---|---|
| `d-evidence` | single | the kiosk photo has been read | Treat it as unreliable; ask about food and drink; re-inspect or recapture after a rinse |
| `d-disease` | single | danger-sign questions, neuro exam and SLR done | Non-specific LBP, no red flags, no imaging or referral, with safety-netting |
| `d-pattern` | single | `d-evidence` answered; tongue (direct or recaptured), pulse, modifiers and cold–heat asked | Cold-damp obstruction with liver–kidney insufficiency |
| `d-rx-review` | multiple | dispensary query read; aspirin found (asked or read) | New signed version (substitute or omit) **and** record aspirin, manage the blood-activating herbs, counsel, inform his doctor |
| `d-followup` | single | status, adherence, adverse effects and danger signs asked; sachets counted; neuro re-checked | Partial response from adherence and exposure; keep the assessment, adapt the plan, continue |

### Execution as state

ClinicalCraft has no prescription object yet ([docs/ENGINE_EXTENSIONS.md](../../../docs/ENGINE_EXTENSIONS.md)), so the case models the prescription lifecycle with interventions, records and checklist steps.

- **Version 1** is `rx-draft`, which can be given once.
- **The dispensary query** is the record `dispensary-query`. Its `availability.when` is `{"intervened": "rx-draft"}`, so it does not exist until version 1 has been submitted.
- **Version 2** is either of two acceptable pathways: `rx-v2-substitute` (naming 槲寄生) or `rx-v2-omit` (leaving 桑寄生 out). Each is a checklist step that is valid only after the query has been read.
- **Supply** is `dispense`, a checklist step and the *version check*. An attempt while no valid version 2 exists is recorded as an invalid attempt: nothing is supplied, it uses none of the step's doses, and it is shown in the verdict (`g-outdated-version-intercepted`).
- **Needling** is `acu-insert`, a checklist step whose prerequisites are consent, clean-technique preparation and a lying position. An attempt without them is intercepted (`g-needling-refused`).
- **Withdrawal** is `acu-remove`, the needle count. It is valid only after a valid insertion.

### Rubric (15 deterministic items, 33 points; 2 examiner-judged communication items)

| Item | Domain | Weight | Notes |
|---|---|---|---|
| `r-redflags` | history | 3 | **critical**: neuro, bladder/bowel/saddle and systemic questions plus the neuro exam |
| `r-inquiry` | history | 2 | site, modifiers, cold–heat, knees, past history, medicines |
| `r-antithrombotic` | safety | 2 | aspirin found (asked specifically, or the printout read) |
| `r-four-exam` | examination | 2 | inspection, tongue, listening/smelling, pulse, lumbar palpation |
| `r-evidence` | investigations | 2 | `d-evidence` first try and a reliable look at the tongue |
| `r-disease` | diagnosis | 2 | `d-disease` first try |
| `r-pattern` | diagnosis | 3 | `d-pattern` first try |
| `r-rx-review` | management | 2 | `d-rx-review` first try |
| `r-rx-version` | safety | 3 | **critical**: valid supply, no verbal swap |
| `r-acu-sequence` | safety | 3 | consent → preparation → lying → needling → withdrawal and count, by committed sequence |
| `r-needle-count` | safety | 3 | **critical**, scored once needles went in |
| `r-self-management` | management | 1 | stay active, exercise, posture, warmth |
| `r-no-imaging` | efficiency | 1 | avoided-harm item, scored once `d-disease` is attempted or imaging is referred |
| `r-coordination` | management | 1 | letter to his polyclinic and heart-clinic doctors |
| `r-followup` | management | 3 | `d-followup` first try, adherence plan, no relabelling, no dose doubling; scored once the review opens (or a wrong step is taken) |

### Safety gates

| Gate | Verdict | When |
|---|---|---|
| `g-unauthorised-substitution` | safety-critical (cap 40 %) | `rx-verbal-swap` |
| `g-needles-unaccounted` | safety-critical (cap 40 %) | valid needling without a valid withdrawal and count |
| `g-stop-antiplatelet` | safety-critical (cap 40 %) | `stop-aspirin` |
| `g-outdated-version-intercepted` | complication | an invalid `dispense` attempt (version check refused it) |
| `g-needling-refused` | complication | an invalid `acu-insert` attempt (prerequisites missing) |

### How paths score

Replayed with `python3 tools/pack_check.py --paths` (paths in `tools/paths/tcm-sg-lbp-01.json`):

| Path | Score | Critical missed | Gates |
|---|---|---|---|
| Reference path | 33/33 = 100 % | — | — |
| Version 2 leaves 桑寄生 out (the other acceptable pathway) | 100 % | — | — |
| Adds tuina after consent | 100 % | — | — |
| Reads the kiosk photo at face value first | 94 % | — | — |
| Calls damp-heat first | 91 % | — | — |
| Agrees the substitution by phone first | 40 % (capped) | `r-rx-version` | `g-unauthorised-substitution` |
| Tries to dispense version 1 first (intercepted) | 100 % | — | `g-outdated-version-intercepted` (complication) |
| Tries to needle before positioning (intercepted) | 100 % | — | `g-needling-refused` (complication) |
| Never withdraws and counts the needles | 40 % (capped); the review never opens | `r-needle-count` | `g-needles-unaccounted` |
| Advises stopping aspirin | 40 % (capped) | — | `g-stop-antiplatelet` |
| Refers for MRI | 97 % | — | — |
| Relabels damp-heat at review | 91 % | — | — |
| Stops after booking the review | 91 %; the case cannot finish | — | — |
| Does nothing | 0/26 = 0 % | `r-redflags`, `r-rx-version` | — |

Intercepted attempts cost no points by design. The interception is the system working, and it is recorded as its own line in the verdict: the original error, the interception and the final outcome are kept apart, as the design asks (docs/DESIGN.md §8.1).

## Reference path (`solution`)

1. `start`.
2. 31 history items.
3. 11 consult-phase examinations.
4. Read the kiosk photo → `d-evidence` (`recheck`).
5. Direct tongue inspection, the standard recapture and the polyclinic printout.
6. `d-disease` (`nslbp`) and `d-pattern` (`cold-damp`). The treatment phase opens.
7. Self-management advice, consent and prescription version 1.
8. Read the dispensary query → `d-rx-review` (`new-version` + `aspirin-managed`).
9. `rx-v2-substitute`, `dispense`, `counsel-herbs` and `gp-letter`.
10. `acu-prep`, `acu-position`, `acu-insert`, `acu-remove`, `acu-document` and `arrange-followup`. The follow-up phase opens.
11. Six follow-up history items and five follow-up examinations.
12. Read the dispensing record, the session record and the sachet count → `d-followup` (`adherence`).
13. `adherence-plan`, `continue-course` and `finish`.

## Clinical numbers check

- **BMI.** 78 kg / (1.70 m)² = 27.0.
- **Pain.** 6/10 at the first visit, 4/10 at review.
- **Sachets.** 7 days × 2 = 14. Taken: 7 morning + 1 evening = 8. Left: 6. That is 6 missed doses: 2 on night shifts and 4 forgotten evenings. His own "three evenings" understates it, which is kept deliberately and noted on the result.
- **Needles.** BL23 ×2, BL25 ×2, BL40 ×2, GB30 ×1, Ashi ×3 = 10 in, 10 out.
- **Formula (crude-herb equivalent, g/day).** 独活 9, 桑寄生 15, 杜仲 10, 牛膝 10, 秦艽 9, 防风 9, 桂枝 6, 茯苓 15, 当归 9, 川芎 6, 白芍 12, 熟地黄 12, 党参 12, 炙甘草 6. Each dose is within the usual ranges authors work from; check them against the Pharmacopoeia (see *To verify*).

## Facilitator notes

### Debrief questions (PEARLS)

1. **Reactions.** How did it feel to discover the aspirin only after the dispensary asked?
2. **Description.** Walk me through the evidence you used for the pattern. Which pieces did you trust, and why?
3. **Analysis.**
   - What made the kiosk photo unreliable? How would you have known without the kiosk's own flag?
   - Why is "槲寄生 is close enough" a prescription change and not a dispensing decision?
   - What would have made you refer him urgently, and what did you tell him to watch for?
   - At review, what told you this was an execution problem rather than an assessment problem?
4. **Summary.** Name one habit you will change in your own practice.

### Common learner errors and how the case surfaces them

| Error | How the case surfaces it |
|---|---|
| Damp-heat from the kiosk photo | `d-evidence` and `d-pattern` feedback; Dr Ho's correction (`photo-damp-heat`) |
| Missing the aspirin | It is `specific` disclosure; the dispensary's second query point; `r-antithrombotic` |
| A verbal "just swap it" | `rx-verbal-swap` is contraindicated with a harm text; the safety-critical gate; Mr Lim's correction (`herb-identity`) |
| Needling him sitting up | `acu-insert` is refused until he is lying (the prior faint is `specific` disclosure, but the prerequisite holds regardless) |
| "No acupuncture on aspirin" | Dr Ho's correction (`aspirin-no-acupuncture`); `d-followup` feedback |
| Stopping aspirin | Contraindicated, with a safety-critical gate; Mr Lim's and Dr Wong's corrections |
| Escalating at review (new pattern, MRI, double dose) | `d-followup` options and their feedback; contraindicated interventions |

## Embodied mode

- **Grounding.** Everything the patient and staff say comes from the case. Unrecorded facts (his blood results, the product manufacturer, long-term outcome) are `unknowns`, and his last blood tests are a `disclosure: "unknown"` item.
- **Where things happen.**
  - He starts seated on the examination couch of consulting room 1.
  - `acu-position` moves him onto a couch in the acupuncture and tuina room (`destination: {"roomKind": "rehabilitation"}`, `posture: "lying"`).
  - The follow-up phase brings him back to a consulting room (`location: {"roomKind": "consult"}`).
- **Kit.** Records (`records`) are read at a records terminal: every consulting room has one, and the dispensary has the review terminal. Supply (`medications`) is at the herbal dispensary: the herb cabinets and the granule dispenser. The case requires only canonical ClinicalCraft capabilities. The acupuncture cart, tongue-imaging station and TDP lamps are drawn and tagged, but they do not yet gate the acts, because the capability vocabulary has no TCM entries ([docs/ENGINE_EXTENSIONS.md §1](../../../docs/ENGINE_EXTENSIONS.md)).
- **Scope of practice.**
  - Consent, prescriptions, needling, needle withdrawal, tuina and the letter are `scope: "medical"`: a registered practitioner's acts.
  - The clinic assistant (role `nurse`) prepares the room and helps him lie down, and never needles.
  - The dispenser (role `pharmacist`) reviews and fills only the current version.

## Fidelity limits

- **Prescriptions.** A prescription is a set of interventions and records, not an object with items, units and versions. Dose and unit errors therefore cannot be made or caught at item level.
- **Evidence.** Tongue and pulse findings are authored text; there are no images, audio or pulse waveforms yet. The kiosk photo is described, not shown.
- **Acupuncture.** Points are named, not located on a body model. The needle count is one step, not item-by-item identity as in SurgeryCraft's surgical count.
- **One episode.** The review is a single authored branch. The escalation and non-improvement variants of docs/DESIGN.md §7 are future cases in the same case family.
- **Static clock.** Durations (20-minute retention, one week) are narrative, not simulated time.

## Matcher notes

- Follow-up items are phase twins. `h-fu-status` supersedes `h-presenting`, `h-severity` and `h-character`; `h-fu-redflags` supersedes `h-redflag-neuro` and `h-redflag-ce`; `h-fu-adverse` supersedes `h-bruising`. Twins carry only "now"-phrasings, so first-visit questions are never answered by follow-up items.
- `h-meds` excludes aspirin, blood-thinner, herb and granule words, so those questions reach `h-antithrombotic`, `h-herbs-supplements` or `h-fu-adherence`.
- `h-urine-stool` (TCM 二便 inquiry) and `h-redflag-ce` (control and saddle) exclude each other's words.
- The corpus has 43 utterances in both languages, with every required item paraphrased. `cases verify` passes all 43; the matcher port in `tools/pack_check.py`, which agrees with ClinicalCraft on all 1,579 utterances of the built-in cases, checks them offline.

## References

1. National Institute for Health and Care Excellence. Low back pain and sciatica in over 16s: assessment and management (NICE guideline NG59). London: NICE; 2016 (updated 2020).
2. Qaseem A, Wilt TJ, McLean RM, Forciea MA; Clinical Guidelines Committee of the American College of Physicians. Noninvasive treatments for acute, subacute, and chronic low back pain: a clinical practice guideline from the American College of Physicians. Ann Intern Med. 2017;166(7):514-30.
3. Foster NE, Anema JR, Cherkin D, Chou R, Cohen SP, Gross DP, et al. Prevention and treatment of low back pain: evidence, challenges, and promising directions. Lancet. 2018;391(10137):2368-83.
4. World Health Organization. WHO benchmarks for the practice of acupuncture. Geneva: WHO; 2020.
5. World Health Organization. WHO international standard terminologies on traditional Chinese medicine. Geneva: WHO; 2022.
6. Chinese Pharmacopoeia Commission. Pharmacopoeia of the People's Republic of China, Volume I. 2020 ed. Beijing: China Medical Science Press; 2020.
7. Traditional Chinese Medicine Practitioners Board (Singapore). Ethical code and ethical guidelines for TCM practitioners. Singapore: TCMPB.
8. Health Sciences Authority (Singapore). Chinese proprietary medicines: overview. Singapore: HSA.

### To verify

No DOIs are given: none was verified with a lookup in this session.

- The page ranges and issue numbers of references 2 and 3, and the edition and year of reference 7.
- Every herb dose against the 2020 Chinese Pharmacopoeia ranges, including 槲寄生 at 15 g as a replacement.
- The regulatory status in Singapore of Asarum (细辛), omitted from the teaching formula, and the classification of single-herb granule products (CPM or TMM).
- That the WHO acupuncture benchmarks cover the fainting precautions as worded in teaching point 4. The point now says "see" rather than attributing the wording.
- The TDP lamp distance in the catalog's usage text.

## Changelog

- **0.1.0 (2026-11-06).** First version: the phase 1 episode of docs/DESIGN.md.

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

`tools/check.sh` runs ClinicalCraft's `cases validate --strict`, `cases verify`, `facilities validate --all` and the offline demonstration against the pinned ClinicalCraft revision.

Last engine run (ClinicalCraft `4569808`, CI): `cases validate --strict` 0 errors and 0 warnings; `cases verify` 90 steps, objectives 6/6, decisions 5/5, utterances 43/43, 33/33 (100 %); offline demonstration finished and completed at 100 %.

## 中文摘要

**病例概要。** 陈先生（化名），52岁，物流公司运营主管，长期在冷气很强的控制室久坐、每周两个夜班。腰痛反复发作3年，这次搬柜子后加重3周。

- **西医判断。** 复发性非特异性腰痛，伴臀部牵涉痛，无红旗征、无神经根受累。
- **中医诊断。** 腰痛，证属寒湿痹阻、兼肝肾不足。
- **证据陷阱。** 自助机舌象照片在暖光、无色卡、刚喝过咖啡的情况下拍摄，显示黄厚苔；漱口后在标准光下为白腻苔。
- **用药。** 患者主动只说了降压药和降脂药；阿司匹林100 mg（冠脉支架术后）要追问或看自带的用药清单才能发现。
- **晕针史。** 两年前空腹坐位针灸时差点晕倒。

**学习目标。**

1. 筛查危险信号，判断无需影像或转诊。
2. 评估舌象证据质量。
3. 四诊合参，鉴别寒湿与湿热、瘀血腰痛。
4. 把药房审方意见作为新版本处方处理，并在发药前核实抗血小板药。
5. 按同意、准备、卧位、进针、出针核对的顺序完成针灸。
6. 复诊时依据执行记录区分依从性问题与辨证错误。

**关键决策。**

- 舌象照片要重新采集。
- 无红旗征，不做影像。
- 证属寒湿痹阻兼肝肾不足。
- 处方改动由处方医师签发新版本（换用槲寄生或去掉桑寄生均可），补记阿司匹林并告知主诊医生。
- 复诊维持辨证，按班次调整服药和自我管理，继续疗程。

**复盘要点。**

- 证据有来源、时间和质量。
- 处方是有版本的执行对象，药房只按现行版本调剂。
- 有晕针史者取卧位，出针时核对针数。
- 不能让患者自行停用支架术后的阿司匹林。
- 疗效有限时先核对“实际发生了什么”，再判断是不是辨证问题。
- 针灸的推荐因指南而异（ACP 2017 列为选项，NICE NG59 不推荐），知情同意时要如实说明。
