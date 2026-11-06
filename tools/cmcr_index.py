#!/usr/bin/env python3
"""Write docs/CMCR_CORPUS.md: the 80 CMCR case reports in `CMCR中医案例80篇/`, mapped to TCMCraft modules.

Reads only the manifest CSV inside each ZIP (`本包案例目录.csv`); the PDFs are not extracted. The module mapping below is
an authoring aid for choosing phase 2+ cases (docs/DESIGN.md §9.2), made from the titles alone — confirm each against
the full text before adapting it.

    python3 tools/cmcr_index.py           # rewrite docs/CMCR_CORPUS.md
    python3 tools/cmcr_index.py --check   # exit 1 if it is out of date
"""

from __future__ import annotations

import csv
import io
import sys
import zipfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "CMCR中医案例80篇"
OUT = ROOT / "docs" / "CMCR_CORPUS.md"

MODULES = {
    "msk": "Musculoskeletal pain and spine (phase 1–2 pathway)",
    "escalation": "Escalation / care transition (a biomedical cause behind the presentation)",
    "acu": "Acupuncture and external techniques (AcuCraft, procedures)",
    "nursing": "TCM nursing techniques and care coordination",
    "gi": "Gastrointestinal (generalisation set)",
    "mind": "Sleep, mood and mental health (generalisation set)",
    "herbal": "Herbal prescribing in chronic disease (kidney, metabolic, liver)",
    "onc": "Oncology supportive care",
    "resp": "Respiratory, infection and critical care (coordination with hospital care)",
    "cv": "Cardiovascular (antiplatelet and anticoagulant interactions)",
    "women": "Women's health",
    "paeds": "Paediatrics",
    "other": "Other",
}

