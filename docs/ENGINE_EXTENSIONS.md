# Engine extensions TCMCraft needs from ClinicalCraft

The design (DESIGN §1, §10) keeps TCM knowledge in this content pack and puts mechanisms that other clinical
domains could use into the shared engine. Phase 1 was built with what ClinicalCraft offers today (revision
`4569808889ca`). The workarounds it uses, and the engine features that would replace them, are listed below in
rough priority order.

Each item says what phase 1 does now, why that is not enough, and a proposed shape that follows ClinicalCraft's
conventions: zod schema first, a pure engine in `core`, one tool path in `agent`, conditions usable in rubrics, and a
doc contract. None of this is implemented here; a ClinicalCraft change would carry it.

## 1. Capability vocabulary for TCM

- **Now.** `CAPABILITIES` has no TCM entries. A non-canonical capability is a parse warning, which fails
  `cases validate --strict`. So the case requires only canonical capabilities (`records`, `medications`,
  `reflex-hammer`). The acupuncture cart, tongue-imaging station, TDP lamp and decoction machine are drawn and
  tagged, but they gate nothing: in in-world mode, needling needs only the clinician at the patient.
- **Proposed.** Add these capabilities: `acupuncture` (sterile needles and a sharps bin at the couch),
  `tongue-imaging` (standard light and colour card), `moxibustion`, `cupping`, `tuina-couch`, `tcm-dispensing`
  (herb cabinet or granule dispenser) and `decoction`. Then give the case's `acu-insert`, `tuina` and
  `tongue-recapture` their real kit.
- **Found by the 2026-11-12 audit.** Six of the ten TCM equipment types have `interaction.kind = none` and none
  has a device `behavior`, so in embodied mode dispensing succeeds at the patient's side without anyone operating
  the herb cabinet or the granule dispenser. A pharmacy skills station (identify the medicinal, select the active
  version, dispense, check the label, each error recorded) needs device behaviours wired to the prescription
  object of §2.

## 2. Prescriptions as versioned, executable objects

- **Now.** Version 1, version 2 (two forms), supply and counselling are separate interventions. The version check is
  a `checklist` step's `contraindicatedWhen`, and the dispensary's query is a record that appears once version 1
  exists. This cannot represent:
  - items, doses, units and routes as data, or catch a unit error at item level;
  - a third version, or a query raised by the dispensary on its own;
  - stock, batch, expiry or an inventory transaction;
  - idempotent tool requests: a retried "dispense" is only stopped by `maxDoses`.
- **Proposed.** A `prescriptions` section in the case and a `prescription` action family, modelled on
  `StudyOpSchema`:

  ```text
  draft {items[], route, frequency, duration, form} → submit (version n) → review {by, findings[]}
    → revise (version n+1, supersedes n) | confirm → dispense {version, lines[{item, product, batch, qty}]}
    → counsel → use (reported adherence, returned quantity)
  ```

  - Requests are idempotent by key, as studies are. A dispense names a version, and the reducer refuses a superseded
    or unreviewed one.
  - Condition leaves would include `{ "prescription": { "version": 2, "status": "dispensed" } }` and
    `{ "dispensed": { "item": "…", "matches": "current-version" } }`.
  - The facility's dispensary devices (`behavior` with `clinical: { tool: "dispense" }`) would act through it, and a
    catalog of medicinal products would carry identity, part used, processing, form, the Singapore class
    (CPM / TMM) and synonyms.
- **What the pack does meanwhile (audit 2026-11-12).** Mutually exclusive versions: each form of version 2 is
  refused once the other is valid, and signing needs the query answered and the medicines verified. The review then
  follows the version dispensed through gated actions: tcm-sg-gi-01's version 3 exists only when version 2 kept
  liquorice. What it cannot do is *say* which version was supplied in a single record. A record's text cannot vary
  with what was signed, and two version-specific records with one name would not work either: the record lookup
  (`retrieveReport`) takes the first record whose name matches, available or not. So the dispensing records name the
  version without listing its ingredients.

