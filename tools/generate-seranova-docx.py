#!/usr/bin/env python3
"""Generate DOCX briefing for Seranova (valinectra) — Non-steroidal selective MRA for CKD in T2D.

Reuses images from existing AZ site CDNs (no new image generation required).
"""

import os
import sys
import tempfile
import urllib.request
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml

# --- Configuration ---
SITE_NAME = "seranova"
BRAND_COLOUR = RGBColor(0x00, 0x72, 0xB2)  # Cerulean Blue (renal/cardio)
ACCENT_COLOUR = RGBColor(0xD4, 0x85, 0x1F)  # Warm Amber
AZ_MAGENTA = RGBColor(0x83, 0x00, 0x51)
DARK_TEXT = RGBColor(0x36, 0x3B, 0x3B)
GREY_TEXT = RGBColor(0x66, 0x66, 0x66)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
RED_NOTICE = RGBColor(0xCC, 0x00, 0x00)

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(PROJECT_DIR, "sites", SITE_NAME, "Seranova-Website-Briefing.docx")

# --- Image CDN Mapping (reusing existing site images) ---
# Each tuple: (display_name, cdn_url, usage_context)
IMAGE_MAP = {
    # Hero images (16:9, 1440x810)
    "hero-home": ("https://novapril-images.pages.dev/hero-home.jpeg", "Home — hero"),
    "hero-efficacy": ("https://zenturis-images.pages.dev/hero-efficacy.jpeg", "RENOVA Data — hero"),
    "hero-dosing": ("https://eluvion-images.pages.dev/hero-dosing.jpeg", "Dosing — hero"),
    "hero-moa": ("https://eluvion-images.pages.dev/hero-moa.jpeg", "How SERANOVA Works — hero"),
    # Card images (4:3, 800x600)
    "card-renal": ("https://eluvion-images.pages.dev/trial1-results.jpeg", "Home — renal outcomes card"),
    "card-cv": ("https://revantha-images.pages.dev/card-efficacy.jpeg", "Home — CV outcomes card"),
    "card-oral": ("https://zenturis-images.pages.dev/card-dosing.jpeg", "Home — oral dosing card"),
    "card-hyperkalaemia": ("https://eluvion-images.pages.dev/safety-hypertension.jpeg", "Safety — hyperkalaemia card"),
    "card-renal-function": ("https://eluvion-images.pages.dev/safety-proteinuria.jpeg", "Safety — renal function card"),
    "card-cv-safety": ("https://vitessa-images.pages.dev/safety-zoster.jpeg", "Safety — CV safety card"),
    "card-prescribing": ("https://revantha-images.pages.dev/resource-prescribing.jpeg", "Resources — prescribing card"),
    "card-clinical-summary": ("https://revantha-images.pages.dev/resource-education.jpeg", "Resources — clinical data card"),
    "card-patient": ("https://novapril-images.pages.dev/resource-patient.jpeg", "Resources — patient materials card"),
    # Column images (4:3, 800x600)
    "columns-moa-preview": ("https://eluvion-images.pages.dev/drug-mechanism.jpeg", "Home — MoA teaser"),
    "columns-kidney-pathway": ("https://eluvion-images.pages.dev/pathway-disease.jpeg", "MoA — kidney pathway"),
    "columns-mr-blockade": ("https://eluvion-images.pages.dev/pathway-cascade.jpeg", "MoA — MR blockade"),
    "columns-dosing": ("https://zenturis-images.pages.dev/columns-dose-adjust.jpeg", "Dosing — titration"),
    "columns-admin": ("https://zenturis-images.pages.dev/columns-admin.jpeg", "Dosing — administration"),
    "columns-monitoring": ("https://lumivex-images.pages.dev/columns-monitoring.jpeg", "Dosing — monitoring"),
    "columns-special-pops": ("https://revantha-images.pages.dev/patient-support.jpeg", "Safety — special populations"),
    "columns-contact": ("https://revantha-images.pages.dev/contact-support.jpeg", "Resources — contact"),
    # Tab images (4:3, 800x600)
    "tab-renova-ckd": ("https://zenturis-images.pages.dev/tab-zenith1.jpeg", "RENOVA Data — CKD tab"),
    "tab-renova-hf": ("https://zenturis-images.pages.dev/tab-zenith2.jpeg", "RENOVA Data — HF tab"),
    # Shared assets
    "astrazeneca-logo": ("https://novapril-images.pages.dev/astrazeneca-logo.svg", "Header/footer logo"),
    "search": ("https://revantha-images.pages.dev/search.svg", "Header search icon"),
}

# --- Image cache ---
_img_cache = {}
_tmp_dir = None


def get_tmp_dir():
    global _tmp_dir
    if _tmp_dir is None:
        _tmp_dir = tempfile.mkdtemp(prefix="seranova-briefing-")
    return _tmp_dir


def download_image(key):
    """Download image from CDN and cache locally. Returns local path or None."""
    if key in _img_cache:
        return _img_cache[key]

    if key not in IMAGE_MAP:
        _img_cache[key] = None
        return None

    url = IMAGE_MAP[key][0]
    ext = os.path.splitext(url)[1] or ".jpeg"
    local_path = os.path.join(get_tmp_dir(), f"{key}{ext}")

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "AZ-Briefing-Generator/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
            if len(data) > 1000:  # Valid image
                with open(local_path, "wb") as f:
                    f.write(data)
                _img_cache[key] = local_path
                print(f"  [OK] {key}: {url}")
                return local_path
    except Exception as e:
        print(f"  [SKIP] {key}: {e}")

    _img_cache[key] = None
    return None


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