# case id → (primary module, note). From the titles; confirm against the full text.
MAP = {
    "1599800": ("msk", "Refractory low back and leg pain — the closest real case to tcm-sg-lbp-01"),
    "1571923": ("escalation", "Brucellosis presenting as low back pain, misdiagnosed as disc herniation — the escalation variant of DESIGN §7"),
    "1543230": ("escalation", "Cervical myelopathy treated in steps — a neurological red-flag pathway"),
    "1663729": ("escalation", "Central cord syndrome after re-injury post-ACCF — trauma and neurology"),
    "1506921": ("nursing", "Child with kyphosis, multidisciplinary nursing"),
    "1666233": ("acu", "Shoulder-hand syndrome after stroke: 黄芪桂枝五物汤 with acupuncture and TMS"),
    "1602988": ("acu", "Meridian gua sha for oral ulcers in Behçet's disease (nursing)"),
    "1504429": ("acu", "Auricular gua sha in primary Sjögren's syndrome"),
    "1494202": ("acu", "Intradermal needles with auricular gua sha for recurrent oral ulcers"),
    "1477723": ("gi", "Epigastric fullness, spleen–stomach deficiency-cold, TCM techniques (nursing)"),
    "1437010": ("acu", "Facial palsy with intractable hiccups (nursing)"),
    "1501264": ("nursing", "Lymphoedema after breast cancer, qi stagnation and blood stasis (nursing)"),
    "1485788": ("mind", "Anxiety, psychosomatic model with TCM"),
    "1517099": ("mind", "Obsessive–compulsive disorder, integrative treatment"),
    "1598240": ("gi", "Eosinophilic gastritis"),
    "1578797": ("gi", "Crohn's disease with refractory stricture"),
    "1547636": ("gi", "Diabetic gastroparesis, spleen–stomach weakness"),
    "1515367": ("gi", "Ulcerative colitis"),
    "1488155": ("gi", "Crohn's disease mainly of the rectum"),
    "1668559": ("onc", "Dysphagia in oesophageal SCC after chemo-immunotherapy, pattern-based treatment"),
    "1457194": ("onc", "Maintenance TCM after suboptimal debulking of ovarian cancer"),
    "1451400": ("onc", "Photodynamic therapy with TCM for a bleeding ulcerated tumour"),
    "1459894": ("onc", "Herbal maintenance after surgery for ovarian clear-cell carcinoma with liver metastases"),
    "1356075": ("onc", "Metastatic gastric cancer: camrelizumab, raltitrexed and herbs"),
    "1573423": ("onc", "Long survival with nasopharyngeal carcinoma and lung metastases"),
    "1563139": ("onc", "Unexplained ascites after ovarian cancer surgery, staged treatment"),
    "1549725": ("onc", "Marrow suppression after chemotherapy for metastatic retroperitoneal sarcoma"),
    "1670046": ("onc", "Severe chemotherapy-related hand-foot syndrome"),
    "1659165": ("herbal", "Renal amyloidosis, CKD 3a"),
    "1652542": ("herbal", "Herbs with haemoperfusion for CKD-associated pruritus"),
    "1620474": ("herbal", "Herbal treatment of diabetic foot gangrene"),
    "1670054": ("herbal", "CKD 3 with heart failure"),
    "1666161": ("herbal", "Diabetes with heavy proteinuria"),
    "1666174": ("herbal", "Reversal of early cirrhosis"),
    "1666221": ("herbal", "Renal amyloidosis, with literature review"),
    "1659168": ("herbal", "Minimal-change nephrotic syndrome"),
    "1573207": ("herbal", "Acute-on-chronic liver failure with jaundice"),
    "1564971": ("herbal", "Monoclonal gammopathy of renal significance"),
    "1546730": ("herbal", "Slowing diabetic kidney disease"),
    "1548240": ("herbal", "Recurrent IgA vasculitis nephritis (type IIb)"),
    "1545358": ("herbal", "Type 2 diabetes with obesity"),
    "1542166": ("herbal", "Small-volume BPH with overactive bladder"),
    "1537504": ("escalation", "Diabetic ketoacidosis treated with integrative care"),
    "1530761": ("herbal", "ANCA-associated vasculitis with renal injury"),
    "1530150": ("herbal", "CKD stage 5"),
    "1506965": ("paeds", "Adolescent CKD 5 with severe anaemia"),
    "1564974": ("herbal", "Autoimmune gastritis with severe anaemia"),
    "1670082": ("nursing", "Peritonitis related to peritoneal dialysis (nursing)"),
    "1598944": ("nursing", "Narrative and integrative nursing around ureteric cancer surgery"),
    "1450856": ("nursing", "Glaucoma after vitrectomy during lactation (nursing, with video)"),
    "1579303": ("cv", "Fulminant myocarditis in an older patient: ECMO, IABP and TCM cardiac rehabilitation"),
    "1526660": ("cv", "Integrative care after PCI for coronary heart disease — the antiplatelet theme of tcm-sg-lbp-01"),
    "1501430": ("cv", "Severe cerebral ischaemia–reperfusion injury"),
    "1541176": ("resp", "Recurrent respiratory infections with allergic rhinitis, microbiome approach"),
    "1182743": ("resp", "COVID-19 (wind-heat invading the lung): herbal analysis and medication monitoring"),
    "1664965": ("resp", "Recurrent pleural effusion, 'the lung governs water'"),
    "1665197": ("resp", "Primary ciliary dyskinesia type 29"),
    "1652010": ("resp", "Severe pancreatitis with lung inflammation and effusion"),
    "1650793": ("resp", "S. aureus pneumonia, septic shock and pyopneumothorax"),
    "1593557": ("resp", "Severe pneumonia with ARDS"),
    "1579758": ("resp", "Hypersensitivity pneumonitis"),
    "1573198": ("resp", "Pulmonary aspergillosis in an older patient"),
    "1551515": ("resp", "Klebsiella liver abscess"),
    "1546842": ("resp", "COVID-19 with Legionella pneumonia, molecular diagnosis"),
    "1536715": ("resp", "COPD with Pneumocystis pneumonia"),
    "1528905": ("resp", "Idiopathic pulmonary fibrosis with infection"),
    "1525452": ("resp", "Acute exacerbation of COPD"),
    "1523338": ("resp", "Integrative long-term management of COPD"),
    "1496994": ("resp", "Psittacosis pneumonia, isothermal amplification"),
    "1653781": ("women", "Retained products of conception for a year after curettage"),
    "1551860": ("women", "Complex chronic abnormal uterine bleeding"),
    "1546243": ("women", "Tubal abscess after induced abortion"),
    "1578451": ("women", "Plasma cell mastitis"),
    "1652212": ("paeds", "Herpangina with bronchitis"),
    "1603024": ("paeds", "Severe mycoplasma pneumonia in a child"),
    "1585756": ("paeds", "Histiocytic necrotising lymphadenitis in a child"),
    "1581636": ("paeds", "Critically ill preterm infant"),
    "1570490": ("paeds", "Influenza in a child"),
    "1553776": ("paeds", "Mycoplasma pneumonia in a child"),
    "1535559": ("paeds", "Periodic fever in a child"),
}


