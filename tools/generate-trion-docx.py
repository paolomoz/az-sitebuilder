#!/usr/bin/env python3
"""Generate DOCX briefing for Trion (trionafenib) — Selective oral KRAS G12C inhibitor for NSCLC.

Reuses images from Velox site (images/velox/).
Includes CDN URLs as captions for each image.
"""

import os
import sys
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml

# --- Configuration ---
SITE_NAME = "trion"
SOURCE_SITE = "velox"  # Reusing velox images
BRAND_COLOUR = RGBColor(0x6A, 0x1B, 0x9A)   # Deep Purple (oncology)
ACCENT_COLOUR = RGBColor(0x00, 0x82, 0x7F)   # Teal
AZ_MAGENTA = RGBColor(0x83, 0x00, 0x51)
DARK_TEXT = RGBColor(0x36, 0x3B, 0x3B)
GREY_TEXT = RGBColor(0x66, 0x66, 0x66)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
RED_NOTICE = RGBColor(0xCC, 0x00, 0x00)

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(PROJECT_DIR, "images", SOURCE_SITE)  # Reuse velox images
CDN_BASE = f"https://{SOURCE_SITE}-images.pages.dev"
OUTPUT_PATH = os.path.join(PROJECT_DIR, "sites", SITE_NAME, "Trion-Website-Briefing.docx")

# --- Image manifest (velox filename → trion usage context) ---
IMAGE_MANIFEST = {
    "hero-home.jpeg": "Home — hero",
    "hero-efficacy.jpeg": "TRIFORCE Data — hero",
    "hero-moa.jpeg": "How TRION Works — hero",
    "card-stroke.jpeg": "Home — objective response rate card",
    "card-bleeding.jpeg": "Home — progression-free survival card",
    "card-dosing.jpeg": "Home — oral dosing convenience card",
    "columns-moa-preview.jpeg": "Home — MoA teaser",
    "tab-velocity-af.jpeg": "TRIFORCE Data — TRIFORCE-1 tab",
    "tab-velocity-bleed.jpeg": "TRIFORCE Data — TRIFORCE-LUNG tab",
    "card-bleeding-events.jpeg": "Safety — hepatotoxicity card",
    "card-hepatic.jpeg": "Safety — GI events card",
    "card-gi-events.jpeg": "Safety — QTc monitoring card",
    "columns-dosing.jpeg": "Dosing — twice-daily regimen",
    "columns-monitoring.jpeg": "Dosing — monitoring requirements",
    "card-prescribing.jpeg": "Resources — prescribing guide card",
}


# --- Document helpers ---

def set_cell_shading(cell, color_hex):
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading)


def add_heading(doc, text, level=1, color=None):
    h = doc.add_heading(text, level=level)
    if color:
        for run in h.runs:
            run.font.color.rgb = color
    return h


def add_body(doc, text, bold=False, italic=False, size=Pt(10)):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.size = size
    run.font.color.rgb = DARK_TEXT
    run.bold = bold
    run.italic = italic
    return p


def add_image_with_caption(doc, filename, width=Inches(4.5)):
    """Add image from velox image directory with CDN URL caption."""
    local_path = os.path.join(IMG_DIR, filename)
    cdn_url = f"{CDN_BASE}/{filename}"
    usage = IMAGE_MANIFEST.get(filename, "")

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    if os.path.isfile(local_path) and os.path.getsize(local_path) > 1000:
        run = p.add_run()
        try:
            run.add_picture(local_path, width=width)
            print(f"  [OK] {filename}")
        except Exception as e:
            run = p.add_run(f"[Image: {filename} — file exists but embed failed: {e}]")
            run.font.color.rgb = GREY_TEXT
            run.font.size = Pt(9)
            run.italic = True
    else:
        run = p.add_run(f"[Image: {filename} — not found in {SOURCE_SITE} images]")
        run.font.color.rgb = GREY_TEXT
        run.font.size = Pt(9)
        run.italic = True
        print(f"  [SKIP] {filename} — not found at {local_path}")

    # CDN URL caption
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = cap.add_run(cdn_url)
    r.font.size = Pt(8)
    r.font.color.rgb = RGBColor(0x00, 0x55, 0x99)
    r.underline = True

    # Usage context
    if usage:
        usage_p = doc.add_paragraph()
        usage_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r2 = usage_p.add_run(f"Usage: {usage}")
        r2.font.size = Pt(8)
        r2.font.color.rgb = GREY_TEXT
        r2.italic = True

    return p


def add_table(doc, headers, rows):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = 'Table Grid'

    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = ""
        p = cell.paragraphs[0]
        run = p.add_run(h)
        run.bold = True
        run.font.size = Pt(9)
        run.font.color.rgb = WHITE
        set_cell_shading(cell, "830051")

    for r_idx, row in enumerate(rows):
        for c_idx, val in enumerate(row):
            cell = table.rows[r_idx + 1].cells[c_idx]
            cell.text = ""
            p = cell.paragraphs[0]
            run = p.add_run(str(val))
            run.font.size = Pt(9)
            run.font.color.rgb = DARK_TEXT
            if r_idx % 2 == 1:
                set_cell_shading(cell, "F8F8F8")

    return table


def add_separator(doc):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("\u2500" * 60)
    run.font.color.rgb = RGBColor(0xCC, 0xCC, 0xCC)
    run.font.size = Pt(8)


def add_field_value(doc, label, value, label_bold=True):
    p = doc.add_paragraph()
    run_l = p.add_run(f"{label}: ")
    run_l.bold = label_bold
    run_l.font.size = Pt(10)
    run_v = p.add_run(value)
    run_v.font.size = Pt(10)
    return p


# =====================================================================
# MAIN DOCUMENT BUILD
# =====================================================================