def add_image_with_caption(doc, key, width=Inches(4.5)):
    """Add image with CDN URL caption. Downloads from existing CDN."""
    img_path = download_image(key)
    url = IMAGE_MAP.get(key, (None, None))[0]
    usage = IMAGE_MAP.get(key, (None, ""))[1]

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    if img_path and os.path.isfile(img_path) and os.path.getsize(img_path) > 1000:
        run = p.add_run()
        try:
            run.add_picture(img_path, width=width)
        except Exception:
            run = p.add_run(f"[Image: {key} — download OK but embed failed]")
            run.font.color.rgb = GREY_TEXT
            run.font.size = Pt(9)
            run.italic = True
    else:
        run = p.add_run(f"[Image: {key} — reused from existing CDN]")
        run.font.color.rgb = GREY_TEXT
        run.font.size = Pt(9)
        run.italic = True

    # CDN URL caption
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if url:
        r = cap.add_run(url)
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
    """Add a label: value paragraph."""
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
    run = title.add_run("SERANOVA\u2122")
    run.font.size = Pt(36)
    run.font.color.rgb = AZ_MAGENTA
    run.bold = True

    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = sub.add_run("(valinectra)")
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
    run = tagline.add_run("Protecting what matters.")
    run.font.size = Pt(14)
    run.font.color.rgb = BRAND_COLOUR
    run.italic = True

    doc.add_paragraph()

    for line in [
        "Document type: Final approved marketing brief for HCP website build",
        "Prepared by: Marketing \u2014 UK Cardiorenal Franchise",
        "Approval status: MLR-approved copy \u2014 do not modify",
        "Date: March 2026",
        "Approval code: GB-96017 | DOP: March 2026",
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
        "3. Clinical Programme: RENOVA",
        "4. Safety Profile",
        "5. Prescribing Information",
        "6. Adverse Event Reporting",
        "7. References",
        "8. Site Navigation",
        "9. Page Content",
        "   Page 1: Home",
        "   Page 2: RENOVA Data",
        "   Page 3: Safety",
        "   Page 4: Dosing & Monitoring",
        "   Page 5: How SERANOVA Works",
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
        ("Brand name", "SERANOVA"),
        ("Generic name", "valinectra"),
        ("Drug class", "Non-steroidal selective mineralocorticoid receptor antagonist (ns-MRA)"),
        ("Indication", "Reduction of sustained eGFR decline, end-stage kidney disease, cardiovascular death, and hospitalisation for heart failure in adults with chronic kidney disease associated with type 2 diabetes mellitus"),
        ("Extended indication", "Reduction of cardiovascular death and hospitalisation for heart failure in adults with chronic kidney disease (eGFR 25\u201375 mL/min/1.73m\u00b2 and UACR \u226530 mg/g) associated with type 2 diabetes mellitus"),
        ("Formulation", "10 mg and 20 mg film-coated tablets"),
        ("Dosing", "10 mg once daily, uptitrated to 20 mg once daily after 4 weeks based on serum potassium"),
        ("Approval", "MHRA \u2014 February 2026"),
        ("Brand colour", "Cerulean Blue #0072B2"),
        ("Accent colour", "Warm Amber #D4851F"),
        ("Approval code", "GB-96017"),
    ]
    add_table(doc, ["Field", "Detail"], profile_data)

    doc.add_paragraph()

    # Brand rules
    brand_notice = doc.add_paragraph()
    run = brand_notice.add_run(
        "SERANOVA brand rule: SERANOVA always appears in capitals, with \u2122 on first mention per page. "
        "Generic name (valinectra) appears in lowercase parentheses on first mention. "
        'The approved tagline "Protecting what matters." may only be used verbatim \u2014 no variations permitted.'
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
        "Valinectra is a non-steroidal selective antagonist of the mineralocorticoid receptor (MR). "
        "Unlike steroidal MRAs such as spironolactone and eplerenone, valinectra binds to the MR ligand-binding "
        "domain with a distinct non-steroidal pharmacophore, conferring high selectivity for the MR over "
        "glucocorticoid, androgen, and progesterone receptors, thereby minimising off-target endocrine effects."
    ))
    add_body(doc, (
        "In chronic kidney disease associated with type 2 diabetes, persistent hyperglycaemia and haemodynamic "
        "stress drive excessive activation of the mineralocorticoid receptor in renal tubular epithelial cells, "
        "podocytes, mesangial cells, and cardiac fibroblasts. MR overactivation promotes:"
    ))

    mr_effects = [
        "Renal fibrosis through pro-inflammatory and pro-fibrotic gene transcription (NF-\u03baB, TGF-\u03b2, PAI-1)",
        "Podocyte injury and proteinuria via direct podocyte MR signalling",
        "Endothelial dysfunction and vascular inflammation",
        "Cardiac fibrosis and left ventricular remodelling",
        "Sodium retention and potassium excretion, contributing to volume overload and hypokalaemia correction",
    ]
    for effect in mr_effects:
        p = doc.add_paragraph(style='List Bullet')
        run = p.add_run(effect)
        run.font.size = Pt(10)

    add_body(doc, (
        "By selectively blocking MR activation, valinectra reduces inflammation-driven kidney injury, "
        "attenuates proteinuria, slows the decline in glomerular filtration rate, and provides cardiorenal "
        "protection \u2014 complementing the mechanisms of RAAS inhibitors, SGLT2 inhibitors, and GLP-1 receptor "
        "agonists in the comprehensive management of diabetic kidney disease."
    ))

    add_separator(doc)

    # =================================================================
    # 3. CLINICAL PROGRAMME
    # =================================================================
    add_heading(doc, "3. Clinical Programme: RENOVA", level=1, color=AZ_MAGENTA)

    # RENOVA-CKD
    add_heading(doc, "RENOVA-CKD (Phase III, pivotal \u2014 Kidney outcomes in CKD + T2D)", level=2, color=AZ_MAGENTA)
    for label, val in [
        ("Design", "Randomised, double-blind, placebo-controlled, event-driven Phase III trial"),
        ("Population", "7,352 adults with CKD (eGFR 25\u201375 mL/min/1.73m\u00b2, UACR 30\u20135,000 mg/g) "
         "associated with type 2 diabetes, receiving maximum tolerated RAAS inhibition"),
        ("Median follow-up", "3.4 years"),
        ("Primary endpoint", "Composite of sustained \u226557% eGFR decline from baseline, end-stage kidney disease "
         "(ESKD), renal death, or cardiovascular death"),
        ("Key secondary endpoints", "Composite of CV death or hospitalisation for heart failure (HHF); "
         "sustained \u226540% eGFR decline; total eGFR slope; change in UACR at Month 4"),
        ("Publication", "Nakamura et al. N Engl J Med 2025; 393(8): 712\u2013726"),
    ]:
        add_field_value(doc, label, val)

    doc.add_paragraph()
    add_body(doc, "Key results:", bold=True)
    add_table(doc,
        ["Endpoint", "SERANOVA (n=3,676)", "Placebo (n=3,676)", "Treatment effect"],
        [
            ("Primary composite (kidney + CV death)",
             "504 events (13.7%)", "648 events (17.6%)",
             "HR 0.77 (0.67\u20130.88); P<0.001"),
            ("Sustained \u226557% eGFR decline or ESKD",
             "360 events (9.8%)", "474 events (12.9%)",
             "HR 0.75 (0.64\u20130.87); P<0.001"),
            ("CV death or HHF",
             "367 events (10.0%)", "446 events (12.1%)",
             "HR 0.82 (0.71\u20130.94); P=0.005"),
            ("Total eGFR slope (mL/min/1.73m\u00b2/year)",
             "\u22122.1", "\u22123.8",
             "Difference: +1.7 (1.3 to 2.1); P<0.001"),
            ("UACR change at Month 4",
             "\u221236%", "\u22122%",
             "Ratio 0.65 (0.61\u20130.70); P<0.001"),
            ("All-cause mortality",
             "284 (7.7%)", "335 (9.1%)",
             "HR 0.84 (0.72\u20130.99); P=0.034"),
        ])

    doc.add_paragraph()

    # RENOVA-HF
    add_heading(doc, "RENOVA-HF (Phase III \u2014 Heart failure outcomes in CKD + T2D)", level=2, color=AZ_MAGENTA)
    for label, val in [
        ("Design", "Randomised, double-blind, placebo-controlled, event-driven Phase III trial"),
        ("Population", "3,814 adults with heart failure (NYHA II\u2013IV, LVEF \u226440%), CKD (eGFR 25\u201360 mL/min/1.73m\u00b2), "
         "and type 2 diabetes, receiving guideline-directed medical therapy"),
        ("Median follow-up", "2.8 years"),
        ("Primary endpoint", "Composite of cardiovascular death or hospitalisation for heart failure"),
        ("Publication", "Tanaka et al. Lancet 2026; 407(10332): 245\u2013259"),
    ]:
        add_field_value(doc, label, val)

    doc.add_paragraph()
    add_body(doc, "Key results:", bold=True)
    add_table(doc,
        ["Endpoint", "SERANOVA (n=1,907)", "Placebo (n=1,907)", "Treatment effect"],
        [
            ("Primary composite (CV death + HHF)",
             "374 events (19.6%)", "453 events (23.8%)",
             "HR 0.82 (0.72\u20130.93); P=0.002"),
            ("CV death",
             "186 (9.8%)", "224 (11.7%)",
             "HR 0.83 (0.68\u20131.01); P=0.058"),
            ("Hospitalisation for heart failure",
             "268 events", "331 events",
             "HR 0.80 (0.68\u20130.94); P=0.007"),
            ("Kansas City Cardiomyopathy Questionnaire (KCCQ-TSS) change at Month 12",
             "+4.8 points", "+1.9 points",
             "Difference: +2.9 (1.6 to 4.2); P<0.001"),
            ("eGFR slope (mL/min/1.73m\u00b2/year)",
             "\u22121.8", "\u22123.2",
             "Difference: +1.4 (0.9 to 1.9); P<0.001"),
        ])

    add_separator(doc)

    # =================================================================
    # 4. SAFETY PROFILE
    # =================================================================
    add_heading(doc, "4. Safety Profile (Pooled RENOVA data, N=5,583 SERANOVA)", level=1, color=AZ_MAGENTA)

    add_heading(doc, "Most common adverse events (\u22652%)", level=2, color=AZ_MAGENTA)
    add_table(doc,
        ["Adverse event", "SERANOVA (%)", "Placebo (%)"],
        [
            ("Hyperkalaemia (any grade)", "8.6", "3.2"),
            ("Hypotension", "4.2", "2.8"),
            ("Hypokalaemia", "0.4", "2.1"),
            ("Dizziness", "3.1", "2.4"),
            ("Diarrhoea", "2.8", "2.3"),
            ("Nasopharyngitis", "2.6", "2.7"),
            ("Back pain", "2.3", "2.0"),
            ("Urinary tract infection", "2.1", "1.9"),
            ("Acute kidney injury", "1.8", "1.4"),
        ])

    doc.add_paragraph()

    add_heading(doc, "Hyperkalaemia \u2014 the principal safety consideration", level=2, color=AZ_MAGENTA)
    add_body(doc, (
        "Hyperkalaemia is an expected pharmacological effect of mineralocorticoid receptor antagonism and "
        "was the most frequently reported adverse event with SERANOVA. Proactive serum potassium monitoring "
        "and protocol-defined dose adjustment guidance minimised clinical impact:\u00b3"
    ))

    hyperk_data = [
        "Serum potassium >5.5 mmol/L: 14.2% SERANOVA vs 6.3% placebo",
        "Serum potassium >6.0 mmol/L: 1.4% vs 0.3%",
        "Hyperkalaemia leading to hospitalisation: 1.1% vs 0.4%",
        "Hyperkalaemia leading to permanent discontinuation: 1.7% vs 0.4%",
        "No fatal hyperkalaemic events in either treatment group",
        "Median time to first hyperkalaemia event: 8 months",
        "Events were manageable with dose reduction (20 mg \u2192 10 mg) and standard potassium-lowering measures",
    ]
    for item in hyperk_data:
        p = doc.add_paragraph(style='List Bullet')
        run = p.add_run(item)
        run.font.size = Pt(10)

    doc.add_paragraph()

    add_heading(doc, "Key safety findings", level=2, color=AZ_MAGENTA)
    safety_findings = [
        ("Serious adverse events", "21.4% SERANOVA vs 23.8% placebo"),
        ("Treatment discontinuation due to AEs", "6.2% vs 5.1% (driven primarily by hyperkalaemia)"),
        ("All-cause mortality", "7.7% vs 9.1% (HR 0.84; numerical reduction favouring SERANOVA)"),
        ("Acute kidney injury", "1.8% vs 1.4% (no imbalance in serious AKI events requiring dialysis)"),
        ("Gynaecomastia", "0.1% vs 0.1% (no signal for anti-androgenic effects, consistent with non-steroidal mechanism)\u00b3"),
        ("Hepatic events", "ALT >3\u00d7 ULN: 0.5% vs 0.4% (no cases meeting Hy\u2019s Law criteria)\u00b3"),
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
        "Renal impairment: No dose adjustment for eGFR 25\u201375 mL/min/1.73m\u00b2 (studied population). SERANOVA has not been studied in patients with eGFR <25 mL/min/1.73m\u00b2 or on dialysis. Do not initiate if eGFR <25 mL/min/1.73m\u00b2.\u2074",
        "Hepatic impairment: No dose adjustment for mild hepatic impairment (Child-Pugh A). Use with caution in moderate hepatic impairment (Child-Pugh B). Contraindicated in severe hepatic impairment (Child-Pugh C).\u2074",
        "Elderly (\u226565 years): No dose adjustment required. 42% of RENOVA-CKD patients were \u226565 years; efficacy and safety were consistent with the overall population.\u2074",
        "Pregnancy and lactation: Contraindicated in pregnancy. Women of childbearing potential must use effective contraception during treatment and for 1 week after the last dose. It is not known whether valinectra is excreted in human milk; a decision must be made whether to discontinue breastfeeding or discontinue therapy.\u2074",
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
        "SERANOVA (valinectra) 10 mg and 20 mg film-coated tablets. Please refer to the Summary of Product "
        "Characteristics (SmPC) before prescribing. Indication: Reduction of sustained eGFR decline, end-stage "
        "kidney disease, cardiovascular death, and hospitalisation for heart failure in adults with chronic kidney "
        "disease associated with type 2 diabetes mellitus. Dosage and administration: Initiate at 10 mg once daily. "
        "Measure serum potassium before initiation and within 4 weeks. If serum potassium \u22644.8 mmol/L, uptitrate "
        "to 20 mg once daily. If serum potassium >4.8 to 5.0 mmol/L, maintain 10 mg. If serum potassium >5.0 mmol/L, "
        "withhold and recheck. Contraindications: Hypersensitivity to valinectra or any excipient. Concomitant use "
        "with strong CYP3A4 inhibitors (e.g. itraconazole, ketoconazole, ritonavir, clarithromycin). Addison\u2019s "
        "disease. Severe hepatic impairment (Child-Pugh C). Warnings and precautions: Monitor serum potassium "
        "before initiation, at 4 weeks, and periodically thereafter. Interrupt treatment if potassium >5.5 mmol/L. "
        "Do not initiate if serum potassium >5.0 mmol/L or eGFR <25 mL/min/1.73m\u00b2. Use with caution in patients "
        "receiving potassium-sparing diuretics or potassium supplements. An initial eGFR decline may occur upon "
        "treatment initiation; this is typically reversible and not a reason to discontinue. Interactions: "
        "Contraindicated with strong CYP3A4 inhibitors. Avoid grapefruit juice. Moderate CYP3A4 inhibitors: "
        "no dose adjustment required but monitor potassium more frequently. Side effects: Very common (\u22651/10): "
        "none. Common (\u22651/100 to <1/10): hyperkalaemia, hypotension. Uncommon (\u22651/1000 to <1/100): "
        "dizziness, pruritus, hyponatraemia. Legal category: POM. Pack and price: 28 tablets (10 mg): \u00a3524.60; "
        "28 tablets (20 mg): \u00a3524.60. Marketing authorisation holder: AstraZeneca UK Ltd. MA number: "
        "PLGB 17901/0527. Full prescribing information available from: AstraZeneca UK Ltd, 2 Pancras Square, "
        "London N1C 4AG. GB-96017 | DOP: March 2026."
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
        "Nakamura et al. N Engl J Med 2025; 393(8): 712\u2013726.",
        "Tanaka et al. Lancet 2026; 407(10332): 245\u2013259.",
        "SERANOVA (valinectra) Summary of Product Characteristics. AstraZeneca UK Ltd. February 2026.",
        "Agarwal R, et al. Nat Rev Nephrol 2024; 20(6): 381\u2013398.",
        "Kidney Disease: Improving Global Outcomes (KDIGO) CKD Work Group. Kidney Int Suppl 2024; 14(4): S1\u2013S127.",
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
        ("Main navigation pages", "RENOVA Data | Safety | Dosing & Monitoring | How SERANOVA Works | Resources"),
        ("Utility", "Search | Login"),
    ]
    for label, val in nav_items:
        add_field_value(doc, label, val)

    doc.add_page_break()

    # =================================================================
    # 9. PAGE CONTENT
    # =================================================================
    add_heading(doc, "9. Page Content", level=1, color=AZ_MAGENTA)

    # Important notice
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
        'SERANOVA brand rule: SERANOVA always appears in capitals, with \u2122 on first mention per page. '
        'Generic name (valinectra) in lowercase parentheses on first mention. '
        'Tagline "Protecting what matters." verbatim only.'
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
    add_field_value(doc, "URL path", "/seranova/")
    add_separator(doc)

    # Section 1 — Hero
    add_heading(doc, "Section 1 \u2014 Hero (full-width image with text overlay)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "hero-teaser")
    doc.add_paragraph()
    add_image_with_caption(doc, "hero-home", width=Inches(5.5))

    add_field_value(doc, "Heading", "SERANOVA\u2122 (valinectra)")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Cardiorenal protection for adults with chronic kidney disease and type 2 diabetes. "
        "Protecting what matters.\u00b9"
    )
    add_field_value(doc, "Call to action", "Explore the RENOVA data \u2192 /seranova/renova-data")

    add_separator(doc)

    # Section 2 — Key benefit cards
    add_heading(doc, "Section 2 \u2014 Three key benefit cards (equal columns)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "cards-teaser")

    # Card 1 — Renal
    doc.add_paragraph()
    add_image_with_caption(doc, "card-renal", width=Inches(3))
    add_field_value(doc, "Card heading", "23% reduction in kidney disease progression")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "In RENOVA-CKD, SERANOVA reduced the risk of the composite kidney outcome (sustained \u226557% eGFR "
        "decline, ESKD, renal death, or CV death) by 23% compared with placebo in adults with CKD and "
        "type 2 diabetes receiving maximum tolerated RAAS inhibition (HR 0.77; P<0.001).\u00b9"
    )
    add_field_value(doc, "Card link", "View RENOVA data \u2192 /seranova/renova-data")

    add_separator(doc)

    # Card 2 — CV
    add_image_with_caption(doc, "card-cv", width=Inches(3))
    add_field_value(doc, "Card heading", "18% reduction in cardiovascular events")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "SERANOVA reduced the composite of cardiovascular death or hospitalisation for heart failure by "
        "18% in RENOVA-CKD (HR 0.82; P=0.005) and by 18% in RENOVA-HF in patients with coexisting heart "
        "failure (HR 0.82; P=0.002), demonstrating consistent cardiorenal benefit.\u00b9\u00b2"
    )
    add_field_value(doc, "Card link", "Explore cardiovascular outcomes \u2192 /seranova/renova-data")

    add_separator(doc)

    # Card 3 — Oral
    add_image_with_caption(doc, "card-oral", width=Inches(3))
    add_field_value(doc, "Card heading", "Once-daily oral tablet with simple titration")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "SERANOVA is initiated at 10 mg once daily and uptitrated to 20 mg after 4 weeks based on serum "
        "potassium. A simple oral regimen designed to complement existing guideline-directed therapy "
        "for diabetic kidney disease.\u00b3"
    )
    add_field_value(doc, "Card link", "View dosing guidance \u2192 /seranova/dosing")

    add_separator(doc)

    # Section 3 — Disease context
    add_heading(doc, "Section 3 \u2014 Disease context (centred text) | light background", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "introduction")
    p = doc.add_paragraph()
    run = p.add_run("Section metadata: ")
    run.bold = True
    run2 = p.add_run("Style: light")
    run2.font.color.rgb = GREY_TEXT

    add_field_value(doc, "Heading", "Diabetic kidney disease: a growing cardiorenal challenge")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Approximately 40% of adults with type 2 diabetes develop chronic kidney disease, and CKD in the "
        "context of diabetes is associated with a 2\u20133-fold increased risk of cardiovascular events and "
        "premature death.\u2074 Despite RAAS inhibition, SGLT2 inhibitors, and glycaemic optimisation, "
        "residual risk of kidney disease progression and cardiovascular events remains substantial. "
        "Mineralocorticoid receptor overactivation is an independent driver of this residual risk, "
        "representing a distinct and complementary therapeutic target.\u2075"
    )

    add_separator(doc)

    # Section 4 — Mechanism teaser
    add_heading(doc, "Section 4 \u2014 Mechanism teaser (two-column: image left, text right) | highlight background", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "columns-teaser")
    p = doc.add_paragraph()
    run = p.add_run("Section metadata: ")
    run.bold = True
    run2 = p.add_run("Style: highlight")
    run2.font.color.rgb = GREY_TEXT

    doc.add_paragraph()
    add_image_with_caption(doc, "columns-moa-preview", width=Inches(3.5))

    add_field_value(doc, "Heading", "Targeting the mineralocorticoid receptor")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Excessive MR activation in the kidney and heart drives inflammation, fibrosis, and organ damage "
        "in diabetic kidney disease. SERANOVA selectively blocks MR signalling with a non-steroidal "
        "mechanism, providing cardiorenal protection beyond RAAS inhibition alone.\u00b3"
    )
    add_field_value(doc, "Call to action", "Explore how SERANOVA works \u2192 /seranova/how-seranova-works")

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
    add_body(doc, "Title: SERANOVA (valinectra) | Cardiorenal Protection in CKD & T2D | AstraZeneca UK")
    add_body(doc, "Description: SERANOVA (valinectra) is a non-steroidal selective MRA for adults with chronic kidney disease associated with type 2 diabetes. Explore RENOVA clinical data, safety, and dosing for UK healthcare professionals.")

    # =====================================================================
    # PAGE 2: RENOVA DATA
    # =====================================================================
    doc.add_page_break()
    add_heading(doc, "PAGE 2: RENOVA Data", level=2, color=AZ_MAGENTA)
    add_field_value(doc, "URL path", "/seranova/renova-data")
    add_separator(doc)

    # Hero
    add_heading(doc, "Section 1 \u2014 Hero (full-width image with text overlay)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "hero-teaser")
    doc.add_paragraph()
    add_image_with_caption(doc, "hero-efficacy", width=Inches(5.5))

    add_field_value(doc, "Heading", "The RENOVA clinical programme")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "SERANOVA\u2122 (valinectra) demonstrated significant kidney and cardiovascular protection in over "
        "11,000 adults with chronic kidney disease and type 2 diabetes across two Phase III trials.\u00b9 \u00b2"
    )

    add_separator(doc)

    # Programme overview
    add_heading(doc, "Section 2 \u2014 Programme overview (centred text) | light background", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "introduction")
    p = doc.add_paragraph()
    run = p.add_run("Section metadata: ")
    run.bold = True
    p.add_run("Style: light").font.color.rgb = GREY_TEXT

    add_field_value(doc, "Heading", "Comprehensive cardiorenal evidence across two pivotal trials")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "The RENOVA programme evaluated valinectra in two distinct but complementary populations: "
        "RENOVA-CKD assessed kidney and cardiovascular outcomes in 7,352 adults with CKD and type 2 diabetes, "
        "establishing the primary indication. RENOVA-HF assessed cardiovascular outcomes in 3,814 adults with "
        "coexisting heart failure, CKD, and type 2 diabetes, extending the evidence to the highest-risk patients.\u00b9 \u00b2"
    )

    add_separator(doc)

    # Tabs
    add_heading(doc, "Section 3 \u2014 Clinical data (two tabs)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "tabs-large")

    # Tab 1 — RENOVA-CKD
    doc.add_paragraph()
    add_body(doc, 'Tab 1: "RENOVA-CKD: Kidney outcomes"', bold=True)
    add_image_with_caption(doc, "tab-renova-ckd", width=Inches(3.5))

    add_field_value(doc, "Heading", "RENOVA-CKD: 23% reduction in the composite kidney outcome")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "In RENOVA-CKD, a randomised, double-blind, placebo-controlled trial in 7,352 adults with CKD "
        "(eGFR 25\u201375 mL/min/1.73m\u00b2, UACR 30\u20135,000 mg/g) and type 2 diabetes on maximum tolerated RAAS "
        "inhibition, SERANOVA reduced the primary composite endpoint (sustained \u226557% eGFR decline, ESKD, "
        "renal death, or CV death) by 23% versus placebo (HR 0.77; 95% CI: 0.67\u20130.88; P<0.001).\u00b9"
    )
    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run("Body text (continued): ")
    run.bold = True
    p.add_run(
        "SERANOVA slowed the rate of kidney function decline, with a total eGFR slope of \u22122.1 vs \u22123.8 "
        "mL/min/1.73m\u00b2/year (difference: +1.7; P<0.001). Albuminuria was reduced by 36% from baseline "
        "at Month 4 (ratio 0.65; P<0.001). The cardiovascular co-primary endpoint (CV death or HHF) was also "
        "significantly reduced (HR 0.82; P=0.005).\u00b9"
    )

    add_body(doc, "Data table:", bold=True)
    add_table(doc,
        ["Endpoint", "SERANOVA (n=3,676)", "Placebo (n=3,676)", "Treatment effect"],
        [
            ("Primary composite (kidney + CV death)", "13.7%", "17.6%", "HR 0.77 (0.67\u20130.88); P<0.001"),
            ("Sustained \u226557% eGFR decline or ESKD", "9.8%", "12.9%", "HR 0.75 (0.64\u20130.87); P<0.001"),
            ("CV death or HHF", "10.0%", "12.1%", "HR 0.82 (0.71\u20130.94); P=0.005"),
            ("eGFR slope (mL/min/1.73m\u00b2/yr)", "\u22122.1", "\u22123.8", "+1.7 (1.3\u20132.1); P<0.001"),
            ("UACR change at Month 4", "\u221236%", "\u22122%", "Ratio 0.65 (0.61\u20130.70); P<0.001"),
        ])

    add_separator(doc)

    # Tab 2 — RENOVA-HF
    add_body(doc, 'Tab 2: "RENOVA-HF: Heart failure outcomes"', bold=True)
    add_image_with_caption(doc, "tab-renova-hf", width=Inches(3.5))

    add_field_value(doc, "Heading", "RENOVA-HF: 18% reduction in CV death or hospitalisation for heart failure")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "RENOVA-HF was a randomised, double-blind, placebo-controlled trial in 3,814 adults with heart failure "
        "(NYHA II\u2013IV, LVEF \u226440%), CKD (eGFR 25\u201360 mL/min/1.73m\u00b2), and type 2 diabetes receiving "
        "guideline-directed medical therapy including RAAS inhibition and SGLT2 inhibitors.\u00b2"
    )
    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run("Body text (continued): ")
    run.bold = True
    p.add_run(
        "SERANOVA reduced the primary composite of cardiovascular death or hospitalisation for heart failure "
        "by 18% (HR 0.82; 95% CI: 0.72\u20130.93; P=0.002). Hospitalisations for heart failure were reduced by "
        "20% (HR 0.80; P=0.007). Patients reported clinically meaningful improvements in heart failure symptoms "
        "(KCCQ-TSS difference: +2.9 points; P<0.001). SERANOVA also slowed kidney function decline "
        "(eGFR slope: \u22121.8 vs \u22123.2 mL/min/1.73m\u00b2/year; P<0.001).\u00b2"
    )

    add_body(doc, "Data table:", bold=True)
    add_table(doc,
        ["Endpoint", "SERANOVA (n=1,907)", "Placebo (n=1,907)", "Treatment effect"],
        [
            ("CV death or HHF (primary)", "19.6%", "23.8%", "HR 0.82 (0.72\u20130.93); P=0.002"),
            ("HHF alone", "268 events", "331 events", "HR 0.80 (0.68\u20130.94); P=0.007"),
            ("CV death", "9.8%", "11.7%", "HR 0.83 (0.68\u20131.01); P=0.058"),
            ("KCCQ-TSS change at Month 12", "+4.8", "+1.9", "+2.9 (1.6\u20134.2); P<0.001"),
            ("eGFR slope (mL/min/1.73m\u00b2/yr)", "\u22121.8", "\u22123.2", "+1.4 (0.9\u20131.9); P<0.001"),
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
    add_body(doc, "Title: RENOVA Data | SERANOVA (valinectra) | Kidney & CV Outcomes | AstraZeneca UK")
    add_body(doc, "Description: Explore the RENOVA clinical programme for SERANOVA (valinectra) \u2014 Phase III kidney outcomes, cardiovascular protection, and heart failure data in adults with CKD and type 2 diabetes.")

    # =====================================================================
    # PAGE 3: SAFETY
    # =====================================================================
    doc.add_page_break()
    add_heading(doc, "PAGE 3: Safety", level=2, color=AZ_MAGENTA)
    add_field_value(doc, "URL path", "/seranova/safety")
    add_separator(doc)

    # Title block
    add_heading(doc, "Section 1 \u2014 Page header (text only, no image)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "title")
    add_field_value(doc, "Heading", "Safety profile of SERANOVA")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "SERANOVA\u2122 (valinectra) has been evaluated in over 5,500 patients across the RENOVA clinical "
        "programme, with a median follow-up of 3.4 years in RENOVA-CKD and 2.8 years in RENOVA-HF.\u00b9 \u00b2 \u00b3"
    )

    add_separator(doc)

    # Hyperkalaemia warning
    add_heading(doc, "Section 2 \u2014 Hyperkalaemia monitoring (centred text) | highlight background", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "introduction")
    p = doc.add_paragraph()
    run = p.add_run("Section metadata: ")
    run.bold = True
    p.add_run("Style: highlight").font.color.rgb = GREY_TEXT

    add_field_value(doc, "Heading", "Hyperkalaemia \u2014 monitoring and management")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Hyperkalaemia is an expected pharmacological effect of mineralocorticoid receptor antagonism and "
        "is the principal safety consideration with SERANOVA. Measure serum potassium before initiation, "
        "within 4 weeks of starting or changing dose, and periodically thereafter. Use the potassium-guided "
        "dose titration algorithm to manage serum potassium levels. Withhold treatment if potassium exceeds "
        "5.5 mmol/L and resume at the lower dose once potassium is \u22645.0 mmol/L.\u00b3"
    )

    add_separator(doc)

    # Safety overview
    add_heading(doc, "Section 3 \u2014 Safety overview (centred text) | light background", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "introduction")
    p = doc.add_paragraph()
    run = p.add_run("Section metadata: ")
    run.bold = True
    p.add_run("Style: light").font.color.rgb = GREY_TEXT

    add_field_value(doc, "Heading", "A well-characterised safety profile with proactive potassium management")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Across the RENOVA programme, the safety profile of SERANOVA was consistent with selective "
        "non-steroidal MR antagonism. Serious adverse events were lower with SERANOVA than placebo "
        "(21.4% vs 23.8%), driven by fewer cardiovascular hospitalisations. Treatment discontinuation "
        "due to adverse events was 6.2% vs 5.1%, with hyperkalaemia being the most common reason for "
        "discontinuation (1.7%). No anti-androgenic effects (gynaecomastia, breast pain) were observed "
        "above placebo rates, consistent with the non-steroidal mechanism.\u00b9 \u00b2 \u00b3"
    )

    add_separator(doc)

    # AE table
    add_heading(doc, "Section 4 \u2014 Adverse events table | light background", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "table-data")
    p = doc.add_paragraph()
    run = p.add_run("Section metadata: ")
    run.bold = True
    p.add_run("Style: light").font.color.rgb = GREY_TEXT

    add_table(doc,
        ["Adverse event", "SERANOVA (%)", "Placebo (%)"],
        [
            ("Hyperkalaemia (any grade)", "8.6", "3.2"),
            ("Hypotension", "4.2", "2.8"),
            ("Dizziness", "3.1", "2.4"),
            ("Diarrhoea", "2.8", "2.3"),
            ("Nasopharyngitis", "2.6", "2.7"),
            ("Back pain", "2.3", "2.0"),
            ("Urinary tract infection", "2.1", "1.9"),
            ("Acute kidney injury", "1.8", "1.4"),
        ])

    add_separator(doc)

    # Safety consideration cards
    add_heading(doc, "Section 5 \u2014 Key safety consideration cards (equal columns)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "cards-teaser")

    # Card 1
    doc.add_paragraph()
    add_image_with_caption(doc, "card-hyperkalaemia", width=Inches(3))
    add_field_value(doc, "Card heading", "Hyperkalaemia management")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "Hyperkalaemia (serum K\u207a >5.5 mmol/L) occurred in 14.2% of SERANOVA-treated patients vs 6.3% "
        "with placebo. Events were manageable through potassium-guided dose titration: withhold if K\u207a "
        ">5.5 mmol/L, resume at 10 mg when K\u207a \u22645.0 mmol/L. Hyperkalaemia leading to permanent "
        "discontinuation occurred in only 1.7%.\u00b3"
    )

    add_separator(doc)

    # Card 2
    add_image_with_caption(doc, "card-renal-function", width=Inches(3))
    add_field_value(doc, "Card heading", "Renal function considerations")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "An initial eGFR decline of approximately 2\u20134 mL/min/1.73m\u00b2 may occur within the first "
        "4 weeks of SERANOVA treatment. This haemodynamic effect is typically reversible and is not a "
        "reason to discontinue treatment. Over longer follow-up, SERANOVA slowed the chronic eGFR decline "
        "by 1.7 mL/min/1.73m\u00b2/year compared with placebo.\u00b9 \u00b3"
    )

    add_separator(doc)

    # Card 3
    add_image_with_caption(doc, "card-cv-safety", width=Inches(3))
    add_field_value(doc, "Card heading", "Cardiovascular and metabolic safety")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "No increase in major adverse cardiovascular events was observed with SERANOVA. All-cause mortality "
        "was numerically lower with SERANOVA (7.7% vs 9.1%). Blood pressure reduction was modest (systolic "
        "\u22123 to \u22125 mmHg), and symptomatic hypotension was infrequent (4.2% vs 2.8%). "
        "No clinically significant effects on glycaemic control, lipid parameters, or body weight were observed.\u00b9 \u00b2 \u00b3"
    )

    add_separator(doc)

    # Special populations
    add_heading(doc, "Section 6 \u2014 Special populations (two-column: image left, text right) | highlight background", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "columns-teaser")
    p = doc.add_paragraph()
    run = p.add_run("Section metadata: ")
    run.bold = True
    p.add_run("Style: highlight").font.color.rgb = GREY_TEXT

    doc.add_paragraph()
    add_image_with_caption(doc, "columns-special-pops", width=Inches(3.5))

    add_field_value(doc, "Heading", "Special populations")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Pregnancy and fertility: SERANOVA is contraindicated in pregnancy. Women of childbearing potential "
        "must use effective contraception during treatment and for 1 week after the last dose.\u00b3\n\n"
        "Elderly patients: No dose adjustment required in patients aged \u226565 years. In RENOVA-CKD, 42% of "
        "patients were \u226565 years, with consistent efficacy and safety.\u00b3\n\n"
        "Hepatic impairment: No dose adjustment for mild impairment (Child-Pugh A). Use with caution in "
        "moderate impairment. Contraindicated in severe impairment (Child-Pugh C).\u00b3\n\n"
        "Renal impairment: Studied in eGFR 25\u201375 mL/min/1.73m\u00b2. Do not initiate if eGFR <25 mL/min/1.73m\u00b2. "
        "Not studied in patients on dialysis.\u00b3"
    )

    add_separator(doc)

    # Accordion + metadata
    add_heading(doc, "Section 7 \u2014 Prescribing information footer", level=3, color=BRAND_COLOUR)
    add_body(doc, "Block: accordion  |  Expandable: PI | AE Reporting | References", italic=True)

    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run("Page metadata")
    run.bold = True
    run.font.color.rgb = AZ_MAGENTA
    add_body(doc, "Title: Safety | SERANOVA (valinectra) | Hyperkalaemia & Monitoring | AstraZeneca UK")
    add_body(doc, "Description: Review the safety profile of SERANOVA (valinectra) including hyperkalaemia management, adverse event rates, and special population recommendations for adults with CKD and type 2 diabetes.")

    # =====================================================================
    # PAGE 4: DOSING & MONITORING
    # =====================================================================
    doc.add_page_break()
    add_heading(doc, "PAGE 4: Dosing & Monitoring", level=2, color=AZ_MAGENTA)
    add_field_value(doc, "URL path", "/seranova/dosing")
    add_separator(doc)

    # Hero
    add_heading(doc, "Section 1 \u2014 Hero (full-width image with text overlay)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "hero-teaser")
    doc.add_paragraph()
    add_image_with_caption(doc, "hero-dosing", width=Inches(5.5))

    add_field_value(doc, "Heading", "Dosing and monitoring")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "SERANOVA\u2122 (valinectra) uses a simple potassium-guided titration to optimise cardiorenal "
        "protection while managing the risk of hyperkalaemia.\u00b3"
    )

    add_separator(doc)

    # Titration guidance
    add_heading(doc, "Section 2 \u2014 Potassium-guided titration (two-column) | light background", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "columns-teaser")
    p = doc.add_paragraph()
    run = p.add_run("Section metadata: ")
    run.bold = True
    p.add_run("Style: light").font.color.rgb = GREY_TEXT

    doc.add_paragraph()
    add_image_with_caption(doc, "columns-dosing", width=Inches(3.5))

    add_field_value(doc, "Heading", "Potassium-guided dose titration")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Step 1 \u2014 Before initiation: Measure serum potassium. Do not initiate if K\u207a >5.0 mmol/L "
        "or eGFR <25 mL/min/1.73m\u00b2.\u00b3\n\n"
        "Step 2 \u2014 Initiate: Start SERANOVA 10 mg once daily.\u00b3\n\n"
        "Step 3 \u2014 Check at 4 weeks: Measure serum potassium.\u00b3\n\n"
        "Step 4 \u2014 Titrate based on potassium:\n"
        "  \u2022 K\u207a \u22644.8 mmol/L: Uptitrate to 20 mg once daily\n"
        "  \u2022 K\u207a >4.8 to 5.0 mmol/L: Maintain 10 mg once daily\n"
        "  \u2022 K\u207a >5.0 to 5.5 mmol/L: Maintain current dose; recheck in 4 weeks\n"
        "  \u2022 K\u207a >5.5 mmol/L: Withhold SERANOVA; recheck; resume 10 mg when K\u207a \u22645.0 mmol/L\u00b3"
    )

    add_separator(doc)

    # Administration
    add_heading(doc, "Section 3 \u2014 Administration guidance (two-column)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "columns-teaser")

    doc.add_paragraph()
    add_image_with_caption(doc, "columns-admin", width=Inches(3.5))

    add_field_value(doc, "Heading", "Administration and practical guidance")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "SERANOVA should be taken once daily, with or without food. Tablets should be swallowed whole "
        "with water.\u00b3\n\n"
        "If a dose is missed, take it as soon as remembered on the same day. Do not take two doses on "
        "the same day to make up for a missed dose.\u00b3\n\n"
        "SERANOVA may be prescribed alongside existing guideline-directed therapy including ACE inhibitors "
        "or ARBs, SGLT2 inhibitors, and GLP-1 receptor agonists. In the RENOVA programme, 97% of patients "
        "received concomitant RAAS inhibition, 59% received SGLT2 inhibitors, and 12% received GLP-1 RAs.\u00b9\n\n"
        "Do not use with strong CYP3A4 inhibitors (contraindicated) or with other potassium-sparing "
        "diuretics (use with caution).\u00b3"
    )

    add_separator(doc)

    # Monitoring
    add_heading(doc, "Section 4 \u2014 Ongoing monitoring (two-column) | highlight background", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "columns-teaser")
    p = doc.add_paragraph()
    run = p.add_run("Section metadata: ")
    run.bold = True
    p.add_run("Style: highlight").font.color.rgb = GREY_TEXT

    doc.add_paragraph()
    add_image_with_caption(doc, "columns-monitoring", width=Inches(3.5))

    add_field_value(doc, "Heading", "Monitoring recommendations")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Serum potassium: Measure before initiation, within 4 weeks of starting or dose change, "
        "and periodically thereafter. Additional monitoring is recommended during intercurrent illness, "
        "changes in concomitant medications affecting potassium, or changes in renal function.\u00b3\n\n"
        "Renal function: Measure eGFR at baseline and periodically. An initial eGFR decline of "
        "2\u20134 mL/min/1.73m\u00b2 may occur within the first 4 weeks; this is typically haemodynamic and "
        "reversible. Continue treatment unless eGFR declines below 25 mL/min/1.73m\u00b2 on two consecutive "
        "measurements.\u00b3\n\n"
        "Hepatic function: Monitor liver function tests periodically during treatment.\u00b3"
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
    add_body(doc, "Title: Dosing | SERANOVA (valinectra) | Potassium-Guided Titration | AstraZeneca UK")
    add_body(doc, "Description: Dosing and monitoring guidance for SERANOVA (valinectra) including potassium-guided titration, administration, concomitant therapy, and monitoring recommendations for CKD with type 2 diabetes.")

    # =====================================================================
    # PAGE 5: HOW SERANOVA WORKS
    # =====================================================================
    doc.add_page_break()
    add_heading(doc, "PAGE 5: How SERANOVA Works", level=2, color=AZ_MAGENTA)
    add_field_value(doc, "URL path", "/seranova/how-seranova-works")
    add_separator(doc)

    # Hero
    add_heading(doc, "Section 1 \u2014 Hero (full-width image with text overlay)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "hero-teaser")
    doc.add_paragraph()
    add_image_with_caption(doc, "hero-moa", width=Inches(5.5))

    add_field_value(doc, "Heading", "Targeting the mineralocorticoid receptor in diabetic kidney disease")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "SERANOVA\u2122 (valinectra) selectively blocks MR overactivation \u2014 an independent driver of kidney "
        "and cardiovascular damage in patients with CKD and type 2 diabetes, complementing RAAS inhibition "
        "and SGLT2 inhibitor therapy.\u00b3"
    )

    add_separator(doc)

    # Disease pathway
    add_heading(doc, "Section 2 \u2014 The MR pathway in diabetic kidney disease (two-column)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "columns-teaser")

    doc.add_paragraph()
    add_image_with_caption(doc, "columns-kidney-pathway", width=Inches(3.5))

    add_field_value(doc, "Heading", "Why the mineralocorticoid receptor matters in CKD")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "In diabetic kidney disease, chronic hyperglycaemia, haemodynamic stress, and obesity drive excessive "
        "aldosterone production and inappropriate MR activation in renal and cardiac tissues \u2014 independent "
        "of angiotensin II levels.\u2074 \u2075\n\n"
        "MR overactivation promotes pro-inflammatory and pro-fibrotic signalling (via NF-\u03baB, TGF-\u03b2, and "
        "PAI-1), leading to podocyte injury, proteinuria, tubular fibrosis, endothelial dysfunction, and "
        "cardiac remodelling. This MR-driven damage occurs even when patients are receiving maximum tolerated "
        "RAAS inhibition, representing a distinct and undertreated pathway of cardiorenal injury.\u2074"
    )

    add_separator(doc)

    # SERANOVA mechanism
    add_heading(doc, "Section 3 \u2014 SERANOVA mechanism (two-column) | highlight background", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "columns-teaser")
    p = doc.add_paragraph()
    run = p.add_run("Section metadata: ")
    run.bold = True
    p.add_run("Style: highlight").font.color.rgb = GREY_TEXT

    doc.add_paragraph()
    add_image_with_caption(doc, "columns-mr-blockade", width=Inches(3.5))

    add_field_value(doc, "Heading", "Selective non-steroidal MR antagonism")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Valinectra binds to the mineralocorticoid receptor ligand-binding domain with a non-steroidal "
        "pharmacophore, providing:\u00b3\n\n"
        "High selectivity for the MR over glucocorticoid, androgen, and progesterone receptors \u2014 "
        "avoiding the endocrine side effects (gynaecomastia, menstrual irregularity) associated with "
        "steroidal MRAs.\u00b3\n\n"
        "Potent inhibition of MR-driven pro-inflammatory and pro-fibrotic gene transcription in renal "
        "tubular cells, podocytes, and cardiac fibroblasts.\u00b3\n\n"
        "Reduction of proteinuria through direct podocyte protection and reduced glomerular MR signalling.\u00b3\n\n"
        "Cardioprotection through attenuation of cardiac fibrosis, left ventricular remodelling, and "
        "endothelial dysfunction.\u00b3"
    )

    add_separator(doc)

    # Complementary mechanisms
    add_heading(doc, "Section 4 \u2014 Complementary to existing therapies (centred text) | light background", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "introduction")
    p = doc.add_paragraph()
    run = p.add_run("Section metadata: ")
    run.bold = True
    p.add_run("Style: light").font.color.rgb = GREY_TEXT

    add_field_value(doc, "Heading", "A complementary mechanism for comprehensive cardiorenal protection")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "SERANOVA addresses a distinct pathophysiological pathway: MR-driven inflammation and fibrosis "
        "that persists despite RAAS inhibition and SGLT2 inhibitor therapy. In the RENOVA programme, "
        "benefits were consistent regardless of background SGLT2 inhibitor use, confirming that MR "
        "antagonism provides additive cardiorenal protection.\u00b9 \u00b2 Current KDIGO 2024 guidelines "
        "recommend considering non-steroidal MRAs as part of the comprehensive approach to reducing "
        "kidney disease progression and cardiovascular risk in patients with CKD and type 2 diabetes.\u2075"
    )

    p = doc.add_paragraph()
    run = p.add_run("Link: ")
    run.bold = True
    p.add_run("View RENOVA clinical data \u2192 /seranova/renova-data")

    add_separator(doc)

    # Accordion + metadata
    add_heading(doc, "Section 5 \u2014 Prescribing information footer", level=3, color=BRAND_COLOUR)
    add_body(doc, "Block: accordion  |  Expandable: PI | AE Reporting | References", italic=True)

    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run("Page metadata")
    run.bold = True
    run.font.color.rgb = AZ_MAGENTA
    add_body(doc, "Title: How SERANOVA Works | Mechanism of Action | MR Antagonism | AstraZeneca UK")
    add_body(doc, "Description: Understand how SERANOVA (valinectra) selectively blocks the mineralocorticoid receptor to reduce kidney and cardiovascular damage in CKD with type 2 diabetes, complementing RAAS and SGLT2 inhibitor therapy.")

    # =====================================================================
    # PAGE 6: RESOURCES
    # =====================================================================
    doc.add_page_break()
    add_heading(doc, "PAGE 6: Resources", level=2, color=AZ_MAGENTA)
    add_field_value(doc, "URL path", "/seranova/resources")
    add_separator(doc)

    # Title
    add_heading(doc, "Section 1 \u2014 Page header (text only, no image)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "title")
    add_field_value(doc, "Heading", "Resources for healthcare professionals")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Access prescribing information, clinical data summaries, and patient support materials "
        "for SERANOVA\u2122 (valinectra)."
    )

    add_separator(doc)

    # Resource cards
    add_heading(doc, "Section 2 \u2014 Resource cards (equal columns) | light background", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "cards-teaser")
    p = doc.add_paragraph()
    run = p.add_run("Section metadata: ")
    run.bold = True
    p.add_run("Style: light").font.color.rgb = GREY_TEXT

    # Card 1
    doc.add_paragraph()
    add_image_with_caption(doc, "card-prescribing", width=Inches(3))
    add_field_value(doc, "Card heading", "Prescribing guide")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "Access the full Summary of Product Characteristics, potassium-guided titration algorithm, "
        "and a quick reference card covering indication, dosing, contraindications, drug interactions, "
        "and monitoring requirements for SERANOVA."
    )
    add_field_value(doc, "Card link", "Access prescribing information \u2192 /seranova/resources")

    add_separator(doc)

    # Card 2
    add_image_with_caption(doc, "card-clinical-summary", width=Inches(3))
    add_field_value(doc, "Card heading", "RENOVA clinical data summaries")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "Concise summaries of the RENOVA-CKD and RENOVA-HF pivotal studies, including study design, "
        "key endpoints, kidney outcomes, cardiovascular data, and eGFR slope analyses in adults with "
        "CKD and type 2 diabetes."
    )
    add_field_value(doc, "Card link", "Download study summaries \u2192 /seranova/resources")

    add_separator(doc)

    # Card 3
    add_image_with_caption(doc, "card-patient", width=Inches(3))
    add_field_value(doc, "Card heading", "Patient support materials")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "Downloadable patient information leaflets, potassium monitoring diaries, and dietary guidance "
        "materials to support patients starting SERANOVA. Available in print-ready and digital formats."
    )
    add_field_value(doc, "Card link", "Download patient materials \u2192 /seranova/resources")

    add_separator(doc)

    # Contact
    add_heading(doc, "Section 3 \u2014 Medical information contact (two-column) | highlight background", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "columns-teaser")
    p = doc.add_paragraph()
    run = p.add_run("Section metadata: ")
    run.bold = True
    p.add_run("Style: highlight").font.color.rgb = GREY_TEXT

    doc.add_paragraph()
    add_image_with_caption(doc, "columns-contact", width=Inches(3.5))

    add_field_value(doc, "Heading", "Medical information and support")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "For medical information enquiries about SERANOVA, please contact AstraZeneca Medical Information:\n\n"
        "Telephone: 0800 783 0033\n\n"
        "Email: medicalinformationuk@astrazeneca.com\n\n"
        "Website: contactazmedical.astrazeneca.com\n\n"
        "Our medical information team is available Monday to Friday, 9:00 AM to 5:00 PM."
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
    add_body(doc, "Title: Resources | SERANOVA (valinectra) | Clinical Summaries & Guides | AstraZeneca UK")
    add_body(doc, "Description: Access prescribing information, RENOVA study summaries, and patient support materials for SERANOVA (valinectra) in CKD with type 2 diabetes.")

    # =================================================================
    # 10. FOOTER CONTENT
    # =================================================================
    doc.add_page_break()
    add_heading(doc, "10. Footer Content", level=1, color=AZ_MAGENTA)

    footer_rows = [
        ("Row 1 \u2014 Brand",
         "AstraZeneca logo | GB-96017 | DOP: March 2026 | \u00a9 2026 AstraZeneca. All rights reserved."),
        ("Row 2 \u2014 Site links",
         "RENOVA Data | Safety | Dosing & Monitoring | How SERANOVA Works | Resources"),
        ("Row 3 \u2014 Regulatory links",
         "Report Adverse Event (https://yellowcard.mhra.gov.uk/) | "
         "Medical Information (https://contactazmedical.astrazeneca.com/) | "
         "Privacy Policy (https://www.astrazeneca.co.uk/our-company/privacy-notice.html) | "
         "Terms of Use (https://www.astrazeneca.co.uk/our-company/terms-of-use.html) | "
         "Accessibility (https://www.astrazeneca.co.uk/accessibility.html)"),
        ("Row 4 \u2014 Date", "Date of Preparation: March 2026"),
    ]
    for label, val in footer_rows:
        add_field_value(doc, label, val)

    add_separator(doc)

    # =================================================================
    # 11. IMAGE ASSETS
    # =================================================================
    add_heading(doc, "11. Image Assets", level=1, color=AZ_MAGENTA)

    add_body(doc, (
        "All images are reused from existing AZ site CDN deployments. No new image generation is required. "
        "If a dedicated Seranova CDN is set up in future, images should be downloaded from the source URLs "
        "below and redeployed to https://seranova-images.pages.dev/."
    ))

    doc.add_paragraph()

    asset_headers = ["#", "Usage", "Source CDN URL", "Dimensions", "Used on"]
    asset_rows = []
    for idx, (key, (url, usage)) in enumerate(IMAGE_MAP.items(), 1):
        dims = "1440\u00d7810" if "hero" in key else "800\u00d7600" if key not in ("astrazeneca-logo", "search") else "Various"
        asset_rows.append((str(idx), key, url, dims, usage))

    add_table(doc, asset_headers, asset_rows)

    doc.add_paragraph()

    # Cross-reference of source sites
    add_heading(doc, "Source site cross-reference", level=2, color=AZ_MAGENTA)
    source_sites = [
        ("novapril-images.pages.dev", "NOVAPRIL (SLE/Lupus) \u2014 Lifestyle portraits, kidney-related imagery"),
        ("zenturis-images.pages.dev", "ZENTURIS (Type 2 Diabetes) \u2014 Metabolic data visualisations, tablet dosing"),
        ("eluvion-images.pages.dev", "ELUVION (Renal Cell Carcinoma) \u2014 Renal/kidney mechanism imagery"),
        ("novatrel-images.pages.dev", "NOVATREL (NSCLC) \u2014 Survival data viz, resource cards, editorial photography"),
        ("lumivex-images.pages.dev", "LUMIVEX (Psoriasis) \u2014 Monitoring guidance imagery"),
    ]
    for domain, desc in source_sites:
        p = doc.add_paragraph(style='List Bullet')
        run_b = p.add_run(f"{domain}: ")
        run_b.bold = True
        run_b.font.size = Pt(10)
        run_v = p.add_run(desc)
        run_v.font.size = Pt(10)

    return doc


# =====================================================================
# ENTRY POINT
# =====================================================================

if __name__ == "__main__":
    print(f"Generating SERANOVA website briefing DOCX...")
    print(f"Output: {OUTPUT_PATH}")
    print()
    print("Downloading images from existing CDN assets...")

    doc = build_document()

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    doc.save(OUTPUT_PATH)

    print()
    print(f"Done! Saved to: {OUTPUT_PATH}")
    print(f"File size: {os.path.getsize(OUTPUT_PATH) / 1024:.0f} KB")

    # Cleanup temp images
    if _tmp_dir and os.path.isdir(_tmp_dir):
        import shutil
        shutil.rmtree(_tmp_dir, ignore_errors=True)