def manifests():
    rows = []
    for z in sorted(ARCHIVE.glob("*.zip")):
        with zipfile.ZipFile(z) as f:
            name = next(n for n in f.namelist() if n.endswith(".csv"))
            reader = csv.DictReader(io.StringIO(f.read(name).decode("utf-8-sig")))
            for row in reader:
                rows.append({**row, "package": z.name})
    return sorted(rows, key=lambda r: int(r["序号"]))


def render(rows) -> str:
    dois = Counter(r["DOI"] for r in rows)
    years = Counter(r["发表年份"] for r in rows)
    by_module = Counter(MAP.get(r["案例编号"], ("other", ""))[0] for r in rows)
    out = [
        "# CMCR TCM case corpus (80 reports)",
        "",
        "The archive in [`CMCR中医案例80篇/`](../CMCR中医案例80篇/) holds 80 published case reports of TCM and integrative care,",
        "packed in 29 ZIP files. This index is generated by `tools/cmcr_index.py` from the manifest inside each ZIP; the PDFs",
        "are not extracted. It is for **authors**, not learners: the titles name diagnoses.",
        "",
        "**Use.** Phase 1 (`tcm-sg-lbp-01`) is synthetic. Phase 2 and later (docs/DESIGN.md §9) can adapt these reports, as",
        "ClinicalCraft's CMCR collection does (its docs/CMCR_CASES.md: paraphrase, pseudonyms, relative time, unknowns kept",
        "unknown, the source shown only once the case is complete). The module column is a first sort made from the **titles alone** — confirm",
        "each against the full text.",
        "",
        "**Data-quality and governance notes.**",
        "",
        f"- The manifests give **one DOI for all {len(rows)} reports** (`{dois.most_common(1)[0][0]}`, {dois.most_common(1)[0][1]} rows): it is not",
        "  each report's DOI. Use the yiigle article link (`https://rs.yiigle.com/cmaid/<案例编号>`) and take the DOI from the",
        "  article itself before citing.",
        "- The PDFs remain © their publishers and authors. ClinicalCraft does not distribute source PDFs in Git; confirm the",
        "  permission basis for keeping them in this repository and check each one for identifying details before a case",
        "  uses it.",
        "",
        "Years: " + ", ".join(f"{y} ({n})" for y, n in sorted(years.items())) + ".",
        "",
        "## By module",
        "",
        "| Module | Reports |",
        "|---|---:|",
    ]
    for key, label in MODULES.items():
        if by_module.get(key):
            out.append(f"| {label} | {by_module[key]} |")
    out += ["", "## Priority sources for the next cases", ""]
    for cid in ("1599800", "1571923", "1526660", "1543230", "1666233", "1477723", "1485788"):
        r = next(x for x in rows if x["案例编号"] == cid)
        out.append(f"- **{cid}** {r['标题']} — {MAP[cid][1]}.")
    out += ["", "## All reports", "", "| # | Case | Year | Pages | Title | Module | Note | Package |", "|---:|---|---|---:|---|---|---|---|"]
    for r in rows:
        module, note = MAP.get(r["案例编号"], ("other", ""))
        out.append(f"| {r['序号']} | [{r['案例编号']}]({r['原文链接']}) | {r['发表年份']} | {r['页数']} | {r['标题']} | {module} | {note} | {r['package'].removesuffix('.zip').split('_')[-1]} |")
    unmapped = [r["案例编号"] for r in rows if r["案例编号"] not in MAP]
    out += ["", f"Unmapped: {', '.join(unmapped) or 'none'}.", ""]
    return "\n".join(out)


def main() -> int:
    text = render(manifests())
    if "--check" in sys.argv[1:]:
        ok = OUT.exists() and OUT.read_text(encoding="utf-8") == text
        print("docs/CMCR_CORPUS.md is up to date" if ok else "docs/CMCR_CORPUS.md is out of date: run python3 tools/cmcr_index.py")
        return 0 if ok else 1
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
