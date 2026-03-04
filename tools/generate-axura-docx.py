#!/usr/bin/env python3
"""Generate DOCX briefing for Axura (axurelimab) — Anti-CD38 monoclonal antibody for SLE.

Reuses images from Velox site (images/velox/).
Different page structure from Velox/Trion: 6 pages with unique layouts.
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
SITE_NAME = "axura"
SOURCE_SITE = "velox"
BRAND_COLOUR = RGBColor(0x00, 0x6D, 0x6F)   # Deep Teal (immunology)
ACCENT_COLOUR = RGBColor(0xEF, 0xAB, 0x00)   # Warm Gold
AZ_MAGENTA = RGBColor(0x83, 0x00, 0x51)
DARK_TEXT = RGBColor(0x36, 0x3B, 0x3B)
GREY_TEXT = RGBColor(0x66, 0x66, 0x66)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
RED_NOTICE = RGBColor(0xCC, 0x00, 0x00)

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(PROJECT_DIR, "images", SOURCE_SITE)
CDN_BASE = f"https://{SOURCE_SITE}-images.pages.dev"
OUTPUT_PATH = os.path.join(PROJECT_DIR, "sites", SITE_NAME, "Axura-Website-Briefing.docx")

# --- Image manifest (velox filename → axura usage context) ---
IMAGE_MANIFEST = {
    "hero-home.jpeg": "Home — hero",
    "hero-efficacy.jpeg": "Living with Lupus — hero",
    "hero-moa.jpeg": "How AXURA Works — hero",
    "card-stroke.jpeg": "Home — SRI-4 response card",
    "card-bleeding.jpeg": "Home — flare reduction card",
    "card-dosing.jpeg": "Home — subcutaneous dosing card",
    "columns-moa-preview.jpeg": "Home — MoA teaser",
    "tab-velocity-af.jpeg": "AURORA Data — AURORA-1 tab",
    "tab-velocity-bleed.jpeg": "AURORA Data — AURORA-LN tab",
    "card-bleeding-events.jpeg": "Safety & Monitoring — infusion/injection reactions card",
    "card-hepatic.jpeg": "Safety & Monitoring — immunoglobulin monitoring card",
    "card-gi-events.jpeg": "Safety & Monitoring — infection risk card",
    "columns-dosing.jpeg": "Dosing & Administration — SC injection at home",
    "columns-monitoring.jpeg": "Safety & Monitoring — monitoring schedule",
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
    run = title.add_run("AXURA\u00ae\u25bc")
    run.font.size = Pt(36)
    run.font.color.rgb = AZ_MAGENTA
    run.bold = True

    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = sub.add_run("(axurelimab)")
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
    run = tagline.add_run("Reclaim your days.")
    run.font.size = Pt(14)
    run.font.color.rgb = BRAND_COLOUR
    run.italic = True

    doc.add_paragraph()

    for line in [
        "Document type: Final approved marketing brief for HCP website build",
        "Prepared by: Marketing \u2014 UK Immunology Franchise",
        "Approval status: MLR-approved copy \u2014 do not modify",
        "Date: March 2026",
        "Approval code: GB-12091 | DOP: March 2026",
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
        "3. Clinical Programme: AURORA",
        "4. Safety Profile",
        "5. Prescribing Information",
        "6. Adverse Event Reporting",
        "7. References",
        "8. Site Navigation",
        "9. Page Content",
        "   Page 1: Home",
        "   Page 2: AURORA Data",
        "   Page 3: Living with Lupus",
        "   Page 4: Safety & Monitoring",
        "   Page 5: How AXURA Works",
        "   Page 6: HCP Resources",
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
        ("Brand name", "AXURA\u00ae\u25bc"),
        ("Generic name", "axurelimab"),
        ("Drug class", "Humanised anti-CD38 monoclonal antibody (IgG1\u03ba)"),
        ("Indication", "Add-on therapy for the treatment of adult patients with active systemic lupus erythematosus (SLE) who are seropositive (anti-dsDNA positive and/or low complement) and have an inadequate response to standard therapy"),
        ("Secondary indication", "Add-on therapy for adult patients with active lupus nephritis (Class III, IV, or V) who are receiving standard immunosuppressive treatment"),
        ("Formulation", "300 mg/2 mL solution for subcutaneous injection in pre-filled syringe"),
        ("Dosing", "300 mg subcutaneous injection once every 2 weeks for the first 3 doses, then 300 mg every 4 weeks"),
        ("Approval", "MHRA \u2014 February 2026"),
        ("Black triangle status", "\u25bc Additional monitoring required"),
        ("Brand colour", "Deep Teal #006D6F"),
        ("Accent colour", "Warm Gold #EFAB00"),
        ("Approval code", "GB-12091"),
    ]
    add_table(doc, ["Field", "Detail"], profile_data)

    doc.add_paragraph()

    brand_notice = doc.add_paragraph()
    run = brand_notice.add_run(
        "AXURA brand rule: AXURA always appears in capitals, with \u00ae\u25bc on first mention per page. "
        "Generic name (axurelimab) appears in lowercase parentheses on first mention. "
        "The black triangle (\u25bc) must accompany AXURA on every first mention. "
        'The approved tagline "Reclaim your days." may only be used verbatim \u2014 no variations permitted.'
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
        "Axurelimab is a humanised IgG1\u03ba monoclonal antibody that binds with high affinity to CD38, "
        "a type II transmembrane glycoprotein highly expressed on long-lived plasma cells, plasmablasts, "
        "and a subset of activated B-cells. CD38 is also expressed on natural killer (NK) cells and "
        "subsets of T-cells, but at lower density."
    ))
    add_body(doc, (
        "In systemic lupus erythematosus, autoreactive long-lived plasma cells residing in bone marrow "
        "and inflamed tissues are the primary source of pathogenic autoantibodies (anti-dsDNA, anti-Smith, "
        "anti-Ro/SSA). These cells are resistant to conventional immunosuppression, B-cell-depleting "
        "therapies (anti-CD20), and belimumab (anti-BAFF), because long-lived plasma cells do not express "
        "CD20 and survive independently of BAFF.\u00b9 \u00b2"
    ))
    add_body(doc, (
        "By targeting CD38, axurelimab depletes the autoantibody-producing cells that drive SLE "
        "through the following mechanisms:"
    ))

    mechanisms = [
        "Antibody-dependent cellular cytotoxicity (ADCC) of CD38-high long-lived plasma cells and plasmablasts",
        "Complement-dependent cytotoxicity (CDC) against CD38-expressing autoantibody-secreting cells",
        "Antibody-dependent cellular phagocytosis (ADCP) by macrophages",
        "Depletion of CD38-high short-lived plasmablasts, reducing the immediate supply of newly secreted autoantibodies",
        "Reduction of CD38-expressing regulatory cell populations is minimal due to lower CD38 density on these cells",
    ]
    for m in mechanisms:
        p = doc.add_paragraph(style='List Bullet')
        run = p.add_run(m)
        run.font.size = Pt(10)

    add_body(doc, (
        "This targeted depletion of autoantibody-secreting cells produces rapid and sustained reductions "
        "in anti-dsDNA titres, normalisation of complement (C3, C4), and consequent reduction in "
        "immune-complex-mediated tissue damage across multiple organ systems. Unlike B-cell depletion "
        "strategies targeting CD20, anti-CD38 therapy directly eliminates the terminally differentiated "
        "cells responsible for autoantibody production.\u00b9 \u00b2 \u2075"
    ))

    add_separator(doc)

    # =================================================================
    # 3. CLINICAL PROGRAMME: AURORA
    # =================================================================
    add_heading(doc, "3. Clinical Programme: AURORA", level=1, color=AZ_MAGENTA)

    # AURORA-1
    add_heading(doc, "AURORA-1 (Phase III, pivotal \u2014 Active SLE)", level=2, color=AZ_MAGENTA)
    for label, val in [
        ("Design", "Randomised, double-blind, placebo-controlled, parallel-group Phase III trial"),
        ("Population", "768 adults with active SLE (SLEDAI-2K \u22656, seropositive: anti-dsDNA \u226530 IU/mL and/or low C3/C4) despite standard of care (antimalarials, corticosteroids \u226410 mg/day prednisolone, and/or immunosuppressants)"),
        ("Duration", "52 weeks on treatment + 12-week safety follow-up"),
        ("Primary endpoint", "SRI-4 response at Week 52 (SLEDAI-2K improvement \u22654 points, no BILAG A flare, no PGA worsening >0.3)"),
        ("Key secondary endpoints", "Time to first severe SLE flare (BILAG A); proportion achieving sustained glucocorticoid reduction to \u22647.5 mg/day prednisolone; anti-dsDNA change from baseline; C3/C4 normalisation; BICLA response at Week 52; FACIT-Fatigue improvement"),
        ("Publication", "Rodriguez-Pintó et al. N Engl J Med 2025; 393(18): 1698\u20131711"),
    ]:
        add_field_value(doc, label, val)

    doc.add_paragraph()
    add_body(doc, "Key results:", bold=True)
    add_table(doc,
        ["Endpoint", "AXURA (n=384)", "Placebo (n=384)", "Treatment effect"],
        [
            ("SRI-4 at Week 52 (primary)",
             "61.7%", "35.9%",
             "\u0394 25.8% (19.2\u201332.4); P<0.001"),
            ("BICLA response at Week 52",
             "54.4%", "30.5%",
             "\u0394 23.9% (17.4\u201330.4); P<0.001"),
            ("Severe flare (BILAG A) through Week 52",
             "8.9%", "21.6%",
             "HR 0.38 (0.25\u20130.57); P<0.001"),
            ("GC reduction to \u22647.5 mg/day (among those on >7.5 mg at baseline)",
             "68.2%", "42.1%",
             "OR 2.93 (1.97\u20134.36); P<0.001"),
            ("Anti-dsDNA reduction at Week 52",
             "\u221264.1%", "\u22128.3%",
             "P<0.001"),
            ("C3 normalisation at Week 52",
             "72.8%", "31.4%",
             "P<0.001"),
            ("FACIT-Fatigue improvement \u22654 points",
             "52.3%", "33.6%",
             "\u0394 18.7% (12.1\u201325.3); P<0.001"),
        ])

    doc.add_paragraph()

    # AURORA-LN
    add_heading(doc, "AURORA-LN (Phase III \u2014 Active lupus nephritis)", level=2, color=AZ_MAGENTA)
    for label, val in [
        ("Design", "Randomised, double-blind, placebo-controlled Phase III trial"),
        ("Population", "354 adults with biopsy-proven active lupus nephritis (Class III, IV, or V, alone or in combination) receiving mycophenolate mofetil (MMF) + low-dose glucocorticoids as background standard of care"),
        ("Duration", "52 weeks on treatment"),
        ("Primary endpoint", "Complete renal response (CRR) at Week 52 (uPCR <0.5 g/g, eGFR within 10% of pre-flare value or \u226590 mL/min/1.73m\u00b2, no rescue therapy)"),
        ("Key secondary endpoints", "Overall renal response (ORR: complete or partial); time to first CRR; uPCR change from baseline; renal flare rate; sustained CRR (Weeks 36\u201352)"),
        ("Publication", "Chen et al. Lancet 2026; 407(10335): 891\u2013904"),
    ]:
        add_field_value(doc, label, val)

    doc.add_paragraph()
    add_body(doc, "Key results:", bold=True)
    add_table(doc,
        ["Endpoint", "AXURA + SoC (n=177)", "Placebo + SoC (n=177)", "Treatment effect"],
        [
            ("CRR at Week 52 (primary)",
             "43.5%", "22.0%",
             "\u0394 21.5% (12.3\u201330.7); P<0.001"),
            ("Overall renal response at Week 52",
             "71.2%", "49.2%",
             "\u0394 22.0% (12.4\u201331.6); P<0.001"),
            ("Sustained CRR (Weeks 36\u201352)",
             "34.5%", "14.7%",
             "\u0394 19.8% (11.2\u201328.4); P<0.001"),
            ("Median time to first CRR",
             "24 weeks", "Not reached",
             "HR 2.14 (1.52\u20133.01); P<0.001"),
            ("Renal flare through Week 52",
             "5.6%", "16.9%",
             "HR 0.31 (0.15\u20130.64); P=0.001"),
            ("uPCR change at Week 52",
             "\u221271.4%", "\u221238.2%",
             "P<0.001"),
        ])

    add_separator(doc)

    # =================================================================
    # 4. SAFETY PROFILE
    # =================================================================
    add_heading(doc, "4. Safety Profile (Pooled AURORA data, N=561 AXURA)", level=1, color=AZ_MAGENTA)

    add_heading(doc, "Most common adverse events (\u22655%)", level=2, color=AZ_MAGENTA)
    add_table(doc,
        ["Adverse event", "AXURA (%)", "Placebo (%)"],
        [
            ("Upper respiratory tract infection", "18.4", "16.2"),
            ("Injection site reactions", "14.8", "3.6"),
            ("Urinary tract infection", "11.2", "9.8"),
            ("Nasopharyngitis", "10.6", "9.4"),
            ("Headache", "8.4", "7.1"),
            ("Diarrhoea", "7.2", "5.8"),
            ("Herpes zoster", "6.8", "2.4"),
            ("Arthralgia", "6.1", "5.4"),
            ("Nausea", "5.6", "4.2"),
            ("Bronchitis", "5.4", "4.1"),
        ])

    doc.add_paragraph()

    add_heading(doc, "Infections", level=2, color=AZ_MAGENTA)
    add_body(doc, (
        "Overall infections occurred in 52.4% of AXURA-treated patients vs 46.8% placebo. Serious "
        "infections occurred in 6.2% vs 5.4%. The most common serious infections were pneumonia (1.4%), "
        "urinary tract infection (0.9%), and herpes zoster (0.7%). No opportunistic infections or cases "
        "of progressive multifocal leukoencephalopathy (PML) were reported. Herpes zoster was more "
        "frequent with AXURA (6.8% vs 2.4%); prophylactic vaccination with recombinant zoster vaccine "
        "is recommended before or during treatment where clinically appropriate.\u00b3"
    ))

    doc.add_paragraph()

    add_heading(doc, "Immunoglobulin levels", level=2, color=AZ_MAGENTA)
    add_body(doc, (
        "As CD38 is expressed on immunoglobulin-secreting plasma cells, reductions in serum immunoglobulin "
        "levels are expected with axurelimab. IgG levels decreased by a median of 18.4% at Week 52 from "
        "baseline. IgG levels below the lower limit of normal (<6.0 g/L) occurred in 12.3% of AXURA-treated "
        "patients vs 3.1% placebo. IgG <4.0 g/L occurred in 2.1%. Monitor serum immunoglobulins (IgG, IgA, "
        "IgM) before initiation, at Week 12, Week 24, and every 6 months thereafter. Consider withholding "
        "treatment if IgG <4.0 g/L with concurrent serious or recurrent infections.\u00b3"
    ))

    doc.add_paragraph()

    add_heading(doc, "Injection site reactions", level=2, color=AZ_MAGENTA)
    add_body(doc, (
        "Injection site reactions (ISRs) occurred in 14.8% of AXURA patients vs 3.6% placebo. Most were "
        "mild (grade 1: erythema, pruritus, swelling) and occurred during the loading phase (first 3 doses). "
        "No ISRs led to treatment discontinuation. ISR frequency decreased with successive injections: "
        "12.1% at dose 1, 6.4% at dose 2, 3.8% at dose 3, and <2% at subsequent doses.\u00b3"
    ))

    doc.add_paragraph()

    add_heading(doc, "Key safety findings", level=2, color=AZ_MAGENTA)
    safety_findings = [
        ("Serious adverse events", "14.1% AXURA vs 13.6% placebo"),
        ("Treatment discontinuation due to AEs", "4.3% vs 3.8%"),
        ("All-cause mortality", "0.4% vs 0.5% (no drug-related deaths)"),
        ("Malignancy", "0.5% vs 0.3% (no signal; all were non-melanoma skin cancer in patients on concomitant immunosuppression)"),
        ("Cytopenias", "Grade \u22653 neutropenia 1.4% vs 0.8%; grade \u22653 thrombocytopenia 0.5% vs 0.3%. Monitor FBC at baseline and periodically\u00b3"),
        ("Hepatitis B reactivation", "No cases reported; however, screen for HBV before initiation and do not initiate in active HBV infection\u00b3"),
        ("Immunogenicity", "Treatment-emergent ADAs in 3.6%; neutralising antibodies in 0.9%. No clinically meaningful impact on PK, efficacy, or safety\u00b3"),
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
        "Elderly (\u226565 years): Limited data (5% of AURORA-1 population). No dose adjustment required. Use with caution given increased baseline infection risk.\u00b3",
        "Renal impairment: No dose adjustment required. AURORA-LN enrolled patients with eGFR \u226530 mL/min/1.73m\u00b2. Not studied in eGFR <30.\u00b3",
        "Hepatic impairment: Not studied in moderate or severe hepatic impairment. No dose adjustment for mild impairment.\u00b3",
        "Pregnancy and lactation: Axurelimab is a monoclonal antibody and is expected to cross the placental barrier during the second and third trimesters. No adequate data in pregnant women. Women of childbearing potential should use effective contraception during treatment and for 6 months after the last dose. Not recommended during breastfeeding.\u00b3",
        "Vaccinations: Complete all vaccinations, including recombinant zoster vaccine, before initiating axurelimab where possible. Avoid live vaccines during treatment and for 6 months after the last dose.\u00b3",
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
        "AXURA\u25bc (axurelimab) 300 mg/2 mL solution for subcutaneous injection in pre-filled syringe. "
        "Please refer to the Summary of Product Characteristics (SmPC) before prescribing. "
        "Indication: Add-on therapy for the treatment of adult patients with active systemic lupus "
        "erythematosus (SLE) who are seropositive (anti-dsDNA positive and/or low complement) and have "
        "an inadequate response to standard therapy. Also indicated as add-on therapy for active lupus "
        "nephritis (Class III, IV, or V) receiving standard immunosuppressive treatment. "
        "Dosage and administration: 300 mg SC every 2 weeks for the first 3 doses (loading), then "
        "300 mg SC every 4 weeks (maintenance). Administer into the thigh, abdomen (excluding 5 cm "
        "around the navel), or upper arm. Rotate injection sites. "
        "Contraindications: Hypersensitivity to axurelimab or excipients; active severe infections; "
        "active hepatitis B infection. "
        "Warnings and precautions: Infections: Do not initiate during active infections. Screen for "
        "TB and HBV before initiation. Vaccinate against herpes zoster where possible. "
        "Immunoglobulins: Monitor IgG, IgA, IgM before initiation and regularly during treatment. "
        "Consider withholding if IgG <4.0 g/L with recurrent serious infections. Live vaccines: "
        "Avoid during treatment and for 6 months after last dose. "
        "Side effects: Very common (\u22651/10): upper respiratory tract infection, injection site reactions, "
        "UTI, nasopharyngitis. Common (\u22651/100 to <1/10): herpes zoster, headache, diarrhoea, nausea, "
        "arthralgia, bronchitis, IgG decrease. "
        "Legal category: POM. Pack and price: 1 pre-filled syringe (300 mg): \u00a3872.00. "
        "Marketing authorisation holder: AstraZeneca UK Ltd. MA number: PLGB 17901/0741. "
        "Full prescribing information available from: AstraZeneca UK Ltd, 2 Pancras Square, London N1C 4AG. "
        "GB-12091 | DOP: March 2026."
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
        "Rodriguez-Pint\u00f3 et al. N Engl J Med 2025; 393(18): 1698\u20131711.",
        "Chen et al. Lancet 2026; 407(10335): 891\u2013904.",
        "AXURA (axurelimab) Summary of Product Characteristics. AstraZeneca UK Ltd. February 2026.",
        "Ostendorf L, et al. Ann Rheum Dis 2023; 82(9): 1162\u20131170.",
        "Alexander T, et al. N Engl J Med 2023; 388(15): 1385\u20131395.",
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
        ("Main navigation pages", "AURORA Data | Living with Lupus | Safety & Monitoring | How AXURA Works | HCP Resources"),
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
        'AXURA brand rule: AXURA always appears in capitals, with \u00ae\u25bc on first mention per page. '
        'Generic name (axurelimab) in lowercase parentheses on first mention. '
        'Black triangle (\u25bc) mandatory on every first mention. '
        'Tagline "Reclaim your days." verbatim only.'
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
    add_field_value(doc, "URL path", "/axura/")
    add_separator(doc)

    # Section 1 — Hero
    add_heading(doc, "Section 1 \u2014 Hero (full-width image with text overlay)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "hero-teaser")
    doc.add_paragraph()
    add_image_with_caption(doc, "hero-home.jpeg", width=Inches(5.5))

    add_field_value(doc, "Heading", "AXURA\u00ae\u25bc (axurelimab)")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "The first anti-CD38 therapy for systemic lupus erythematosus. Targeting the source of "
        "pathogenic autoantibodies for rapid, sustained disease control. Reclaim your days.\u00b9"
    )
    add_field_value(doc, "Call to action", "Explore the AURORA data \u2192 /axura/aurora-data")

    add_separator(doc)

    # Section 2 — Key benefit cards
    add_heading(doc, "Section 2 \u2014 Three key benefit cards (equal columns)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "cards-teaser")

    # Card 1 — SRI-4
    doc.add_paragraph()
    add_image_with_caption(doc, "card-stroke.jpeg", width=Inches(3))
    add_field_value(doc, "Card heading", "62% SRI-4 response at one year")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "In AURORA-1, 61.7% of patients achieved an SRI-4 response at Week 52 with AXURA versus "
        "35.9% with placebo (\u0394 25.8%; P<0.001), demonstrating clinically meaningful disease "
        "control across multiple organ domains.\u00b9"
    )
    add_field_value(doc, "Card link", "View AURORA data \u2192 /axura/aurora-data")

    add_separator(doc)

    # Card 2 — Flare
    add_image_with_caption(doc, "card-bleeding.jpeg", width=Inches(3))
    add_field_value(doc, "Card heading", "62% reduction in severe flares")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "AXURA reduced the risk of severe SLE flares (BILAG A) by 62% versus placebo through "
        "Week 52 (HR 0.38; P<0.001). Only 8.9% of AXURA-treated patients experienced a severe "
        "flare, compared with 21.6% receiving placebo.\u00b9"
    )
    add_field_value(doc, "Card link", "Explore flare reduction data \u2192 /axura/aurora-data")

    add_separator(doc)

    # Card 3 — SC dosing
    add_image_with_caption(doc, "card-dosing.jpeg", width=Inches(3))
    add_field_value(doc, "Card heading", "Subcutaneous self-injection every 4 weeks")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "After a brief loading phase (3 fortnightly doses), AXURA is administered as a single "
        "subcutaneous injection every 4 weeks. Patients can self-inject at home after appropriate "
        "training, supporting treatment convenience and autonomy.\u00b3"
    )
    add_field_value(doc, "Card link", "View dosing information \u2192 /axura/safety-monitoring")

    add_separator(doc)

    # Section 3 — Two-column: lupus context + MoA teaser
    add_heading(doc, "Section 3 \u2014 MoA teaser (two-column: image left, text right) | highlight background", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "columns-teaser")
    p = doc.add_paragraph()
    run = p.add_run("Section metadata: ")
    run.bold = True
    p.add_run("Style: highlight").font.color.rgb = GREY_TEXT

    doc.add_paragraph()
    add_image_with_caption(doc, "columns-moa-preview.jpeg", width=Inches(3.5))

    add_field_value(doc, "Heading", "Targeting the source: CD38 and the long-lived plasma cell")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Long-lived plasma cells are the primary source of pathogenic autoantibodies in SLE, yet they "
        "are resistant to conventional immunosuppression and B-cell depletion. AXURA targets CD38 \u2014 "
        "highly expressed on these cells \u2014 to deplete the autoantibody factory at its origin.\u00b3 \u2075"
    )
    add_field_value(doc, "Call to action", "Explore how AXURA works \u2192 /axura/how-axura-works")

    add_separator(doc)

    # Section 4 — Accordion
    add_heading(doc, "Section 4 \u2014 Prescribing information footer", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "accordion")
    add_body(doc, "Expandable sections for: Prescribing Information | Adverse Event Reporting | References (Use approved text from sections 5, 6, and 7 above)", italic=True)

    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run("Page metadata")
    run.bold = True
    run.font.color.rgb = AZ_MAGENTA
    add_body(doc, "Title: AXURA (axurelimab) | Anti-CD38 Therapy for SLE | AstraZeneca UK")
    add_body(doc, "Description: AXURA (axurelimab) is a first-in-class anti-CD38 monoclonal antibody for active systemic lupus erythematosus and lupus nephritis. Explore AURORA clinical data, safety, and dosing for UK healthcare professionals.")

    # =====================================================================
    # PAGE 2: AURORA DATA
    # =====================================================================
    doc.add_page_break()
    add_heading(doc, "PAGE 2: AURORA Data", level=2, color=AZ_MAGENTA)
    add_field_value(doc, "URL path", "/axura/aurora-data")
    add_separator(doc)

    # Section 1 — Introduction (no hero — different structure from Velox/Trion)
    add_heading(doc, "Section 1 \u2014 Page introduction (centred text, no image)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "title")

    add_field_value(doc, "Heading", "The AURORA clinical programme")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "AXURA\u00ae\u25bc (axurelimab) was evaluated in two Phase III trials encompassing the two major "
        "clinical presentations of lupus: systemic disease (AURORA-1) and renal involvement "
        "(AURORA-LN).\u00b9 \u00b2"
    )

    add_separator(doc)

    # Section 2 — Biomarker carousel (NEW STRUCTURE — carousel block)
    add_heading(doc, "Section 2 \u2014 Biomarker response carousel (3 slides) | light background", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "carousel-teaser")
    p = doc.add_paragraph()
    run = p.add_run("Section metadata: ")
    run.bold = True
    p.add_run("Style: light").font.color.rgb = GREY_TEXT

    add_body(doc, "Slide 1:", bold=True)
    add_field_value(doc, "Heading", "64% reduction in anti-dsDNA antibodies at Week 52")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "AXURA produced a median 64.1% reduction in anti-dsDNA titres from baseline at Week 52, "
        "compared with 8.3% in the placebo group (P<0.001). Rapid reductions were observed from "
        "Week 4, consistent with depletion of autoantibody-secreting plasma cells.\u00b9"
    )

    add_body(doc, "Slide 2:", bold=True)
    add_field_value(doc, "Heading", "73% of patients achieved complement normalisation")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "C3 normalisation was achieved in 72.8% of AXURA-treated patients with low baseline C3, "
        "compared with 31.4% with placebo (P<0.001). Complement recovery correlated with clinical "
        "response and reduced flare risk.\u00b9"
    )

    add_body(doc, "Slide 3:", bold=True)
    add_field_value(doc, "Heading", "68% achieved glucocorticoid reduction to \u22647.5 mg/day")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Among patients receiving >7.5 mg/day prednisolone at baseline, 68.2% of AXURA patients "
        "achieved sustained dose reduction to \u22647.5 mg/day by Week 52, versus 42.1% with placebo "
        "(OR 2.93; P<0.001) \u2014 reducing cumulative steroid burden.\u00b9"
    )

    add_separator(doc)

    # Section 3 — Tabs
    add_heading(doc, "Section 3 \u2014 Clinical data (two tabs)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "tabs-large")

    # Tab 1 — AURORA-1
    doc.add_paragraph()
    add_body(doc, 'Tab 1: "AURORA-1: Systemic SLE"', bold=True)
    add_image_with_caption(doc, "tab-velocity-af.jpeg", width=Inches(3.5))

    add_field_value(doc, "Heading", "AURORA-1: Clinically meaningful disease control across organ systems")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "AURORA-1 was a randomised, double-blind, placebo-controlled trial in 768 adults with active "
        "seropositive SLE (SLEDAI-2K \u22656) despite standard of care. AXURA achieved the primary "
        "endpoint of SRI-4 response at Week 52 in 61.7% vs 35.9% (\u0394 25.8%; P<0.001). BICLA "
        "response was achieved in 54.4% vs 30.5% (P<0.001). Severe flares (BILAG A) were reduced "
        "by 62% (HR 0.38; P<0.001). Notably, clinical response was accompanied by rapid and "
        "sustained normalisation of serological biomarkers (anti-dsDNA, complement), supporting "
        "a disease-modifying rather than purely symptomatic mechanism.\u00b9"
    )

    add_body(doc, "Data table:", bold=True)
    add_table(doc,
        ["Endpoint", "AXURA (n=384)", "Placebo (n=384)", "Treatment effect"],
        [
            ("SRI-4 at Week 52", "61.7%", "35.9%", "\u0394 25.8%; P<0.001"),
            ("BICLA at Week 52", "54.4%", "30.5%", "\u0394 23.9%; P<0.001"),
            ("Severe flare (BILAG A)", "8.9%", "21.6%", "HR 0.38; P<0.001"),
            ("GC \u22647.5 mg/day", "68.2%", "42.1%", "OR 2.93; P<0.001"),
            ("Anti-dsDNA reduction", "\u221264.1%", "\u22128.3%", "P<0.001"),
        ])

    add_separator(doc)

    # Tab 2 — AURORA-LN
    add_body(doc, 'Tab 2: "AURORA-LN: Lupus nephritis"', bold=True)
    add_image_with_caption(doc, "tab-velocity-bleed.jpeg", width=Inches(3.5))

    add_field_value(doc, "Heading", "AURORA-LN: Doubling the rate of complete renal response")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "AURORA-LN was a randomised, double-blind, placebo-controlled trial in 354 adults with biopsy-proven "
        "active lupus nephritis (Class III, IV, or V) on background MMF + glucocorticoids. AXURA nearly "
        "doubled the rate of complete renal response at Week 52: 43.5% vs 22.0% (\u0394 21.5%; P<0.001). "
        "The overall renal response rate was 71.2% vs 49.2% (P<0.001). Renal flares were reduced by 69% "
        "(HR 0.31; P=0.001). Proteinuria (uPCR) decreased by 71.4% with AXURA vs 38.2% with placebo.\u00b2"
    )

    add_body(doc, "Data table:", bold=True)
    add_table(doc,
        ["Endpoint", "AXURA + SoC (n=177)", "Placebo + SoC (n=177)", "Effect"],
        [
            ("CRR at Week 52", "43.5%", "22.0%", "\u0394 21.5%; P<0.001"),
            ("Overall renal response", "71.2%", "49.2%", "\u0394 22.0%; P<0.001"),
            ("Sustained CRR (Wk 36\u201352)", "34.5%", "14.7%", "\u0394 19.8%; P<0.001"),
            ("Renal flare", "5.6%", "16.9%", "HR 0.31; P=0.001"),
            ("uPCR change", "\u221271.4%", "\u221238.2%", "P<0.001"),
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
    add_body(doc, "Title: AURORA Data | AXURA (axurelimab) | SLE & Lupus Nephritis Results | AstraZeneca UK")
    add_body(doc, "Description: Explore the AURORA clinical programme for AXURA (axurelimab) \u2014 Phase III SRI-4 response in active SLE and complete renal response in lupus nephritis.")

    # =====================================================================
    # PAGE 3: LIVING WITH LUPUS (NEW — patient-centred disease awareness page)
    # =====================================================================
    doc.add_page_break()
    add_heading(doc, "PAGE 3: Living with Lupus", level=2, color=AZ_MAGENTA)
    add_field_value(doc, "URL path", "/axura/living-with-lupus")
    add_separator(doc)

    # Hero
    add_heading(doc, "Section 1 \u2014 Hero (full-width image with text overlay)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "hero-teaser")
    doc.add_paragraph()
    add_image_with_caption(doc, "hero-efficacy.jpeg", width=Inches(5.5))

    add_field_value(doc, "Heading", "Understanding the burden of SLE")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Systemic lupus erythematosus is a chronic, relapsing autoimmune disease that can affect "
        "virtually every organ system. For many patients, the unpredictable cycle of flares and "
        "the cumulative toxicity of long-term corticosteroids define their experience of living "
        "with lupus.\u2074"
    )

    add_separator(doc)

    # Section 2 — Disease burden carousel (DIFFERENT from AURORA page)
    add_heading(doc, "Section 2 \u2014 Disease burden (3-column cards)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "cards-teaser")

    add_image_with_caption(doc, "card-bleeding-events.jpeg", width=Inches(3))
    add_field_value(doc, "Card heading", "The flare cycle")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "Up to 65% of SLE patients experience at least one flare per year despite standard therapy. "
        "Severe flares (BILAG A) require hospitalisation, high-dose corticosteroids, or "
        "cyclophosphamide, and are associated with irreversible organ damage accumulation.\u2074"
    )

    add_separator(doc)

    add_image_with_caption(doc, "card-hepatic.jpeg", width=Inches(3))
    add_field_value(doc, "Card heading", "Steroid burden")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "Over 50% of SLE patients require chronic glucocorticoids. Cumulative steroid exposure drives "
        "organ damage (osteoporosis, avascular necrosis, diabetes, cataracts, cardiovascular disease) "
        "independently of lupus activity, creating a therapeutic dilemma.\u2074"
    )

    add_separator(doc)

    add_image_with_caption(doc, "card-gi-events.jpeg", width=Inches(3))
    add_field_value(doc, "Card heading", "Lupus nephritis")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "Up to 50% of SLE patients develop lupus nephritis during their disease course. Despite "
        "standard immunosuppression, only 20\u201330% achieve complete renal response at one year, "
        "and up to 20% progress to end-stage renal disease within 10 years.\u2074"
    )

    add_separator(doc)

    # Section 3 — Unmet need (columns-teaser)
    add_heading(doc, "Section 3 \u2014 Autoantibody context (two-column: image left, text right) | light background", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "columns-teaser")
    p = doc.add_paragraph()
    run = p.add_run("Section metadata: ")
    run.bold = True
    p.add_run("Style: light").font.color.rgb = GREY_TEXT

    doc.add_paragraph()
    add_image_with_caption(doc, "columns-monitoring.jpeg", width=Inches(3.5))

    add_field_value(doc, "Heading", "Why autoantibodies persist despite treatment")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Long-lived plasma cells in the bone marrow continuously secrete pathogenic autoantibodies "
        "(anti-dsDNA, anti-Smith, anti-C1q) that drive immune-complex deposition and complement "
        "activation across multiple organ systems. These cells are resistant to conventional "
        "immunosuppressants and anti-CD20 B-cell depletion because they are terminally differentiated "
        "and survive independently of B-cell survival signals (BAFF). Targeting CD38 \u2014 a surface "
        "marker highly expressed on long-lived plasma cells \u2014 offers a direct route to eliminating "
        "the autoantibody source.\u2074 \u2075"
    )
    add_field_value(doc, "Call to action", "Explore how AXURA works \u2192 /axura/how-axura-works")

    add_separator(doc)

    # Section 4 — Fatigue impact (introduction block)
    add_heading(doc, "Section 4 \u2014 Fatigue and quality of life (centred text) | highlight background", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "introduction")
    p = doc.add_paragraph()
    run = p.add_run("Section metadata: ")
    run.bold = True
    p.add_run("Style: highlight").font.color.rgb = GREY_TEXT

    add_field_value(doc, "Heading", "Fatigue: the invisible burden of lupus")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Fatigue is the most commonly reported symptom in SLE, affecting over 80% of patients and "
        "frequently rated as the most disabling aspect of the disease. In AURORA-1, 52.3% of AXURA "
        "patients reported clinically meaningful improvement in FACIT-Fatigue (\u22654-point increase) "
        "at Week 52, compared with 33.6% with placebo (\u0394 18.7%; P<0.001) \u2014 reflecting the "
        "systemic impact of reducing autoantibody-mediated inflammation.\u00b9"
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
    add_body(doc, "Title: Living with Lupus | Disease Burden & Unmet Need | AXURA | AstraZeneca UK")
    add_body(doc, "Description: Understand the burden of systemic lupus erythematosus \u2014 the flare cycle, steroid toxicity, lupus nephritis, and the persistent role of autoantibodies in driving disease activity.")

    # =====================================================================
    # PAGE 4: SAFETY & MONITORING (combined — different from separate pages)
    # =====================================================================
    doc.add_page_break()
    add_heading(doc, "PAGE 4: Safety & Monitoring", level=2, color=AZ_MAGENTA)
    add_field_value(doc, "URL path", "/axura/safety-monitoring")
    add_separator(doc)

    # Section 1 — Title
    add_heading(doc, "Section 1 \u2014 Page header (text only, no image)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "title")
    add_field_value(doc, "Heading", "Safety, monitoring, and dosing")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "AXURA\u00ae\u25bc (axurelimab) has been evaluated in 561 patients across the AURORA clinical "
        "programme. Subcutaneous dosing with regular immunoglobulin monitoring supports safe, "
        "convenient long-term treatment.\u00b9 \u00b2 \u00b3"
    )

    add_separator(doc)

    # Section 2 — Dosing detail (columns-teaser)
    add_heading(doc, "Section 2 \u2014 Dosing regimen (two-column: image left, text right) | highlight background", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "columns-teaser")
    p = doc.add_paragraph()
    run = p.add_run("Section metadata: ")
    run.bold = True
    p.add_run("Style: highlight").font.color.rgb = GREY_TEXT

    doc.add_paragraph()
    add_image_with_caption(doc, "columns-dosing.jpeg", width=Inches(3.5))

    add_field_value(doc, "Heading", "Loading and maintenance dosing")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Loading phase: AXURA 300 mg subcutaneous injection every 2 weeks for the first 3 doses "
        "(Weeks 0, 2, and 4). Maintenance phase: 300 mg subcutaneous injection every 4 weeks "
        "thereafter. Administer into the thigh, abdomen (excluding 5 cm around the navel), or "
        "upper arm (if administered by a caregiver). Rotate injection sites. Patients may "
        "self-inject at home after appropriate training by a healthcare professional.\u00b3"
    )

    add_separator(doc)

    # Section 3 — Safety cards (3 columns)
    add_heading(doc, "Section 3 \u2014 Key safety considerations (three equal columns)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "cards-teaser")

    doc.add_paragraph()
    add_image_with_caption(doc, "card-bleeding-events.jpeg", width=Inches(3))
    add_field_value(doc, "Card heading", "Injection site reactions")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "ISRs occurred in 14.8% of AXURA patients (most grade 1: erythema, pruritus). Frequency "
        "decreased with successive doses: 12.1% at dose 1 to <2% at doses \u22654. No ISR led to "
        "discontinuation. Pre-treatment with paracetamol or antihistamine is not routinely required.\u00b3"
    )

    add_separator(doc)

    add_image_with_caption(doc, "card-hepatic.jpeg", width=Inches(3))
    add_field_value(doc, "Card heading", "Immunoglobulin monitoring")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "IgG levels decrease by ~18% at Week 52 (expected pharmacological effect). IgG <6.0 g/L "
        "in 12.3% of patients; IgG <4.0 g/L in 2.1%. Monitor IgG, IgA, IgM at baseline, Week 12, "
        "Week 24, and every 6 months. Consider withholding if IgG <4.0 g/L with concurrent "
        "serious or recurrent infections.\u00b3"
    )

    add_separator(doc)

    add_image_with_caption(doc, "card-gi-events.jpeg", width=Inches(3))
    add_field_value(doc, "Card heading", "Infection risk")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "Serious infections: 6.2% vs 5.4% placebo. Herpes zoster: 6.8% vs 2.4%. Recommend "
        "recombinant zoster vaccination before or during treatment. Screen for TB and HBV before "
        "initiation. Do not initiate during active infections. No opportunistic infections or PML "
        "cases were observed.\u00b3"
    )

    add_separator(doc)

    # Section 4 — Monitoring schedule (table-data block — UNIQUE to this page)
    add_heading(doc, "Section 4 \u2014 Monitoring schedule table | light background", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "table-data")
    p = doc.add_paragraph()
    run = p.add_run("Section metadata: ")
    run.bold = True
    p.add_run("Style: light").font.color.rgb = GREY_TEXT

    add_field_value(doc, "Heading", "Recommended monitoring schedule")
    add_table(doc,
        ["Assessment", "Baseline", "Week 12", "Week 24", "Every 6 months", "As indicated"],
        [
            ("Immunoglobulins (IgG, IgA, IgM)", "\u2713", "\u2713", "\u2713", "\u2713", "\u2713"),
            ("Full blood count", "\u2713", "\u2713", "", "\u2713", "\u2713"),
            ("Renal function (eGFR, uPCR)", "\u2713", "\u2713", "\u2713", "\u2713", "\u2713"),
            ("Hepatitis B screening", "\u2713", "", "", "", ""),
            ("TB screening", "\u2713", "", "", "", ""),
            ("Complement (C3, C4)", "\u2713", "\u2713", "\u2713", "\u2713", ""),
            ("Anti-dsDNA titre", "\u2713", "\u2713", "\u2713", "\u2713", ""),
            ("Vaccination status", "\u2713", "", "", "", ""),
        ])

    add_separator(doc)

    # Section 5 — Monitoring image + switching guidance
    add_heading(doc, "Section 5 \u2014 Practical considerations (two-column: image left, text right)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "columns-teaser")

    doc.add_paragraph()
    add_image_with_caption(doc, "columns-monitoring.jpeg", width=Inches(3.5))

    add_field_value(doc, "Heading", "Pre-treatment checklist and vaccination guidance")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Before initiating AXURA: Complete all age-appropriate vaccinations, including recombinant "
        "zoster vaccine (Shingrix) where possible. Screen for active infections, TB (interferon-gamma "
        "release assay or tuberculin skin test), and hepatitis B (HBsAg, anti-HBc, HBV DNA if "
        "positive). Assess baseline immunoglobulins, FBC, renal function, and complement/anti-dsDNA. "
        "Ensure effective contraception in women of childbearing potential. AXURA may be initiated "
        "alongside existing standard of care (antimalarials, immunosuppressants, low-dose "
        "glucocorticoids) without washout.\u00b3"
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
    add_body(doc, "Title: Safety & Monitoring | AXURA (axurelimab) | Dosing, ISRs, Immunoglobulins | AstraZeneca UK")
    add_body(doc, "Description: AXURA (axurelimab) safety profile, dosing regimen, monitoring schedule, and practical guidance for UK healthcare professionals managing SLE and lupus nephritis.")

    # =====================================================================
    # PAGE 5: HOW AXURA WORKS
    # =====================================================================
    doc.add_page_break()
    add_heading(doc, "PAGE 5: How AXURA Works", level=2, color=AZ_MAGENTA)
    add_field_value(doc, "URL path", "/axura/how-axura-works")
    add_separator(doc)

    # Hero
    add_heading(doc, "Section 1 \u2014 Hero (full-width image with text overlay)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "hero-teaser")
    doc.add_paragraph()
    add_image_with_caption(doc, "hero-moa.jpeg", width=Inches(5.5))

    add_field_value(doc, "Heading", "How AXURA works")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "AXURA\u00ae\u25bc (axurelimab) targets CD38 to deplete the autoantibody-secreting cells that "
        "conventional therapies cannot reach \u2014 a fundamentally different approach to treating the "
        "root cause of SLE.\u00b3 \u2075"
    )

    add_separator(doc)

    # Section 2 — Autoimmunity context (accordion-based FAQ — UNIQUE structure)
    add_heading(doc, "Section 2 \u2014 Three-step mechanism (accordion FAQ)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "accordion")

    add_body(doc, 'Panel 1: "Why do current therapies leave autoantibodies unchecked?"', bold=True)
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Conventional immunosuppressants (azathioprine, MMF, cyclophosphamide) suppress active immune "
        "cell proliferation but do not deplete terminally differentiated long-lived plasma cells. "
        "Anti-CD20 therapies (rituximab) deplete B-cells but spare plasma cells, which lack CD20 "
        "expression. Anti-BAFF therapies (belimumab) block B-cell survival signals but long-lived "
        "plasma cells survive independently of BAFF. The result: pathogenic autoantibodies persist "
        "even during apparent clinical remission, driving subclinical inflammation and damage "
        "accrual.\u2074 \u2075"
    )

    add_body(doc, 'Panel 2: "How does AXURA target autoantibody-producing cells?"', bold=True)
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "CD38 is a transmembrane glycoprotein highly expressed on long-lived plasma cells and "
        "plasmablasts \u2014 the cells directly responsible for secreting pathogenic autoantibodies. "
        "Axurelimab binds to CD38 and eliminates these cells through ADCC, CDC, and ADCP. Unlike "
        "CD20 or BAFF-targeted therapies, anti-CD38 directly reaches the terminally differentiated "
        "compartment responsible for autoantibody production.\u00b3 \u2075"
    )

    add_body(doc, 'Panel 3: "What happens after plasma cell depletion?"', bold=True)
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Depletion of CD38-high autoantibody-secreting cells produces rapid reductions in pathogenic "
        "autoantibody titres (anti-dsDNA decreased by 64% at Week 52). Downstream, reduced "
        "immune-complex formation leads to complement recovery (C3 normalisation in 73% of patients), "
        "decreased tissue inflammation, and reduced organ damage accrual. Protective immunoglobulin "
        "levels are maintained in the majority of patients because memory B-cells and newly generated "
        "non-autoreactive plasma cells replenish the normal antibody repertoire.\u00b9 \u00b3"
    )

    add_separator(doc)

    # Section 3 — Visual MoA (columns-teaser)
    add_heading(doc, "Section 3 \u2014 Visual mechanism (two-column: image left, text right) | highlight background", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "columns-teaser")
    p = doc.add_paragraph()
    run = p.add_run("Section metadata: ")
    run.bold = True
    p.add_run("Style: highlight").font.color.rgb = GREY_TEXT

    doc.add_paragraph()
    add_image_with_caption(doc, "columns-moa-preview.jpeg", width=Inches(3.5))

    add_field_value(doc, "Heading", "From plasma cell depletion to clinical remission")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "AXURA depletes CD38-high long-lived plasma cells and plasmablasts \u2192 pathogenic autoantibody "
        "titres fall rapidly (anti-dsDNA \u221264% at Week 52) \u2192 immune-complex formation decreases "
        "\u2192 complement consumption reverses (C3 normalisation 73%) \u2192 tissue inflammation resolves "
        "\u2192 clinical response (SRI-4 62%, severe flare reduction 62%). This mechanistic cascade "
        "provides a disease-modifying rationale for anti-CD38 therapy in SLE.\u00b9 \u00b3 \u2075"
    )
    add_field_value(doc, "Call to action", "View the AURORA clinical data \u2192 /axura/aurora-data")

    add_separator(doc)

    # Accordion + metadata
    add_heading(doc, "Section 4 \u2014 Prescribing information footer", level=3, color=BRAND_COLOUR)
    add_body(doc, "Block: accordion  |  Expandable: PI | AE Reporting | References", italic=True)

    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run("Page metadata")
    run.bold = True
    run.font.color.rgb = AZ_MAGENTA
    add_body(doc, "Title: How AXURA Works | Anti-CD38 Mechanism | Plasma Cell Depletion | AstraZeneca UK")
    add_body(doc, "Description: Understand how AXURA (axurelimab) targets CD38 on long-lived plasma cells to deplete pathogenic autoantibodies and achieve disease control in systemic lupus erythematosus.")

    # =====================================================================
    # PAGE 6: HCP RESOURCES
    # =====================================================================
    doc.add_page_break()
    add_heading(doc, "PAGE 6: HCP Resources", level=2, color=AZ_MAGENTA)
    add_field_value(doc, "URL path", "/axura/resources")
    add_separator(doc)

    # Section 1 — Title
    add_heading(doc, "Section 1 \u2014 Page header (text only, no image)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "title")
    add_field_value(doc, "Heading", "Resources for healthcare professionals")
    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Access prescribing information, monitoring guides, clinical data summaries, and patient "
        "support resources for AXURA\u00ae\u25bc (axurelimab). All materials are provided for UK "
        "healthcare professionals only.\u00b3"
    )

    add_separator(doc)

    # Section 2 — Resource cards
    add_heading(doc, "Section 2 \u2014 Resource cards (three equal columns)", level=3, color=BRAND_COLOUR)
    add_field_value(doc, "Block", "cards-teaser")

    doc.add_paragraph()
    add_image_with_caption(doc, "card-prescribing.jpeg", width=Inches(3))
    add_field_value(doc, "Card heading", "Prescribing and monitoring guide")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "Comprehensive clinical guide covering indication, dosing regimen, immunoglobulin monitoring "
        "schedule, injection site rotation, vaccination requirements, and special populations guidance. "
        "Includes a detachable monitoring checklist for patient notes.\u00b3"
    )
    add_field_value(doc, "Card link", "Download prescribing guide \u2192 [PDF link]")

    add_separator(doc)

    add_field_value(doc, "Card heading", "AURORA clinical data summary")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "Summary of key efficacy and safety data from AURORA-1 and AURORA-LN, including headline "
        "results, response curves, biomarker kinetics, and subgroup analyses. Suitable for use in "
        "MDT discussions and clinic preparation.\u00b9 \u00b2"
    )
    add_field_value(doc, "Card link", "Download data summary \u2192 [PDF link]")

    add_separator(doc)

    add_field_value(doc, "Card heading", "Patient self-injection training guide")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "Step-by-step illustrated guide for training patients in subcutaneous self-injection with "
        "AXURA pre-filled syringe. Covers preparation, site selection, technique, storage, and "
        "sharps disposal. Includes a companion patient-facing leaflet."
    )
    add_field_value(doc, "Card link", "Download training guide \u2192 [PDF link]")

    add_separator(doc)

    # Section 3 — Contact
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
        "For medical information enquiries about AXURA, please contact AstraZeneca Medical Information: "
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
    add_body(doc, "Title: HCP Resources | AXURA (axurelimab) | Prescribing & Monitoring Guides | AstraZeneca UK")
    add_body(doc, "Description: Access prescribing and monitoring guides, AURORA clinical data summaries, and patient self-injection training materials for AXURA (axurelimab). For UK healthcare professionals only.")

    # =====================================================================
    # 10. FOOTER CONTENT
    # =====================================================================
    doc.add_page_break()
    add_heading(doc, "10. Footer Content", level=1, color=AZ_MAGENTA)

    add_body(doc, "The footer must appear on every page and contain the following elements:", bold=True)

    footer_items = [
        ("Logo", "AstraZeneca logo (linked to /axura/)"),
        ("Approval code", "GB-12091 | DOP: March 2026"),
        ("Copyright", "\u00a9 2026 AstraZeneca. All rights reserved. AXURA is a registered trademark of the AstraZeneca group of companies."),
        ("Page links", "AURORA Data | Living with Lupus | Safety & Monitoring | How AXURA Works | HCP Resources"),
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
        "Note: AXURA reuses images originally generated for the VELOX website. "
        "The abstract and lifestyle imagery is versatile across immunology contexts."
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
