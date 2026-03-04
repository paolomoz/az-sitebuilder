#!/usr/bin/env python3
"""Generate DOCX briefing for Klera (klerafistat) — Selective oral THR-β agonist for MASH with fibrosis.

Reuses images from Velox site (images/velox/).
Unique page structure: Home → Understanding MASH → CLARITY Data → How KLERA Works →
Safety, Dosing & Monitoring → HCP Resources & Support.
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
SITE_NAME = "klera"
SOURCE_SITE = "velox"
BRAND_COLOUR = RGBColor(0x2E, 0x7D, 0x32)   # Forest Green (liver/metabolic)
ACCENT_COLOUR = RGBColor(0xD4, 0x85, 0x1F)   # Warm Amber
AZ_MAGENTA = RGBColor(0x83, 0x00, 0x51)
DARK_TEXT = RGBColor(0x36, 0x3B, 0x3B)
GREY_TEXT = RGBColor(0x66, 0x66, 0x66)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
RED_NOTICE = RGBColor(0xCC, 0x00, 0x00)

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(PROJECT_DIR, "images", SOURCE_SITE)
CDN_BASE = f"https://{SOURCE_SITE}-images.pages.dev"
OUTPUT_PATH = os.path.join(PROJECT_DIR, "sites", SITE_NAME, "Klera-Website-Briefing.docx")

IMAGE_MANIFEST = {
    "hero-home.jpeg": "Home — hero",
    "hero-efficacy.jpeg": "Understanding MASH — hero",
    "hero-moa.jpeg": "How KLERA Works — hero",
    "card-stroke.jpeg": "Home — fibrosis improvement card",
    "card-bleeding.jpeg": "Home — MASH resolution card",
    "card-dosing.jpeg": "Home — oral once-daily card",
    "columns-moa-preview.jpeg": "Home — MoA teaser",
    "tab-velocity-af.jpeg": "CLARITY Data — CLARITY-FIBROSIS tab",
    "tab-velocity-bleed.jpeg": "CLARITY Data — CLARITY-RESOLVE tab",
    "card-bleeding-events.jpeg": "Understanding MASH — progression card",
    "card-hepatic.jpeg": "Understanding MASH — comorbidity card",
    "card-gi-events.jpeg": "Understanding MASH — diagnosis card",
    "columns-dosing.jpeg": "Safety, Dosing & Monitoring — daily regimen",
    "columns-monitoring.jpeg": "Safety, Dosing & Monitoring — hepatic monitoring",
    "card-prescribing.jpeg": "HCP Resources — prescribing guide card",
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
            run = p.add_run(f"[Image: {filename} — embed failed: {e}]")
            run.font.color.rgb = GREY_TEXT
            run.font.size = Pt(9)
            run.italic = True
    else:
        run = p.add_run(f"[Image: {filename} — not found in {SOURCE_SITE} images]")
        run.font.color.rgb = GREY_TEXT
        run.font.size = Pt(9)
        run.italic = True
        print(f"  [SKIP] {filename}")

    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = cap.add_run(cdn_url)
    r.font.size = Pt(8)
    r.font.color.rgb = RGBColor(0x00, 0x55, 0x99)
    r.underline = True

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

    section = doc.sections[0]
    section.page_width = Cm(21)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2)
    section.bottom_margin = Cm(2)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(2.5)

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
    run = title.add_run("KLERA\u00ae")
    run.font.size = Pt(36)
    run.font.color.rgb = AZ_MAGENTA
    run.bold = True

    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = sub.add_run("(klerafistat)")
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
    run = tagline.add_run("Clearing the path to liver health.")
    run.font.size = Pt(14)
    run.font.color.rgb = BRAND_COLOUR
    run.italic = True

    doc.add_paragraph()

    for line in [
        "Document type: Final approved marketing brief for HCP website build",
        "Prepared by: Marketing \u2014 UK Metabolic & Hepatology Franchise",
        "Approval status: MLR-approved copy \u2014 do not modify",
        "Date: March 2026",
        "Approval code: GB-13402 | DOP: March 2026",
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
        "3. Clinical Programme: CLARITY",
        "4. Safety Profile",
        "5. Prescribing Information",
        "6. Adverse Event Reporting",
        "7. References",
        "8. Site Navigation",
        "9. Page Content",
        "   Page 1: Home",
        "   Page 2: Understanding MASH",
        "   Page 3: CLARITY Data",
        "   Page 4: How KLERA Works",
        "   Page 5: Safety, Dosing & Monitoring",
        "   Page 6: HCP Resources & Support",
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
        ("Brand name", "KLERA\u00ae"),
        ("Generic name", "klerafistat"),
        ("Drug class", "Selective oral thyroid hormone receptor beta (THR-\u03b2) agonist"),
        ("Indication", "Treatment of adults with non-cirrhotic metabolic dysfunction-associated steatohepatitis (MASH) with moderate to advanced liver fibrosis (stage F2 or F3)"),
        ("Biomarker context", "Diagnosis confirmed by liver biopsy or validated non-invasive assessment (FibroScan\u00ae \u22658 kPa with NAS \u22654, or ELF \u22659.8)"),
        ("Formulation", "80 mg and 100 mg film-coated tablets"),
        ("Dosing", "80 mg once daily for the first 3 months, then 100 mg once daily thereafter"),
        ("Approval", "MHRA \u2014 January 2026"),
        ("Brand colour", "Forest Green #2E7D32"),
        ("Accent colour", "Warm Amber #D4851F"),
        ("Approval code", "GB-13402"),
    ]
    add_table(doc, ["Field", "Detail"], profile_data)

    doc.add_paragraph()

    brand_notice = doc.add_paragraph()
    run = brand_notice.add_run(
        "KLERA brand rule: KLERA always appears in capitals, with \u00ae on first mention per page. "
        "Generic name (klerafistat) appears in lowercase parentheses on first mention. "
        'The approved tagline "Clearing the path to liver health." may only be used verbatim \u2014 '
        "no variations permitted."
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
        "Klerafistat is a liver-directed, selective agonist of thyroid hormone receptor beta (THR-\u03b2), "
        "the predominant thyroid hormone receptor isoform expressed in hepatocytes. THR-\u03b2 activation in "
        "the liver regulates key metabolic processes including hepatic lipid metabolism, cholesterol "
        "homeostasis, and mitochondrial \u03b2-oxidation of fatty acids."
    ))
    add_body(doc, (
        "In MASH, hepatic steatosis (fat accumulation) drives lipotoxicity, oxidative stress, "
        "hepatocyte injury, and progressive inflammation leading to fibrogenesis. Current standard of "
        "care (lifestyle modification, weight loss) achieves histological improvement in a minority of "
        "patients, and no pharmacological therapy with a liver fibrosis endpoint had been approved in "
        "the UK prior to klerafistat.\u00b9 \u00b2"
    ))
    add_body(doc, "By selectively activating THR-\u03b2 in the liver, klerafistat produces the following effects:")

    mechanisms = [
        "Increased mitochondrial \u03b2-oxidation of hepatic free fatty acids, reducing intrahepatic triglyceride content",
        "Enhanced LDL receptor expression on hepatocytes, lowering circulating LDL-cholesterol",
        "Reduced de novo lipogenesis via suppression of SREBP-1c and ACC activity",
        "Decreased hepatic lipotoxic lipid species (diacylglycerols, ceramides), reducing hepatocyte injury signals",
        "Attenuation of hepatic stellate cell activation and collagen deposition through reduced lipotoxicity-driven inflammation",
    ]
    for m in mechanisms:
        p = doc.add_paragraph(style='List Bullet')
        run = p.add_run(m)
        run.font.size = Pt(10)

    add_body(doc, (
        "Critically, klerafistat achieves >30-fold selectivity for THR-\u03b2 over THR-\u03b1, the isoform "
        "predominant in the heart and bone. This selectivity avoids the cardiac (tachycardia, arrhythmia) "
        "and skeletal (bone loss) effects of non-selective thyroid hormone action, enabling chronic "
        "therapeutic use.\u00b9 \u00b2 \u2075"
    ))

    add_separator(doc)

    # =================================================================
    # 3. CLINICAL PROGRAMME: CLARITY
    # =================================================================
    add_heading(doc, "3. Clinical Programme: CLARITY", level=1, color=AZ_MAGENTA)

    # CLARITY-FIBROSIS
    add_heading(doc, "CLARITY-FIBROSIS (Phase III, pivotal \u2014 Fibrosis improvement in MASH)", level=2, color=AZ_MAGENTA)
    for label, val in [
        ("Design", "Randomised, double-blind, placebo-controlled Phase III trial"),
        ("Population", "966 adults with biopsy-confirmed MASH (NAS \u22654 with each component \u22651) and liver fibrosis stage F2 or F3, with or without type 2 diabetes"),
        ("Duration", "52 weeks on treatment with paired liver biopsies at baseline and Week 52"),
        ("Primary endpoint", "Proportion achieving \u22651-stage improvement in liver fibrosis without worsening of MASH (NAS) at Week 52"),
        ("Key secondary endpoints", "MASH resolution (ballooning 0, inflammation 0\u20131) without worsening of fibrosis; combined endpoint (\u22651-stage fibrosis improvement AND MASH resolution); change in liver fat by MRI-PDFF; change in LDL-cholesterol; change in ELF score"),
        ("Publication", "Sanyal et al. N Engl J Med 2025; 393(4): 312\u2013326"),
    ]:
        add_field_value(doc, label, val)

    doc.add_paragraph()
    add_body(doc, "Key results:", bold=True)
    add_table(doc,
        ["Endpoint", "KLERA 100 mg (n=483)", "Placebo (n=483)", "Treatment effect"],
        [
            ("\u22651-stage fibrosis improvement without MASH worsening (primary)",
             "37.1%", "14.5%",
             "\u0394 22.6% (17.2\u201328.0); P<0.001"),
            ("MASH resolution without fibrosis worsening",
             "44.2%", "16.8%",
             "\u0394 27.4% (21.8\u201333.0); P<0.001"),
            ("Combined: fibrosis improvement + MASH resolution",
             "25.4%", "6.8%",
             "\u0394 18.6% (14.1\u201323.1); P<0.001"),
            ("Liver fat reduction (MRI-PDFF, relative change)",
             "\u221252.3%", "\u221210.4%",
             "P<0.001"),
            ("LDL-cholesterol change at Week 52",
             "\u221218.7%", "+1.2%",
             "P<0.001"),
            ("ELF score change at Week 52",
             "\u22120.72", "\u22120.08",
             "P<0.001"),
            ("\u22652-stage fibrosis improvement",
             "12.8%", "3.1%",
             "\u0394 9.7% (6.5\u201312.9); P<0.001"),
        ])

    doc.add_paragraph()

    # CLARITY-RESOLVE
    add_heading(doc, "CLARITY-RESOLVE (Phase III \u2014 MASH resolution with metabolic benefits)", level=2, color=AZ_MAGENTA)
    for label, val in [
        ("Design", "Randomised, double-blind, placebo-controlled Phase III trial"),
        ("Population", "748 adults with biopsy-confirmed MASH (NAS \u22654) and fibrosis stage F1\u2013F3, with type 2 diabetes (HbA1c 7.0\u201310.0%)"),
        ("Duration", "52 weeks on treatment with paired liver biopsies"),
        ("Primary endpoint", "MASH resolution (ballooning 0, inflammation 0\u20131) without worsening of fibrosis at Week 52"),
        ("Key secondary endpoints", "Fibrosis improvement \u22651 stage; combined endpoint; HbA1c change; body weight change; liver fat reduction; triglyceride and VLDL-cholesterol change"),
        ("Publication", "Harrison et al. Lancet 2026; 407(10321): 218\u2013232"),
    ]:
        add_field_value(doc, label, val)

    doc.add_paragraph()
    add_body(doc, "Key results:", bold=True)
    add_table(doc,
        ["Endpoint", "KLERA 100 mg (n=374)", "Placebo (n=374)", "Treatment effect"],
        [
            ("MASH resolution without fibrosis worsening (primary)",
             "48.9%", "18.4%",
             "\u0394 30.5% (24.1\u201336.9); P<0.001"),
            ("\u22651-stage fibrosis improvement",
             "34.8%", "15.0%",
             "\u0394 19.8% (13.8\u201325.8); P<0.001"),
            ("Combined: fibrosis improvement + MASH resolution",
             "24.6%", "7.5%",
             "\u0394 17.1% (12.2\u201322.0); P<0.001"),
            ("Liver fat reduction (MRI-PDFF)",
             "\u221258.1%", "\u221212.8%",
             "P<0.001"),
            ("HbA1c change at Week 52",
             "\u22120.42%", "\u22120.06%",
             "\u0394 \u22120.36%; P<0.001"),
            ("Body weight change",
             "\u22122.4 kg", "\u22120.3 kg",
             "\u0394 \u22122.1 kg; P<0.001"),
            ("Triglycerides change",
             "\u221224.6%", "\u22123.8%",
             "P<0.001"),
            ("LDL-cholesterol change",
             "\u221216.9%", "+0.8%",
             "P<0.001"),
        ])

    add_separator(doc)

    # =================================================================
    # 4. SAFETY PROFILE
    # =================================================================
    add_heading(doc, "4. Safety Profile (Pooled CLARITY data, N=857 KLERA)", level=1, color=AZ_MAGENTA)

    add_heading(doc, "Most common adverse events (\u22655%)", level=2, color=AZ_MAGENTA)
    add_table(doc,
        ["Adverse event", "KLERA (%)", "Placebo (%)"],
        [
            ("Diarrhoea", "26.4", "12.1"),
            ("Nausea", "18.7", "8.3"),
            ("Abdominal pain", "9.1", "5.4"),
            ("Weight loss", "7.8", "2.1"),
            ("Headache", "6.4", "5.8"),
            ("Fatigue", "5.9", "4.2"),
            ("Nasopharyngitis", "5.6", "5.4"),
        ])

    doc.add_paragraph()

    add_heading(doc, "Thyroid and cardiac safety", level=2, color=AZ_MAGENTA)
    add_body(doc, (
        "Consistent with selective THR-\u03b2 agonism, klerafistat produced modest reductions in serum TSH "
        "(median nadir \u22120.8 mIU/L at Week 12, stabilising within normal range in >94% of patients) and "
        "total T4 levels without clinically meaningful effects on free T4 or T3. No cases of clinical "
        "hyperthyroidism or thyrotoxicosis were reported.\u00b3"
    ))
    add_body(doc, (
        "Cardiac safety was assessed by 24-hour Holter monitoring at Weeks 12 and 52 in a pre-specified "
        "sub-study (n=204). Mean resting heart rate increased by 1.8 bpm with KLERA vs 0.2 bpm placebo. "
        "No clinically significant arrhythmias, QTc prolongation, or MACE signal was observed. Atrial "
        "fibrillation occurred in 0.6% KLERA vs 0.5% placebo.\u00b3"
    ))

    doc.add_paragraph()

    add_heading(doc, "Hepatic safety", level=2, color=AZ_MAGENTA)
    add_body(doc, (
        "Transient ALT elevations >3\u00d7 ULN occurred in 3.8% of KLERA patients vs 1.9% placebo, "
        "predominantly during the dose-escalation phase (Weeks 1\u201312). These were asymptomatic, "
        "not associated with bilirubin elevation, and resolved with continued dosing in the majority "
        "of cases. No cases of drug-induced liver injury (DILI), Hy\u2019s Law, or liver failure were "
        "observed. One patient (0.1%) discontinued due to persistent ALT elevation.\u00b3"
    ))
    add_body(doc, (
        "Hepatic monitoring: Assess ALT, AST, alkaline phosphatase, and bilirubin before initiation, "
        "monthly for the first 3 months (dose-escalation phase), then every 3 months during maintenance.\u00b3"
    ), bold=True)

    doc.add_paragraph()

    add_heading(doc, "Gastrointestinal events", level=2, color=AZ_MAGENTA)
    add_body(doc, (
        "Diarrhoea (26.4%) and nausea (18.7%) were the most common adverse events, predominantly grade 1\u20132. "
        "Grade \u22653 diarrhoea occurred in 2.8% vs 0.6% placebo. GI events were most frequent during the first "
        "4 weeks and typically self-limited. Dose-escalation from 80 mg to 100 mg at Month 3 was designed to "
        "mitigate GI intolerance. Treatment discontinuation due to GI events was 2.1%.\u00b3"
    ))

    doc.add_paragraph()

    add_heading(doc, "Key safety findings", level=2, color=AZ_MAGENTA)
    safety_findings = [
        ("Serious adverse events", "7.2% KLERA vs 8.4% placebo"),
        ("Treatment discontinuation due to AEs", "5.6% vs 3.4% (GI events 2.1%, ALT elevation 0.1%)"),
        ("All-cause mortality", "0.1% vs 0.2% (no drug-related deaths)"),
        ("MACE (adjudicated)", "0.8% vs 0.7% (no signal; independent adjudication committee confirmed no cardiac safety concern)"),
        ("Bone density (DXA at Week 52)", "No significant change in lumbar spine or femoral neck BMD with KLERA vs placebo, consistent with THR-\u03b2 selectivity and sparing of THR-\u03b1 in bone\u00b3"),
        ("Gallbladder events", "Cholelithiasis 1.6% vs 0.8%. Cholecystitis 0.5% vs 0.2%. Consistent with increased hepatic cholesterol clearance\u00b3"),
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
        "Type 2 diabetes: 58% of CLARITY-FIBROSIS and 100% of CLARITY-RESOLVE patients had T2D. HbA1c improved by 0.36% vs placebo. Hypoglycaemia was not increased. No dose adjustment for concurrent metformin, SGLT2 inhibitors, or GLP-1 RAs.\u00b3",
        "Elderly (\u226565 years): 24% of pooled population. Efficacy and safety consistent with overall population. Increased GI sensitivity was observed (\u22655% higher diarrhoea incidence). No dose adjustment required.\u00b3",
        "Renal impairment: No dose adjustment for eGFR \u226530 mL/min/1.73m\u00b2. Not studied in eGFR <30.\u00b3",
        "Hepatic impairment: Indicated only in non-cirrhotic MASH (F2\u2013F3). Contraindicated in decompensated cirrhosis (Child-Pugh B or C). Not studied in Child-Pugh A cirrhosis.\u00b3",
        "Pregnancy and lactation: Contraindicated in pregnancy. Animal studies showed embryofetal toxicity at supratherapeutic doses. Women of childbearing potential must use effective contraception during treatment and for 1 month after the last dose. Discontinue breastfeeding during treatment.\u00b3",
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
        "KLERA (klerafistat) 80 mg and 100 mg film-coated tablets. "
        "Please refer to the Summary of Product Characteristics (SmPC) before prescribing. "
        "Indication: Treatment of adults with non-cirrhotic metabolic dysfunction-associated steatohepatitis "
        "(MASH) with moderate to advanced liver fibrosis (stage F2 or F3). "
        "Dosage and administration: 80 mg once daily for the first 3 months, then 100 mg once daily, "
        "taken with food. Swallow whole; do not crush or chew. "
        "Contraindications: Hypersensitivity to klerafistat or excipients; pregnancy; decompensated "
        "cirrhosis (Child-Pugh B or C); active thyrotoxicosis. "
        "Warnings and precautions: Hepatotoxicity: Monitor LFTs before initiation, monthly for 3 months, "
        "then every 3 months. Gastrointestinal: Dose escalation designed to mitigate GI effects. "
        "Thyroid function: Monitor TSH at baseline and if clinically indicated. Gallbladder: Increased "
        "risk of cholelithiasis. "
        "Interactions: No clinically significant CYP interactions identified. Caution with bile acid "
        "sequestrants (cholestyramine, colesevelam): may reduce klerafistat absorption; administer KLERA "
        "\u22654 hours before or 4 hours after bile acid sequestrants. Caution with statins: additive "
        "LDL-lowering effect; monitor for myopathy. "
        "Side effects: Very common (\u22651/10): diarrhoea, nausea. Common (\u22651/100 to <1/10): abdominal "
        "pain, weight loss, headache, fatigue, ALT increased, cholelithiasis. Uncommon (\u22651/1000 to "
        "<1/100): cholecystitis, TSH suppression. "
        "Legal category: POM. Pack and price: 28 tablets (80 mg): \u00a3476.00; 28 tablets (100 mg): "
        "\u00a3476.00. Marketing authorisation holder: AstraZeneca UK Ltd. MA number: PLGB 17901/0756. "
        "Full prescribing information available from: AstraZeneca UK Ltd, 2 Pancras Square, London N1C 4AG. "
        "GB-13402 | DOP: March 2026."
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
        "Sanyal et al. N Engl J Med 2025; 393(4): 312\u2013326.",
        "Harrison et al. Lancet 2026; 407(10321): 218\u2013232.",
        "KLERA (klerafistat) Summary of Product Characteristics. AstraZeneca UK Ltd. January 2026.",
        "Younossi ZM, et al. Hepatology 2023; 77(4): 1335\u20131347.",
        "Harrison SA, et al. N Engl J Med 2023; 389(13): 1169\u20131180.",
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
        ("Main navigation pages", "Understanding MASH | CLARITY Data | How KLERA Works | Safety, Dosing & Monitoring | HCP Resources & Support"),
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
        'KLERA brand rule: KLERA always appears in capitals, with \u00ae on first mention per page. '
        'Generic name (klerafistat) in lowercase parentheses on first mention. '
        'Tagline "Clearing the path to liver health." verbatim only.'
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
    add_field_value(doc, "URL path", "/klera/")
    add_separator(doc)

    # Section 1 — Hero
    add_heading(doc, "Section 1 \u2014 Hero (full-width image with text overlay)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "hero-teaser")
    doc.add_paragraph()
    add_image_with_caption(doc, "hero-home.jpeg", width=Inches(5.5))

    add_field_value(doc, "Heading", "KLERA\u00ae (klerafistat)")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "The first oral therapy approved to improve liver fibrosis in non-cirrhotic MASH. "
        "37% of patients achieved fibrosis improvement at one year, with concomitant reductions "
        "in liver fat, LDL-cholesterol, and HbA1c. Clearing the path to liver health.\u00b9"
    )
    add_field_value(doc, "Call to action", "Explore the CLARITY data \u2192 /klera/clarity-data")

    add_separator(doc)

    # Section 2 — Three benefit cards
    add_heading(doc, "Section 2 \u2014 Three key benefit cards (equal columns)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "cards-teaser")

    # Card 1 — Fibrosis
    doc.add_paragraph()
    add_image_with_caption(doc, "card-stroke.jpeg", width=Inches(3))
    add_field_value(doc, "Card heading", "37% achieved fibrosis improvement")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "In CLARITY-FIBROSIS, 37.1% of patients achieved \u22651-stage fibrosis improvement without "
        "worsening of MASH at Week 52, compared with 14.5% placebo (\u0394 22.6%; P<0.001). This "
        "is the first pharmacotherapy to demonstrate a fibrosis endpoint in a Phase III MASH trial.\u00b9"
    )
    add_field_value(doc, "Card link", "View CLARITY data \u2192 /klera/clarity-data")

    add_separator(doc)

    # Card 2 — MASH resolution
    add_image_with_caption(doc, "card-bleeding.jpeg", width=Inches(3))
    add_field_value(doc, "Card heading", "49% achieved MASH resolution")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "In CLARITY-RESOLVE, 48.9% of patients with MASH and type 2 diabetes achieved histological "
        "MASH resolution without fibrosis worsening at Week 52, compared with 18.4% placebo "
        "(\u0394 30.5%; P<0.001).\u00b2"
    )
    add_field_value(doc, "Card link", "Explore MASH resolution data \u2192 /klera/clarity-data")

    add_separator(doc)

    # Card 3 — Oral once daily
    add_image_with_caption(doc, "card-dosing.jpeg", width=Inches(3))
    add_field_value(doc, "Card heading", "Oral once-daily with metabolic benefits")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "One tablet once daily with food. Beyond liver histology, KLERA reduced LDL-cholesterol "
        "by 19%, lowered triglycerides by 25%, and improved HbA1c by 0.36% in patients with "
        "type 2 diabetes \u2014 addressing the cardiometabolic comorbidities of MASH.\u00b9 \u00b2 \u00b3"
    )
    add_field_value(doc, "Card link", "View dosing information \u2192 /klera/safety-dosing-monitoring")

    add_separator(doc)

    # Section 3 — MoA teaser
    add_heading(doc, "Section 3 \u2014 MoA teaser (two-column: image left, text right) | highlight background", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "columns-teaser")
    p = doc.add_paragraph()
    run = p.add_run("Section metadata: ")
    run.bold = True
    p.add_run("Style: highlight").font.color.rgb = GREY_TEXT

    doc.add_paragraph()
    add_image_with_caption(doc, "columns-moa-preview.jpeg", width=Inches(3.5))

    add_field_value(doc, "Heading", "Harnessing thyroid hormone biology to reverse liver damage")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "THR-\u03b2 is the predominant thyroid hormone receptor in the liver. By selectively activating "
        "THR-\u03b2, KLERA enhances hepatic fat oxidation, reduces lipotoxicity, and attenuates "
        "fibrogenesis \u2014 without the cardiac and bone effects of non-selective thyroid hormone "
        "action.\u00b3 \u2075"
    )
    add_field_value(doc, "Call to action", "Explore how KLERA works \u2192 /klera/how-klera-works")

    add_separator(doc)

    # Section 4 — Accordion
    add_heading(doc, "Section 4 \u2014 Prescribing information footer", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "accordion")
    add_body(doc, "Expandable sections for: Prescribing Information | Adverse Event Reporting | References", italic=True)

    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run("Page metadata")
    run.bold = True
    run.font.color.rgb = AZ_MAGENTA
    add_body(doc, "Title: KLERA (klerafistat) | Oral Treatment for MASH Liver Fibrosis | AstraZeneca UK")
    add_body(doc, "Description: KLERA (klerafistat) is the first oral THR-\u03b2 agonist approved for non-cirrhotic MASH with liver fibrosis. Explore CLARITY clinical data, mechanism of action, and dosing for UK healthcare professionals.")

    # =====================================================================
    # PAGE 2: UNDERSTANDING MASH (disease-first — unique to Klera)
    # =====================================================================
    doc.add_page_break()
    add_heading(doc, "PAGE 2: Understanding MASH", level=2, color=AZ_MAGENTA)
    add_field_value(doc, "URL path", "/klera/understanding-mash")
    add_separator(doc)

    # Hero
    add_heading(doc, "Section 1 \u2014 Hero (full-width image with text overlay)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "hero-teaser")
    doc.add_paragraph()
    add_image_with_caption(doc, "hero-efficacy.jpeg", width=Inches(5.5))

    add_field_value(doc, "Heading", "MASH: the silent liver epidemic")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Metabolic dysfunction-associated steatohepatitis affects an estimated 3\u20135% of the UK adult "
        "population. Most patients are undiagnosed until advanced fibrosis or cirrhosis develops, at "
        "which point treatment options are limited and prognosis is poor.\u2074"
    )

    add_separator(doc)

    # Section 2 — Disease burden cards (3 columns)
    add_heading(doc, "Section 2 \u2014 Disease burden (three equal columns)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "cards-teaser")

    doc.add_paragraph()
    add_image_with_caption(doc, "card-bleeding-events.jpeg", width=Inches(3))
    add_field_value(doc, "Card heading", "Progressive fibrosis")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "Fibrosis stage is the strongest independent predictor of liver-related mortality in MASH. "
        "Patients with stage F3 fibrosis have a 3.5-fold increased risk of liver-related death "
        "compared with F0\u2013F1, and 10\u201315% progress to cirrhosis within 5 years.\u2074"
    )

    add_separator(doc)

    add_image_with_caption(doc, "card-hepatic.jpeg", width=Inches(3))
    add_field_value(doc, "Card heading", "Cardiometabolic comorbidity")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "MASH is intrinsically linked to the metabolic syndrome: over 70% of MASH patients have "
        "type 2 diabetes, dyslipidaemia, or both. Cardiovascular disease is the leading cause of "
        "death in patients with MASH, accounting for more deaths than liver-related events.\u2074"
    )

    add_separator(doc)

    add_image_with_caption(doc, "card-gi-events.jpeg", width=Inches(3))
    add_field_value(doc, "Card heading", "Diagnostic challenges")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "MASH is often asymptomatic until advanced disease. Non-invasive biomarkers (FIB-4, ELF, "
        "FibroScan\u00ae) can identify patients at risk, but definitive MASH diagnosis and fibrosis "
        "staging historically required liver biopsy. Increasing use of non-invasive pathways is "
        "improving earlier identification of at-risk patients.\u2074"
    )

    add_separator(doc)

    # Section 3 — Disease progression pathway (accordion — UNIQUE: educational FAQ)
    add_heading(doc, "Section 3 \u2014 MASH disease pathway (accordion FAQ) | light background", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "accordion")
    p = doc.add_paragraph()
    run = p.add_run("Section metadata: ")
    run.bold = True
    p.add_run("Style: light").font.color.rgb = GREY_TEXT

    add_body(doc, 'Panel 1: "From steatosis to steatohepatitis"', bold=True)
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Hepatic steatosis (fat accumulation >5% of hepatocytes) is driven by insulin resistance, "
        "excess caloric intake, and impaired hepatic lipid metabolism. In a subset of patients, "
        "accumulated lipotoxic lipid species (diacylglycerols, ceramides, free cholesterol) trigger "
        "hepatocyte injury, activating inflammatory pathways (NF-\u03baB, JNK) and driving the transition "
        "from benign steatosis to steatohepatitis (MASH). Histologically, MASH is defined by steatosis "
        "with hepatocyte ballooning and lobular inflammation.\u2074 \u2075"
    )

    add_body(doc, 'Panel 2: "From inflammation to fibrosis"', bold=True)
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Chronic hepatocyte injury in MASH activates hepatic stellate cells \u2014 the principal "
        "fibrogenic cells in the liver. Activated stellate cells deposit excess extracellular matrix "
        "(collagen, fibronectin), progressively distorting hepatic architecture. Fibrosis progresses "
        "through stages F1 (perisinusoidal) \u2192 F2 (portal/periportal) \u2192 F3 (bridging) \u2192 "
        "F4 (cirrhosis). Once cirrhosis develops, risk of decompensation, hepatocellular carcinoma, "
        "and liver transplant requirement increases substantially.\u2074"
    )

    add_body(doc, 'Panel 3: "Why fibrosis stage determines prognosis"', bold=True)
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Large meta-analyses demonstrate that fibrosis stage, not steatohepatitis activity, is the "
        "strongest predictor of all-cause and liver-related mortality in MASH. Each one-stage increase "
        "in fibrosis is associated with a 1.5\u20132.5-fold increased mortality risk. Fibrosis stage "
        "F3 (bridging fibrosis) represents a critical intervention window: advanced enough to carry "
        "significant prognostic risk, but potentially reversible with effective therapy before the "
        "architectural disruption of cirrhosis.\u2074"
    )

    add_separator(doc)

    # Section 4 — Identification pathway (introduction)
    add_heading(doc, "Section 4 \u2014 Patient identification (centred text) | highlight background", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "introduction")
    p = doc.add_paragraph()
    run = p.add_run("Section metadata: ")
    run.bold = True
    p.add_run("Style: highlight").font.color.rgb = GREY_TEXT

    add_field_value(doc, "Heading", "Identifying patients who may benefit from KLERA")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Consider KLERA for adults with confirmed MASH and stage F2 or F3 liver fibrosis. "
        "Non-invasive assessment pathways (FIB-4 \u2192 ELF or FibroScan) can identify patients "
        "with significant fibrosis in primary and secondary care. Liver biopsy remains the gold "
        "standard for staging but is not mandatory for treatment initiation when non-invasive "
        "markers are consistent with F2\u2013F3 disease.\u00b3 \u2074"
    )

    add_separator(doc)

    # Accordion
    add_heading(doc, "Section 5 \u2014 Prescribing information footer", level=3, color=BRAND_COLOUR)
    add_body(doc, "Block: accordion  |  Expandable: PI | AE Reporting | References", italic=True)

    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run("Page metadata")
    run.bold = True
    run.font.color.rgb = AZ_MAGENTA
    add_body(doc, "Title: Understanding MASH | Liver Fibrosis & Disease Progression | KLERA | AstraZeneca UK")
    add_body(doc, "Description: Learn about metabolic dysfunction-associated steatohepatitis (MASH) \u2014 disease burden, fibrosis progression, cardiometabolic comorbidities, and patient identification pathways.")

    # =====================================================================
    # PAGE 3: CLARITY DATA
    # =====================================================================
    doc.add_page_break()
    add_heading(doc, "PAGE 3: CLARITY Data", level=2, color=AZ_MAGENTA)
    add_field_value(doc, "URL path", "/klera/clarity-data")
    add_separator(doc)

    # Section 1 — Title (no hero — text-only header, DIFFERENT from other sites)
    add_heading(doc, "Section 1 \u2014 Page header (text only, no image)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "title")

    add_field_value(doc, "Heading", "The CLARITY clinical programme")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "KLERA\u00ae (klerafistat) was evaluated in over 1,700 patients across two biopsy-confirmed "
        "Phase III trials, demonstrating clinically meaningful liver histology improvement with "
        "concomitant cardiometabolic benefits.\u00b9 \u00b2"
    )

    add_separator(doc)

    # Section 2 — Headline stats carousel (carousel-teaser — UNIQUE block choice for data page)
    add_heading(doc, "Section 2 \u2014 Headline statistics carousel (4 slides) | light background", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "carousel-teaser")
    p = doc.add_paragraph()
    run = p.add_run("Section metadata: ")
    run.bold = True
    p.add_run("Style: light").font.color.rgb = GREY_TEXT

    add_body(doc, "Slide 1:", bold=True)
    add_field_value(doc, "Heading", "37% achieved fibrosis improvement")
    add_body(doc, "In CLARITY-FIBROSIS, \u22651-stage fibrosis improvement without MASH worsening in 37.1% vs 14.5% placebo (\u0394 22.6%; P<0.001).\u00b9")

    add_body(doc, "Slide 2:", bold=True)
    add_field_value(doc, "Heading", "49% achieved MASH resolution")
    add_body(doc, "In CLARITY-RESOLVE, MASH resolution without fibrosis worsening in 48.9% vs 18.4% placebo (\u0394 30.5%; P<0.001).\u00b2")

    add_body(doc, "Slide 3:", bold=True)
    add_field_value(doc, "Heading", "52% liver fat reduction")
    add_body(doc, "Relative reduction in hepatic fat content by MRI-PDFF: \u221252.3% with KLERA vs \u221210.4% placebo at Week 52 (P<0.001).\u00b9")

    add_body(doc, "Slide 4:", bold=True)
    add_field_value(doc, "Heading", "19% LDL-cholesterol reduction")
    add_body(doc, "LDL-cholesterol decreased by 18.7% with KLERA vs +1.2% with placebo at Week 52, addressing cardiovascular risk alongside liver disease (P<0.001).\u00b9")

    add_separator(doc)

    # Section 3 — Tabs
    add_heading(doc, "Section 3 \u2014 Clinical data (two tabs)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "tabs-large")

    # Tab 1 — CLARITY-FIBROSIS
    doc.add_paragraph()
    add_body(doc, 'Tab 1: "CLARITY-FIBROSIS: Fibrosis improvement"', bold=True)
    add_image_with_caption(doc, "tab-velocity-af.jpeg", width=Inches(3.5))

    add_field_value(doc, "Heading", "CLARITY-FIBROSIS: The first Phase III trial to achieve a fibrosis endpoint in MASH")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "CLARITY-FIBROSIS was a randomised, double-blind, placebo-controlled trial in 966 adults "
        "with biopsy-confirmed MASH (NAS \u22654) and fibrosis stage F2 or F3, with or without type 2 "
        "diabetes. KLERA 100 mg once daily (after 80 mg run-in) was evaluated with paired liver "
        "biopsies at baseline and Week 52.\u00b9"
    )
    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run("Body text (continued): ")
    run.bold = True
    p.add_run(
        "The primary endpoint was met: 37.1% of KLERA patients achieved \u22651-stage fibrosis "
        "improvement without worsening of MASH, compared with 14.5% placebo (\u0394 22.6%; P<0.001). "
        "MASH resolution was achieved in 44.2% vs 16.8% (P<0.001). The combined endpoint (fibrosis "
        "improvement AND MASH resolution) was achieved in 25.4% vs 6.8% (P<0.001). Notably, 12.8% "
        "of KLERA patients achieved \u22652-stage fibrosis improvement, suggesting the potential for "
        "substantial histological reversal in a subset of patients. Liver fat decreased by 52.3% "
        "(MRI-PDFF) and LDL-cholesterol by 18.7%.\u00b9"
    )

    add_body(doc, "Data table:", bold=True)
    add_table(doc,
        ["Endpoint", "KLERA (n=483)", "Placebo (n=483)", "Effect"],
        [
            ("Fibrosis improvement (primary)", "37.1%", "14.5%", "\u0394 22.6%; P<0.001"),
            ("MASH resolution", "44.2%", "16.8%", "\u0394 27.4%; P<0.001"),
            ("Combined endpoint", "25.4%", "6.8%", "\u0394 18.6%; P<0.001"),
            ("Liver fat (MRI-PDFF)", "\u221252.3%", "\u221210.4%", "P<0.001"),
            ("LDL-C change", "\u221218.7%", "+1.2%", "P<0.001"),
        ])

    add_separator(doc)

    # Tab 2 — CLARITY-RESOLVE
    add_body(doc, 'Tab 2: "CLARITY-RESOLVE: MASH resolution with metabolic benefits"', bold=True)
    add_image_with_caption(doc, "tab-velocity-bleed.jpeg", width=Inches(3.5))

    add_field_value(doc, "Heading", "CLARITY-RESOLVE: MASH resolution and cardiometabolic improvement in T2D")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "CLARITY-RESOLVE was a randomised, double-blind, placebo-controlled trial in 748 adults with "
        "biopsy-confirmed MASH (NAS \u22654) and fibrosis stage F1\u2013F3, all with type 2 diabetes "
        "(HbA1c 7.0\u201310.0%). This trial specifically assessed whether KLERA could address both liver "
        "histology and the metabolic comorbidities that drive morbidity in MASH.\u00b2"
    )
    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run("Body text (continued): ")
    run.bold = True
    p.add_run(
        "KLERA achieved a MASH resolution rate of 48.9% vs 18.4% placebo (\u0394 30.5%; P<0.001). "
        "Fibrosis improvement (\u22651 stage) was achieved in 34.8% vs 15.0% (P<0.001). Beyond liver "
        "histology, KLERA improved HbA1c by 0.36% vs placebo, reduced body weight by 2.1 kg, "
        "lowered triglycerides by 24.6%, and reduced LDL-cholesterol by 16.9%. Liver fat decreased "
        "by 58.1% (MRI-PDFF). These cardiometabolic benefits address the multi-organ nature of "
        "MASH and its associated morbidity.\u00b2"
    )

    add_body(doc, "Data table:", bold=True)
    add_table(doc,
        ["Endpoint", "KLERA (n=374)", "Placebo (n=374)", "Effect"],
        [
            ("MASH resolution (primary)", "48.9%", "18.4%", "\u0394 30.5%; P<0.001"),
            ("Fibrosis improvement", "34.8%", "15.0%", "\u0394 19.8%; P<0.001"),
            ("HbA1c change", "\u22120.42%", "\u22120.06%", "\u0394 \u22120.36%; P<0.001"),
            ("Body weight", "\u22122.4 kg", "\u22120.3 kg", "\u0394 \u22122.1 kg; P<0.001"),
            ("Triglycerides", "\u221224.6%", "\u22123.8%", "P<0.001"),
            ("LDL-C change", "\u221216.9%", "+0.8%", "P<0.001"),
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
    add_body(doc, "Title: CLARITY Data | KLERA (klerafistat) | Fibrosis & MASH Resolution | AstraZeneca UK")
    add_body(doc, "Description: Explore the CLARITY clinical programme for KLERA (klerafistat) \u2014 Phase III fibrosis improvement, MASH resolution, and cardiometabolic outcomes in adults with MASH and liver fibrosis.")

    # =====================================================================
    # PAGE 4: HOW KLERA WORKS
    # =====================================================================
    doc.add_page_break()
    add_heading(doc, "PAGE 4: How KLERA Works", level=2, color=AZ_MAGENTA)
    add_field_value(doc, "URL path", "/klera/how-klera-works")
    add_separator(doc)

    # Hero
    add_heading(doc, "Section 1 \u2014 Hero (full-width image with text overlay)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "hero-teaser")
    doc.add_paragraph()
    add_image_with_caption(doc, "hero-moa.jpeg", width=Inches(5.5))

    add_field_value(doc, "Heading", "How KLERA works")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "KLERA\u00ae (klerafistat) selectively activates thyroid hormone receptor beta in the liver, "
        "harnessing the body\u2019s own metabolic machinery to clear hepatic fat and halt "
        "fibrosis progression.\u00b3 \u2075"
    )

    add_separator(doc)

    # Section 2 — THR biology (introduction)
    add_heading(doc, "Section 2 \u2014 THR biology (centred text) | light background", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "introduction")
    p = doc.add_paragraph()
    run = p.add_run("Section metadata: ")
    run.bold = True
    p.add_run("Style: light").font.color.rgb = GREY_TEXT

    add_field_value(doc, "Heading", "THR-\u03b2: the liver\u2019s metabolic master switch")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Thyroid hormones regulate hepatic metabolism through two receptor isoforms: THR-\u03b1 "
        "(predominant in heart and bone) and THR-\u03b2 (predominant in liver). THR-\u03b2 activation "
        "in hepatocytes drives mitochondrial fatty acid \u03b2-oxidation, upregulates LDL receptor "
        "expression, and suppresses de novo lipogenesis. Patients with MASH frequently exhibit "
        "features of relative hepatic hypothyroidism \u2014 reduced intrahepatic T3 signalling despite "
        "normal systemic thyroid function \u2014 contributing to impaired hepatic lipid clearance.\u2074 \u2075"
    )

    add_separator(doc)

    # Section 3 — MoA detail (columns-teaser with image)
    add_heading(doc, "Section 3 \u2014 Mechanism detail (two-column: image left, text right) | highlight background", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "columns-teaser")
    p = doc.add_paragraph()
    run = p.add_run("Section metadata: ")
    run.bold = True
    p.add_run("Style: highlight").font.color.rgb = GREY_TEXT

    doc.add_paragraph()
    add_image_with_caption(doc, "columns-moa-preview.jpeg", width=Inches(3.5))

    add_field_value(doc, "Heading", "Selective THR-\u03b2 agonism: liver-directed fat clearance")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Klerafistat binds to THR-\u03b2 with >30-fold selectivity over THR-\u03b1. In the hepatocyte, "
        "THR-\u03b2 activation upregulates mitochondrial \u03b2-oxidation enzymes (CPT1A, ACADL), increasing "
        "fatty acid catabolism and reducing intracellular triglyceride, diacylglycerol, and ceramide "
        "pools. Concurrently, de novo lipogenesis is suppressed through downregulation of SREBP-1c "
        "and ACC. The net effect is a >50% reduction in hepatic fat content within 12 weeks.\u00b3 \u2075"
    )
    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run("Body text (continued): ")
    run.bold = True
    p.add_run(
        "Reduced lipotoxicity diminishes hepatocyte injury signals, attenuating the activation of "
        "hepatic stellate cells and slowing collagen deposition. Additionally, KLERA upregulates "
        "hepatic LDL receptor expression, lowering circulating LDL-cholesterol by ~19% and "
        "addressing the cardiovascular risk that is the leading cause of death in MASH patients. "
        "THR-\u03b1 sparing preserves cardiac rhythm and bone density, enabling chronic use.\u00b3 \u2075"
    )
    add_field_value(doc, "Call to action", "View the CLARITY data \u2192 /klera/clarity-data")

    add_separator(doc)

    # Section 4 — Selectivity (introduction with key stat)
    add_heading(doc, "Section 4 \u2014 THR-\u03b2 selectivity (centred text)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "introduction")

    add_field_value(doc, "Heading", ">30-fold selectivity for THR-\u03b2 over THR-\u03b1")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Non-selective thyroid hormone action causes tachycardia, atrial fibrillation, and "
        "accelerated bone turnover. KLERA achieves >30-fold selectivity for the liver-predominant "
        "THR-\u03b2 isoform, sparing THR-\u03b1-mediated effects. In CLARITY, mean heart rate increased "
        "by only 1.8 bpm vs 0.2 bpm placebo, no arrhythmia signal was detected, and bone mineral "
        "density was unchanged at Week 52.\u00b3"
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
    add_body(doc, "Title: How KLERA Works | THR-\u03b2 Agonist Mechanism | Liver-Directed Therapy | AstraZeneca UK")
    add_body(doc, "Description: Understand how KLERA (klerafistat) selectively activates THR-\u03b2 in the liver to clear hepatic fat, reduce lipotoxicity, and improve fibrosis in MASH.")

    # =====================================================================
    # PAGE 5: SAFETY, DOSING & MONITORING (all-in-one — UNIQUE structure)
    # =====================================================================
    doc.add_page_break()
    add_heading(doc, "PAGE 5: Safety, Dosing & Monitoring", level=2, color=AZ_MAGENTA)
    add_field_value(doc, "URL path", "/klera/safety-dosing-monitoring")
    add_separator(doc)

    # Section 1 — Title
    add_heading(doc, "Section 1 \u2014 Page header (text only, no image)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "title")
    add_field_value(doc, "Heading", "Safety, dosing, and monitoring")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "KLERA\u00ae (klerafistat) has been evaluated in 857 patients across the CLARITY clinical "
        "programme. A simple oral once-daily regimen with dose escalation and structured hepatic "
        "monitoring supports safe long-term treatment.\u00b9 \u00b2 \u00b3"
    )

    add_separator(doc)

    # Section 2 — Dosing (columns-teaser)
    add_heading(doc, "Section 2 \u2014 Dosing regimen (two-column: image left, text right) | highlight background", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "columns-teaser")
    p = doc.add_paragraph()
    run = p.add_run("Section metadata: ")
    run.bold = True
    p.add_run("Style: highlight").font.color.rgb = GREY_TEXT

    doc.add_paragraph()
    add_image_with_caption(doc, "columns-dosing.jpeg", width=Inches(3.5))

    add_field_value(doc, "Heading", "Dose escalation for tolerability")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Month 1\u20133: KLERA 80 mg once daily with food. Month 4 onwards: increase to 100 mg once "
        "daily with food. This dose-escalation approach was designed to mitigate gastrointestinal "
        "adverse events during treatment initiation. Tablets should be swallowed whole. If a dose "
        "is missed, take it as soon as remembered on the same day; do not double-dose.\u00b3"
    )

    add_separator(doc)

    # Section 3 — Safety overview (3-column cards)
    add_heading(doc, "Section 3 \u2014 Key safety topics (three equal columns)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "cards-teaser")

    doc.add_paragraph()
    add_image_with_caption(doc, "card-bleeding-events.jpeg", width=Inches(3))
    add_field_value(doc, "Card heading", "Gastrointestinal events")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "Diarrhoea (26.4%) and nausea (18.7%) were the most common AEs, predominantly grade 1\u20132 "
        "and most frequent during the first 4 weeks. Grade \u22653 diarrhoea: 2.8%. Treatment "
        "discontinuation due to GI events: 2.1%. Dose-escalation mitigates GI intolerance.\u00b3"
    )

    add_separator(doc)

    add_image_with_caption(doc, "card-hepatic.jpeg", width=Inches(3))
    add_field_value(doc, "Card heading", "Hepatic safety")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "Transient ALT >3\u00d7 ULN in 3.8% (vs 1.9% placebo), predominantly during dose escalation. "
        "Asymptomatic, no bilirubin elevation, resolved with continued dosing in most cases. No DILI "
        "or Hy\u2019s Law cases. Monitor LFTs monthly for 3 months, then quarterly.\u00b3"
    )

    add_separator(doc)

    add_image_with_caption(doc, "card-gi-events.jpeg", width=Inches(3))
    add_field_value(doc, "Card heading", "Thyroid and cardiac safety")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "TSH suppression was modest (\u22120.8 mIU/L nadir at Week 12); >94% remained within normal "
        "range. No clinical thyrotoxicosis. Mean heart rate +1.8 bpm. No arrhythmia or QTc signal. "
        "Bone density unchanged at Week 52, confirming THR-\u03b1 sparing.\u00b3"
    )

    add_separator(doc)

    # Section 4 — Monitoring schedule (table-data — UNIQUE to this page layout)
    add_heading(doc, "Section 4 \u2014 Monitoring schedule table | light background", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "table-data")
    p = doc.add_paragraph()
    run = p.add_run("Section metadata: ")
    run.bold = True
    p.add_run("Style: light").font.color.rgb = GREY_TEXT

    add_field_value(doc, "Heading", "Recommended monitoring schedule")
    add_table(doc,
        ["Assessment", "Baseline", "Month 1", "Month 2", "Month 3", "Every 3 months"],
        [
            ("ALT, AST, ALP, bilirubin", "\u2713", "\u2713", "\u2713", "\u2713", "\u2713"),
            ("TSH", "\u2713", "", "", "\u2713*", "As indicated"),
            ("Lipid panel (LDL-C, TG)", "\u2713", "", "", "\u2713", "\u2713"),
            ("HbA1c (if T2D)", "\u2713", "", "", "\u2713", "\u2713"),
            ("eGFR", "\u2713", "", "", "", "\u2713"),
            ("Weight", "\u2713", "\u2713", "\u2713", "\u2713", "\u2713"),
            ("Pregnancy test (if applicable)", "\u2713", "", "", "", ""),
            ("FibroScan / ELF (optional)", "\u2713", "", "", "", "Every 12 months"),
        ])

    p = doc.add_paragraph()
    run = p.add_run("*Reassess TSH at Month 3 (end of 80 mg dose phase). Monitor further only if clinically indicated.")
    run.font.size = Pt(8)
    run.font.italic = True
    run.font.color.rgb = GREY_TEXT

    add_separator(doc)

    # Section 5 — Monitoring / drug interactions (columns-teaser)
    add_heading(doc, "Section 5 \u2014 Practical guidance (two-column: image left, text right)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "columns-teaser")

    doc.add_paragraph()
    add_image_with_caption(doc, "columns-monitoring.jpeg", width=Inches(3.5))

    add_field_value(doc, "Heading", "Drug interactions and co-prescribing considerations")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "No clinically significant CYP-mediated drug interactions have been identified. Bile acid "
        "sequestrants (cholestyramine, colesevelam) may reduce klerafistat absorption: administer KLERA "
        "\u22654 hours before or after bile acid sequestrants. Statins: additive LDL-lowering; monitor for "
        "myopathy symptoms at initiation. KLERA may be used alongside metformin, SGLT2 inhibitors, "
        "GLP-1 receptor agonists, and insulin without dose adjustment. Monitor for hypoglycaemia if "
        "HbA1c improvement leads to relative over-treatment of diabetes.\u00b3"
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
    add_body(doc, "Title: Safety, Dosing & Monitoring | KLERA (klerafistat) | MASH Treatment | AstraZeneca UK")
    add_body(doc, "Description: KLERA (klerafistat) safety, dosing regimen with dose escalation, monitoring schedule, and drug interaction guidance for UK healthcare professionals managing MASH with liver fibrosis.")

    # =====================================================================
    # PAGE 6: HCP RESOURCES & SUPPORT
    # =====================================================================
    doc.add_page_break()
    add_heading(doc, "PAGE 6: HCP Resources & Support", level=2, color=AZ_MAGENTA)
    add_field_value(doc, "URL path", "/klera/resources")
    add_separator(doc)

    # Section 1 — Title
    add_heading(doc, "Section 1 \u2014 Page header (text only, no image)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "title")
    add_field_value(doc, "Heading", "Resources and support for healthcare professionals")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Access prescribing guides, MASH patient identification tools, CLARITY data summaries, "
        "and monitoring resources for KLERA\u00ae (klerafistat). All materials are provided for "
        "UK healthcare professionals only.\u00b3"
    )

    add_separator(doc)

    # Section 2 — Resource cards (3 columns)
    add_heading(doc, "Section 2 \u2014 Resource cards (three equal columns)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "cards-teaser")

    doc.add_paragraph()
    add_image_with_caption(doc, "card-prescribing.jpeg", width=Inches(3))
    add_field_value(doc, "Card heading", "Prescribing and monitoring guide")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "Comprehensive guide covering indication, dose escalation, LFT monitoring schedule, "
        "drug interactions, and special populations. Includes a detachable monitoring tracker "
        "for patient records.\u00b3"
    )
    add_field_value(doc, "Card link", "Download prescribing guide \u2192 [PDF link]")

    add_separator(doc)

    add_field_value(doc, "Card heading", "MASH patient identification pathway")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "Non-invasive assessment algorithm for identifying patients with MASH and significant "
        "fibrosis (F2\u2013F3) using FIB-4, ELF, and FibroScan. Designed for use in primary care, "
        "diabetology, and hepatology clinics to streamline referral and treatment initiation.\u2074"
    )
    add_field_value(doc, "Card link", "Download pathway tool \u2192 [PDF link]")

    add_separator(doc)

    add_field_value(doc, "Card heading", "CLARITY clinical data summary")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "Summary of key histological, metabolic, and safety results from CLARITY-FIBROSIS and "
        "CLARITY-RESOLVE, including data tables, response curves, and subgroup analyses by fibrosis "
        "stage and T2D status.\u00b9 \u00b2"
    )
    add_field_value(doc, "Card link", "Download data summary \u2192 [PDF link]")

    add_separator(doc)

    # Section 3 — Contact
    add_heading(doc, "Section 3 \u2014 Contact and medical information (centred text) | light background", level=3, color=BRAND_COLOUR)
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
        "For medical information enquiries about KLERA, please contact AstraZeneca Medical Information: "
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
    add_body(doc, "Title: HCP Resources | KLERA (klerafistat) | MASH Guides & Clinical Data | AstraZeneca UK")
    add_body(doc, "Description: Access prescribing guides, MASH patient identification pathways, CLARITY clinical data summaries, and monitoring tools for KLERA (klerafistat). For UK healthcare professionals only.")

    # =====================================================================
    # 10. FOOTER CONTENT
    # =====================================================================
    doc.add_page_break()
    add_heading(doc, "10. Footer Content", level=1, color=AZ_MAGENTA)

    add_body(doc, "The footer must appear on every page and contain the following elements:", bold=True)

    footer_items = [
        ("Logo", "AstraZeneca logo (linked to /klera/)"),
        ("Approval code", "GB-13402 | DOP: March 2026"),
        ("Copyright", "\u00a9 2026 AstraZeneca. All rights reserved. KLERA is a registered trademark of the AstraZeneca group of companies."),
        ("Page links", "Understanding MASH | CLARITY Data | How KLERA Works | Safety, Dosing & Monitoring | HCP Resources & Support"),
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

    add_body(doc, f"All images sourced from shared CDN: {CDN_BASE}/")
    add_body(doc, (
        "Note: KLERA reuses images originally generated for the VELOX website. "
        "The abstract and lifestyle imagery translates well to the hepatology/metabolic context."
    ), italic=True)

    doc.add_paragraph()
    add_body(doc, "Complete image manifest:", bold=True)
    doc.add_paragraph()

    img_table_rows = []
    for filename, usage in IMAGE_MANIFEST.items():
        cdn_url = f"{CDN_BASE}/{filename}"
        img_table_rows.append((filename, usage, cdn_url))

    add_table(doc, ["Filename", "Usage", "CDN URL"], img_table_rows)

    doc.add_paragraph()

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
