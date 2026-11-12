# TCMCraft — Singapore Edition

**An interactive environment for longitudinal, collaborative Traditional Chinese Medicine care.** A learner or
an AI agent works a whole encounter, and every step is recorded as state that can be checked:

**Assessment → the four examinations → disease and pattern assessment → treatment planning → execution →
follow-up and revision.**

TCMCraft is a [ClinicalCraft](https://github.com/psknlr/ClinicalCraft) **content pack**, as
[SurgeryCraft](https://github.com/psknlr/SurgeryCraft) is: plain JSON that ClinicalCraft loads through its
`contentDirs` setting. The design is in [docs/DESIGN.md](docs/DESIGN.md), what is built so far in
[docs/IMPLEMENTATION.md](docs/IMPLEMENTATION.md), and the engine work it still needs from ClinicalCraft in
[docs/ENGINE_EXTENSIONS.md](docs/ENGINE_EXTENSIONS.md).

## Phase 1: one complete Singapore outpatient episode

### `tcm-sg-lbp-01` · 腰痛反复发作 · Recurrent low back pain · 52-year-old man

The case is fictional, set in a community TCM clinic in Singapore, and runs in Mandarin or English. It has three
phases: the first visit, the treatment, and a review a week later. Facilitator guide:
[content/cases/tcm-sg-lbp-01/README.md](content/cases/tcm-sg-lbp-01/README.md) (spoilers).

- **Inquiry and the four examinations.**
  - Danger-sign screen.
  - Inspection: spirit, complexion, build and tongue.
  - Listening and smelling.
  - Palpation: pulse and lumbar.
  - The lower-limb neurological examination.
- **Evidence quality.** The waiting-room kiosk's tongue photo was taken under warm light, without a colour card and
  after a coffee. Using it uncritically leads to the wrong pattern.
- **Disease and pattern assessment.** Biomedical danger signs come first; then the TCM pattern, with the evidence
  for and against it.
- **Prescription as executable state.** Version 1 goes to the dispensary. The dispensary queries it (a herb out of
  stock and a different herb offered; an incomplete medication list). The prescriber issues version 2 — two
  acceptable forms — and only the current version can be dispensed. The patient's aspirin is found, recorded and
  coordinated with his doctor.
- **Acupuncture with explicit prerequisites.** Consent → clean-needle preparation → a lying position (he has fainted
  with needles before) → needling → withdrawal with the needles counted in and out → documentation.
- **Longitudinal review.** The dispensing record, the session record, a sachet count, adherence, adverse effects and
  danger signs separate incomplete adherence from a wrong assessment.

Scoring:

- A rubric of 17 items: 15 deterministic and 2 examiner-judged.
- Five safety gates. Unsafe acts cap the score. Intercepted attempts are recorded separately from the final outcome.
- The reference path scores 100 %, both acceptable prescription pathways score 100 %, and doing nothing scores 0 %.

The review status is **unreviewed** (AI-assisted authoring). It needs review by a registered TCM physician and a
family physician before teaching use.

## Phase 2 (in progress): the 12-case prototype

The plan, coverage and status are in [docs/PHASE2.md](docs/PHASE2.md). 7 of 12 cases are built: all the synthetic
ones. The other five adapt published case reports and wait on the permission question. There are three families:

- `sg-lbp`: one first visit, four reviews;
- `sg-insomnia`: one first visit, two reviews;
- `sg-gi`: its base case.

| Case | Review | Phase 2 dimension |
|---|---|---|
| [`tcm-sg-lbp-01`](content/cases/tcm-sg-lbp-01/README.md) | A — a partial response from missed doses and continuing exposure | uncertain evidence; execution (dispensary query) |
| [`tcm-sg-lbp-02`](content/cases/tcm-sg-lbp-02/README.md) | B — new bilateral sciatica, saddle numbness and urinary hesitancy | alternative follow-up branch: escalation and handover |
| [`tcm-sg-lbp-03`](content/cases/tcm-sg-lbp-03/README.md) | C — he followed the label exactly; the label was wrong | execution discrepancy: incident, correction, open disclosure |
| [`tcm-sg-lbp-04`](content/cases/tcm-sg-lbp-04/README.md) | D — cold-damp has turned to damp-heat, and this time the yellow coating is genuine | alternative follow-up branch: changed condition, prescription version 3 |
| [`tcm-sg-insomnia-01`](content/cases/tcm-sg-insomnia-01/README.md) | A — chronic insomnia in a carer with heavy periods; iron-deficiency anaemia at review | review disagreement: the senior's view, from the intake form alone, resolved by evidence and recorded |
| [`tcm-sg-insomnia-02`](content/cases/tcm-sg-insomnia-02/README.md) | B — a smartwatch and the sleep diary disagree; zolpidem taken with calming herbs | uncertain evidence; herb–drug review |
| [`tcm-sg-gi-01`](content/cases/tcm-sg-gi-01/README.md) | A — the dispensary objects to liquorice in a man on a thiazide; his potassium falls anyway | review disagreement (dispensary); execution: a hidden liquorice source |

Every case's alternative paths state their expected outcome (score, safety gates, critical misses, whether it can
finish), and `tools/pack_check.py --paths` fails when a replay differs.

The [audit of 12 November 2026](docs/AUDIT_2026-11-12.md) is answered in content version 0.2.0:

- the back-pain cases now finish in embodied mode;
- prescription versions are mutually exclusive and need the query answered and the medicines verified;
- needling needs the minimum assessment, and acupuncture can be deferred;
- the emergency handover states only what has been established;
- one policy covers every delaying act at the cauda equina review.

The audit's counterexamples are paths with stated outcomes.

### `tcm-sg-clinic` · TCMCraft Community TCM Clinic (fictional)

A single-storey clinic built from three room templates:

- a waiting hall with registration and the intake kiosk;
- three TCM consulting rooms, each with a pulse pillow, a tongue-imaging station, a records terminal and a case board;
- an acupuncture and tuina room with two face-hole couches, an acupuncture cart, TDP lamps, a sharps bin and a
  needle-count board;
- an herbal dispensary: herb drawer cabinets (百子柜), a granule dispenser, decoction machines, a collection counter
  and a restricted dispensing area;
- a store.

A bus stop is outside. There are ten new equipment types, drawn as voxel parts.

## Layout

```
.clinicalcraft/settings.json          contentDirs → ../content (open this folder as a ClinicalCraft project)
content/
  cases/tcm-sg-lbp-0{1,2,3,4}/        case.json · README.md (facilitator guide); family sg-lbp
  cases/tcm-sg-insomnia-0{1,2}/       family sg-insomnia
  cases/tcm-sg-gi-01/                 family sg-gi
  catalogs/tcmcraft-clinic.json       10 TCM equipment types, 10 materials (bilingual)
  templates/tcm-*.json                consulting room, acupuncture and tuina room, herbal dispensary
  facilities/tcm-sg-clinic.json       the clinic
tools/
  content-gen/                        Python generator that writes content/ (build.py; case_*.py, family.py and *_family.py, clinic.py)
  pack_check.py                       offline checks: schema, integrity, lints, reference-path replay, matcher corpus, facility
  paths/<case id>.json                alternative paths with their expected outcomes (pack_check.py --paths)
  check.sh                            the above, then ClinicalCraft's own validate/verify/demonstration
  clinicalcraft.rev                   the ClinicalCraft commit the pack is checked against
  cmcr_index.py                       writes docs/CMCR_CORPUS.md from the case archive's manifests
docs/                                 DESIGN · IMPLEMENTATION · PHASE2 · ENGINE_EXTENSIONS · CMCR_CORPUS · AUDIT_2026-11-12
CMCR中医案例80篇/                       80 CMCR TCM case reports (ZIP; source material for later phases)
.github/workflows/check.yml           CI: tools/check.sh against the pinned ClinicalCraft
```

## Use it with ClinicalCraft

From a ClinicalCraft checkout next to this repository, at the commit in `tools/clinicalcraft.rev` or a later one:

```bash
npm run cc -- trust --cwd ../TCMCraft
```

```bash
npm run cc -- play tcm-sg-lbp-01 --provider offline --cwd ../TCMCraft
```

```bash
npm run cc -- serve --cwd ../TCMCraft
```

`serve` offers the clinic and the case to the web world.

## Check and regenerate

```bash
python3 tools/content-gen/build.py
```

```bash
python3 tools/pack_check.py --paths
```

```bash
tools/check.sh ../ClinicalCraft
```

- `build.py` rewrites `content/`; `--check` only verifies that it is up to date.
- `pack_check.py` needs no Node.js. Point `CLINICALCRAFT_DIR` at a checkout to include the built-in catalogs.
- `check.sh` runs both, then ClinicalCraft's `facilities validate --all`, `cases validate --strict`, `cases verify`
  and the offline demonstration (`exec --autopilot`) in standard and in embodied mode. Each demonstration must
  finish, complete every objective and score 100 %.

`pack_check.py` ports the parts of ClinicalCraft's checks that decide pass or fail. Its replay reproduces 100 % on
ClinicalCraft's 20 built-in CMCR cases, and its matcher agrees with ClinicalCraft on all 1,579 built-in test
utterances. ClinicalCraft itself remains the authority.

## CMCR 中医案例（80 篇）

[查看压缩包与分包清单](CMCR中医案例80篇/) — 80 published TCM and integrative-care case reports in 29 ZIP files. The
author-facing index, mapped to TCMCraft modules with the data-quality and permission notes, is
[docs/CMCR_CORPUS.md](docs/CMCR_CORPUS.md).

## Disclaimer

Fictional teaching content — not medical advice. Herbs, doses and points in the cases are not for self-treatment.
Scores measure completion of a teaching pathway, not clinical competence.