def build_document():
    doc = Document()

    # Page setup
    section = doc.sections[0]
    section.page_width = Cm(21)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2)
    section.bottom_margin = Cm(2)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(2.5)

    # Styles
    style = doc.styles['Normal']
    style.font.name = 'Calibri'
    style.font.size = Pt(10)
    style.font.color.rgb = DARK_TEXT

    for level in range(1, 5):
        hs = doc.styles[f'Heading {level}']
        hs.font.name = 'Calibri'
        hs.font.color.rgb = AZ_MAGENTA

    # =================================================================
    # COVER PAGE
    # =================================================================
    for _ in range(6):
        doc.add_paragraph()

    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run("TRION\u00ae\u25bc")
    run.font.size = Pt(36)
    run.font.color.rgb = AZ_MAGENTA
    run.bold = True

    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = sub.add_run("(trionafenib)")
    run.font.size = Pt(18)
    run.font.color.rgb = DARK_TEXT

    doc.add_paragraph()

    desc = doc.add_paragraph()
    desc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = desc.add_run("Website Briefing")
    run.font.size = Pt(24)
    run.font.color.rgb = BRAND_COLOUR
    run.bold = True

    doc.add_paragraph()

    tagline = doc.add_paragraph()
    tagline.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = tagline.add_run("Precision where it matters.")
    run.font.size = Pt(14)
    run.font.color.rgb = BRAND_COLOUR
    run.italic = True

    doc.add_paragraph()

    for line in [
        "Document type: Final approved marketing brief for HCP website build",
        "Prepared by: Marketing \u2014 UK Oncology Franchise",
        "Approval status: MLR-approved copy \u2014 do not modify",
        "Date: March 2026",
        "Approval code: GB-11583 | DOP: March 2026",
    ]:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(line)
        run.font.size = Pt(10)
        run.font.color.rgb = GREY_TEXT

    doc.add_page_break()

    # =================================================================
    # TABLE OF CONTENTS
    # =================================================================
    add_heading(doc, "Contents", level=1, color=AZ_MAGENTA)
    toc_items = [
        "1. Drug Profile",
        "2. Mechanism of Action",
        "3. Clinical Programme: TRIFORCE",
        "4. Safety Profile",
        "5. Prescribing Information",
        "6. Adverse Event Reporting",
        "7. References",
        "8. Site Navigation",
        "9. Page Content",
        "   Page 1: Home",
        "   Page 2: TRIFORCE Data",
        "   Page 3: Safety",
        "   Page 4: Dosing & Administration",
        "   Page 5: How TRION Works",
        "   Page 6: Resources",
        "10. Footer Content",
        "11. Image Assets",
    ]
    for item in toc_items:
        p = doc.add_paragraph()
        run = p.add_run(item)
        run.font.size = Pt(10)
        run.font.color.rgb = DARK_TEXT

    doc.add_page_break()

    # =================================================================
    # 1. DRUG PROFILE
    # =================================================================
    add_heading(doc, "1. Drug Profile", level=1, color=AZ_MAGENTA)

    profile_data = [
        ("Brand name", "TRION\u00ae\u25bc"),
        ("Generic name", "trionafenib"),
        ("Drug class", "Selective covalent KRAS G12C inhibitor"),
        ("Indication", "Monotherapy for the treatment of adult patients with locally advanced or metastatic non-small cell lung cancer (NSCLC) harbouring a KRAS G12C mutation, who have progressed on or after at least one prior line of systemic therapy"),
        ("Biomarker requirement", "KRAS G12C mutation confirmed by a validated test on tumour tissue or circulating tumour DNA (ctDNA)"),
        ("Formulation", "200 mg film-coated tablet"),
        ("Dosing", "200 mg orally twice daily, with food"),
        ("Approval", "MHRA \u2014 February 2026"),
        ("Black triangle status", "\u25bc Additional monitoring required \u2014 subject to enhanced pharmacovigilance"),
        ("Brand colour", "Deep Purple #6A1B9A"),
        ("Accent colour", "Teal #00827F"),
        ("Approval code", "GB-11583"),
    ]
    add_table(doc, ["Field", "Detail"], profile_data)

    doc.add_paragraph()

    # Brand rules
    brand_notice = doc.add_paragraph()
    run = brand_notice.add_run(
        "TRION brand rule: TRION always appears in capitals, with \u00ae\u25bc on first mention per page. "
        "Generic name (trionafenib) appears in lowercase parentheses on first mention. "
        "The black triangle (\u25bc) must accompany TRION on every first mention. "
        'The approved tagline "Precision where it matters." may only be used verbatim \u2014 no variations permitted.'
    )
    run.bold = True
    run.font.size = Pt(9)
    run.font.color.rgb = RED_NOTICE

    add_separator(doc)

    # =================================================================
    # 2. MECHANISM OF ACTION
    # =================================================================
    add_heading(doc, "2. Mechanism of Action", level=1, color=AZ_MAGENTA)

    add_body(doc, (
        "Trionafenib is a potent, selective, covalent inhibitor of KRAS G12C, the most prevalent KRAS "
        "mutation in non-small cell lung cancer. KRAS G12C occurs in approximately 13% of NSCLC "
        "adenocarcinomas and drives tumour proliferation and survival through constitutive activation of "
        "the RAS\u2013MAPK signalling pathway."
    ))
    add_body(doc, (
        "The KRAS G12C mutation introduces a reactive cysteine residue (Cys12) adjacent to the nucleotide "
        "binding pocket. Trionafenib exploits this neoantigen by forming an irreversible covalent bond with "
        "Cys12 when KRAS G12C is in its GDP-bound (inactive) state. This covalent modification locks KRAS "
        "in the inactive conformation, preventing the GDP-to-GTP exchange required for RAS activation.\u00b9 \u00b2"
    ))
    add_body(doc, (
        "By selectively targeting KRAS G12C, trionafenib inhibits the following oncogenic signalling cascades:"
    ))

    mechanisms = [
        "RAS\u2013RAF\u2013MEK\u2013ERK pathway: the primary mitogenic signalling axis driving tumour cell proliferation",
        "PI3K\u2013AKT\u2013mTOR pathway: a survival and anti-apoptotic pathway frequently co-activated in KRAS-mutant NSCLC",
        "RAL\u2013GDS signalling: implicated in cell migration, vesicular trafficking, and metastatic potential",
        "KRAS-dependent immune evasion: restoration of tumour antigen presentation and T-cell recognition following KRAS inactivation",
    ]
    for m in mechanisms:
        p = doc.add_paragraph(style='List Bullet')
        run = p.add_run(m)
        run.font.size = Pt(10)

    add_body(doc, (
        "Trionafenib achieves deeper and more sustained KRAS G12C target occupancy than first-generation "
        "inhibitors through a novel binding interaction with the Switch II pocket, resulting in prolonged "
        "pathway suppression and enhanced anti-tumour activity. Preclinical data demonstrate that trionafenib "
        "retains activity against common adaptive resistance mechanisms, including feedback reactivation "
        "through receptor tyrosine kinases (RTKs) and SHP2-mediated RAS cycling.\u00b9 \u00b2 \u2075"
    ))

    add_separator(doc)

    # =================================================================
    # 3. CLINICAL PROGRAMME: TRIFORCE
    # =================================================================
    add_heading(doc, "3. Clinical Programme: TRIFORCE", level=1, color=AZ_MAGENTA)

    # TRIFORCE-1
    add_heading(doc, "TRIFORCE-1 (Phase III, pivotal \u2014 Second-line KRAS G12C NSCLC)", level=2, color=AZ_MAGENTA)
    for label, val in [
        ("Design", "Randomised, open-label, active-controlled Phase III trial"),
        ("Population", "802 adults with locally advanced or metastatic NSCLC harbouring a KRAS G12C mutation (confirmed centrally), who had progressed on or after one prior line of platinum-based chemotherapy with or without anti-PD-(L)1 therapy"),
        ("Duration", "Treated until disease progression, unacceptable toxicity, or withdrawal of consent; median follow-up 15.2 months"),
        ("Comparator", "Docetaxel 75 mg/m\u00b2 IV every 3 weeks"),
        ("Primary endpoint", "Overall survival (OS)"),
        ("Key secondary endpoints", "Progression-free survival (PFS) by blinded independent central review (BICR); confirmed objective response rate (ORR); duration of response (DoR); patient-reported outcomes (EORTC QLQ-LC13)"),
        ("Publication", "Marchetti et al. N Engl J Med 2025; 393(22): 2081\u20132093"),
    ]:
        add_field_value(doc, label, val)

    doc.add_paragraph()
    add_body(doc, "Key results:", bold=True)
    add_table(doc,
        ["Endpoint", "TRION 200 mg BD (n=401)", "Docetaxel (n=401)", "Treatment effect"],
        [
            ("Overall survival (primary)",
             "Median 14.8 months", "Median 10.4 months",
             "HR 0.66 (0.54\u20130.80); P<0.001"),
            ("12-month OS rate",
             "58.3%", "43.6%",
             "\u0394 14.7% (8.1\u201321.3)"),
            ("Progression-free survival (BICR)",
             "Median 7.8 months", "Median 4.1 months",
             "HR 0.52 (0.44\u20130.62); P<0.001"),
            ("Confirmed ORR (BICR)",
             "42.1%", "13.7%",
             "\u0394 28.4% (22.6\u201334.2); P<0.001"),
            ("Complete response",
             "3.2%", "0.5%",
             "\u2014"),
            ("Median DoR (BICR)",
             "11.3 months", "6.1 months",
             "\u2014"),
            ("Disease control rate",
             "82.5%", "56.6%",
             "\u0394 25.9% (19.8\u201332.0); P<0.001"),
            ("Symptom improvement (QLQ-LC13 cough)",
             "48.2%", "28.1%",
             "P<0.001"),
        ])

    doc.add_paragraph()

    # TRIFORCE-LUNG
    add_heading(doc, "TRIFORCE-LUNG (Phase II \u2014 Intracranial activity in brain metastases)", level=2, color=AZ_MAGENTA)
    for label, val in [
        ("Design", "Open-label, single-arm, multicentre Phase II trial"),
        ("Population", "146 adults with KRAS G12C-mutant NSCLC and measurable brain metastases (\u22651 lesion \u226510 mm), who had progressed on \u22651 prior systemic therapy; patients with untreated or progressing brain metastases were eligible"),
        ("Duration", "Treated until disease progression or unacceptable toxicity; median follow-up 12.4 months"),
        ("Primary endpoint", "Intracranial confirmed objective response rate (IC-ORR) by BICR using modified RANO-BM criteria"),
        ("Key secondary endpoints", "Intracranial disease control rate (IC-DCR); intracranial PFS; overall ORR; concordance between intracranial and extracranial responses; overall survival"),
        ("Publication", "Kim et al. Lancet Oncol 2026; 27(3): 341\u2013352"),
    ]:
        add_field_value(doc, label, val)

    doc.add_paragraph()
    add_body(doc, "Key results:", bold=True)
    add_table(doc,
        ["Endpoint", "TRION 200 mg BD (n=146)", "95% CI"],
        [
            ("IC-ORR (primary)", "37.0%", "29.2\u201345.3%"),
            ("IC complete response", "8.2%", "4.3\u201314.0%"),
            ("IC disease control rate", "74.7%", "66.8\u201381.6%"),
            ("Median IC-PFS", "6.9 months", "5.4\u20138.8 months"),
            ("Overall ORR (extracranial)", "39.0%", "31.1\u201347.4%"),
            ("IC\u2013extracranial concordance", "78.1%", "70.3\u201384.6%"),
            ("Median OS", "13.2 months", "10.8\u201316.4 months"),
            ("12-month OS rate", "54.1%", "45.5\u201362.0%"),
        ])

    p = doc.add_paragraph()
    run = p.add_run(
        "Note: TRIFORCE-LUNG included patients with both previously treated and untreated brain metastases. "
        "IC-ORR was 42.1% in untreated brain metastases (n=76) vs 31.4% in previously treated (n=70)."
    )
    run.font.size = Pt(8)
    run.font.italic = True
    run.font.color.rgb = GREY_TEXT

    add_separator(doc)

    # =================================================================
    # 4. SAFETY PROFILE
    # =================================================================
    add_heading(doc, "4. Safety Profile (Pooled TRIFORCE data, N=547 TRION)", level=1, color=AZ_MAGENTA)

    add_heading(doc, "Most common adverse events (\u226510%)", level=2, color=AZ_MAGENTA)
    add_table(doc,
        ["Adverse event", "All grades (%)", "Grade \u22653 (%)"],
        [
            ("Diarrhoea", "62.3", "8.4"),
            ("Nausea", "44.8", "2.6"),
            ("Fatigue", "38.1", "5.3"),
            ("Vomiting", "27.4", "2.0"),
            ("ALT increased", "24.6", "6.4"),
            ("AST increased", "22.8", "4.8"),
            ("Decreased appetite", "21.5", "1.8"),
            ("Arthralgia", "15.2", "0.7"),
            ("Rash", "14.6", "1.3"),
            ("Peripheral oedema", "12.4", "0.5"),
            ("Cough", "11.8", "0.2"),
            ("Anaemia", "10.9", "3.1"),
        ])

    doc.add_paragraph()

    add_heading(doc, "Hepatotoxicity", level=2, color=AZ_MAGENTA)
    add_body(doc, (
        "ALT elevations >3\u00d7 ULN occurred in 6.4% of TRION-treated patients; ALT >5\u00d7 ULN in 2.4%. "
        "AST elevations >3\u00d7 ULN occurred in 4.8%. One case (0.2%) met Hy\u2019s Law criteria and resolved "
        "upon treatment discontinuation. Median time to onset of grade \u22653 transaminase elevation was "
        "6 weeks (range 2\u201318 weeks). In all cases managed with dose modification (interruption or "
        "reduction to 200 mg once daily), transaminases returned to grade \u22641 within a median of "
        "14 days.\u00b3"
    ))
    add_body(doc, (
        "Hepatic monitoring: Assess ALT, AST, and bilirubin before initiation, every 2 weeks for the "
        "first 3 months, then monthly thereafter, and as clinically indicated. Dose modification "
        "guidance is provided in the SmPC.\u00b3"
    ), bold=True)

    doc.add_paragraph()

    add_heading(doc, "Gastrointestinal events", level=2, color=AZ_MAGENTA)
    add_body(doc, (
        "Diarrhoea was the most frequent adverse event (62.3% all grades; 8.4% grade \u22653). Median onset "
        "was 12 days after treatment initiation. Grade \u22653 diarrhoea was managed with dose interruption "
        "(median 5 days) followed by dose reduction in 3.2% of patients. Prophylactic or early loperamide "
        "is recommended. Nausea (44.8%) and vomiting (27.4%) were predominantly grade 1\u20132 and manageable "
        "with standard anti-emetics.\u00b3"
    ))

    doc.add_paragraph()

    add_heading(doc, "QTc prolongation", level=2, color=AZ_MAGENTA)
    add_body(doc, (
        "QTcF increase >60 ms from baseline occurred in 1.8% of patients. QTcF >500 ms was observed in "
        "0.7%. No torsades de pointes or sudden cardiac deaths were reported. Avoid TRION in patients "
        "with baseline QTcF >470 ms. Correct electrolyte abnormalities (potassium, magnesium) before "
        "initiation. ECG monitoring recommended at baseline, Week 4, and as clinically indicated.\u00b3"
    ))

    doc.add_paragraph()

    add_heading(doc, "Key safety findings", level=2, color=AZ_MAGENTA)
    safety_findings = [
        ("Serious adverse events", "28.3% (most common: pneumonia 4.2%, diarrhoea 2.6%, pneumonitis 1.8%)"),
        ("Treatment discontinuation due to AEs", "9.7% (hepatotoxicity 2.4%, pneumonitis 1.5%, diarrhoea 1.3%)"),
        ("Dose reductions", "22.1% (diarrhoea 7.8%, hepatotoxicity 5.1%, fatigue 3.6%)"),
        ("Dose interruptions", "38.6%"),
        ("Fatal AEs", "2.4% (1.6% considered disease-related; 0.5% possibly treatment-related: pneumonitis n=2, hepatic failure n=1)"),
        ("Interstitial lung disease/pneumonitis", "3.8% all grades; 1.8% grade \u22653. Median onset 8.2 weeks. Permanently discontinue for grade \u22652\u00b3"),
    ]
    for label, val in safety_findings:
        p = doc.add_paragraph()
        run_l = p.add_run(f"{label}: ")
        run_l.bold = True
        run_l.font.size = Pt(10)
        run_v = p.add_run(val)
        run_v.font.size = Pt(10)

    doc.add_paragraph()

    add_heading(doc, "Special populations", level=2, color=AZ_MAGENTA)
    special_pops = [
        "Elderly (\u226565 years): 42% of TRIFORCE-1 patients were \u226565 years. Efficacy was consistent (OS HR 0.64 in \u226565 subgroup). Grade \u22653 AEs were modestly higher (52% vs 44% in <65 years), primarily driven by fatigue and hepatotoxicity. No dose adjustment required.\u00b3",
        "Renal impairment: Mild to moderate renal impairment (CrCl 30\u201389 mL/min) does not require dose adjustment. Not studied in severe renal impairment (CrCl <30 mL/min) or dialysis.\u00b3",
        "Hepatic impairment: Not recommended in moderate or severe hepatic impairment (Child-Pugh B or C). No dose adjustment for mild hepatic impairment (Child-Pugh A).\u00b3",
        "Reproductive toxicity: Trionafenib was embryotoxic and teratogenic in animal studies. Women of childbearing potential must use effective contraception during treatment and for 7 days after the last dose. Men with female partners of childbearing potential must use effective contraception during treatment and for 14 days after the last dose.\u00b3",
    ]
    for sp in special_pops:
        p = doc.add_paragraph(style='List Bullet')
        colon_idx = sp.index(":")
        run_b = p.add_run(sp[:colon_idx + 1])
        run_b.bold = True
        run_b.font.size = Pt(10)
        run_v = p.add_run(sp[colon_idx + 1:])
        run_v.font.size = Pt(10)

    add_separator(doc)

    # =================================================================
    # 5. PRESCRIBING INFORMATION
    # =================================================================
    add_heading(doc, "5. Prescribing Information (abbreviated \u2014 for every page footer)", level=1, color=AZ_MAGENTA)

    pi_text = (
        "TRION\u25bc (trionafenib) 200 mg film-coated tablets. "
        "Please refer to the Summary of Product Characteristics (SmPC) before prescribing. "
        "Indication: Monotherapy for the treatment of adult patients with locally advanced or metastatic "
        "non-small cell lung cancer harbouring a KRAS G12C mutation, who have progressed on or after at "
        "least one prior line of systemic therapy. KRAS G12C mutation must be confirmed by a validated test. "
        "Dosage and administration: 200 mg orally twice daily with food. Swallow whole; do not crush or "
        "chew. If a dose is missed by more than 6 hours, skip that dose and take the next scheduled dose. "
        "Dose modifications: Reduce to 200 mg once daily for grade \u22653 adverse reactions per SmPC guidance. "
        "Permanently discontinue for grade \u22652 ILD/pneumonitis or recurrent grade 4 hepatotoxicity. "
        "Contraindications: Hypersensitivity to trionafenib or excipients. Concomitant use of strong "
        "CYP3A4 inducers. Baseline QTcF >470 ms. "
        "Warnings and precautions: Hepatotoxicity: Monitor ALT, AST, bilirubin before initiation, every "
        "2 weeks for 3 months, then monthly. ILD/Pneumonitis: Monitor for new or worsening respiratory "
        "symptoms. QTc prolongation: ECG at baseline and Week 4. Correct electrolytes before initiation. "
        "Interactions: Avoid strong CYP3A4 inducers (rifampicin, phenytoin, carbamazepine, St John\u2019s wort). "
        "Caution with moderate CYP3A4 inhibitors; consider dose reduction to 200 mg once daily. "
        "Avoid concomitant QT-prolonging medications. "
        "Side effects: Very common (\u22651/10): diarrhoea, nausea, fatigue, vomiting, ALT/AST increased, "
        "decreased appetite, arthralgia, rash, peripheral oedema, cough, anaemia. Common (\u22651/100 to "
        "<1/10): pneumonitis/ILD, QTcF prolongation, renal impairment. "
        "Legal category: POM. Pack and price: 120 tablets (200 mg): \u00a35,280.00. "
        "Marketing authorisation holder: AstraZeneca UK Ltd. MA number: PLGB 17901/0734. "
        "Full prescribing information available from: AstraZeneca UK Ltd, 2 Pancras Square, London N1C 4AG. "
        "GB-11583 | DOP: March 2026."
    )
    add_body(doc, pi_text, size=Pt(9))

    add_separator(doc)

    # =================================================================
    # 6. ADVERSE EVENT REPORTING
    # =================================================================
    add_heading(doc, "6. Adverse Event Reporting (for every page footer)", level=1, color=AZ_MAGENTA)
    add_body(doc, (
        "Adverse events should be reported. Reporting forms and information can be found at "
        "www.mhra.gov.uk/yellowcard or search for MHRA Yellow Card in the Google Play or Apple App Store. "
        "Adverse events should also be reported to AstraZeneca by visiting contactazmedical.astrazeneca.com "
        "or by calling 0800 783 0033."
    ))

    add_separator(doc)

    # =================================================================
    # 7. REFERENCES
    # =================================================================
    add_heading(doc, "7. References (for every page footer)", level=1, color=AZ_MAGENTA)
    refs = [
        "Marchetti et al. N Engl J Med 2025; 393(22): 2081\u20132093.",
        "Kim et al. Lancet Oncol 2026; 27(3): 341\u2013352.",
        "TRION (trionafenib) Summary of Product Characteristics. AstraZeneca UK Ltd. February 2026.",
        "Canon J, et al. Nature 2019; 575(7781): 217\u2013223.",
        "Skoulidis F, et al. N Engl J Med 2021; 384(25): 2371\u20132381.",
    ]
    for i, ref in enumerate(refs, 1):
        p = doc.add_paragraph()
        run = p.add_run(f"{i}.  {ref}")
        run.font.size = Pt(10)
        run.italic = True

    add_separator(doc)

    # =================================================================
    # 8. SITE NAVIGATION
    # =================================================================
    add_heading(doc, "8. Site Navigation", level=1, color=AZ_MAGENTA)

    nav_items = [
        ("Top bar links", "Contact Us (https://www.astrazeneca.co.uk/contact-us.html) | AZ Employee Login (https://login.astrazeneca.com)"),
        ("Main navigation pages", "TRIFORCE Data | Safety | Dosing & Administration | How TRION Works | Resources"),
        ("Utility", "Search | Login"),
    ]
    for label, val in nav_items:
        add_field_value(doc, label, val)

    doc.add_page_break()

    # =================================================================
    # 9. PAGE CONTENT
    # =================================================================
    add_heading(doc, "9. Page Content", level=1, color=AZ_MAGENTA)

    notice = doc.add_paragraph()
    run = notice.add_run(
        "IMPORTANT: All copy below is final and MLR-approved. It must be used exactly as written \u2014 "
        "do not modify, rephrase, or abbreviate any text. All superscript reference numbers, statistical "
        "values, and regulatory language must be reproduced verbatim."
    )
    run.bold = True
    run.font.size = Pt(10)
    run.font.color.rgb = RED_NOTICE

    notice2 = doc.add_paragraph()
    run = notice2.add_run(
        "Each page must end with expandable sections for Prescribing Information, Adverse Event Reporting, "
        "and References (see sections 5, 6, and 7 above)."
    )
    run.bold = True
    run.font.size = Pt(10)
    run.font.color.rgb = RED_NOTICE

    notice3 = doc.add_paragraph()
    run = notice3.add_run(
        'TRION brand rule: TRION always appears in capitals, with \u00ae\u25bc on first mention per page. '
        'Generic name (trionafenib) in lowercase parentheses on first mention. '
        'Black triangle (\u25bc) mandatory on every first mention. '
        'Tagline "Precision where it matters." verbatim only.'
    )
    run.bold = True
    run.font.size = Pt(10)
    run.font.color.rgb = RED_NOTICE

    add_separator(doc)

    # =====================================================================
    # PAGE 1: HOME
    # =====================================================================
    doc.add_page_break()
    add_heading(doc, "PAGE 1: Home", level=2, color=AZ_MAGENTA)
    add_field_value(doc, "URL path", "/trion/")
    add_separator(doc)

    # Section 1 — Hero
    add_heading(doc, "Section 1 \u2014 Hero (full-width image with text overlay)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "hero-teaser")
    doc.add_paragraph()
    add_image_with_caption(doc, "hero-home.jpeg", width=Inches(5.5))

    add_field_value(doc, "Heading", "TRION\u00ae\u25bc (trionafenib)")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "A selective oral KRAS G12C inhibitor for previously treated locally advanced or metastatic NSCLC. "
        "42% confirmed objective response rate with a median overall survival of 14.8 months versus "
        "10.4 months with docetaxel. Precision where it matters.\u00b9"
    )
    add_field_value(doc, "Call to action", "Explore the TRIFORCE data \u2192 /trion/triforce-data")

    add_separator(doc)

    # Section 2 — Key benefit cards
    add_heading(doc, "Section 2 \u2014 Three key benefit cards (equal columns)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "cards-teaser")

    # Card 1 — ORR
    doc.add_paragraph()
    add_image_with_caption(doc, "card-stroke.jpeg", width=Inches(3))
    add_field_value(doc, "Card heading", "42% confirmed objective response rate")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "In TRIFORCE-1, TRION demonstrated a confirmed ORR of 42.1% by blinded independent central "
        "review (vs 13.7% with docetaxel; P<0.001), including a 3.2% complete response rate, in adult "
        "patients with previously treated KRAS G12C-mutant NSCLC.\u00b9"
    )
    add_field_value(doc, "Card link", "View TRIFORCE data \u2192 /trion/triforce-data")

    add_separator(doc)

    # Card 2 — Survival
    add_image_with_caption(doc, "card-bleeding.jpeg", width=Inches(3))
    add_field_value(doc, "Card heading", "Significant overall survival benefit")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "TRION significantly improved median overall survival to 14.8 months versus 10.4 months with "
        "docetaxel (HR 0.66; 95% CI: 0.54\u20130.80; P<0.001) \u2014 the first KRAS G12C inhibitor to "
        "demonstrate a statistically significant overall survival advantage in a randomised Phase III trial.\u00b9"
    )
    add_field_value(doc, "Card link", "Explore survival outcomes \u2192 /trion/triforce-data")

    add_separator(doc)

    # Card 3 — Oral dosing
    add_image_with_caption(doc, "card-dosing.jpeg", width=Inches(3))
    add_field_value(doc, "Card heading", "Convenient oral dosing")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "200 mg orally twice daily, taken with food. An oral targeted therapy offering patients an "
        "alternative to IV chemotherapy, with a manageable adverse event profile and established "
        "dose modification guidance for the most common treatment-related events.\u00b3"
    )
    add_field_value(doc, "Card link", "View dosing information \u2192 /trion/dosing")

    add_separator(doc)

    # Section 3 — Disease context
    add_heading(doc, "Section 3 \u2014 Disease context (centred text) | light background", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "introduction")
    p = doc.add_paragraph()
    run = p.add_run("Section metadata: ")
    run.bold = True
    p.add_run("Style: light").font.color.rgb = GREY_TEXT

    add_field_value(doc, "Heading", "KRAS G12C: the most prevalent actionable KRAS mutation in NSCLC")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "KRAS mutations are the most frequent oncogenic driver in NSCLC, occurring in approximately "
        "25\u201330% of lung adenocarcinomas. KRAS G12C is the predominant KRAS mutation subtype, "
        "present in approximately 13% of NSCLC adenocarcinomas. Historically considered undruggable, "
        "KRAS G12C can now be selectively targeted by covalent inhibitors that exploit the unique "
        "cysteine residue at position 12. Despite advances with first-generation inhibitors, outcomes "
        "remain suboptimal with limited overall survival benefit, underscoring the need for more "
        "effective KRAS G12C-directed therapies.\u2074 \u2075"
    )

    add_separator(doc)

    # Section 4 — Mechanism teaser
    add_heading(doc, "Section 4 \u2014 Mechanism teaser (two-column: image left, text right) | highlight background", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "columns-teaser")
    p = doc.add_paragraph()
    run = p.add_run("Section metadata: ")
    run.bold = True
    p.add_run("Style: highlight").font.color.rgb = GREY_TEXT

    doc.add_paragraph()
    add_image_with_caption(doc, "columns-moa-preview.jpeg", width=Inches(3.5))

    add_field_value(doc, "Heading", "Deep and sustained KRAS G12C target engagement")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Trionafenib forms an irreversible covalent bond with the mutant cysteine residue on KRAS G12C, "
        "locking the oncoprotein in its inactive GDP-bound state and shutting down the RAS\u2013MAPK "
        "signalling cascade. A novel Switch II pocket interaction delivers deeper and more sustained "
        "target occupancy than first-generation KRAS G12C inhibitors.\u00b3 \u2075"
    )
    add_field_value(doc, "Call to action", "Explore how TRION works \u2192 /trion/how-trion-works")

    add_separator(doc)

    # Section 5 — Accordion
    add_heading(doc, "Section 5 \u2014 Prescribing information footer", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "accordion")
    add_body(doc, "Expandable sections for: Prescribing Information | Adverse Event Reporting | References (Use approved text from sections 5, 6, and 7 above)", italic=True)

    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run("Page metadata")
    run.bold = True
    run.font.color.rgb = AZ_MAGENTA
    add_body(doc, "Title: TRION (trionafenib) | KRAS G12C Inhibitor for NSCLC | AstraZeneca UK")
    add_body(doc, "Description: TRION (trionafenib) is a selective oral KRAS G12C inhibitor for locally advanced or metastatic NSCLC. Explore TRIFORCE clinical data, safety, and dosing for UK healthcare professionals.")

    # =====================================================================
    # PAGE 2: TRIFORCE DATA
    # =====================================================================
    doc.add_page_break()
    add_heading(doc, "PAGE 2: TRIFORCE Data", level=2, color=AZ_MAGENTA)
    add_field_value(doc, "URL path", "/trion/triforce-data")
    add_separator(doc)

    # Hero
    add_heading(doc, "Section 1 \u2014 Hero (full-width image with text overlay)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "hero-teaser")
    doc.add_paragraph()
    add_image_with_caption(doc, "hero-efficacy.jpeg", width=Inches(5.5))

    add_field_value(doc, "Heading", "The TRIFORCE clinical programme")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "TRION\u00ae\u25bc (trionafenib) demonstrated significant overall survival benefit and intracranial "
        "activity across two clinical trials in patients with KRAS G12C-mutant NSCLC.\u00b9 \u00b2"
    )

    add_separator(doc)

    # Programme overview
    add_heading(doc, "Section 2 \u2014 Programme overview (centred text) | light background", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "introduction")
    p = doc.add_paragraph()
    run = p.add_run("Section metadata: ")
    run.bold = True
    p.add_run("Style: light").font.color.rgb = GREY_TEXT

    add_field_value(doc, "Heading", "Addressing unmet needs in KRAS G12C-mutant NSCLC")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "TRIFORCE-1 was the first Phase III trial to demonstrate a statistically significant overall "
        "survival benefit for a KRAS G12C inhibitor versus standard of care in previously treated NSCLC. "
        "TRIFORCE-LUNG evaluated intracranial activity in patients with measurable brain metastases \u2014 "
        "an area of critical unmet need, as brain metastases occur in up to 40% of patients with "
        "advanced NSCLC and are associated with poor prognosis and limited treatment options.\u00b9 \u00b2"
    )

    add_separator(doc)

    # Tabs
    add_heading(doc, "Section 3 \u2014 Clinical data (two tabs)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "tabs-large")

    # Tab 1 — TRIFORCE-1
    doc.add_paragraph()
    add_body(doc, 'Tab 1: "TRIFORCE-1: Overall survival"', bold=True)
    add_image_with_caption(doc, "tab-velocity-af.jpeg", width=Inches(3.5))

    add_field_value(doc, "Heading", "TRIFORCE-1: The first KRAS G12C inhibitor to demonstrate an OS benefit")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "TRIFORCE-1 was a randomised, open-label, Phase III trial comparing TRION 200 mg twice daily "
        "with docetaxel 75 mg/m\u00b2 IV Q3W in 802 adults with previously treated KRAS G12C-mutant "
        "locally advanced or metastatic NSCLC. Over a median follow-up of 15.2 months, TRION "
        "demonstrated a statistically significant improvement in the primary endpoint of overall "
        "survival: median OS 14.8 months vs 10.4 months (HR 0.66; 95% CI: 0.54\u20130.80; P<0.001).\u00b9"
    )
    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run("Body text (continued): ")
    run.bold = True
    p.add_run(
        "TRION significantly improved progression-free survival (median 7.8 vs 4.1 months; HR 0.52; "
        "P<0.001) and confirmed objective response rate (42.1% vs 13.7%; P<0.001) by blinded "
        "independent central review. The median duration of response was 11.3 months. The disease "
        "control rate was 82.5% with TRION vs 56.6% with docetaxel. Patient-reported symptoms also "
        "improved significantly, with 48.2% of TRION patients reporting improvement in cough "
        "(vs 28.1%; P<0.001).\u00b9"
    )

    add_body(doc, "Data table:", bold=True)
    add_table(doc,
        ["Endpoint", "TRION (n=401)", "Docetaxel (n=401)", "Treatment effect"],
        [
            ("Overall survival", "14.8 months", "10.4 months", "HR 0.66 (0.54\u20130.80); P<0.001"),
            ("12-month OS rate", "58.3%", "43.6%", "\u0394 14.7% (8.1\u201321.3)"),
            ("PFS (BICR)", "7.8 months", "4.1 months", "HR 0.52 (0.44\u20130.62); P<0.001"),
            ("Confirmed ORR (BICR)", "42.1%", "13.7%", "\u0394 28.4% (22.6\u201334.2); P<0.001"),
            ("Disease control rate", "82.5%", "56.6%", "\u0394 25.9% (19.8\u201332.0); P<0.001"),
        ])

    add_separator(doc)

    # Tab 2 — TRIFORCE-LUNG
    add_body(doc, 'Tab 2: "TRIFORCE-LUNG: Intracranial activity"', bold=True)
    add_image_with_caption(doc, "tab-velocity-bleed.jpeg", width=Inches(3.5))

    add_field_value(doc, "Heading", "TRIFORCE-LUNG: Meaningful intracranial activity in brain metastases")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "TRIFORCE-LUNG was an open-label, single-arm Phase II trial in 146 adults with KRAS G12C-mutant "
        "NSCLC and measurable brain metastases (\u22651 lesion \u226510 mm), including patients with untreated "
        "or progressing CNS disease.\u00b2"
    )
    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run("Body text (continued): ")
    run.bold = True
    p.add_run(
        "TRION achieved an intracranial confirmed ORR of 37.0% (95% CI: 29.2\u201345.3%), including 8.2% "
        "intracranial complete responses. The intracranial disease control rate was 74.7%. Intracranial "
        "PFS was a median of 6.9 months. Notably, the intracranial response rate was higher in patients "
        "with previously untreated brain metastases (42.1%) compared with previously treated lesions "
        "(31.4%), suggesting meaningful CNS penetration. Intracranial and extracranial responses were "
        "concordant in 78.1% of patients.\u00b2"
    )

    add_body(doc, "Data table:", bold=True)
    add_table(doc,
        ["Endpoint", "TRION (n=146)", "95% CI"],
        [
            ("IC-ORR (primary)", "37.0%", "29.2\u201345.3%"),
            ("IC complete response", "8.2%", "4.3\u201314.0%"),
            ("IC disease control rate", "74.7%", "66.8\u201381.6%"),
            ("Median IC-PFS", "6.9 months", "5.4\u20138.8 months"),
            ("Overall ORR", "39.0%", "31.1\u201347.4%"),
        ])

    add_separator(doc)

    # Accordion + metadata
    add_heading(doc, "Section 4 \u2014 Prescribing information footer", level=3, color=BRAND_COLOUR)
    add_body(doc, "Block: accordion  |  Expandable: PI | AE Reporting | References", italic=True)

    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run("Page metadata")
    run.bold = True
    run.font.color.rgb = AZ_MAGENTA
    add_body(doc, "Title: TRIFORCE Data | TRION (trionafenib) | OS & Intracranial Activity in NSCLC | AstraZeneca UK")
    add_body(doc, "Description: Explore the TRIFORCE clinical programme for TRION (trionafenib) \u2014 Phase III overall survival benefit and intracranial activity in KRAS G12C-mutant non-small cell lung cancer.")

    # =====================================================================
    # PAGE 3: SAFETY
    # =====================================================================
    doc.add_page_break()
    add_heading(doc, "PAGE 3: Safety", level=2, color=AZ_MAGENTA)
    add_field_value(doc, "URL path", "/trion/safety")
    add_separator(doc)

    # Title block
    add_heading(doc, "Section 1 \u2014 Page header (text only, no image)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "title")
    add_field_value(doc, "Heading", "Safety profile of TRION")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "TRION\u00ae\u25bc (trionafenib) has been evaluated in 547 patients across the TRIFORCE clinical "
        "programme, with a well-characterised safety profile and established dose modification guidance.\u00b9 \u00b2 \u00b3"
    )

    add_separator(doc)

    # Key safety message
    add_heading(doc, "Section 2 \u2014 Key safety message (centred text) | highlight background", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "introduction")
    p = doc.add_paragraph()
    run = p.add_run("Section metadata: ")
    run.bold = True
    p.add_run("Style: highlight").font.color.rgb = GREY_TEXT

    add_field_value(doc, "Heading", "A manageable safety profile with established dose modification guidance")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "The most common adverse events with TRION are gastrointestinal (diarrhoea, nausea, vomiting) "
        "and hepatotoxicity (transaminase elevations), which are manageable with standard supportive care "
        "and protocol-defined dose modifications. Treatment discontinuation due to adverse events occurred "
        "in 9.7% of patients. Hepatic function should be monitored regularly, and patients should be "
        "counselled on early recognition and management of diarrhoea.\u00b3"
    )

    add_separator(doc)

    # Safety cards
    add_heading(doc, "Section 3 \u2014 Safety topic cards (three equal columns)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "cards-teaser")

    # Card 1 — Hepatotoxicity
    doc.add_paragraph()
    add_image_with_caption(doc, "card-bleeding-events.jpeg", width=Inches(3))
    add_field_value(doc, "Card heading", "Hepatotoxicity")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "Grade \u22653 ALT elevation occurred in 6.4% of TRION-treated patients; grade \u22653 AST elevation "
        "in 4.8%. Median onset: 6 weeks. In all cases managed with dose modification, transaminases "
        "returned to grade \u22641 within a median of 14 days. Monitor ALT, AST, and bilirubin every "
        "2 weeks for 3 months, then monthly.\u00b3"
    )

    add_separator(doc)

    # Card 2 — GI events
    add_image_with_caption(doc, "card-hepatic.jpeg", width=Inches(3))
    add_field_value(doc, "Card heading", "Gastrointestinal events")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "Diarrhoea was the most frequent adverse event (62.3% all grades; 8.4% grade \u22653). Nausea "
        "(44.8%) and vomiting (27.4%) were predominantly grade 1\u20132. Grade \u22653 diarrhoea was managed "
        "with dose interruption (median 5 days). Prophylactic or early loperamide is recommended. "
        "Standard anti-emetics are effective for nausea and vomiting.\u00b3"
    )

    add_separator(doc)

    # Card 3 — QTc
    add_image_with_caption(doc, "card-gi-events.jpeg", width=Inches(3))
    add_field_value(doc, "Card heading", "QTc prolongation")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "QTcF increase >60 ms from baseline: 1.8%. QTcF >500 ms: 0.7%. No torsades de pointes or "
        "sudden cardiac deaths were reported. Avoid use if baseline QTcF >470 ms. Correct electrolyte "
        "abnormalities before initiation. ECG at baseline, Week 4, and as clinically indicated.\u00b3"
    )

    add_separator(doc)

    # Section 4 — AE table
    add_heading(doc, "Section 4 \u2014 Adverse events table | light background", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "table-data")
    p = doc.add_paragraph()
    run = p.add_run("Section metadata: ")
    run.bold = True
    p.add_run("Style: light").font.color.rgb = GREY_TEXT

    add_field_value(doc, "Heading", "Most common adverse events (\u226510%) \u2014 pooled TRIFORCE data")

    add_table(doc,
        ["Adverse event", "All grades (%)", "Grade \u22653 (%)"],
        [
            ("Diarrhoea", "62.3", "8.4"),
            ("Nausea", "44.8", "2.6"),
            ("Fatigue", "38.1", "5.3"),
            ("Vomiting", "27.4", "2.0"),
            ("ALT increased", "24.6", "6.4"),
            ("AST increased", "22.8", "4.8"),
            ("Decreased appetite", "21.5", "1.8"),
            ("Arthralgia", "15.2", "0.7"),
            ("Rash", "14.6", "1.3"),
            ("Peripheral oedema", "12.4", "0.5"),
            ("Cough", "11.8", "0.2"),
            ("Anaemia", "10.9", "3.1"),
        ])

    add_separator(doc)

    # Section 5 — ILD/Pneumonitis
    add_heading(doc, "Section 5 \u2014 ILD/Pneumonitis warning (centred text)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "introduction")

    add_field_value(doc, "Heading", "Interstitial lung disease / pneumonitis")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "ILD/pneumonitis occurred in 3.8% of TRION-treated patients (1.8% grade \u22653). Median time "
        "to onset was 8.2 weeks. Two fatal cases of pneumonitis were reported (0.4%), both assessed as "
        "possibly treatment-related. Monitor patients for new or worsening respiratory symptoms "
        "(dyspnoea, cough, fever). Withhold TRION for suspected ILD/pneumonitis pending investigation. "
        "Permanently discontinue for confirmed grade \u22652 ILD/pneumonitis.\u00b3"
    )

    add_separator(doc)

    # Accordion + metadata
    add_heading(doc, "Section 6 \u2014 Prescribing information footer", level=3, color=BRAND_COLOUR)
    add_body(doc, "Block: accordion  |  Expandable: PI | AE Reporting | References", italic=True)

    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run("Page metadata")
    run.bold = True
    run.font.color.rgb = AZ_MAGENTA
    add_body(doc, "Title: Safety Profile | TRION (trionafenib) | Adverse Events & Monitoring | AstraZeneca UK")
    add_body(doc, "Description: Review the safety profile of TRION (trionafenib), including hepatotoxicity, GI events, QTc monitoring, and ILD/pneumonitis guidance from the TRIFORCE clinical programme.")

    # =====================================================================
    # PAGE 4: DOSING & ADMINISTRATION
    # =====================================================================
    doc.add_page_break()
    add_heading(doc, "PAGE 4: Dosing & Administration", level=2, color=AZ_MAGENTA)
    add_field_value(doc, "URL path", "/trion/dosing")
    add_separator(doc)

    # Title block
    add_heading(doc, "Section 1 \u2014 Page header (text only, no image)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "title")
    add_field_value(doc, "Heading", "Dosing and administration")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "TRION\u00ae\u25bc (trionafenib) 200 mg twice daily, taken orally with food. Dose modification "
        "guidance is established for the most common treatment-related adverse events.\u00b3"
    )

    add_separator(doc)

    # Key dosing message
    add_heading(doc, "Section 2 \u2014 Key dosing message (centred text) | highlight background", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "introduction")
    p = doc.add_paragraph()
    run = p.add_run("Section metadata: ")
    run.bold = True
    p.add_run("Style: highlight").font.color.rgb = GREY_TEXT

    add_field_value(doc, "Heading", "Oral targeted therapy with clear dose modification pathways")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "TRION offers patients a convenient oral alternative to intravenous chemotherapy. The recommended "
        "starting dose is 200 mg twice daily with food. If dose reduction is required for adverse events, "
        "reduce to 200 mg once daily. Clear dose interruption and reduction criteria are defined in the "
        "SmPC for hepatotoxicity, diarrhoea, QTc prolongation, and other treatment-emergent events.\u00b3"
    )

    add_separator(doc)

    # Dosing columns
    add_heading(doc, "Section 3 \u2014 Dosing details (two-column: image left, text right)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "columns-teaser")

    doc.add_paragraph()
    add_image_with_caption(doc, "columns-dosing.jpeg", width=Inches(3.5))

    add_field_value(doc, "Heading", "Recommended dose and administration")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "The recommended dose of TRION is 200 mg (one tablet) taken orally twice daily, approximately "
        "12 hours apart, with food. Tablets should be swallowed whole and must not be crushed or chewed. "
        "If a dose is missed by more than 6 hours from the scheduled time, skip that dose and take the "
        "next dose at the regular time. Do not take a double dose.\u00b3"
    )
    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run("Body text (continued): ")
    run.bold = True
    p.add_run(
        "Dose modification for adverse events: For grade \u22653 hepatotoxicity (ALT or AST >5\u00d7 ULN), "
        "withhold until resolution to grade \u22641, then resume at 200 mg once daily. For grade \u22653 diarrhoea "
        "despite optimal medical management, withhold until resolution to grade \u22641, then resume at the "
        "same or reduced dose. For QTcF >500 ms, withhold until QTcF returns to \u2264470 ms and resume at "
        "200 mg once daily. Permanently discontinue for recurrent grade 4 hepatotoxicity or confirmed "
        "grade \u22652 ILD/pneumonitis.\u00b3"
    )

    add_separator(doc)

    # Monitoring columns
    add_heading(doc, "Section 4 \u2014 Monitoring requirements (two-column: image left, text right) | light background", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "columns-teaser")
    p = doc.add_paragraph()
    run = p.add_run("Section metadata: ")
    run.bold = True
    p.add_run("Style: light").font.color.rgb = GREY_TEXT

    doc.add_paragraph()
    add_image_with_caption(doc, "columns-monitoring.jpeg", width=Inches(3.5))

    add_field_value(doc, "Heading", "Monitoring and pre-treatment assessment")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Before initiation: Confirm KRAS G12C mutation by validated test. Assess hepatic function "
        "(ALT, AST, bilirubin). Obtain ECG (QTcF must be \u2264470 ms). Correct electrolyte abnormalities "
        "(potassium, magnesium, calcium). Assess pregnancy status in women of childbearing potential.\u00b3"
    )
    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run("Body text (continued): ")
    run.bold = True
    p.add_run(
        "During treatment: Monitor ALT, AST, and bilirubin every 2 weeks for the first 3 months, then "
        "monthly thereafter and as clinically indicated. Repeat ECG at Week 4 and as clinically indicated. "
        "Assess renal function periodically. Monitor for respiratory symptoms (cough, dyspnoea, fever) "
        "at each visit \u2014 investigate promptly if ILD/pneumonitis is suspected.\u00b3"
    )

    add_separator(doc)

    # Drug interactions
    add_heading(doc, "Section 5 \u2014 Drug interactions (centred text)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "introduction")

    add_field_value(doc, "Heading", "Key drug interactions")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Contraindicated: Strong CYP3A4 inducers (rifampicin, carbamazepine, phenytoin, St John\u2019s wort) "
        "\u2014 may significantly reduce trionafenib plasma concentrations and efficacy. "
        "Caution: Moderate CYP3A4 inhibitors (erythromycin, diltiazem, fluconazole) increase trionafenib "
        "exposure approximately 1.6-fold; consider dose reduction to 200 mg once daily if concomitant use "
        "is unavoidable. Strong CYP3A4 inhibitors (ketoconazole, itraconazole) increase exposure "
        "approximately 2.4-fold; avoid concomitant use. Avoid QT-prolonging medications where possible; "
        "if concomitant use is required, increase ECG monitoring frequency.\u00b3"
    )

    add_separator(doc)

    # Accordion + metadata
    add_heading(doc, "Section 6 \u2014 Prescribing information footer", level=3, color=BRAND_COLOUR)
    add_body(doc, "Block: accordion  |  Expandable: PI | AE Reporting | References", italic=True)

    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run("Page metadata")
    run.bold = True
    run.font.color.rgb = AZ_MAGENTA
    add_body(doc, "Title: Dosing & Administration | TRION (trionafenib) | 200 mg BD Oral | AstraZeneca UK")
    add_body(doc, "Description: TRION (trionafenib) dosing and administration: 200 mg twice daily with food. Dose modification guidance, monitoring requirements, and drug interaction information for UK healthcare professionals.")

    # =====================================================================
    # PAGE 5: HOW TRION WORKS
    # =====================================================================
    doc.add_page_break()
    add_heading(doc, "PAGE 5: How TRION Works", level=2, color=AZ_MAGENTA)
    add_field_value(doc, "URL path", "/trion/how-trion-works")
    add_separator(doc)

    # Hero
    add_heading(doc, "Section 1 \u2014 Hero (full-width image with text overlay)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "hero-teaser")
    doc.add_paragraph()
    add_image_with_caption(doc, "hero-moa.jpeg", width=Inches(5.5))

    add_field_value(doc, "Heading", "How TRION works")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "TRION\u00ae\u25bc (trionafenib) is a selective covalent KRAS G12C inhibitor that locks the "
        "KRAS oncoprotein in its inactive state, shutting down tumour-driving signalling.\u00b3 \u2075"
    )

    add_separator(doc)

    # KRAS context
    add_heading(doc, "Section 2 \u2014 KRAS biology (centred text) | light background", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "introduction")
    p = doc.add_paragraph()
    run = p.add_run("Section metadata: ")
    run.bold = True
    p.add_run("Style: light").font.color.rgb = GREY_TEXT

    add_field_value(doc, "Heading", "KRAS: a master switch in cancer signalling")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "KRAS is a GTPase that acts as a molecular switch, cycling between an active GTP-bound state "
        "and an inactive GDP-bound state. In normal cells, KRAS activation is tightly regulated by "
        "guanine nucleotide exchange factors (GEFs) and GTPase-activating proteins (GAPs). The G12C "
        "mutation impairs GAP-mediated GTP hydrolysis, trapping KRAS in its active state and driving "
        "constitutive activation of the RAS\u2013MAPK, PI3K\u2013AKT, and RAL\u2013GDS signalling pathways \u2014 "
        "promoting tumour cell proliferation, survival, and immune evasion.\u2074 \u2075"
    )

    add_separator(doc)

    # MoA detail columns
    add_heading(doc, "Section 3 \u2014 Mechanism detail (two-column: image left, text right) | highlight background", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "columns-teaser")
    p = doc.add_paragraph()
    run = p.add_run("Section metadata: ")
    run.bold = True
    p.add_run("Style: highlight").font.color.rgb = GREY_TEXT

    doc.add_paragraph()
    add_image_with_caption(doc, "columns-moa-preview.jpeg", width=Inches(3.5))

    add_field_value(doc, "Heading", "Covalent trapping of KRAS G12C in the inactive state")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Trionafenib exploits the mutant cysteine at position 12 \u2014 a neoantigen unique to KRAS G12C "
        "that is absent from wild-type KRAS. When KRAS G12C cycles transiently to its GDP-bound "
        "(inactive) state, trionafenib enters the Switch II pocket and forms an irreversible covalent "
        "bond with Cys12. This locks KRAS in the inactive conformation, preventing GEF-mediated "
        "GDP-to-GTP exchange and permanently silencing RAS signalling in that molecule.\u00b3 \u2075"
    )
    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run("Body text (continued): ")
    run.bold = True
    p.add_run(
        "Trionafenib\u2019s enhanced Switch II pocket binding achieves deeper target occupancy than "
        "first-generation KRAS G12C inhibitors, overcoming adaptive resistance mechanisms including "
        "RTK-mediated feedback reactivation and SHP2-dependent RAS cycling. The result is more complete "
        "and sustained suppression of the RAS\u2013MAPK pathway, which correlates with the improved "
        "response rates and survival outcomes observed in the TRIFORCE programme.\u00b3 \u2075"
    )
    add_field_value(doc, "Call to action", "View the TRIFORCE clinical data \u2192 /trion/triforce-data")

    add_separator(doc)

    # Immune effects
    add_heading(doc, "Section 4 \u2014 Immune modulation (centred text)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "introduction")

    add_field_value(doc, "Heading", "Beyond direct anti-tumour activity: immune reactivation")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "KRAS G12C inhibition has been shown to modulate the tumour immune microenvironment, restoring "
        "MHC class I expression on tumour cells and enhancing T-cell-mediated anti-tumour immunity. "
        "Preclinical models demonstrate that trionafenib increases tumour-infiltrating CD8+ T-cells "
        "and synergises with anti-PD-1 checkpoint inhibition. These findings provide the scientific "
        "rationale for ongoing combination studies evaluating TRION with immunotherapy.\u2074 \u2075"
    )

    add_separator(doc)

    # Accordion + metadata
    add_heading(doc, "Section 5 \u2014 Prescribing information footer", level=3, color=BRAND_COLOUR)
    add_body(doc, "Block: accordion  |  Expandable: PI | AE Reporting | References", italic=True)

    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run("Page metadata")
    run.bold = True
    run.font.color.rgb = AZ_MAGENTA
    add_body(doc, "Title: How TRION Works | KRAS G12C Covalent Inhibition | Mechanism of Action | AstraZeneca UK")
    add_body(doc, "Description: Understand how TRION (trionafenib) selectively inhibits KRAS G12C through covalent binding, shutting down RAS\u2013MAPK signalling and modulating anti-tumour immunity in NSCLC.")

    # =====================================================================
    # PAGE 6: RESOURCES
    # =====================================================================
    doc.add_page_break()
    add_heading(doc, "PAGE 6: Resources", level=2, color=AZ_MAGENTA)
    add_field_value(doc, "URL path", "/trion/resources")
    add_separator(doc)

    # Title block
    add_heading(doc, "Section 1 \u2014 Page header (text only, no image)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "title")
    add_field_value(doc, "Heading", "Resources for healthcare professionals")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Access prescribing guides, KRAS testing information, clinical data summaries, and patient "
        "support materials for TRION\u00ae\u25bc (trionafenib). All materials are provided for UK healthcare "
        "professionals only.\u00b3"
    )

    add_separator(doc)

    # Resource cards
    add_heading(doc, "Section 2 \u2014 Resource cards (three equal columns)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "cards-teaser")

    # Card 1 — Prescribing guide
    doc.add_paragraph()
    add_image_with_caption(doc, "card-prescribing.jpeg", width=Inches(3))
    add_field_value(doc, "Card heading", "Prescribing and dose modification guide")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "A comprehensive clinical guide covering indication, KRAS G12C testing requirements, dosing, "
        "dose modification criteria for hepatotoxicity, diarrhoea, and QTc prolongation, monitoring "
        "schedules, and drug interactions. Designed for rapid reference in oncology clinics.\u00b3"
    )
    add_field_value(doc, "Card link", "Download prescribing guide \u2192 [PDF link]")

    add_separator(doc)

    # Card 2 — KRAS testing
    add_field_value(doc, "Card heading", "KRAS G12C testing pathway")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "Information on KRAS G12C testing methodologies, including tissue-based NGS panels and "
        "ctDNA liquid biopsy options. Guidance on testing workflows, turnaround times, and "
        "recommended UK Genomic Medicine Service laboratories.\u00b3"
    )
    add_field_value(doc, "Card link", "Download testing guide \u2192 [PDF link]")

    add_separator(doc)

    # Card 3 — Clinical data summary
    add_field_value(doc, "Card heading", "TRIFORCE clinical data summary")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "Summary of key efficacy and safety data from TRIFORCE-1 and TRIFORCE-LUNG, including "
        "headline statistics, Kaplan-Meier curves, subgroup forest plots, and waterfall plots. "
        "A comprehensive overview of the clinical evidence supporting TRION.\u00b9 \u00b2"
    )
    add_field_value(doc, "Card link", "Download data summary \u2192 [PDF link]")

    add_separator(doc)

    # Contact section
    add_heading(doc, "Section 3 \u2014 Contact (centred text) | light background", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "introduction")
    p = doc.add_paragraph()
    run = p.add_run("Section metadata: ")
    run.bold = True
    p.add_run("Style: light").font.color.rgb = GREY_TEXT

    add_field_value(doc, "Heading", "Medical information and support")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "For medical information enquiries about TRION, please contact AstraZeneca Medical Information: "
        "Telephone: 0800 783 0033 | Email: medicalinformationuk@astrazeneca.com | "
        "Online: contactazmedical.astrazeneca.com"
    )

    add_separator(doc)

    # Accordion + metadata
    add_heading(doc, "Section 4 \u2014 Prescribing information footer", level=3, color=BRAND_COLOUR)
    add_body(doc, "Block: accordion  |  Expandable: PI | AE Reporting | References", italic=True)

    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run("Page metadata")
    run.bold = True
    run.font.color.rgb = AZ_MAGENTA
    add_body(doc, "Title: Resources | TRION (trionafenib) | KRAS Testing & Prescribing Guides | AstraZeneca UK")
    add_body(doc, "Description: Access prescribing guides, KRAS G12C testing pathways, TRIFORCE clinical data summaries, and support materials for TRION (trionafenib). For UK healthcare professionals only.")

    # =====================================================================
    # 10. FOOTER CONTENT
    # =====================================================================
    doc.add_page_break()
    add_heading(doc, "10. Footer Content", level=1, color=AZ_MAGENTA)

    add_body(doc, "The footer must appear on every page and contain the following elements:", bold=True)

    footer_items = [
        ("Logo", "AstraZeneca logo (linked to /trion/)"),
        ("Approval code", "GB-11583 | DOP: March 2026"),
        ("Copyright", "\u00a9 2026 AstraZeneca. All rights reserved. TRION is a registered trademark of the AstraZeneca group of companies."),
        ("Page links", "TRIFORCE Data | Safety | Dosing & Administration | How TRION Works | Resources"),
        ("Regulatory links", "Report Adverse Event (https://yellowcard.mhra.gov.uk/) | Medical Information (https://contactazmedical.astrazeneca.com/) | Privacy Policy (https://www.astrazeneca.co.uk/our-company/privacy-notice.html) | Terms of Use (https://www.astrazeneca.co.uk/our-company/terms-of-use.html) | Accessibility (https://www.astrazeneca.co.uk/accessibility.html)"),
        ("Date of preparation", "Date of Preparation: March 2026"),
    ]
    for label, val in footer_items:
        add_field_value(doc, label, val)

    add_separator(doc)

    # =====================================================================
    # 11. IMAGE ASSETS
    # =====================================================================
    add_heading(doc, "11. Image Assets", level=1, color=AZ_MAGENTA)

    add_body(doc, (
        f"All images are sourced from the shared CDN: {CDN_BASE}/"
    ))
    add_body(doc, (
        "Note: TRION reuses images originally generated for the VELOX website. "
        "The dramatic, abstract visual style is well-suited to oncology contexts."
    ), italic=True)

    doc.add_paragraph()
    add_body(doc, "Complete image manifest:", bold=True)
    doc.add_paragraph()

    img_table_rows = []
    for filename, usage in IMAGE_MANIFEST.items():
        cdn_url = f"{CDN_BASE}/{filename}"
        img_table_rows.append((filename, usage, cdn_url))

    add_table(doc,
        ["Filename", "Usage", "CDN URL"],
        img_table_rows)

    doc.add_paragraph()

    # Embed all images with previews
    add_heading(doc, "Image previews", level=2, color=AZ_MAGENTA)
    add_body(doc, "Visual previews of all 15 images:", italic=True)

    for filename in IMAGE_MANIFEST:
        doc.add_paragraph()
        add_body(doc, f"{filename} \u2014 {IMAGE_MANIFEST[filename]}", bold=True, size=Pt(9))
        add_image_with_caption(doc, filename, width=Inches(4))

    # --- Save ---
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    doc.save(OUTPUT_PATH)
    print(f"\n\u2705 Briefing saved to: {OUTPUT_PATH}")
    return OUTPUT_PATH


if __name__ == "__main__":
    build_document()