## 3. Evidence with source, time and quality

- **Now.** The kiosk photo, the recapture and direct inspection are three items. Their source and quality are prose,
  plus `extensions.tcmcraft.evidence`, which the engine ignores. Results have no images yet.
- **Proposed.**
  - Optional `provenance` on results and exam findings, with fields for source (patient-captured, clinician-captured,
    clinician-authored description, device measurement, agent interpretation), captured-at and quality (passed or
    failed, with reasons). Front ends would show it, and agents' tools would return it.
  - A tongue-capture study profile (STUDIES.md) whose model reads the patient's state and the acquisition
    conditions: light, colour card, recent food or drink.
  - Pulse waveforms and voice recordings as media assets with the same provenance.

## 4. Structured interpretations and multiple acceptable solutions

- **Now.** The disease and pattern assessments are single-best-answer decisions; the acceptable alternatives
  (versions, tuina, herb choices) are rubric `any` conditions; and expert disagreement lives in extension data.
- **Proposed.**
  - An `assess` action that records a hypothesis with its framework (zang-fu, bi-syndrome, six channels…),
    supporting and conflicting evidence references, and certainty.
  - Case-level `acceptableSolutions`: sets of interpretations and plans, each with the evidence that must have been
    acquired. The rubric could then score "an acceptable solution, supported by evidence the learner actually
    had", and report disagreement without changing facts.

## 5. Acupuncture as a procedure

- **Now.** Needling is one checklist step after consent, preparation and positioning, and the needle count is one
  step.
- **Proposed.** A needling procedure in the PROCEDURE.md family:
  - points as anatomical landmarks on a regional body model (AcuCraft level 3);
  - needles as counted entities with identity, by analogy with SurgeryCraft's swab count (TEAM.md §4.3): inserted,
    retained, withdrawn, disposed;
  - patient feedback events during retention (deqi, pain, pre-syncope) and their responses;
  - site checks (skin integrity, bleeding risk) as prerequisites.

## 6. Longitudinal episodes

- **Now.** "One week later" is a phase. The clock is static, and the follow-up evidence is one authored branch.
- **Proposed.**
  - Episodes with simulated calendar time between them, and scheduled follow-up created by an act.
  - Between-episode processes, such as adherence and exposure, that produce the follow-up evidence from the
    execution record: what was actually dispensed and taken.
  - An explicit label for each outcome source (recorded, authored branch, calibrated model), as DESIGN §5.6 asks.

- **Found by the 2026-11-12 audit.** Facts that depend on what was done. A history answer or an examination
  finding can vary by phase only, so a follow-up cannot describe the treatment actually received. The back-pain
  reviews are therefore written to hold whether or not he was needled, and only the session record, gated by
  `availability.when`, depends on it.
- **Also found.** Conditions cannot see *when* a refused attempt was made (`intervened` with `valid: false` has no
  phase or order, and `inOrder` counts valid attempts only). So a tuina refused at the first visit and one refused at
  the review are the same fact, and "was the transfer delayed?" cannot be measured in minutes on a static clock.
  - A `phase` (or `after`) qualifier on `intervened` would fix the first.
  - Simulated time would fix the second.

## 7. Autonomous outpatient roles

- **Now.** The dispenser, assistant and senior physician are NPC briefs. The dispensary's query is authored, not
  raised by an agent.
- **Proposed.** Extend the care-team scheduler (TEAM.md) beyond theatre: a dispensary role policy that reviews a
  submitted prescription against stock and the medication record and raises a task for the prescriber, and an
  assistant policy that prepares the treatment room and fetches the cart.

## 8. TCM benchmark suite

- **Now.** `cases verify` and the offline demonstration.
- **Proposed.** `bench/tcm-v1` scenarios: the base episode and its evidence-quality, escalation and
  non-improvement variants, all kept in one case family. Hidden facts and future outcomes would be sealed from the
  agent. Reporting would follow DESIGN §8: safe task completion, critical errors, resource use, and expert ratings
  kept separate from automated scores.
