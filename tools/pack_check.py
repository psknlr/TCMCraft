#!/usr/bin/env python3
"""Offline checks for the TCMCraft content pack — a dependency-free approximation of ClinicalCraft's own.

ClinicalCraft is the authority: `tools/check.sh` runs its `cases validate --strict`, `cases verify` and
`facilities validate` against this pack. This script exists so the pack can be checked where the engine
cannot be run, and it mirrors the engine's rules closely enough to catch most authoring errors first:

* cases — schema shape (required fields, enums, bilingual text, id syntax), referential integrity of every
  condition, the reference `solution` replayed through the reducer's rules (phase locks, phase twins,
  record availability, checklist steps, decision requirements, automatic phase transitions, objectives,
  `finish`), the rubric score of the reference path and of doing nothing, safety gates, the content lints of
  docs/CASE_AUTHORING.md §9.8, and the matcher regression corpus (`extensions.testUtterances`) scored with a
  port of the offline history matcher (`packages/core/src/engine/text.ts`, `matcher.ts`, `cli/src/cases.ts`);
* catalogs, room templates and facilities — ids, materials, parts inside footprints, compiled instance
  rects, patient-slot references and every capability a pack case needs.

Usage: python3 tools/pack_check.py [--clinicalcraft PATH] [--paths]   (exit 1 on any error)
`--clinicalcraft` (default `$CLINICALCRAFT_DIR` or ../ClinicalCraft) supplies the built-in catalogs.
`--paths` also replays the alternative paths in tools/paths/<case id>.json (the README score table).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"

errors: list[str] = []
warnings: list[str] = []


def err(where: str, msg: str) -> None:
    errors.append(f"error   {where}: {msg}")


def warn(where: str, msg: str) -> None:
    warnings.append(f"warning {where}: {msg}")


# =============================================================================================
# Text normalisation and phrase scoring (port of packages/core/src/engine/text.ts)
# =============================================================================================

STOP = set(
    (
        "a an the and or but if so of in on at to for from with without by as about into onto over under up down out off "
        "is are was were be been being am do does did done doing have has had having will would shall should can could may might must "
        "i me my mine myself you your yours yourself he him his she her hers it its we us our ours they them their theirs "
        "this that these those there here what which who whom whose when where why how "
        "any some all each every no not nor than then too very just also only ever again more most much many such own same "
        "please tell let get got go going okay ok yes yeah hi hello doctor patient sir madam mr mrs ms dr "
        "like anything something everything"
    ).split()
)
SUFFIXES = [("ingly", ""), ("edly", ""), ("ies", "y"), ("ied", "y"), ("ing", ""), ("ed", ""), ("es", ""), ("ly", ""), ("s", ""), ("e", "")]
LEMMAS = {"med": "medication", "medicin": "medication", "medicat": "medication", "prescription": "prescrib", "abdominal": "abdomen", "cardiovascular": "cardiac"}
SHORT_STEM_ENDINGS = {"s", "es", "ed", "d", "ing", "er", "ers", "y", "ly", "ily", "ful", "fully", "ness", "nes", "less", "les", "ish", "ie", "ies", "ier", "iest", "e", "en"}
GENERIC_CJK_BIGRAMS = {"怎么", "什么", "有没", "没有", "是不", "不是", "会不", "能不", "要不", "哪里", "哪儿", "多少", "为什", "时候", "这个", "那个", "一下"}
FUNCTION_CHARS = set("的了吗呢吧啊呀嘛么什怎哪谁几多少有没是不会能要可以在现这那些个一下还都也就又再过得着你我他她它们您请问说讲想看时候很太最近平常经曾已之前后样为因所对把被给跟和与或者如果该应自己好")
PARTICLES = set("过了着的地得吗呢吧啊呀嘛")
MATCH_THRESHOLD = 0.34
EXCLUDE_FACTOR = 0.2
SELECT_THRESHOLD = 0.55
SELECT_RELATIVE = 0.25
MAX_SELECTED = 3


def half_width(text: str) -> str:
    return "".join(chr(ord(ch) - 0xFEE0) if 0xFF01 <= ord(ch) <= 0xFF5E else ch for ch in text)


def normalize_query(text: str) -> str:
    return re.sub(r"\s+", "", half_width(text).lower())


def compact_text(text: str) -> str:
    return "".join(ch for ch in normalize_query(text) if unicodedata.category(ch)[0] not in "PS")


def is_han(ch: str) -> bool:
    o = ord(ch)
    return 0x3400 <= o <= 0x9FFF or 0xF900 <= o <= 0xFAFF or 0x20000 <= o <= 0x3FFFF


def is_cjk(ch: str) -> bool:
    o = ord(ch)
    return is_han(ch) or 0x3040 <= o <= 0x30FF or 0xAC00 <= o <= 0xD7AF or 0x1100 <= o <= 0x11FF


def has_cjk(text: str) -> bool:
    return any(is_cjk(ch) for ch in text)


def stem(word: str) -> str:
    if len(word) <= 3:
        return word
    for suffix, repl in SUFFIXES:
        if word.endswith(suffix) and len(word) - len(suffix) >= 3:
            return word[: -len(suffix)] + repl
    return word


def fold_spelling(word: str) -> str:
    folded = re.sub(r"[ao]e", "e", word) if len(word) >= 5 else word
    return re.sub(r"^([a-z]{3,})is(e|es|ed|ing|er|ers|ation|ations)$", r"\1iz\2", folded)


def canonical_token(word: str) -> str:
    stemmed = re.sub(r"^([a-z]+olog)ical$", r"\1y", stem(fold_spelling(word)))
    return LEMMAS.get(stemmed, stemmed)


def strip_contraction(word: str) -> str:
    word = re.sub(r"n't$", "", word)
    word = re.sub(r"'(s|re|ve|ll|d|m)$", "", word)
    return word.replace("'", "")


def tokenize(text: str) -> list[str]:
    text = half_width(text).replace("‘", "'").replace("’", "'").lower()
    out = []
    for w in re.split(r"[^\w']+", text):
        w = strip_contraction(w.strip("'"))
        if w and re.fullmatch(r"[a-z0-9]+", w) and w not in STOP:
            out.append(canonical_token(w))
    return out


def tokens_match(a: str, b: str) -> bool:
    if a == b:
        return True
    shorter = min(len(a), len(b))
    prefix = 0
    while prefix < shorter and a[prefix] == b[prefix]:
        prefix += 1
    if shorter >= 4 and prefix == shorter:
        if shorter >= 6:
            return True
        longer = a if len(a) > len(b) else b
        if longer[shorter:] in SHORT_STEM_ENDINGS:
            return True
    max_tail = 4 if prefix >= 8 else 3
    return prefix >= 5 and max(len(a), len(b)) - prefix <= max_tail


class Prepared:
    __slots__ = ("compact", "tokens", "cjk")

    def __init__(self, text: str):
        self.compact = compact_text(text).replace("痛", "疼")
        self.tokens = tokenize(text)
        self.cjk = has_cjk(text)


def gapped_positions(u: str, p: str, slack: int):
    if not p:
        return None
    start = u.find(p[0])
    while start >= 0:
        positions = [start]
        end = min(len(u), start + len(p) + slack)
        i = start + 1
        while i < end and len(positions) < len(p):
            if u[i] == p[len(positions)]:
                positions.append(i)
            i += 1
        if len(positions) == len(p):
            return positions
        start = u.find(p[0], start + 1)
    return None


def topic_run(u: str, p: str):
    best = (0, 0)
    if not u or not p:
        return best
    topical = [0] * (len(u) + 1)
    for i, ch in enumerate(u):
        topical[i + 1] = topical[i] + (0 if ch in FUNCTION_CHARS else 1)
    prev = [0] * (len(p) + 1)
    for i in range(1, len(u) + 1):
        curr = [0] * (len(p) + 1)
        for j in range(1, len(p) + 1):
            run = prev[j - 1] + 1 if u[i - 1] == p[j - 1] else 0
            curr[j] = run
            if run > best[1] and topical[i] > topical[i - run]:
                best = (i - run, run)
        prev = curr
    return best


def particle_positions(u: str, p: str):
    if any(ch in PARTICLES for ch in p):
        return None
    if sum(1 for ch in p if is_han(ch) and ch not in FUNCTION_CHARS) < 2:
        return None
    chars, positions = [], []
    for i, ch in enumerate(u):
        if ch in PARTICLES:
            continue
        chars.append(ch)
        positions.append(i)
    at = "".join(chars).find(p)
    return None if at < 0 else positions[at : at + len(p)]


def character_score(u: str, p: str) -> float:
    if not u or not p:
        return 0.0
    if p in u:
        return 1.0
    common = topic_run(u, p)[1]
    score = 0.0
    if common >= 2:
        score = common / len(p)
        if common < 3:
            lead = p[:common]
            leading = lead in u and lead not in GENERIC_CJK_BIGRAMS
            if not leading and gapped_positions(u, p, 4) is None:
                score = min(score, 0.5)
    if particle_positions(u, p):
        score = max(score, 0.9)
    if score > 0 and len(u) >= 2 and u in p:
        score += 0.15
    return min(1.0, score)


def token_score(u: list[str], p: list[str]) -> float:
    if not p or not u:
        return 0.0
    return sum(1 for pt in p if any(tokens_match(ut, pt) for ut in u)) / len(p)


def phrase_score(u: Prepared, p: Prepared) -> float:
    if p.cjk:
        return character_score(u.compact, p.compact)
    tokens = token_score(u.tokens, p.tokens)
    compact = 0.9 if len(p.compact) >= 4 and p.compact in u.compact else 0.0
    return max(tokens, compact)


def phrase_evidence(u: Prepared, p: Prepared) -> set[str]:
    uc = u.compact

    def keys(positions):
        return {f"c{i}" for i in positions if uc[i] not in FUNCTION_CHARS}

    if p.cjk:
        pc = p.compact
        if not uc or not pc:
            return set()
        at = uc.find(pc)
        if at >= 0:
            return keys(range(at, at + len(pc)))
        spelled = gapped_positions(uc, pc, 4) or particle_positions(uc, pc)
        if spelled:
            return keys(spelled)
        start, length = topic_run(uc, pc)
        return keys(range(start, start + length)) if length >= 2 else set()
    return {f"t{i}" for i, ut in enumerate(u.tokens) if any(tokens_match(ut, pt) for pt in p.tokens)}


# =============================================================================================
# Localised text helpers
# =============================================================================================

def texts(value, locale: str) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    first = value.get(locale) or next(iter(value.values()), "")
    out = [first, *value.values()]
    return list(dict.fromkeys(v for v in out if v.strip()))


def list_entries(value, locale: str) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return list(dict.fromkeys(v for v in value if v.strip()))
    out = list(value.get(locale, [])) + [x for lst in value.values() for x in lst]
    return list(dict.fromkeys(v for v in out if v.strip()))


def lt(value, locale: str) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return value.get(locale) or next(iter(value.values()), "")


# =============================================================================================
# Phase twins (port of engine/twins.ts)
# =============================================================================================

class Twins:
    def __init__(self, case: dict):
        self.items = case.get("history", [])
        self.by_id = {h["id"]: h for h in self.items}
        self.closure: dict[str, set[str]] = {}
        for h in self.items:
            if not h.get("supersedes"):
                continue
            out, stack = set(), list(h["supersedes"])
            while stack:
                i = stack.pop()
                if i == h["id"] or i in out:
                    continue
                out.add(i)
                stack.extend(self.by_id.get(i, {}).get("supersedes", []))
            self.closure[h["id"]] = out

    def any(self) -> bool:
        return bool(self.closure)

    @staticmethod
    def in_phase(item, phase):
        return not item.get("phases") or phase in item["phases"]

    def superseded_in(self, id_: str, phase: str):
        if not self.closure:
            return None
        cands = [h for h in self.items if h["id"] != id_ and self.in_phase(h, phase) and id_ in self.closure.get(h["id"], set())]
        if not cands:
            return None
        for h in cands:
            if not any(o is not h and h["id"] in self.closure.get(o["id"], set()) for o in cands):
                return h["id"]
        return cands[0]["id"]

    def twin(self, id_: str, phase: str):
        item = self.by_id.get(id_)
        if item is None:
            return None
        current, seen = id_, {id_}
        while True:
            nxt = self.superseded_in(current, phase)
            if nxt is None or nxt in seen:
                break
            seen.add(nxt)
            current = nxt
        return current if (current != id_ or self.in_phase(item, phase)) else None

    def credited(self, asked: list[str], id_: str) -> bool:
        if id_ in asked:
            return True
        return any(id_ in self.closure.get(a, set()) for a in asked)


# =============================================================================================
# History matcher and the utterance corpus (matcher.ts matchHistory / distinctHistoryHits, cli checkUtterances)
# =============================================================================================

def history_index(case: dict, locale: str):
    index = []
    for h in case.get("history", []):
        phrases = [Prepared(t) for t in dict.fromkeys(texts(h["question"], locale) + list_entries(h.get("keywords"), locale))]
        phrases = [p for p in phrases if p.compact]
        exclude = [compact_text(x).replace("痛", "疼") for x in list_entries(h.get("excludeKeywords"), "*")]
        index.append({"id": h["id"], "phrases": phrases, "exclude": [x for x in dict.fromkeys(exclude) if x]})
    return index


def match_history(case: dict, utterance: str, locale: str):
    u = Prepared(utterance)
    if not u.compact:
        return []
    hits = []
    for item in history_index(case, locale):
        best = 0.0
        for p in item["phrases"]:
            best = max(best, phrase_score(u, p))
            if best >= 1:
                break
        if best > 0 and any(x in u.compact for x in item["exclude"]):
            best *= EXCLUDE_FACTOR
        score = round(best * 10000) / 10000
        if score >= MATCH_THRESHOLD:
            hits.append((item["id"], score))
    return sorted(hits, key=lambda h: -h[1])


def with_phase_twins(case, twins: Twins, hits, phase):
    if phase is None or not twins.any():
        return list(hits)
    best: dict[str, float] = {}
    for id_, score in hits:
        target = (twins.twin(id_, phase) or id_) if twins.superseded_in(id_, phase) is not None else id_
        best[target] = max(best.get(target, 0), score)
    order = {h["id"]: i for i, h in enumerate(case["history"])}
    return sorted(best.items(), key=lambda kv: (-kv[1], order.get(kv[0], 0)))


def distinct_hits(case, twins: Twins, utterance, locale, hits, phase):
    if len(hits) < 2:
        return list(hits)
    u = Prepared(utterance)
    index = history_index(case, locale)
    use_twins = phase is not None and twins.any()
    evidence = []
    for hit_id, _ in hits:
        best, keys = 0.0, set()
        for item in index:
            if item["id"] != hit_id and not (use_twins and twins.twin(item["id"], phase) == hit_id):
                continue
            for p in item["phrases"]:
                score = phrase_score(u, p)
                if score <= 0 or score < best - 1e-9:
                    continue
                if score > best + 1e-9:
                    keys = set()
                keys |= phrase_evidence(u, p)
                best = max(best, score)
        evidence.append(keys)

    def within(a, b):
        return len(a) > 0 and len(b) > len(a) and a <= b

    return [h for i, h in enumerate(hits) if not any(j != i and within(evidence[i], other) for j, other in enumerate(evidence))]


def check_utterances(case: dict, where: str) -> None:
    corpus = case.get("extensions", {}).get("testUtterances")
    if corpus is None:
        warn(where, "no extensions.testUtterances corpus")
        return
    twins = Twins(case)
    by_id = {h["id"]: h for h in case["history"]}
    failures = 0
    for i, u in enumerate(corpus):
        path = f"{where} extensions.testUtterances.{i}"
        for id_ in u["expect"]:
            if id_ not in by_id:
                err(path, f'unknown history id "{id_}"')
        phase = (by_id.get(u["expect"][0], {}).get("phases") or [None])[0] if u["expect"] else None
        strong = [h for h in with_phase_twins(case, twins, match_history(case, u["text"], u["locale"]), phase) if h[1] >= SELECT_THRESHOLD]
        selected = distinct_hits(case, twins, u["text"], u["locale"], strong, phase)
        got = [h[0] for h in selected]
        if not u["expect"]:
            if got:
                err(path, f'"{u["text"]}" should select nothing, selected {", ".join(got)}')
                failures += 1
            continue
        missing = [x for x in u["expect"] if x not in got]
        if missing or not got or got[0] not in u["expect"]:
            shown = ", ".join(f"{i_} ({s:.2f})" for i_, s in selected) or "nothing"
            err(path, f'"{u["text"]}" ({u["locale"]}) expected {", ".join(u["expect"])}, selected {shown}')
            failures += 1
            continue
        phases = by_id[u["expect"][0]].get("phases")

        def share(a, b):
            return not a or not b or any(x in b for x in a)

        in_phase = [h for h in selected if share(phases, by_id.get(h[0], {}).get("phases"))]
        best = in_phase[0][1] if in_phase else 0
        pipeline = [h for h in in_phase if h[1] >= best - SELECT_RELATIVE][:MAX_SELECTED]
        allowed = set(u["expect"]) | set(u.get("alsoOk", []))
        extra = [h for h in pipeline if h[0] not in allowed]
        if extra:
            warn(path, f'"{u["text"]}" ({u["locale"]}) also selects ' + ", ".join(f"{i_} ({s:.2f})" for i_, s in extra))
    print(f"  utterance corpus: {len(corpus)} utterances, {failures} failing")


# =============================================================================================
# Schema shape (the parts of CaseSchema that are easy to get wrong by hand)
# =============================================================================================

ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
CASE_KEYS = {"schema", "id", "version", "title", "summary", "specialty", "difficulty", "setting", "facility", "locales", "estimatedMinutes", "learningOutcomes",
             "tags", "provenance", "disclaimer", "patient", "phases", "initialPhase", "clock", "history", "exam", "examNotRecorded", "investigations", "studies",
             "orderMatching", "interventions", "physiology", "objectives", "decisions", "rubric", "npcs", "debrief", "procedure", "team", "safetyGates", "unknowns",
             "assets", "solution", "extensions"}
ENUMS = {
    "setting": {"outpatient", "emergency", "inpatient", "icu", "ward", "operating-room", "community"},
    "topic": {"presenting-complaint", "hpi", "pain", "associated-symptoms", "pmh", "psh", "medications", "allergies", "social", "family", "ros", "ice", "obstetric", "developmental", "immunisation", "functional", "other"},
    "disclosure": {"volunteer", "on-ask", "specific", "unknown"},
    "system": {"general", "vitals", "heent", "neck", "cardiovascular", "respiratory", "abdomen", "neurological", "skin", "musculoskeletal", "lymphatic", "genitourinary", "breast", "rectal", "mental-status"},
    "category": {"lab", "imaging", "pathology", "genetics", "bedside", "microbiology", "procedure", "record"},
    "performedAt": {"bedside", "provider", "records"},
    "value": {"essential", "useful", "neutral", "low-value", "harmful"},
    "risk": {"none", "low", "moderate", "high"},
    "kind": {"medication", "oxygen", "fluid", "procedure", "positioning", "monitoring", "consult", "disposition", "airway", "other"},
    "domain": {"history", "examination", "investigations", "diagnosis", "management", "safety", "communication", "efficiency"},
    "role": {"nurse", "radiologist", "pathologist", "lab-tech", "attending", "pharmacist", "consultant", "receptionist", "paramedic"},
    "affect": {"calm", "anxious", "distressed", "in-pain", "drowsy", "irritable", "frightened", "breathless", "confused"},
    "roomKind": {"entrance", "reception", "waiting", "consult", "triage", "resus", "emergency", "ward", "icu", "operating-room", "imaging", "laboratory", "pathology", "pharmacy",
                 "nurse-station", "conference", "office", "corridor", "storage", "restroom", "garden", "build-zone", "rehabilitation", "teaching", "elevator", "stairwell"},
}
CANONICAL_CAPS = {
    "lab-hematology", "lab-chemistry", "lab-blood-gas", "lab-serology", "lab-microbiology", "lab-urinalysis", "lab-endocrine", "flow-cytometry", "point-of-care", "xray", "ct", "mri",
    "ultrasound", "pet-ct", "fluoroscopy", "echocardiography", "histopathology", "cytology", "cytogenetics", "molecular", "ecg-12lead", "cardiac-monitor", "capnography", "stethoscope",
    "otoscope", "reflex-hammer", "thermometer", "scale", "peak-flow", "oxygen", "suction", "airway", "ventilator", "niv", "nebulizer", "iv-access", "infusion-pump", "defibrillator",
    "crash-cart", "medications", "blood-bank", "surgery", "anesthesia", "endoscopy", "endoscopic-camera", "light-source", "insufflator", "dialysis", "anatomy-atlas", "evidence-board",
    "records", "crafting",
}
PERSONAL_KIT = {"stethoscope", "thermometer", "reflex-hammer", "otoscope"}


def check_text(value, locales, where):
    if isinstance(value, str):
        return
    if not isinstance(value, dict):
        err(where, "not a LocalizedText")
        return
    for loc in locales:
        if not value.get(loc, "").strip():
            err(where, f"missing {loc} text")


def check_list(value, locales, where):
    if value is None or isinstance(value, list):
        return
    for loc in locales:
        if loc not in value:
            warn(where, f"no {loc} entries")


def check_enum(value, enum, where):
    if value is not None and value not in ENUMS[enum]:
        err(where, f'"{value}" is not a valid {enum}')


def check_shape(c: dict, w: str) -> None:
    for k in c:
        if k not in CASE_KEYS:
            err(w, f'unknown top-level key "{k}"')
    if c.get("schema") != "clinicalcraft/case@1":
        err(w, "schema must be clinicalcraft/case@1")
    if not re.fullmatch(r"\d+\.\d+\.\d+", c.get("version", "")):
        err(w, "version must be x.y.z")
    locs = c.get("locales", [])
    check_enum(c.get("setting"), "setting", f"{w} setting")
    for key in ("title", "summary", "disclaimer", "examNotRecorded"):
        if key in c:
            check_text(c[key], locs, f"{w} {key}")
    for i, o in enumerate(c.get("learningOutcomes", [])):
        check_text(o, locs, f"{w} learningOutcomes.{i}")
    p = c["patient"]
    for key in ("displayName", "chiefComplaint", "triageNote"):
        check_text(p.get(key), locs, f"{w} patient.{key}")
    for key in ("personality", "speechStyle", "openingLine", "fallbackUnknown", "actingNotes"):
        check_text(p["persona"].get(key), locs, f"{w} patient.persona.{key}")
    check_enum(p["persona"].get("affect"), "affect", f"{w} patient.persona.affect")
    collections = {"phases": ("label",), "history": ("question", "answer"), "exam": ("maneuver", "finding"), "investigations": ("name",), "interventions": ("name",),
                   "objectives": ("title", "hint"), "decisions": ("prompt", "need"), "rubric": ("text",)}
    for coll, fields in collections.items():
        for i, item in enumerate(c.get(coll, [])):
            if not ID_RE.match(item.get("id", "")) or len(item["id"]) > 80:
                err(f"{w} {coll}.{i}", f'bad id "{item.get("id")}"')
            for f in fields:
                check_text(item.get(f), locs, f"{w} {coll}.{i}.{f}")
    for i, h in enumerate(c.get("history", [])):
        check_enum(h["topic"], "topic", f"{w} history.{i}.topic")
        check_enum(h.get("disclosure"), "disclosure", f"{w} history.{i}.disclosure")
        check_list(h.get("keywords"), locs, f"{w} history.{i}.keywords")
    for i, e in enumerate(c.get("exam", [])):
        check_enum(e["system"], "system", f"{w} exam.{i}.system")
    for i, inv in enumerate(c.get("investigations", [])):
        check_enum(inv["category"], "category", f"{w} investigations.{i}.category")
        check_enum(inv.get("performedAt"), "performedAt", f"{w} investigations.{i}.performedAt")
        check_enum(inv.get("value"), "value", f"{w} investigations.{i}.value")
        check_enum(inv.get("risk"), "risk", f"{w} investigations.{i}.risk")
        for phase, r in inv["results"].items():
            check_text(r.get("text"), locs, f"{w} investigations.{i}.results.{phase}.text")
    for i, iv in enumerate(c.get("interventions", [])):
        check_enum(iv["kind"], "kind", f"{w} interventions.{i}.kind")
        check_enum(iv.get("risk"), "risk", f"{w} interventions.{i}.risk")
        for key in ("dose", "harm", "response"):
            if key in iv:
                check_text(iv[key], locs, f"{w} interventions.{i}.{key}")
        if "destination" in iv:
            d = iv["destination"]
            if len(d) != 1:
                err(f"{w} interventions.{i}.destination", "names exactly one of setting, roomKind or capability")
            check_enum(d.get("roomKind"), "roomKind", f"{w} interventions.{i}.destination.roomKind")
    for i, d in enumerate(c.get("decisions", [])):
        for j, o in enumerate(d["options"]):
            check_text(o["text"], locs, f"{w} decisions.{i}.options.{j}.text")
            check_text(o["feedback"], locs, f"{w} decisions.{i}.options.{j}.feedback")
    for i, r in enumerate(c.get("rubric", [])):
        check_enum(r["domain"], "domain", f"{w} rubric.{i}.domain")
    for i, n in enumerate(c.get("npcs", [])):
        check_enum(n["role"], "role", f"{w} npcs.{i}.role")
        check_text(n["knowledge"], locs, f"{w} npcs.{i}.knowledge")
    for coll in ("exam", "investigations", "interventions"):
        for i, item in enumerate(c.get(coll, [])):
            for cap in item.get("requires", []):
                if cap not in CANONICAL_CAPS:
                    warn(f"{w} {coll}.{i}.requires", f'non-canonical capability "{cap}"')


# =============================================================================================
# Conditions and integrity
# =============================================================================================

def leaves(cond, path, out):
    if "all" in cond:
        for i, x in enumerate(cond["all"]):
            leaves(x, f"{path}.all.{i}", out)
    elif "any" in cond:
        for i, x in enumerate(cond["any"]):
            leaves(x, f"{path}.any.{i}", out)
    elif "not" in cond:
        leaves(cond["not"], f"{path}.not", out)
    else:
        out.append((cond, path))
    return out


def check_integrity(c: dict, w: str) -> None:
    ids = {k: [x["id"] for x in c.get(k, [])] for k in ("phases", "history", "exam", "investigations", "interventions", "objectives", "decisions", "rubric")}
    for k, lst in ids.items():
        dup = {x for x in lst if lst.count(x) > 1}
        if dup:
            err(w, f"duplicate {k} ids: {sorted(dup)}")
    sets = {k: set(v) for k, v in ids.items()}
    flags = {f for iv in c.get("interventions", []) for f in iv.get("setFlags", [])}
    inv_by = {i["id"]: i for i in c.get("investigations", [])}
    iv_by = {i["id"]: i for i in c.get("interventions", [])}

    def check_cond(cond, path):
        if cond is None:
            return
        for leaf, at in leaves(cond, path, []):
            key = next(iter(leaf))
            ref = leaf[key]
            table = {"asked": "history", "examined": "exam", "decided": "decisions", "attempted": "decisions", "decidedFirstTry": "decisions",
                     "intervened": "interventions", "phase": "phases", "objective": "objectives"}
            if key in table:
                if ref not in sets[table[key]]:
                    err(at, f'unknown {table[key]} "{ref}"')
            elif key in ("ordered", "read", "resultReady"):
                if ref not in sets["investigations"]:
                    err(at, f'unknown investigation "{ref}"')
                elif "phase" in leaf:
                    if leaf["phase"] not in sets["phases"]:
                        err(at, f'unknown phase "{leaf["phase"]}"')
                    elif key != "ordered" and leaf["phase"] not in inv_by[ref]["results"]:
                        err(at, f'"{ref}" has no result for phase "{leaf["phase"]}"')
            elif key == "inOrder":
                for x in ref:
                    if x not in sets["interventions"]:
                        err(at, f'unknown intervention "{x}"')
            elif key == "flag" and ref not in flags:
                warn(at, f'flag "{ref}" is never set')
            elif key == "datum":
                if not any(h.get("safety", {}).get("datum") == ref for h in c["history"]):
                    warn(at, f'no history item establishes datum "{ref}"')
            elif key not in ("always", "vital", "elapsed", "hints", "held", "procedure", "count", "study"):
                err(at, f"unknown condition leaf {key}")

    for i, p in enumerate(c["phases"]):
        check_cond(p.get("enterWhen"), f"{w} phases.{i}.enterWhen")
        if "location" in p:
            check_enum(p["location"].get("roomKind"), "roomKind", f"{w} phases.{i}.location.roomKind")
    for i, o in enumerate(c["objectives"]):
        check_cond(o["completeWhen"], f"{w} objectives.{i}.completeWhen")
        for j, wp in enumerate(o.get("waypoints", [])):
            check_cond(wp.get("unless"), f"{w} objectives.{i}.waypoints.{j}.unless")
    for i, d in enumerate(c.get("decisions", [])):
        check_cond(d.get("requires"), f"{w} decisions.{i}.requires")
        n = sum(1 for o in d["options"] if o["correct"])
        if n == 0 or (d.get("kind", "single") == "single" and n != 1):
            err(f"{w} decisions.{i}", f"{n} correct options for a {d.get('kind', 'single')} decision")
    for i, iv in enumerate(c.get("interventions", [])):
        check_cond(iv.get("indicatedWhen"), f"{w} interventions.{i}.indicatedWhen")
        check_cond(iv.get("contraindicatedWhen"), f"{w} interventions.{i}.contraindicatedWhen")
    for i, r in enumerate(c.get("rubric", [])):
        check_cond(r.get("met"), f"{w} rubric.{i}.met")
        check_cond(r.get("scoredWhen"), f"{w} rubric.{i}.scoredWhen")
    for i, g in enumerate(c.get("safetyGates", [])):
        check_cond(g["when"], f"{w} safetyGates.{i}.when")
    for i, inv in enumerate(c.get("investigations", [])):
        for phase in inv["results"]:
            if phase not in sets["phases"]:
                err(f"{w} investigations.{i}.results", f'unknown phase "{phase}"')
        av = inv.get("availability", {})
        if av.get("earliestPhase") and av["earliestPhase"] not in sets["phases"]:
            err(f"{w} investigations.{i}.availability", f'unknown phase "{av["earliestPhase"]}"')
        check_cond(av.get("when"), f"{w} investigations.{i}.availability.when")
    for coll in ("history", "exam"):
        for i, item in enumerate(c.get(coll, [])):
            for p in item.get("phases", []) or []:
                if p not in sets["phases"]:
                    err(f"{w} {coll}.{i}.phases", f'unknown phase "{p}"')
    for i, h in enumerate(c["history"]):
        for s in h.get("supersedes", []) or []:
            if s not in sets["history"] or s == h["id"]:
                err(f"{w} history.{i}.supersedes", f'bad supersedes "{s}"')
    for i, n in enumerate(c.get("npcs", [])):
        for x in n.get("interprets", []):
            if x not in sets["investigations"]:
                err(f"{w} npcs.{i}.interprets", f'unknown investigation "{x}"')
    for rule in c.get("orderMatching", {}).get("rules", []):
        for x in rule.get("add", []) + rule.get("remove", []):
            if x not in sets["investigations"]:
                err(f"{w} orderMatching", f'unknown investigation "{x}"')
    for iv in c.get("interventions", []):
        for x in iv.get("mitigates", []):
            if not any(h.get("safety", {}).get("datum") == x for h in c["history"]):
                warn(f"{w} interventions.{iv['id']}.mitigates", f'no history item establishes datum "{x}"')


# =============================================================================================
# Content lints (engine/content-standard.ts, integrity keyword lint)
# =============================================================================================

def dnf(cond, negate=False):
    if "not" in cond:
        return dnf(cond["not"], not negate)
    if "all" in cond or "any" in cond:
        parts = cond.get("all", cond.get("any"))
        conj = ("all" in cond) != negate
        if conj:
            out = [[]]
            for part in parts:
                d = dnf(part, negate)
                out = [a + b for a in out for b in d]
            return out
        return [x for part in parts for x in dnf(part, negate)]
    if "always" in cond:
        return [[]] if cond["always"] != negate else []
    return [[(cond, not negate)]]


def triggers(cond):
    if "any" in cond:
        return [t for x in cond["any"] for t in triggers(x)]
    if any(k in cond for k in ("all", "not", "always")):
        return []
    return [cond]


def covers(trigger, step):
    if "intervened" in trigger and "intervened" in step:
        return trigger["intervened"] == step["intervened"] and trigger.get("minCount", 1) <= step.get("minCount", 1)
    if "ordered" in trigger and "ordered" in step:
        return trigger["ordered"] == step["ordered"] and (trigger.get("phase") is None or trigger.get("phase") == step.get("phase"))
    if "flag" in trigger and "flag" in step:
        return trigger["flag"] == step["flag"]
    return False


def check_lints(c: dict, w: str) -> None:
    locs = c["locales"]
    if len(c.get("rubric", [])) < 8:
        warn(w, "rubric has fewer than 8 items")
    if not any(r["domain"] == "safety" for r in c.get("rubric", [])):
        warn(w, "no safety rubric item")
    if len(c["debrief"].get("teachingPoints", [])) < 3:
        warn(w, "fewer than 3 teaching points")
    if len(c.get("learningOutcomes", [])) < 3:
        warn(w, "fewer than 3 learning outcomes")
    if "review" not in c["provenance"]:
        warn(w, "no provenance.review")
    for i, d in enumerate(c.get("decisions", [])):
        seen = {}
        for j, o in enumerate(d["options"]):
            for loc in locs:
                key = (loc, compact_text(lt(o["feedback"], loc)))
                if key in seen:
                    warn(f"{w} decisions.{i}.options.{j}.feedback", f'same feedback as option {seen[key]}')
                seen[key] = o["id"]
    for i, o in enumerate(c["objectives"]):
        for d in c.get("decisions", []):
            for opt in (x for x in d["options"] if x["correct"]):
                for loc in locs:
                    label = compact_text(lt(opt["text"], loc))
                    significant = len(label) >= (3 if any(is_han(ch) for ch in label) else 6)
                    if significant and label in compact_text(lt(o["hint"], loc)):
                        warn(f"{w} objectives.{i}.hint", f'hint names a correct option of {d["id"]} ({loc})')
    for loc in locs:
        summary = compact_text(lt(c["summary"], loc))
        for key in ("triageNote",):
            a = compact_text(lt(c["patient"].get(key), loc))
            if summary and (a == summary or (len(summary) >= 10 and summary in a)):
                warn(f"{w} patient.{key}", "repeats the library summary")
        a = compact_text(lt(c["patient"]["persona"]["openingLine"], loc))
        if summary and (a == summary or (len(summary) >= 10 and summary in a)):
            warn(f"{w} patient.persona.openingLine", "repeats the library summary")
    corpus = c.get("extensions", {}).get("testUtterances", [])
    by_id = {h["id"]: h for h in c["history"]}
    twins = Twins(c)
    for i, u in enumerate(corpus):
        for id_ in u["expect"]:
            if id_ in by_id and compact_text(lt(by_id[id_]["question"], u["locale"])) == compact_text(u["text"]):
                warn(f"{w} extensions.testUtterances.{i}", f'repeats the canonical question of "{id_}"')
    for i, h in enumerate(c["history"]):
        if not h.get("required"):
            continue
        answers = {h["id"]} | {x["id"] for x in c["history"] if h["id"] in twins.closure.get(x["id"], set())}
        if not any(set(u["expect"]) & answers for u in corpus):
            warn(f"{w} history.{i}", f'required item "{h["id"]}" has no paraphrase in testUtterances')
    for i, inv in enumerate(c.get("investigations", [])):
        if inv.get("performedAt") == "records":
            if any(r not in PERSONAL_KIT | {"records"} for r in inv.get("requires", [])):
                warn(f"{w} investigations.{i}.requires", "a record review requires at most records")
            if inv.get("risk", "none") != "none":
                warn(f"{w} investigations.{i}.risk", "a record review has risk none")
    nr = re.compile(r"\bnot (?:recorded|documented|described|reported)\b|\bunrecorded\b|未记录|未描述|无记录|没有记录|未提及", re.I)
    for i, e in enumerate(c.get("exam", [])):
        if any(nr.search(lt(e["finding"], loc)) for loc in locs):
            warn(f"{w} exam.{i}.finding", "says it is not recorded")
    for coll, field in (("history", "keywords"), ("exam", "keywords"), ("interventions", "aliases")):
        for i, item in enumerate(c.get(coll, [])):
            kw = item.get(field) or {}
            for loc, phrases in (kw.items() if isinstance(kw, dict) else [("*", kw)]):
                for j, phrase in enumerate(phrases):
                    if has_cjk(phrase) or len(phrase.split()) < 3:
                        continue
                    if len(tokenize(phrase)) == 1:
                        warn(f"{w} {coll}.{i}.{field}.{loc}.{j}", f'"{phrase}" reduces to one token')
    for i, r in enumerate(c.get("rubric", [])):
        if not r.get("met") or not r.get("scoredWhen"):
            continue
        gate = triggers(r["scoredWhen"])
        for way in dnf(r["met"], True):
            steps = [leaf for leaf, pos in way if pos and any(k in leaf for k in ("intervened", "ordered", "flag"))]
            if steps and not any(covers(g, s) for g in gate for s in steps):
                warn(f"{w} rubric.{i}.scoredWhen", f"lost by {steps} but scoredWhen does not hold for it")


# =============================================================================================
# A small reducer (engine/reducer.ts, timeline.ts, conditions.ts, records.ts, datum.ts)
# =============================================================================================

class Session:
    def __init__(self, c: dict):
        self.c = c
        self.twins = Twins(c)
        self.started = self.finished = False
        self.phase = c.get("initialPhase") or c["phases"][0]["id"]
        self.reached = [self.phase]
        self.asked: list[str] = []
        self.examined: list[str] = []
        self.orders: set[tuple[str, str]] = set()
        self.seen: set[tuple[str, str]] = set()
        self.decisions: set[str] = set()
        self.attempts: list[tuple[str, bool]] = []
        self.interventions: list[dict] = []
        self.flags: list[str] = []
        self.objectives_done: list[str] = []
        self.seq = 0

    # --- conditions ---
    def ev(self, cond) -> bool:
        if "all" in cond:
            return all(self.ev(x) for x in cond["all"])
        if "any" in cond:
            return any(self.ev(x) for x in cond["any"])
        if "not" in cond:
            return not self.ev(cond["not"])
        if "always" in cond:
            return cond["always"]
        if "asked" in cond:
            return self.twins.credited(self.asked, cond["asked"])
        if "examined" in cond:
            return cond["examined"] in self.examined
        if "ordered" in cond:
            return any(i == cond["ordered"] and (cond.get("phase") is None or p == cond["phase"]) for i, p in self.orders)
        if "read" in cond:
            return any(i == cond["read"] and (cond.get("phase") is None or p == cond["phase"]) for i, p in self.seen)
        if "resultReady" in cond:
            return any(i == cond["resultReady"] and (cond.get("phase") is None or p == cond["phase"]) for i, p in self.orders)
        if "decided" in cond:
            return cond["decided"] in self.decisions
        if "attempted" in cond:
            return any(d == cond["attempted"] for d, _ in self.attempts)
        if "decidedFirstTry" in cond:
            first = next((ok for d, ok in self.attempts if d == cond["decidedFirstTry"]), None)
            return first is True
        if "intervened" in cond:
            valid = cond.get("valid")
            n = sum(1 for r in self.interventions if r["id"] == cond["intervened"] and (valid is None or (r["app"] != "contraindicated") == valid))
            return n >= cond.get("minCount", 1)
        if "inOrder" in cond:
            firsts = []
            for id_ in cond["inOrder"]:
                rec = next((r for r in self.interventions if r["id"] == id_ and r["app"] != "contraindicated"), None)
                firsts.append(None if rec is None else rec["seq"])
            return all(x is not None and (i == 0 or x > firsts[i - 1]) for i, x in enumerate(firsts))
        if "phase" in cond:
            return self.phase == cond["phase"]
        if "flag" in cond:
            return cond["flag"] in self.flags
        if "objective" in cond:
            return cond["objective"] in self.objectives_done
        if "datum" in cond:
            return self.datum(cond["datum"]) in cond["status"]
        return False

    def datum(self, name):
        items = [h for h in self.c["history"] if h.get("safety", {}).get("datum") == name]
        if not items:
            return None
        findings = [h["safety"].get("finding") or ("unknown" if h.get("disclosure") == "unknown" else "negative") for h in items if h["id"] in self.asked]
        if "positive" in findings:
            return "verified-positive"
        if "negative" in findings:
            return "verified-negative"
        mitigators = {iv["id"] for iv in self.c["interventions"] if name in iv.get("mitigates", [])}
        if any(r["id"] in mitigators and not r.get("invalid") for r in self.interventions):
            return "mitigated"
        return "asked-unknown" if any(h["id"] in self.asked for h in items) else "not-asked"

    def record_state(self, inv):
        phases = [p["id"] for p in self.c["phases"] if p["id"] in inv["results"]]
        if not phases:
            return "none"
        av = inv.get("availability", {})
        earliest = av.get("earliestPhase") or phases[0]
        if earliest not in self.reached:
            return "not-yet"
        reached = [p for p in phases if p in self.reached]
        if not reached:
            return "not-yet"
        if av.get("when") and not self.ev(av["when"]):
            return "not-yet"
        return "available"

    # --- actions ---
    def step(self, a: dict):
        """Apply one action; return a rejection message or None."""
        t = a["type"]
        c = self.c
        if self.finished:
            return "finished"
        if not self.started and t != "start":
            return "not-started"
        before = self.snapshot_truth()
        if t == "start":
            if self.started:
                return "invalid: already started"
            self.started = True
        elif t == "ask":
            item = next((h for h in c["history"] if h["id"] == a["itemId"]), None)
            if item is None:
                return "unknown-id"
            if item.get("phases") and self.phase not in item["phases"]:
                return f'phase-locked: "{item["id"]}" not in phase {self.phase}'
            twin = self.twins.superseded_in(item["id"], self.phase)
            if twin:
                return f'phase-locked: superseded by "{twin}"'
            if item["id"] not in self.asked:
                self.asked.append(item["id"])
        elif t == "examine":
            f = next((e for e in c["exam"] if e["id"] == a["findingId"]), None)
            if f is None:
                return "unknown-id"
            if f.get("phases") and self.phase not in f["phases"]:
                return f'phase-locked: "{f["id"]}" not in phase {self.phase}'
            if f["id"] not in self.examined:
                self.examined.append(f["id"])
        elif t == "order":
            inv = next((i for i in c["investigations"] if i["id"] == a["investigationId"]), None)
            if inv is None:
                return "unknown-id"
            if inv.get("performedAt") == "records" and self.record_state(inv) == "not-yet":
                return f'not-ready: "{inv["id"]}" does not exist yet'
            if (inv["id"], self.phase) in self.orders:
                return None  # duplicate: unchanged
            self.orders.add((inv["id"], self.phase))
        elif t == "read":
            inv = next((i for i in c["investigations"] if i["id"] == a["investigationId"]), None)
            if inv is None:
                return "unknown-id"
            phase = a.get("phase") or self.phase
            if (inv["id"], phase) not in self.orders:
                return f'not-ordered: "{inv["id"]}" in phase {phase}'
            if phase not in inv["results"]:
                return f'no-record: "{inv["id"]}" for phase {phase}'
            self.seen.add((inv["id"], phase))
        elif t == "set-phase":
            ph = next((p for p in c["phases"] if p["id"] == a["phase"]), None)
            if ph is None:
                return "unknown-id"
            reached = ph.get("enterWhen") is not None and self.ev(ph["enterWhen"])
            if not ph.get("learnerSwitchable", True) and not reached:
                return f'phase-locked: "{ph["id"]}" cannot be selected manually'
            if self.phase != ph["id"]:
                self.phase = ph["id"]
                if ph["id"] not in self.reached:
                    self.reached.append(ph["id"])
        elif t == "answer":
            d = next((x for x in c["decisions"] if x["id"] == a["decisionId"]), None)
            if d is None:
                return "unknown-id"
            chosen = list(dict.fromkeys(a["optionIds"]))
            if d.get("kind", "single") == "single" and len(chosen) != 1:
                return "invalid: single decision"
            if d["id"] in self.decisions:
                return "already-decided"
            if not self.ev(d.get("requires", {"always": True})):
                return f'requirements-unmet: {lt(d["need"], "en")}'
            correct_ids = [o["id"] for o in d["options"] if o["correct"]]
            ok = chosen[0] in correct_ids if d.get("kind", "single") == "single" else sorted(chosen) == sorted(correct_ids)
            self.attempts.append((d["id"], ok))
            if ok:
                self.decisions.add(d["id"])
        elif t == "intervene":
            iv = next((x for x in c["interventions"] if x["id"] == a["interventionId"]), None)
            if iv is None:
                return "unknown-id"
            given = sum(1 for r in self.interventions if r["id"] == iv["id"] and not r.get("invalid"))
            if iv.get("maxDoses") is not None and given >= iv["maxDoses"]:
                return "max-doses"
            if iv.get("contraindicatedWhen") and self.ev(iv["contraindicatedWhen"]):
                app = "contraindicated"
            elif iv.get("indicatedWhen") and self.ev(iv["indicatedWhen"]):
                app = "indicated"
            else:
                app = "neutral"
            invalid = bool(iv.get("checklist")) and app == "contraindicated"
            self.interventions.append({"id": iv["id"], "app": app, "seq": self.seq + 1, "invalid": invalid})
            if not invalid:
                for f in iv.get("setFlags", []):
                    if f not in self.flags:
                        self.flags.append(f)
        elif t == "finish":
            open_ = [o["id"] for o in c["objectives"] if o["id"] not in self.objectives_done]
            if open_:
                return f"objectives-incomplete: {open_}"
            self.finished = True
        else:
            return f"unsupported action {t}"
        self.seq += 1
        if self.started:
            self.settle(before)
        return None

    def snapshot_truth(self):
        return {p["id"]: (self.ev(p["enterWhen"]) if p.get("enterWhen") else False) for p in self.c["phases"]}

    def settle(self, truth):
        for _ in range(2 + len(self.c["phases"]) + len(self.c["objectives"])):
            changed = False
            for p in self.c["phases"]:
                if not p.get("enterWhen"):
                    continue
                now = self.ev(p["enterWhen"])
                was = truth.get(p["id"], False)
                truth[p["id"]] = now
                if not now or was or self.phase == p["id"]:
                    continue
                self.phase = p["id"]
                if p["id"] not in self.reached:
                    self.reached.append(p["id"])
                changed = True
            for o in self.c["objectives"]:
                if o["id"] not in self.objectives_done and self.ev(o["completeWhen"]):
                    self.objectives_done.append(o["id"])
                    changed = True
            if not changed:
                break

    # --- assessment ---
    def score(self):
        earned = possible = 0.0
        missed_critical = []
        for r in self.c.get("rubric", []):
            if "met" not in r:
                continue
            if r.get("scoredWhen") and not self.ev(r["scoredWhen"]):
                continue
            possible += r.get("weight", 1)
            if self.ev(r["met"]):
                earned += r.get("weight", 1)
            elif r.get("critical"):
                missed_critical.append(r["id"])
        gates = [(g["id"], g["verdict"], g.get("capPercent", 40)) for g in self.c.get("safetyGates", []) if self.ev(g["when"])]
        pct = 100.0 * earned / possible if possible else 0.0
        for _, verdict, cap in gates:
            if verdict == "safety-critical":
                pct = min(pct, cap)
        return earned, possible, pct, missed_critical, gates


def replay(c: dict, actions: list[dict], where: str, *, quiet_rejections=False):
    s = Session(c)
    rejections = []
    for i, a in enumerate(actions):
        msg = s.step(a)
        if msg:
            rejections.append((i, a, msg))
            if not quiet_rejections:
                err(f"{where} solution.{i}", f'{a["type"]} {a.get("itemId") or a.get("findingId") or a.get("investigationId") or a.get("decisionId") or a.get("interventionId") or a.get("phase") or ""} rejected ({msg})')
    return s, rejections


def check_solution(c: dict, w: str) -> None:
    s, _ = replay(c, c.get("solution", []), w)
    for o in c["objectives"]:
        if o["id"] not in s.objectives_done:
            err(f"{w} solution", f'objective "{o["id"]}" is not completed')
    for d in c.get("decisions", []):
        if d["id"] not in s.decisions:
            err(f"{w} solution", f'decision "{d["id"]}" is not answered correctly')
    if not s.finished:
        err(f"{w} solution", "does not finish the case")
    earned, possible, pct, missed, gates = s.score()
    print(f"  reference path: {earned:g}/{possible:g} = {pct:.0f}% (phases reached: {' → '.join(s.reached)})")
    if missed:
        warn(f"{w} solution", f"reference path misses critical items {missed}")
    if gates:
        err(f"{w} solution", f"reference path trips safety gates {gates}")
    for i, h in enumerate(c["history"]):
        if h.get("required") and not s.twins.credited(s.asked, h["id"]):
            warn(f"{w} solution", f'required history item "{h["id"]}" is never asked')
    nothing = Session(c)
    nothing.step({"type": "start"})
    e2, p2, pct2, _, _ = nothing.score()
    print(f"  doing nothing: {e2:g}/{p2:g} = {pct2:.0f}%")
    if e2 > 0:
        err(f"{w} rubric", f"a learner who does nothing earns {e2:g} points")


def replay_paths(c: dict, w: str) -> None:
    """Replay the alternative paths in `tools/paths/<case id>.json` (the README score table) and print their scores."""
    paths_file = ROOT / "tools" / "paths" / f"{c['id']}.json"
    if not paths_file.exists():
        return
    for path in json.loads(paths_file.read_text(encoding="utf-8")):
        actions = list(c["solution"])
        for edit in path.get("replace", []):
            actions = [edit["with"] if a == edit["step"] else a for a in actions]
            actions = [x for a in actions for x in (a if isinstance(a, list) else [a])]
        for edit in path.get("insertBefore", []):
            idx = actions.index(edit["step"])
            actions[idx:idx] = edit["actions"]
        if path.get("truncateAfter") is not None:
            actions = actions[: path["truncateAfter"]]
        s, rej = replay(c, actions, f'{w} path "{path["id"]}"', quiet_rejections=True)
        earned, possible, pct, missed, gates = s.score()
        gate_ids = ", ".join(g[0] for g in gates) or "none"
        print(f'  path {path["id"]:<28} {earned:>4g}/{possible:<4g} {pct:5.0f}%  finished: {"yes" if s.finished else "no "}  critical missed: {", ".join(missed) or "none"}; gates: {gate_ids}; rejected steps: {len(rej)}')
        check_expectation(path, pct, missed, gates, s.finished, f'{w} path "{path["id"]}"')


def check_expectation(path: dict, pct: float, missed: list[str], gates: list, finished: bool, where: str) -> None:
    """A path's `expect` is its defined failure condition (docs/PHASE2.md): the outcome must be exactly what it says.

    `percent`: a number (to the nearest whole percent) or `[low, high]`; `gates`: the safety gates that hold (exact
    set); `criticalMissed`: the critical rubric items missed (exact set); `finished`: whether the case can finish.
    """
    expect = path.get("expect")
    if expect is None:
        err(where, "no `expect`: every path states its outcome")
        return
    want = expect.get("percent")
    if isinstance(want, (int, float)) and round(pct) != round(want):
        err(where, f"expected {want}%, got {pct:.0f}%")
    if isinstance(want, list) and not (want[0] <= round(pct) <= want[1]):
        err(where, f"expected {want[0]}–{want[1]}%, got {pct:.0f}%")
    if "gates" in expect and sorted(expect["gates"]) != sorted(g[0] for g in gates):
        err(where, f"expected gates {sorted(expect['gates'])}, got {sorted(g[0] for g in gates)}")
    if "criticalMissed" in expect and sorted(expect["criticalMissed"]) != sorted(missed):
        err(where, f"expected critical misses {sorted(expect['criticalMissed'])}, got {sorted(missed)}")
    if "finished" in expect and bool(expect["finished"]) != finished:
        err(where, f"expected finished={expect['finished']}, got {finished}")


def check_families(cases: list[dict]) -> None:
    """Cases of one family (extensions.tcmcraft.caseFamily) share a split and every shared first-visit fact.

    A case's review is its last phase: items limited to that phase, and records' results for it, may differ between
    the family's cases; everything else is the shared first visit and must be identical.
    """
    families: dict[str, list[dict]] = {}
    for c in cases:
        fam = c.get("extensions", {}).get("tcmcraft", {}).get("caseFamily")
        if fam:
            families.setdefault(fam, []).append(c)
    for fam, members in families.items():
        w = f"family {fam}"
        splits = {m["extensions"]["tcmcraft"].get("split") for m in members}
        if len(splits) != 1 or None in splits:
            err(w, f"cases disagree on the split: {sorted(map(str, splits))}")
        for coll in ("history", "exam"):
            seen: dict[str, tuple[str, str]] = {}
            for m in members:
                review = m["phases"][-1]["id"]
                for item in m[coll]:
                    if item.get("phases") and set(item["phases"]) <= {review}:
                        continue
                    key = json.dumps({k: item.get(k) for k in ("question", "answer", "maneuver", "finding", "phases")}, ensure_ascii=False, sort_keys=True)
                    if item["id"] in seen and seen[item["id"]][1] != key:
                        err(w, f'{coll} item "{item["id"]}" differs between {seen[item["id"]][0]} and {m["id"]}')
                    seen.setdefault(item["id"], (m["id"], key))
        shared_records: dict[str, tuple[str, str]] = {}
        for m in members:
            review = m["phases"][-1]["id"]
            for inv in m["investigations"]:
                early = {ph: r for ph, r in inv["results"].items() if ph != review}
                if not early:
                    continue
                key = json.dumps(early, ensure_ascii=False, sort_keys=True)
                if inv["id"] in shared_records and shared_records[inv["id"]][1] != key:
                    err(w, f'record "{inv["id"]}" differs between {shared_records[inv["id"]][0]} and {m["id"]} before the review')
                shared_records.setdefault(inv["id"], (m["id"], key))
        print(f"  family {fam}: {len(members)} case(s), split {', '.join(map(str, splits))}: {', '.join(m['id'] for m in members)}")


# =============================================================================================
# Catalogs, templates, facilities
# =============================================================================================

def load_catalogs(cc: Path | None):
    catalogs = {}
    dirs = [CONTENT / "catalogs"]
    if cc:
        dirs.insert(0, cc / "packages" / "content" / "catalogs")
    for d in dirs:
        for f in sorted(d.glob("*.json")):
            data = json.loads(f.read_text(encoding="utf-8"))
            catalogs[data["id"]] = data
    return catalogs


def check_catalog(cat: dict, materials: set[str], where: str) -> None:
    for i, e in enumerate(cat.get("equipment", [])):
        w = f"{where} equipment.{i} ({e['id']})"
        fp = e["footprint"]
        for j, part in enumerate(e["parts"]):
            if part["m"] not in materials:
                err(w, f'part {j} uses unknown material "{part["m"]}"')
            (px, py, pz), (sx, sy, sz) = part["p"], part["s"]
            eps = 1e-6
            if abs(px) + sx / 2 > fp["w"] / 2 + eps or abs(pz) + sz / 2 > fp["d"] / 2 + eps or py - sy / 2 < -eps or py + sy / 2 > fp["h"] + eps:
                warn(w, f"part {j} leaves the footprint")
        if e.get("screen", "none") != "none" and not any(p.get("name") == "screen" for p in e["parts"]):
            warn(w, "has a screen kind but no part named screen")
        for cap in e.get("capabilities", []):
            if cap not in CANONICAL_CAPS:
                warn(w, f'non-canonical capability "{cap}"')


def rotate(x, z, rot):
    rot %= 360
    return {0: (x, z), 90: (z, -x), 180: (-x, -z), 270: (-z, x)}[rot]


def compile_facility(fac: dict, templates: dict):
    rooms = list(fac.get("rooms", []))
    placements = list(fac.get("placements", []))
    slots = list(fac.get("patientSlots", []))
    staff = list(fac.get("staff", []))
    for inst in fac.get("instances", []):
        t = templates.get(inst["template"])
        if t is None:
            err(f'facility {fac["id"]} instances.{inst["id"]}', f'unknown template "{inst["template"]}"')
            continue
        rot = inst.get("rot", 0)
        w, d = (t["size"]["w"], t["size"]["d"]) if rot in (0, 180) else (t["size"]["d"], t["size"]["w"])
        rooms.append({"id": inst["id"], "kind": t["kind"], "rect": {"x": inst["x"], "z": inst["z"], "w": w, "d": d}, "name": t["name"]})
        omit = set(inst.get("overrides", {}).get("omit", []))
        for p in t.get("placements", []):
            if p["id"] in omit:
                continue
            x, z = rotate(p["x"], p["z"], rot)
            q = dict(p, id=f'{inst["id"]}.{p["id"]}', x=inst["x"] + x, z=inst["z"] + z, room=inst["id"], rot=p.get("rot", 0) + rot)
            q.update(inst.get("overrides", {}).get("placements", {}).get(p["id"], {}))
            placements.append(q)
        for s in t.get("patientSlots", []):
            if s["id"] in omit:
                continue
            x, z = rotate(s["x"], s["z"], rot)
            q = dict(s, id=f'{inst["id"]}.{s["id"]}', x=inst["x"] + x, z=inst["z"] + z, room=inst["id"])
            for k in ("bed", "monitor"):
                if k in s:
                    q[k] = f'{inst["id"]}.{s[k]}'
            q.update(inst.get("overrides", {}).get("patientSlots", {}).get(s["id"], {}))
            slots.append(q)
        for s in t.get("staff", []):
            if s["id"] in omit:
                continue
            x, z = rotate(s["x"], s["z"], rot)
            staff.append(dict(s, id=f'{inst["id"]}.{s["id"]}', x=inst["x"] + x, z=inst["z"] + z, room=inst["id"]))
    return rooms, placements, slots, staff


def inside(rect, x, z, margin=0.0):
    return rect["x"] - rect["w"] / 2 - margin <= x <= rect["x"] + rect["w"] / 2 + margin and rect["z"] - rect["d"] / 2 - margin <= z <= rect["z"] + rect["d"] / 2 + margin


def check_facility(fac: dict, templates: dict, catalogs: dict, cases: list[dict]) -> None:
    w = f'facility {fac["id"]}'
    types = {}
    for cid in fac.get("catalogs", []):
        if cid not in catalogs:
            err(w, f'unknown catalog "{cid}" (pass --clinicalcraft for the built-in ones)')
            continue
        for e in catalogs[cid].get("equipment", []):
            types[e["id"]] = e
    rooms, placements, slots, staff = compile_facility(fac, templates)
    ids = [r["id"] for r in rooms] + [p["id"] for p in placements] + [s["id"] for s in slots] + [s["id"] for s in staff]
    dup = {x for x in ids if ids.count(x) > 1}
    if dup:
        err(w, f"duplicate ids {sorted(dup)}")
    room_by = {r["id"]: r for r in rooms}
    b = fac["bounds"]
    for i, r in enumerate(rooms):
        for o in rooms[i + 1 :]:
            a, c = r["rect"], o["rect"]
            ox = min(a["x"] + a["w"] / 2, c["x"] + c["w"] / 2) - max(a["x"] - a["w"] / 2, c["x"] - c["w"] / 2)
            oz = min(a["z"] + a["d"] / 2, c["z"] + c["d"] / 2) - max(a["z"] - a["d"] / 2, c["z"] - c["d"] / 2)
            if ox > 1e-6 and oz > 1e-6:
                err(w, f'rooms {r["id"]} and {o["id"]} overlap')
    for p in placements:
        if p["type"] not in types:
            err(w, f'placement {p["id"]}: unknown equipment type "{p["type"]}"')
            continue
        if not (b["minX"] <= p["x"] <= b["maxX"] and b["minZ"] <= p["z"] <= b["maxZ"]):
            err(w, f'placement {p["id"]} is outside the bounds')
        room = room_by.get(p.get("room"))
        if room and not inside(room["rect"], p["x"], p["z"], 0.05):
            warn(w, f'placement {p["id"]} lies outside its room {room["id"]}')
        elif room:
            # the footprint must stay clear of the room's walls (0.35 m, centred on the room edge: inner face 0.175 m in)
            fp = types[p["type"]]["footprint"]
            hw, hd = (fp["w"] / 2, fp["d"] / 2) if round(p.get("rot", 0)) % 180 == 0 else (fp["d"] / 2, fp["w"] / 2)
            r, m = room["rect"], 0.175 - 1e-6
            if (p["x"] - hw < r["x"] - r["w"] / 2 + m or p["x"] + hw > r["x"] + r["w"] / 2 - m
                    or p["z"] - hd < r["z"] - r["d"] / 2 + m or p["z"] + hd > r["z"] + r["d"] / 2 - m):
                warn(w, f'placement {p["id"]} ({p["type"]}) reaches into a wall of {room["id"]}')
    pl_by = {p["id"]: p for p in placements}
    for s in slots:
        if s.get("bed") and s["bed"] not in pl_by:
            err(w, f'slot {s["id"]}: unknown bed "{s["bed"]}"')
        elif s.get("bed") and types.get(pl_by[s["bed"]]["type"], {}).get("interaction", {}).get("kind") != "bed":
            warn(w, f'slot {s["id"]}: placement "{s["bed"]}" is not a bed (interaction kind is not "bed")')
        if s["room"] not in room_by:
            err(w, f'slot {s["id"]}: unknown room "{s["room"]}"')
    for s in staff:
        if s["room"] not in room_by:
            err(w, f'staff {s["id"]}: unknown room "{s["room"]}"')
    caps = set(PERSONAL_KIT)
    for p in placements:
        caps |= set(types.get(p["type"], {}).get("capabilities", [])) | set(p.get("capabilities", []))
    kinds = {r["kind"] for r in rooms}
    print(f"  {fac['id']}: {len(rooms)} rooms, {len(placements)} placements, {len(slots)} patient slots, {len(staff)} staff; capabilities: {', '.join(sorted(caps))}")
    for c in cases:
        if c.get("facility") != fac["id"]:
            continue
        if not any(c["setting"] in s["accepts"] for s in slots):
            err(w, f'no patient slot accepts the {c["setting"]} case {c["id"]}')
        used = set()
        for a in c.get("solution", []):
            coll, key = {"examine": ("exam", "findingId"), "order": ("investigations", "investigationId"), "intervene": ("interventions", "interventionId")}.get(a["type"], (None, None))
            if coll:
                item = next(x for x in c[coll] if x["id"] == a[key])
                used |= set(item.get("requires", []))
        gaps = used - caps
        if gaps:
            err(w, f'case {c["id"]} needs capabilities the facility lacks: {sorted(gaps)}')
        for coll in ("interventions",):
            for iv in c[coll]:
                dest = iv.get("destination", {})
                if dest.get("roomKind") and dest["roomKind"] not in kinds:
                    err(w, f'case {c["id"]} intervention {iv["id"]} goes to a {dest["roomKind"]} room the facility lacks')
        for p in c["phases"]:
            loc = p.get("location", {})
            if loc.get("roomKind") and loc["roomKind"] not in kinds:
                err(w, f'case {c["id"]} phase {p["id"]} is located in a {loc["roomKind"]} room the facility lacks')


# =============================================================================================
# Main
# =============================================================================================

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--clinicalcraft", default=os.environ.get("CLINICALCRAFT_DIR", str(ROOT.parent / "ClinicalCraft")))
    ap.add_argument("--paths", action="store_true", help="replay each case's alternative paths (tools/paths/<id>.json)")
    args = ap.parse_args()
    cc = Path(args.clinicalcraft)
    if not (cc / "packages" / "content" / "catalogs").is_dir():
        print(f"(no ClinicalCraft checkout at {cc}: built-in catalogs are not checked)")
        cc = None

    cases = []
    for f in sorted((CONTENT / "cases").glob("*/case.json")):
        c = json.loads(f.read_text(encoding="utf-8"))
        cases.append(c)
        w = f"case {c['id']}"
        print(f"case {c['id']}")
        check_shape(c, w)
        check_integrity(c, w)
        check_lints(c, w)
        check_solution(c, w)
        check_utterances(c, w)
        if args.paths:
            replay_paths(c, w)

    check_families(cases)

    catalogs = load_catalogs(cc)
    materials = {m["id"] for cat in catalogs.values() for m in cat.get("materials", [])}
    for f in sorted((CONTENT / "catalogs").glob("*.json")):
        cat = json.loads(f.read_text(encoding="utf-8"))
        print(f"catalog {cat['id']}: {len(cat.get('equipment', []))} equipment types, {len(cat.get('materials', []))} materials")
        if cc:
            check_catalog(cat, materials, f"catalog {cat['id']}")
    templates = {}
    tdirs = [CONTENT / "templates"] + ([cc / "packages" / "content" / "templates"] if cc else [])
    for d in tdirs:
        for f in sorted(d.glob("*.json")):
            t = json.loads(f.read_text(encoding="utf-8"))
            templates.setdefault(t["id"], t)
    for f in sorted((CONTENT / "templates").glob("*.json")):
        t = json.loads(f.read_text(encoding="utf-8"))
        check_enum(t["kind"], "roomKind", f"template {t['id']} kind")
        if cc:
            check_facility({"id": f"template:{t['id']}", "bounds": {"minX": -50, "maxX": 50, "minZ": -50, "maxZ": 50},
                            "catalogs": ["materials", "core-furniture", "core-clinical", "core-diagnostics"] + [x for x in catalogs if x.startswith("tcmcraft")],
                            "instances": [{"id": t["id"], "template": t["id"], "x": 0, "z": 0}]}, templates, catalogs, [])
    for f in sorted((CONTENT / "facilities").glob("*.json")):
        fac = json.loads(f.read_text(encoding="utf-8"))
        print(f"facility {fac['id']}")
        if cc:
            check_facility(fac, templates, catalogs, cases)

    for line in errors + warnings:
        print(line)
    print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
