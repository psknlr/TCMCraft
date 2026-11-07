# Implementation status

How the design ([DESIGN.md](DESIGN.md)) is realised in this repository, what each part maps to in ClinicalCraft today,
and what is still open. Engine work the design needs, and that belongs in ClinicalCraft rather than in this content
pack, is in [ENGINE_EXTENSIONS.md](ENGINE_EXTENSIONS.md).

Engine revision written and checked against: ClinicalCraft `4569808889ca` (`tools/clinicalcraft.rev`).

## Roadmap

| Phase (DESIGN §10) | Status | What exists |
|---|---|---|
| **1. A single longitudinal encounter** | **Built and passing on the engine; awaiting the in-world walk-through and clinical review** | Case `tcm-sg-lbp-01` (three phases, 38 history items, 17 examinations, 7 investigations and records, 23 interventions, 5 decisions, 17 rubric items, 5 safety gates, a 90-step reference path, a 43-utterance matcher corpus); the fictional clinic `tcm-sg-clinic` (3 room templates, 10 equipment types); offline checks and CI against the pinned engine |
| 2. 12-case prototype | Not started | Candidate sources: [CMCR_CORPUS.md](CMCR_CORPUS.md) |
| 3. 60-case engineering pilot | Not started | — |
| 4. Formal benchmark | Not started | — |
| 5. Specialised capabilities | Not started | — |

**Phase 1 acceptance criterion** — "every meaningful action is reflected correctly in the event log and final
state". What has been shown and what has not:

- **Shown offline.** `tools/pack_check.py` replays the reference path and 13 alternative paths through a port of the
  reducer's rules. Every step is accepted where it should be, every intercepted step is recorded as invalid, the
  phases open when they should, every objective and decision completes, and the scores and safety verdicts come out
  as the README tables say.
  - Port fidelity: it reproduces upstream's 100 % on all 20 built-in CMCR cases, and its matcher agrees with
    ClinicalCraft on all 1,579 built-in test utterances.
- **Shown on the engine.** ClinicalCraft at the pinned revision ran in CI (`tools/check.sh` from
  `.github/workflows/check.yml`):
  - `cases validate --strict`: 0 errors, 0 warnings.
  - `cases verify`: the 90-step path, objectives 6/6, decisions 5/5, utterances 43/43, 33/33 (100 %).
  - The offline demonstration (`exec --autopilot`): finished and completed at 100 %.
  - `facilities validate --all`: every file valid. The warnings left say that built-in outpatient cases needing labs
    or imaging cannot be completed in this TCM clinic, and that this case cannot be completed in `clinic-v4`. Both
    are expected: the web does not offer a facility that cannot complete a case.
- **Not yet shown.** The in-world walk-through in the web client, and a model-driven (non-offline) run.

## Design element → implementation

| Design element | In this pack | Mechanism in ClinicalCraft |
|---|---|---|
| Fictional Singapore outpatient TCM centre (§2.1) | `content/facilities/tcm-sg-clinic.json`: waiting hall with registration and an intake kiosk, three consulting rooms (one for reviews), an acupuncture and tuina room, an herbal dispensary with a restricted dispensing area, a store, a bus stop | Facility composed of room templates (`instances`), access zones, staff positions |
| English and Mandarin (§2.1) | Every learner-facing string in zh-CN and en; the patient prefers Mandarin; reception can arrange Malay or Tamil interpretation | `LocalizedText`, `locales: ["zh-CN", "en"]` |
| SGD scenario costs (§2.1) | Fictional fees in the receptionist's brief | NPC knowledge (no structured cost model) |
| Separate professional roles (§2.1, §6) | TCM physician (learner), senior physician (attending), clinic assistant (nurse), TCM dispenser (pharmacist), polyclinic family physician (consultant), reception | NPC briefs with `corrections`; intervention `scope: "medical"` for consent, prescribing, needling and tuina |
| Consent, records, referral (§2.2) | `explain-consent` (evidence and guideline disagreement stated), `acu-document`, `gp-letter`; examiner-judged communication items | Interventions, rubric `judgeGuidance` |
| Local environment (§2.3) | Air-conditioned workplace, rainy days and humidity are history facts that bear on the pattern | Case facts |
| Verifiable execution (§3 C1) | Prescription v1 → dispensary query (a record that exists only after v1) → v2 (two acceptable forms) → supply (version-checked) → counselling → recorded use (dispensing record, sachet count) | Interventions, `checklist` steps (an out-of-order attempt is recorded invalid and applies nothing), `availability.when`, `inOrder`, safety gates |
| Active multimodal evidence (§3 C2, §5.1) | Kiosk photo (failed colour check, warm light, recent coffee) vs. recapture under standard light vs. direct inspection after rinsing; source and quality in `extensions.tcmcraft.evidence` | Record review vs. bedside study vs. examination finding; decision `d-evidence` opens when the photo is read |
| Multiple defensible pathways (§3 C3, §8.2) | Two acceptable versions of the revised prescription (`rx-v2-substitute`, `rx-v2-omit`), optional tuina, either choice on the blood-activating herbs; `extensions.tcmcraft.acceptablePathways`, `unacceptable`, `expertDisagreement` | Rubric conditions with `any`; a `multiple` decision; extension data |
| Longitudinal reasoning from execution history (§3 C4, §5.6) | One-week review: dispensing record, session record, sachet count, adherence, adverse effects, danger signs; `d-followup` separates adherence and exposure from a wrong assessment | Phases with `enterWhen`, phase twins (`supersedes`), records in the simulated timeline |
| Five layers of the patient model (§4.2) | Facts: history, examination and results. Evidence: what was asked, examined, read. Interpretations: decisions. Execution: interventions, flags and records. Longitudinal: follow-up phase items | The session state (`asked`, `examined`, `seen`, `decisions`, `interventions`, `flags`) |
| Not asked / not examined / uncertain / not recorded / absent (§4.2) | `disclosure: "specific"` (aspirin, previous faint, food before arrival), `disclosure: "unknown"` (blood tests), `examNotRecorded`, `unknowns` | Grounding rules (CASE_AUTHORING §1) |
| Explicit action contracts (§4.3) | Each act has prerequisites (`contraindicatedWhen` on checklist steps), effects (`setFlags`), destinations (`acu-position` → treatment room, lying) | Interventions; the session's single tool path |
| Version check, no duplication (§4.3) | `dispense` refuses a version with an open query; `maxDoses: 1` on prescription, supply and needling steps | `checklist`, `maxDoses` |
| Herb identity and product class (§5.2) | 桑寄生 vs 槲寄生 (separate monographs); granules in crude-herb equivalents; CPM vs TMM noted on the dispensing record; a CPM shelf in the dispensary | Record text and catalog (no product model) |
| Herb–drug interaction (§5.2) | Aspirin with 当归 and 川芎: recorded, managed, counselled, the doctor informed; the evidence level stated as mostly theoretical | Decision `d-rx-review`, NPC knowledge |
| AcuCraft level 2 workflow (§5.3) | Suitability (skin, danger signs), consent, clean-technique preparation, lying position (syncope history), needling, withdrawal and count, documentation | Checklist interventions, `inOrder`, safety gates |
| Tuina (§5.4) | Optional adjunct after consent | Checklist intervention |
| Coordination with conventional care (§5.5) | Danger-sign screen, no imaging or referral now, safety-netting; a letter to the polyclinic and heart clinic | Decisions, interventions, consultant NPC |
| Intercepted unsafe orders recorded separately (§8.1) | Invalid `dispense` and `acu-insert` attempts are kept in the record and shown as complication verdicts; unsafe acts are safety-critical verdicts that cap the score | `safetyGates` |
| Safe task completion as primary endpoint (§8.1) | All objectives complete with no safety-critical gate; critical rubric items named first in the debrief | Assessment report |

## Open items for phase 1

1. Walk the case in in-world mode (`npm run cc -- serve --cwd ../TCMCraft`) and check that the patient moves to
   the treatment couch and back, and that the dispensary zone and staff behave.
2. Clinical review by a registered TCM physician and a family physician, then set `provenance.review` honestly.
   The case README lists what is "to verify" (doses, edition and page details, Asarum and granule regulatory status).
3. Images: tongue photos (kiosk vs. standard) with clear licences, local-only if they come from patients.
