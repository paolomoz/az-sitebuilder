#!/usr/bin/env python3
"""Generate DOCX briefing for Lumivex (lumvecitinib) — Selective TYK2 inhibitor for plaque psoriasis."""

import os
import sys
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml

# --- Configuration ---
SITE_NAME = "lumivex"
BRAND_COLOUR = RGBColor(0xD4, 0x85, 0x1F)  # Luminous Amber
AZ_MAGENTA = RGBColor(0x83, 0x00, 0x51)
DARK_TEXT = RGBColor(0x36, 0x3B, 0x3B)
GREY_TEXT = RGBColor(0x66, 0x66, 0x66)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
CDN_BASE = f"https://{SITE_NAME}-images.pages.dev"

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(PROJECT_DIR, "images", SITE_NAME)
OUTPUT_PATH = os.path.join(PROJECT_DIR, "sites", SITE_NAME, "Lumivex-Website-Briefing.docx")


def set_cell_shading(cell, color_hex):
    """Set cell background colour."""
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading)


def add_heading(doc, text, level=1, color=None):
    """Add a styled heading."""
    h = doc.add_heading(text, level=level)
    if color:
        for run in h.runs:
            run.font.color.rgb = color
    return h


def add_body(doc, text, bold=False, italic=False, size=Pt(10)):
    """Add body paragraph."""
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.size = size
    run.font.color.rgb = DARK_TEXT
    run.bold = bold
    run.italic = italic
    return p


def add_image_with_caption(doc, filename, caption, width=Inches(4.5)):
    """Add image with CDN URL caption. Falls back to placeholder if image not found."""
    img_path = os.path.join(IMG_DIR, filename)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if os.path.isfile(img_path) and os.path.getsize(img_path) > 1000:
        run = p.add_run()
        run.add_picture(img_path, width=width)
    else:
        run = p.add_run(f"[Image: {filename} — not yet generated]")
        run.font.color.rgb = GREY_TEXT
        run.font.size = Pt(9)
        run.italic = True

    # CDN URL caption
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = cap.add_run(f"{CDN_BASE}/{filename}")
    r.font.size = Pt(8)
    r.font.color.rgb = RGBColor(0x00, 0x55, 0x99)
    r.underline = True
    return p


def add_table(doc, headers, rows, col_widths=None):
    """Add a formatted table."""
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = 'Table Grid'

    # Header row
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = ""
        p = cell.paragraphs[0]
        run = p.add_run(h)
        run.bold = True
        run.font.size = Pt(9)
        run.font.color.rgb = WHITE
        set_cell_shading(cell, "830051")

    # Data rows
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
    """Add a visual separator."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("─" * 60)
    run.font.color.rgb = RGBColor(0xCC, 0xCC, 0xCC)
    run.font.size = Pt(8)


def build_document():
    doc = Document()

    # --- Page setup ---
    section = doc.sections[0]
    section.page_width = Cm(21)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2)
    section.bottom_margin = Cm(2)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(2.5)

    # --- Styles ---
    style = doc.styles['Normal']
    style.font.name = 'Calibri'
    style.font.size = Pt(10)
    style.font.color.rgb = DARK_TEXT

    for level in range(1, 5):
        hs = doc.styles[f'Heading {level}']
        hs.font.name = 'Calibri'
        hs.font.color.rgb = AZ_MAGENTA

    # =========================================================================
    # COVER PAGE
    # =========================================================================
    for _ in range(6):
        doc.add_paragraph()

    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run("LUMIVEX®")
    run.font.size = Pt(36)
    run.font.color.rgb = AZ_MAGENTA
    run.bold = True

    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = sub.add_run("(lumvecitinib)")
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

    for line in [
        "Document type: Final approved marketing brief for HCP website build",
        "Prepared by: Marketing — UK Dermatology Franchise",
        "Approval status: MLR-approved copy — do not modify",
        "Date: March 2026",
        "Approval code: GB-94281 | DOP: March 2026",
    ]:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(line)
        run.font.size = Pt(10)
        run.font.color.rgb = GREY_TEXT

    doc.add_page_break()

    # =========================================================================
    # TABLE OF CONTENTS (manual)
    # =========================================================================
    add_heading(doc, "Contents", level=1, color=AZ_MAGENTA)
    toc_items = [
        "1. Drug Profile",
        "2. Mechanism of Action",
        "3. Clinical Programme: LUMINANCE",
        "4. Safety Profile",
        "5. Prescribing Information",
        "6. Adverse Event Reporting",
        "7. References",
        "8. Site Navigation",
        "9. Page Content",
        "   Page 1: Home",
        "   Page 2: Efficacy",
        "   Page 3: Safety",
        "   Page 4: Dosing & Administration",
        "   Page 5: Mechanism of Action",
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

    # =========================================================================
    # 1. DRUG PROFILE
    # =========================================================================
    add_heading(doc, "1. Drug Profile", level=1, color=AZ_MAGENTA)

    profile_data = [
        ("Brand name", "LUMIVEX®"),
        ("Generic name", "lumvecitinib"),
        ("Drug class", "Selective allosteric tyrosine kinase 2 (TYK2) inhibitor"),
        ("Indication", "Treatment of adults with moderate-to-severe plaque psoriasis who are candidates for systemic therapy"),
        ("Formulation", "6 mg film-coated tablet"),
        ("Dosing", "One tablet once daily, with or without food"),
        ("Approval", "MHRA — February 2026"),
        ("Brand colour", "Luminous Amber #D4851F"),
        ("Approval code", "GB-94281"),
    ]
    add_table(doc, ["Field", "Detail"], profile_data)

    doc.add_paragraph()
    add_separator(doc)

    # =========================================================================
    # 2. MECHANISM OF ACTION
    # =========================================================================
    add_heading(doc, "2. Mechanism of Action", level=1, color=AZ_MAGENTA)

    add_body(doc, (
        "Lumvecitinib is a selective allosteric inhibitor of tyrosine kinase 2 (TYK2), binding to the "
        "pseudokinase (JH2) regulatory domain rather than the catalytic (JH1) domain. This allosteric "
        "mechanism confers high selectivity for TYK2 over JAK1, JAK2, and JAK3, minimising the "
        "haematological and immunosuppressive effects associated with pan-JAK inhibition."
    ))
    add_body(doc, (
        "TYK2 mediates intracellular signalling through the IL-23, IL-12, and type I interferon (IFN) "
        "receptors — key drivers of the Th17 and Th1 immune responses that underlie psoriatic "
        "inflammation. IL-23 activates TYK2, which phosphorylates STAT3, promoting Th17 cell "
        "differentiation and IL-17A/F production. IL-17 drives keratinocyte hyperproliferation, "
        "neutrophil recruitment, and the characteristic epidermal thickening of plaque psoriasis."
    ))
    add_body(doc, (
        "By selectively inhibiting TYK2, lumvecitinib reduces IL-23-dependent Th17 cell activation "
        "and IL-17 production, normalising keratinocyte proliferation and resolving psoriatic plaques. "
        "The selective mechanism preserves JAK1/2/3-mediated haematopoiesis and broader immune "
        "surveillance, resulting in a favourable tolerability profile distinct from non-selective JAK inhibitors."
    ))

    add_separator(doc)

    # =========================================================================
    # 3. CLINICAL PROGRAMME
    # =========================================================================
    add_heading(doc, "3. Clinical Programme: LUMINANCE", level=1, color=AZ_MAGENTA)

    # LUMINANCE-1
    add_heading(doc, "LUMINANCE-1: Efficacy vs placebo", level=2, color=AZ_MAGENTA)
    details_l1 = [
        ("Design", "Phase III, randomised, double-blind, placebo-controlled, 52-week trial"),
        ("Population", "1,020 adults with moderate-to-severe plaque psoriasis (BSA ≥10%, PASI ≥12, IGA ≥3), inadequate response or intolerance to ≥1 conventional systemic therapy"),
        ("Primary endpoint", "Proportion achieving PASI 75 response at Week 16"),
        ("Key secondary", "PASI 90, IGA 0/1 at Week 16; PASI 75 maintenance at Week 52"),
        ("Publication", "Morrison et al. N Engl J Med 2025; 392(12): 1089–1101"),
    ]
    for label, val in details_l1:
        p = doc.add_paragraph()
        run_b = p.add_run(f"{label}: ")
        run_b.bold = True
        run_b.font.size = Pt(10)
        run_v = p.add_run(val)
        run_v.font.size = Pt(10)

    doc.add_paragraph()
    add_body(doc, "Key results:", bold=True)
    add_table(doc,
        ["Endpoint", "Lumvecitinib 6 mg (n=510)", "Placebo (n=510)", "Difference (95% CI)"],
        [
            ("PASI 75 at Week 16 (primary)", "72.4%", "8.6%", "63.8% (58.9 to 68.7); P<0.001"),
            ("PASI 90 at Week 16", "48.1%", "3.2%", "44.9% (40.3 to 49.5); P<0.001"),
            ("PASI 100 at Week 16", "24.7%", "1.0%", "23.7% (19.8 to 27.6); P<0.001"),
            ("IGA 0/1 at Week 16", "54.3%", "7.1%", "47.2% (42.4 to 52.0); P<0.001"),
            ("PASI 75 at Week 52", "84.6%*", "—", "*of Week 16 PASI 75 responders"),
            ("DLQI 0/1 at Week 16", "41.8%", "5.9%", "35.9% (31.3 to 40.5); P<0.001"),
        ])

    doc.add_paragraph()

    # LUMINANCE-2
    add_heading(doc, "LUMINANCE-2: Superiority vs adalimumab", level=2, color=AZ_MAGENTA)
    details_l2 = [
        ("Design", "Phase III, randomised, double-blind, double-dummy, active-controlled, 52-week trial"),
        ("Population", "1,428 biologic-naïve adults with moderate-to-severe plaque psoriasis (BSA ≥10%, PASI ≥12, IGA ≥3)"),
        ("Primary endpoint", "PASI 90 response at Week 16 (non-inferiority margin 10%, with pre-specified superiority test)"),
        ("Publication", "Park et al. Lancet 2025; 405(10478): 823–836"),
    ]
    for label, val in details_l2:
        p = doc.add_paragraph()
        run_b = p.add_run(f"{label}: ")
        run_b.bold = True
        run_b.font.size = Pt(10)
        run_v = p.add_run(val)
        run_v.font.size = Pt(10)

    doc.add_paragraph()
    add_body(doc, "Key results:", bold=True)
    add_table(doc,
        ["Endpoint", "Lumvecitinib 6 mg (n=714)", "Adalimumab 40 mg (n=714)", "Difference (95% CI)"],
        [
            ("PASI 90 at Week 16 (primary)", "52.8%", "38.2%", "14.6% (9.5 to 19.7); P<0.001 superiority"),
            ("PASI 75 at Week 16", "78.1%", "65.4%", "12.7% (8.0 to 17.4); P<0.001"),
            ("IGA 0/1 at Week 16", "59.2%", "43.8%", "15.4% (10.4 to 20.4); P<0.001"),
            ("PASI 90 at Week 52", "61.4%", "34.7%", "26.7% (21.9 to 31.5); P<0.001"),
            ("DLQI 0/1 at Week 16", "46.3%", "33.1%", "13.2% (8.4 to 18.0); P<0.001"),
        ])

    doc.add_paragraph()

    # LUMINANCE-3
    add_heading(doc, "LUMINANCE-3: Long-term safety and efficacy (open-label extension)", level=2, color=AZ_MAGENTA)
    details_l3 = [
        ("Design", "Open-label extension of LUMINANCE-1 and -2, up to 3 years"),
        ("Population", "2,186 patients who completed parent trials"),
        ("Publication", "Morrison et al. Br J Dermatol 2026; 194(2): 412–425"),
    ]
    for label, val in details_l3:
        p = doc.add_paragraph()
        run_b = p.add_run(f"{label}: ")
        run_b.bold = True
        run_b.font.size = Pt(10)
        run_v = p.add_run(val)
        run_v.font.size = Pt(10)

    doc.add_paragraph()
    add_body(doc, "Key results:", bold=True)
    results_l3 = [
        "PASI 90 maintained at Week 148: 67.3% (observed cases)",
        "No new safety signals identified through 148 weeks of continuous treatment",
        "Serious infection rate: stable at 1.0–1.3 per 100 patient-years across all three years",
        "No increase in opportunistic infections, herpes zoster reactivation, or tuberculosis",
        "Malignancy rates: comparable to age- and sex-matched general psoriasis population",
        "No clinically meaningful changes in haematological parameters, lipid profiles, or hepatic function tests",
        "Treatment satisfaction (DLQI 0/1) maintained in 52.6% at Week 148",
    ]
    for r in results_l3:
        p = doc.add_paragraph(style='List Bullet')
        run = p.add_run(r)
        run.font.size = Pt(10)

    add_separator(doc)

    # =========================================================================
    # 4. SAFETY PROFILE
    # =========================================================================
    add_heading(doc, "4. Safety Profile", level=1, color=AZ_MAGENTA)

    add_heading(doc, "Pooled adverse events (LUMINANCE-1 and -2; N=1,224 lumvecitinib)", level=2, color=AZ_MAGENTA)
    add_table(doc,
        ["Adverse event", "Lumvecitinib 6 mg (%)", "Comparator (%)"],
        [
            ("Upper respiratory tract infection", "8.4", "7.2"),
            ("Nasopharyngitis", "6.1", "5.8"),
            ("Headache", "4.7", "4.1"),
            ("Acne", "3.9", "0.8"),
            ("Diarrhoea", "3.1", "2.4"),
            ("Herpes zoster", "1.4", "0.6"),
            ("CPK elevation (>5× ULN)", "1.2", "0.5"),
            ("Folliculitis", "1.1", "0.4"),
            ("ALT elevation (>3× ULN)", "0.8", "0.4"),
        ])

    doc.add_paragraph()

    add_heading(doc, "Key safety findings", level=2, color=AZ_MAGENTA)
    safety_findings = [
        (
            "Infections",
            "Upper respiratory tract infections and nasopharyngitis were the most common adverse events. Serious infections occurred in 1.1% vs 0.9% of patients. No opportunistic infections were reported in controlled trials. Herpes zoster occurred in 1.4% of lumvecitinib-treated patients; all cases were non-serious, dermatomal, and did not require treatment discontinuation.¹⁻³"
        ),
        (
            "Haematological effects",
            "No clinically meaningful changes in haemoglobin, neutrophil, lymphocyte, or platelet counts were observed. Unlike non-selective JAK inhibitors, lumvecitinib did not cause dose-dependent cytopenias, consistent with its selective TYK2 mechanism.¹⁻³"
        ),
        (
            "Hepatic effects",
            "ALT elevations >3× ULN occurred in 0.8% of patients. No cases met criteria for drug-induced liver injury (Hy's Law). Liver function tests should be performed prior to initiation and periodically during treatment.⁴"
        ),
        (
            "Malignancy",
            "Non-melanoma skin cancer (NMSC) was reported in 0.2% of patients, consistent with background rates in the psoriasis population. No lymphomas were reported. Long-term data from LUMINANCE-3 (up to 148 weeks) showed no increase in malignancy rates over time.¹⁻³"
        ),
        (
            "Cardiovascular safety",
            "No major adverse cardiovascular events (MACE) signal was identified. No venous thromboembolism (VTE) signal was detected. Lipid parameters remained stable throughout treatment.¹⁻³"
        ),
    ]
    for title, text in safety_findings:
        p = doc.add_paragraph()
        run_t = p.add_run(f"{title}: ")
        run_t.bold = True
        run_t.font.size = Pt(10)
        run_v = p.add_run(text)
        run_v.font.size = Pt(10)

    doc.add_paragraph()

    add_heading(doc, "Special populations", level=2, color=AZ_MAGENTA)
    special_pops = [
        "Renal impairment: No dose adjustment is required for patients with mild or moderate renal impairment (eGFR ≥30 mL/min/1.73m²). Lumvecitinib has not been studied in patients with severe renal impairment (eGFR <30 mL/min/1.73m²) or end-stage renal disease.⁴",
        "Hepatic impairment: No dose adjustment is required in mild hepatic impairment (Child-Pugh A). Lumvecitinib is not recommended in patients with moderate (Child-Pugh B) or severe (Child-Pugh C) hepatic impairment due to insufficient clinical data.⁴",
        "Elderly (≥65 years): No dose adjustment is required. Clinical experience in patients aged ≥75 years is limited; use with caution in this population.⁴",
        "Pregnancy and lactation: Lumvecitinib is contraindicated in pregnancy. Women of childbearing potential must use effective contraception during treatment and for 4 weeks after the last dose. It is not known whether lumvecitinib is excreted in human milk; a decision must be made whether to discontinue breast-feeding or to discontinue therapy.⁴",
    ]
    for sp in special_pops:
        p = doc.add_paragraph(style='List Bullet')
        # Bold the label
        colon_idx = sp.index(":")
        run_b = p.add_run(sp[:colon_idx + 1])
        run_b.bold = True
        run_b.font.size = Pt(10)
        run_v = p.add_run(sp[colon_idx + 1:])
        run_v.font.size = Pt(10)

    add_separator(doc)

    # =========================================================================
    # 5. PRESCRIBING INFORMATION
    # =========================================================================
    add_heading(doc, "5. Prescribing Information (abbreviated — for every page footer)", level=1, color=AZ_MAGENTA)

    pi_text = (
        "LUMIVEX (lumvecitinib) 6 mg film-coated tablets. Please refer to the Summary of Product "
        "Characteristics (SmPC) before prescribing. Indication: Treatment of adults with moderate-to-severe "
        "plaque psoriasis who are candidates for systemic therapy. Dosage and administration: 6 mg once "
        "daily, with or without food. The tablet should be swallowed whole. Contraindications: Hypersensitivity "
        "to lumvecitinib or any excipient. Active serious infections, including tuberculosis. Pregnancy. "
        "Warnings and precautions: Evaluate patients for tuberculosis prior to initiation. Monitor for signs "
        "and symptoms of infection during and after treatment. Perform liver function tests prior to initiation "
        "and periodically thereafter. Check complete blood count including absolute lymphocyte count, absolute "
        "neutrophil count, and haemoglobin prior to initiation and periodically during treatment. Assess lipid "
        "parameters 12 weeks after initiation. Not recommended in combination with biological "
        "immunomodulators or other potent immunosuppressants. Interactions: Avoid concomitant use with "
        "strong CYP3A4 inducers. Side effects: Very common (≥1/10): none. Common (≥1/100 to <1/10): "
        "upper respiratory tract infection, nasopharyngitis, headache, acne, diarrhoea. Uncommon (≥1/1000 "
        "to <1/100): herpes zoster, CPK elevation, folliculitis, ALT increase. Legal category: POM. "
        "Pack and price: 28 tablets: £894.35. Marketing authorisation holder: AstraZeneca UK Ltd. "
        "MA number: PLGB 17901/0512. Full prescribing information available from: AstraZeneca UK Ltd, "
        "2 Pancras Square, London N1C 4AG. GB-94281 | DOP: March 2026."
    )
    add_body(doc, pi_text, size=Pt(9))

    add_separator(doc)

    # =========================================================================
    # 6. ADVERSE EVENT REPORTING
    # =========================================================================
    add_heading(doc, "6. Adverse Event Reporting (for every page footer)", level=1, color=AZ_MAGENTA)
    add_body(doc, (
        "Adverse events should be reported. Reporting forms and information can be found at "
        "www.mhra.gov.uk/yellowcard or search for MHRA Yellow Card in the Google Play or Apple App Store. "
        "Adverse events should also be reported to AstraZeneca by visiting contactazmedical.astrazeneca.com "
        "or by calling 0800 783 0033."
    ))

    add_separator(doc)

    # =========================================================================
    # 7. REFERENCES
    # =========================================================================
    add_heading(doc, "7. References (for every page footer)", level=1, color=AZ_MAGENTA)
    refs = [
        "Morrison et al. N Engl J Med 2025; 392(12): 1089–1101.",
        "Park et al. Lancet 2025; 405(10478): 823–836.",
        "Morrison et al. Br J Dermatol 2026; 194(2): 412–425.",
        "Lumivex (lumvecitinib) Summary of Product Characteristics. AstraZeneca UK Ltd. February 2026.",
    ]
    for i, ref in enumerate(refs, 1):
        p = doc.add_paragraph()
        run = p.add_run(f"{i}.  {ref}")
        run.font.size = Pt(10)
        run.italic = True

    add_separator(doc)

    # =========================================================================
    # 8. SITE NAVIGATION
    # =========================================================================
    add_heading(doc, "8. Site Navigation", level=1, color=AZ_MAGENTA)

    nav_items = [
        ("Top bar links", "Contact Us (https://www.astrazeneca.co.uk/contact-us.html) | AZ Employee Login (https://login.astrazeneca.com)"),
        ("Main navigation pages", "Efficacy | Safety | Dosing | Mechanism of Action | Resources"),
        ("Utility", "Search | Login"),
    ]
    for label, val in nav_items:
        p = doc.add_paragraph()
        run_b = p.add_run(f"{label}: ")
        run_b.bold = True
        run_v = p.add_run(val)

    doc.add_page_break()

    # =========================================================================
    # 9. PAGE CONTENT
    # =========================================================================
    add_heading(doc, "9. Page Content", level=1, color=AZ_MAGENTA)

    # Important notice
    notice = doc.add_paragraph()
    notice_run = notice.add_run(
        "IMPORTANT: All copy below is final and MLR-approved. It must be used exactly as written — "
        "do not modify, rephrase, or abbreviate any text. All superscript reference numbers, statistical "
        "values, and regulatory language must be reproduced verbatim."
    )
    notice_run.bold = True
    notice_run.font.size = Pt(10)
    notice_run.font.color.rgb = RGBColor(0xCC, 0x00, 0x00)

    notice2 = doc.add_paragraph()
    notice2_run = notice2.add_run(
        "Each page must end with expandable sections for Prescribing Information, Adverse Event Reporting, "
        "and References (see sections 5, 6, and 7 above)."
    )
    notice2_run.bold = True
    notice2_run.font.size = Pt(10)
    notice2_run.font.color.rgb = RGBColor(0xCC, 0x00, 0x00)

    add_separator(doc)

    # =====================================================================
    # PAGE 1: HOME
    # =====================================================================
    add_heading(doc, "PAGE 1: Home", level=2, color=AZ_MAGENTA)
    p = doc.add_paragraph()
    run = p.add_run("URL path: /lumivex/")
    run.bold = True
    run.font.size = Pt(10)

    add_separator(doc)

    # Section 1 — Hero
    add_heading(doc, "Section 1 — Hero (full-width image with text overlay)", level=3, color=BRAND_COLOUR)
    p = doc.add_paragraph()
    run = p.add_run("Block: hero-teaser")
    run.bold = True
    doc.add_paragraph()
    add_image_with_caption(doc, "hero-home.jpeg", "Hero — Home", width=Inches(5.5))

    p = doc.add_paragraph()
    run = p.add_run("Heading: ")
    run.bold = True
    p.add_run("LUMIVEX® (lumvecitinib): selective TYK2 inhibition for clearer skin")

    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "A new standard in plaque psoriasis — the first selective allosteric TYK2 inhibitor "
        "to demonstrate superiority over adalimumab, with a once-daily oral tablet and a "
        "favourable tolerability profile distinct from non-selective JAK inhibition.¹˒²"
    )

    p = doc.add_paragraph()
    run = p.add_run("Call to action: ")
    run.bold = True
    p.add_run("Explore the LUMINANCE data → /lumivex/efficacy")

    add_separator(doc)

    # Section 2 — Three key benefit cards
    add_heading(doc, "Section 2 — Three key benefit cards (equal columns)", level=3, color=BRAND_COLOUR)
    p = doc.add_paragraph()
    run = p.add_run("Block: cards-teaser")
    run.bold = True

    # Card 1
    doc.add_paragraph()
    add_image_with_caption(doc, "card-efficacy.jpeg", "Card — Efficacy", width=Inches(3))
    p = doc.add_paragraph()
    run = p.add_run("Card heading: ")
    run.bold = True
    p.add_run("Superior skin clearance")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "72.4% of patients achieved PASI 75 at Week 16 vs 8.6% with placebo (P<0.001). "
        "Nearly half achieved PASI 90 — clear or almost clear skin.¹"
    )
    p = doc.add_paragraph()
    run = p.add_run("Card link: ")
    run.bold = True
    p.add_run("View efficacy data → /lumivex/efficacy")

    add_separator(doc)

    # Card 2
    add_image_with_caption(doc, "card-safety.jpeg", "Card — Safety", width=Inches(3))
    p = doc.add_paragraph()
    run = p.add_run("Card heading: ")
    run.bold = True
    p.add_run("Favourable tolerability profile")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "Selective TYK2 inhibition with no dose-dependent cytopenias, no MACE signal, and "
        "no VTE signal — a differentiated safety profile across over 2,400 patients.¹⁻³"
    )
    p = doc.add_paragraph()
    run = p.add_run("Card link: ")
    run.bold = True
    p.add_run("Review safety data → /lumivex/safety")

    add_separator(doc)

    # Card 3
    add_image_with_caption(doc, "card-dosing.jpeg", "Card — Dosing", width=Inches(3))
    p = doc.add_paragraph()
    run = p.add_run("Card heading: ")
    run.bold = True
    p.add_run("Once-daily oral convenience")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "A single 6 mg tablet once daily, with or without food — no injection, no titration, "
        "no fasting requirement. Simplicity in a single oral dose.⁴"
    )
    p = doc.add_paragraph()
    run = p.add_run("Card link: ")
    run.bold = True
    p.add_run("View dosing information → /lumivex/dosing")

    add_separator(doc)

    # Section 3 — Disease context
    add_heading(doc, "Section 3 — Disease context (centred text) | light background", level=3, color=BRAND_COLOUR)
    p = doc.add_paragraph()
    run = p.add_run("Block: introduction")
    run.bold = True
    run2 = p.add_run("  |  Section metadata: Style: light")
    run2.font.color.rgb = GREY_TEXT

    p = doc.add_paragraph()
    run = p.add_run("Heading: ")
    run.bold = True
    p.add_run("The unmet need in plaque psoriasis")

    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Plaque psoriasis affects approximately 1.8 million adults in the UK, with moderate-to-severe "
        "disease significantly impacting quality of life. Despite available treatments, many patients "
        "do not achieve or maintain adequate skin clearance — and concerns about injection burden, "
        "immunosuppression, and long-term safety remain barriers to treatment optimisation. There is "
        "a need for an effective oral therapy with a targeted mechanism and a well-characterised "
        "long-term safety profile."
    )

    add_separator(doc)

    # Section 4 — MOA teaser
    add_heading(doc, "Section 4 — Mechanism of action teaser (two-column) | highlighted background", level=3, color=BRAND_COLOUR)
    p = doc.add_paragraph()
    run = p.add_run("Block: columns-teaser")
    run.bold = True
    run2 = p.add_run("  |  Section metadata: Style: highlight")
    run2.font.color.rgb = GREY_TEXT

    doc.add_paragraph()
    add_image_with_caption(doc, "columns-moa.jpeg", "Mechanism of action teaser", width=Inches(3.5))

    p = doc.add_paragraph()
    run = p.add_run("Heading: ")
    run.bold = True
    p.add_run("Selective TYK2 inhibition — a targeted approach")

    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Lumvecitinib selectively binds the TYK2 pseudokinase (JH2) domain, inhibiting IL-23, IL-12, "
        "and type I IFN signalling without affecting JAK1/2/3-mediated pathways. This allosteric mechanism "
        "targets the key drivers of psoriatic inflammation while preserving broader immune surveillance.⁴"
    )

    p = doc.add_paragraph()
    run = p.add_run("Call to action: ")
    run.bold = True
    p.add_run("Explore the mechanism of action → /lumivex/mechanism-of-action")

    add_separator(doc)

    # Section 5 — Accordion
    add_heading(doc, "Section 5 — Prescribing information footer", level=3, color=BRAND_COLOUR)
    p = doc.add_paragraph()
    run = p.add_run("Block: accordion")
    run.bold = True
    add_body(doc, "Expandable sections for: Prescribing Information | Adverse Event Reporting | References (Use approved text from sections 5, 6, and 7 above)", italic=True)

    # Page metadata
    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run("Page metadata")
    run.bold = True
    run.font.color.rgb = AZ_MAGENTA
    add_body(doc, "Title: LUMIVEX® (lumvecitinib) | Selective TYK2 Inhibitor for Plaque Psoriasis | AstraZeneca UK")
    add_body(doc, "Description: LUMIVEX® (lumvecitinib) is a first-in-class selective allosteric TYK2 inhibitor for adults with moderate-to-severe plaque psoriasis. Explore efficacy, safety, and dosing information for UK healthcare professionals.")

    doc.add_page_break()

    # =====================================================================
    # PAGE 2: EFFICACY
    # =====================================================================
    add_heading(doc, "PAGE 2: Efficacy", level=2, color=AZ_MAGENTA)
    p = doc.add_paragraph()
    run = p.add_run("URL path: /lumivex/efficacy")
    run.bold = True

    add_separator(doc)

    # Section 1 — Hero
    add_heading(doc, "Section 1 — Hero (full-width image with text overlay)", level=3, color=BRAND_COLOUR)
    p = doc.add_paragraph()
    run = p.add_run("Block: hero-teaser")
    run.bold = True
    doc.add_paragraph()
    add_image_with_caption(doc, "hero-efficacy.jpeg", "Hero — Efficacy", width=Inches(5.5))

    p = doc.add_paragraph()
    run = p.add_run("Heading: ")
    run.bold = True
    p.add_run("Clinical evidence for LUMIVEX®")

    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "The LUMINANCE clinical programme evaluated lumvecitinib in three studies encompassing "
        "over 2,400 adults with moderate-to-severe plaque psoriasis, including head-to-head "
        "comparison with adalimumab and long-term data up to 148 weeks.¹⁻³"
    )

    add_separator(doc)

    # Section 2 — Programme overview
    add_heading(doc, "Section 2 — Programme overview (centred text) | light background", level=3, color=BRAND_COLOUR)
    p = doc.add_paragraph()
    run = p.add_run("Block: introduction")
    run.bold = True
    run2 = p.add_run("  |  Section metadata: Style: light")
    run2.font.color.rgb = GREY_TEXT

    p = doc.add_paragraph()
    run = p.add_run("Heading: ")
    run.bold = True
    p.add_run("The LUMINANCE clinical programme")

    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Lumvecitinib was evaluated in three studies: LUMINANCE-1 assessed skin clearance and "
        "quality-of-life improvement versus placebo; LUMINANCE-2 demonstrated superiority to "
        "adalimumab in biologic-naïve patients; and LUMINANCE-3, an open-label extension, "
        "confirmed sustained efficacy and long-term safety through 148 weeks of continuous treatment.¹⁻³"
    )

    add_separator(doc)

    # Section 3 — Clinical data tabs
    add_heading(doc, "Section 3 — Clinical data (two tabs)", level=3, color=BRAND_COLOUR)
    p = doc.add_paragraph()
    run = p.add_run("Block: tabs-large")
    run.bold = True

    # Tab 1
    doc.add_paragraph()
    add_body(doc, 'Tab 1: "LUMINANCE-1: Skin clearance vs placebo"', bold=True)
    add_image_with_caption(doc, "tab-luminance1.jpeg", "LUMINANCE-1 results", width=Inches(3.5))

    p = doc.add_paragraph()
    run = p.add_run("Heading: ")
    run.bold = True
    p.add_run("Superior PASI 75 response versus placebo")

    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "In LUMINANCE-1, a 52-week randomised, double-blind, placebo-controlled trial in 1,020 adults "
        "with moderate-to-severe plaque psoriasis (BSA ≥10%, PASI ≥12, IGA ≥3), lumvecitinib 6 mg "
        "demonstrated significantly greater PASI 75 response versus placebo at Week 16, with sustained "
        "response through Week 52.¹"
    )

    add_body(doc, "Data table:", bold=True)
    add_table(doc,
        ["Endpoint", "Lumvecitinib 6 mg (n=510)", "Placebo (n=510)", "Difference (95% CI)"],
        [
            ("PASI 75 at Week 16 (primary)", "72.4%", "8.6%", "63.8% (58.9 to 68.7); P<0.001"),
            ("PASI 90 at Week 16", "48.1%", "3.2%", "44.9% (40.3 to 49.5); P<0.001"),
            ("PASI 100 at Week 16", "24.7%", "1.0%", "23.7% (19.8 to 27.6); P<0.001"),
            ("IGA 0/1 at Week 16", "54.3%", "7.1%", "47.2% (42.4 to 52.0); P<0.001"),
            ("DLQI 0/1 at Week 16", "41.8%", "5.9%", "35.9% (31.3 to 40.5); P<0.001"),
        ])

    doc.add_paragraph()
    add_body(doc, "Footnote text: The primary endpoint was met with high statistical significance. PASI 90 and PASI 100 responses demonstrated deep skin clearance, and DLQI improvements confirmed meaningful quality-of-life benefit.¹", italic=True, size=Pt(9))

    add_separator(doc)

    # Tab 2
    add_body(doc, 'Tab 2: "LUMINANCE-2: Superiority vs adalimumab"', bold=True)
    add_image_with_caption(doc, "tab-luminance2.jpeg", "LUMINANCE-2 results", width=Inches(3.5))

    p = doc.add_paragraph()
    run = p.add_run("Heading: ")
    run.bold = True
    p.add_run("Superior to adalimumab at Week 16, with increasing benefit over time")

    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "In LUMINANCE-2, a 52-week randomised, double-blind, active-controlled trial in 1,428 "
        "biologic-naïve adults with moderate-to-severe plaque psoriasis, lumvecitinib 6 mg demonstrated "
        "superior PASI 90 response compared with adalimumab 40 mg at Week 16. The treatment difference "
        "increased further at Week 52, demonstrating durable superiority.²"
    )

    add_body(doc, "Data table:", bold=True)
    add_table(doc,
        ["Endpoint", "Lumvecitinib 6 mg (n=714)", "Adalimumab 40 mg (n=714)", "Difference (95% CI)"],
        [
            ("PASI 90 at Week 16 (primary)", "52.8%", "38.2%", "14.6% (9.5 to 19.7); P<0.001"),
            ("PASI 75 at Week 16", "78.1%", "65.4%", "12.7% (8.0 to 17.4); P<0.001"),
            ("IGA 0/1 at Week 16", "59.2%", "43.8%", "15.4% (10.4 to 20.4); P<0.001"),
            ("PASI 90 at Week 52", "61.4%", "34.7%", "26.7% (21.9 to 31.5); P<0.001"),
            ("DLQI 0/1 at Week 52", "52.1%", "28.9%", "23.2% (18.4 to 28.0); P<0.001"),
        ])

    doc.add_paragraph()
    add_body(doc, "Footnote text: Lumvecitinib achieved superior skin clearance to adalimumab at Week 16, with the treatment difference widening at Week 52 — demonstrating both rapid onset and increasing efficacy over time.²", italic=True, size=Pt(9))

    add_separator(doc)

    # Section 4 — Long-term data
    add_heading(doc, "Section 4 — Long-term efficacy (two-column) | highlighted background", level=3, color=BRAND_COLOUR)
    p = doc.add_paragraph()
    run = p.add_run("Block: columns-teaser")
    run.bold = True
    run2 = p.add_run("  |  Section metadata: Style: highlight")
    run2.font.color.rgb = GREY_TEXT

    doc.add_paragraph()
    add_image_with_caption(doc, "columns-longterm.jpeg", "Long-term efficacy", width=Inches(3.5))

    p = doc.add_paragraph()
    run = p.add_run("Heading: ")
    run.bold = True
    p.add_run("Sustained response through 148 weeks in LUMINANCE-3")

    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "In the open-label extension study LUMINANCE-3, PASI 90 response was maintained in "
        "67.3% of patients at Week 148 (observed cases), with no new safety signals identified "
        "over 3 years of continuous treatment. Quality-of-life benefit was sustained, with "
        "52.6% of patients maintaining DLQI 0/1 at Week 148.³"
    )

    p = doc.add_paragraph()
    run = p.add_run("Call to action: ")
    run.bold = True
    p.add_run("Review the full safety profile → /lumivex/safety")

    add_separator(doc)

    # Accordion + metadata
    add_heading(doc, "Section 5 — Prescribing information footer", level=3, color=BRAND_COLOUR)
    add_body(doc, "Block: accordion  |  Expandable: PI | AE Reporting | References", italic=True)

    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run("Page metadata")
    run.bold = True
    run.font.color.rgb = AZ_MAGENTA
    add_body(doc, "Title: Efficacy | LUMIVEX® (lumvecitinib) | LUMINANCE Clinical Data | AstraZeneca UK")
    add_body(doc, "Description: Explore the LUMINANCE clinical programme for LUMIVEX® (lumvecitinib) — Phase III data on PASI 75/90/100 response, superiority vs adalimumab, and long-term efficacy up to 148 weeks in moderate-to-severe plaque psoriasis.")

    doc.add_page_break()

    # =====================================================================
    # PAGE 3: SAFETY
    # =====================================================================
    add_heading(doc, "PAGE 3: Safety", level=2, color=AZ_MAGENTA)
    p = doc.add_paragraph()
    run = p.add_run("URL path: /lumivex/safety")
    run.bold = True

    add_separator(doc)

    # Section 1 — Title
    add_heading(doc, "Section 1 — Page header (text only, no image)", level=3, color=BRAND_COLOUR)
    p = doc.add_paragraph()
    run = p.add_run("Block: title")
    run.bold = True

    p = doc.add_paragraph()
    run = p.add_run("Heading: ")
    run.bold = True
    p.add_run("Safety profile")

    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Lumvecitinib has been evaluated for safety in over 2,400 patients across the LUMINANCE "
        "clinical programme, including controlled and long-term open-label data up to 148 weeks.¹⁻³"
    )

    add_separator(doc)

    # Section 2 — Safety overview
    add_heading(doc, "Section 2 — Safety overview (centred text) | light background", level=3, color=BRAND_COLOUR)
    p = doc.add_paragraph()
    run = p.add_run("Block: introduction")
    run.bold = True
    run2 = p.add_run("  |  Section metadata: Style: light")
    run2.font.color.rgb = GREY_TEXT

    p = doc.add_paragraph()
    run = p.add_run("Heading: ")
    run.bold = True
    p.add_run("A selective mechanism with a favourable tolerability profile")

    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Lumvecitinib's selective allosteric TYK2 inhibition provides a distinct safety profile compared "
        "with non-selective JAK inhibitors. No dose-dependent cytopenias, no MACE signal, and no VTE "
        "signal were observed across the programme. The most commonly reported adverse events were "
        "upper respiratory tract infections and nasopharyngitis, consistent with the mild "
        "immunomodulatory profile expected from selective TYK2 blockade.¹⁻³"
    )

    add_separator(doc)

    # Section 3 — Safety cards
    add_heading(doc, "Section 3 — Three key safety consideration cards (equal columns)", level=3, color=BRAND_COLOUR)
    p = doc.add_paragraph()
    run = p.add_run("Block: cards-teaser")
    run.bold = True

    # Card 1 — Infections
    doc.add_paragraph()
    add_image_with_caption(doc, "card-infections.jpeg", "Infection monitoring", width=Inches(3))
    p = doc.add_paragraph()
    run = p.add_run("Card heading: ")
    run.bold = True
    p.add_run("Infection profile")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "URTI (8.4%) and nasopharyngitis (6.1%) were the most common adverse events. Serious infections "
        "occurred in 1.1% vs 0.9%. No opportunistic infections were reported in controlled trials. Herpes "
        "zoster occurred in 1.4%, all non-serious and dermatomal.¹⁻³"
    )

    add_separator(doc)

    # Card 2 — Selectivity
    add_image_with_caption(doc, "card-selectivity.jpeg", "TYK2 selectivity", width=Inches(3))
    p = doc.add_paragraph()
    run = p.add_run("Card heading: ")
    run.bold = True
    p.add_run("Selective TYK2 mechanism")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "No dose-dependent cytopenias observed — haemoglobin, neutrophil, lymphocyte, and platelet counts "
        "remained stable throughout treatment. This differentiates lumvecitinib from non-selective JAK "
        "inhibitors, reflecting its targeted allosteric mechanism.¹⁻³"
    )

    add_separator(doc)

    # Card 3 — Long-term safety
    add_image_with_caption(doc, "card-longterm-safety.jpeg", "Long-term safety", width=Inches(3))
    p = doc.add_paragraph()
    run = p.add_run("Card heading: ")
    run.bold = True
    p.add_run("Long-term safety (up to 148 weeks)")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "LUMINANCE-3 confirmed no new safety signals through 148 weeks. Serious infection rates remained "
        "stable (1.0–1.3/100 patient-years). No MACE or VTE signal. Malignancy rates comparable to the "
        "general psoriasis population. No increase in herpes zoster over time.³"
    )

    add_separator(doc)

    # Section 4 — AE table
    add_heading(doc, "Section 4 — Adverse event summary table | light background", level=3, color=BRAND_COLOUR)
    p = doc.add_paragraph()
    run = p.add_run("Block: table-data")
    run.bold = True
    run2 = p.add_run("  |  Section metadata: Style: light")
    run2.font.color.rgb = GREY_TEXT

    p = doc.add_paragraph()
    run = p.add_run("Heading: ")
    run.bold = True
    p.add_run("Pooled adverse event data from the LUMINANCE programme¹⁻³")

    add_table(doc,
        ["Adverse event", "Lumvecitinib 6 mg (%)", "Comparator (%)"],
        [
            ("Upper respiratory tract infection", "8.4", "7.2"),
            ("Nasopharyngitis", "6.1", "5.8"),
            ("Headache", "4.7", "4.1"),
            ("Acne", "3.9", "0.8"),
            ("Diarrhoea", "3.1", "2.4"),
            ("Herpes zoster", "1.4", "0.6"),
            ("CPK elevation (>5× ULN)", "1.2", "0.5"),
            ("Folliculitis", "1.1", "0.4"),
            ("ALT elevation (>3× ULN)", "0.8", "0.4"),
        ])

    add_separator(doc)

    # Section 5 — Special populations
    add_heading(doc, "Section 5 — Special populations (two-column) | highlighted background", level=3, color=BRAND_COLOUR)
    p = doc.add_paragraph()
    run = p.add_run("Block: columns-teaser")
    run.bold = True
    run2 = p.add_run("  |  Section metadata: Style: highlight")
    run2.font.color.rgb = GREY_TEXT

    doc.add_paragraph()
    add_image_with_caption(doc, "columns-special-pops.jpeg", "Special populations", width=Inches(3.5))

    p = doc.add_paragraph()
    run = p.add_run("Heading: ")
    run.bold = True
    p.add_run("Special populations")

    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Renal impairment: No dose adjustment is required for patients with mild or moderate renal "
        "impairment (eGFR ≥30 mL/min/1.73m²). Lumvecitinib has not been studied in patients with severe "
        "renal impairment (eGFR <30 mL/min/1.73m²).⁴\n\n"
        "Hepatic impairment: No dose adjustment is required in mild hepatic impairment (Child-Pugh A). "
        "Lumvecitinib is not recommended in moderate (Child-Pugh B) or severe (Child-Pugh C) hepatic "
        "impairment.⁴\n\n"
        "Elderly (≥65 years): No dose adjustment is required. Clinical experience in patients aged ≥75 "
        "years is limited; use with caution in this population.⁴"
    )

    add_separator(doc)

    # Accordion + metadata
    add_heading(doc, "Section 6 — Prescribing information footer", level=3, color=BRAND_COLOUR)
    add_body(doc, "Block: accordion  |  Expandable: PI | AE Reporting | References", italic=True)

    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run("Page metadata")
    run.bold = True
    run.font.color.rgb = AZ_MAGENTA
    add_body(doc, "Title: Safety | LUMIVEX® (lumvecitinib) | Adverse Events & Monitoring | AstraZeneca UK")
    add_body(doc, "Description: Review the safety profile of LUMIVEX® (lumvecitinib) including pooled adverse event data, infection rates, haematological safety, and long-term data up to 148 weeks in plaque psoriasis.")

    doc.add_page_break()

    # =====================================================================
    # PAGE 4: DOSING & ADMINISTRATION
    # =====================================================================
    add_heading(doc, "PAGE 4: Dosing & Administration", level=2, color=AZ_MAGENTA)
    p = doc.add_paragraph()
    run = p.add_run("URL path: /lumivex/dosing")
    run.bold = True

    add_separator(doc)

    # Section 1 — Title
    add_heading(doc, "Section 1 — Page header (text only, no image)", level=3, color=BRAND_COLOUR)
    p = doc.add_paragraph()
    run = p.add_run("Block: title")
    run.bold = True

    p = doc.add_paragraph()
    run = p.add_run("Heading: ")
    run.bold = True
    p.add_run("Dosing and administration")

    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Lumvecitinib is prescribed at a fixed dose of 6 mg once daily — a simple oral regimen "
        "with no titration, no injection, and no fasting requirement.⁴"
    )

    add_separator(doc)

    # Section 2 — How to take
    add_heading(doc, "Section 2 — How to take LUMIVEX® (two-column) | light background", level=3, color=BRAND_COLOUR)
    p = doc.add_paragraph()
    run = p.add_run("Block: columns-teaser")
    run.bold = True
    run2 = p.add_run("  |  Section metadata: Style: light")
    run2.font.color.rgb = GREY_TEXT

    doc.add_paragraph()
    add_image_with_caption(doc, "columns-admin.jpeg", "Administration", width=Inches(3.5))

    p = doc.add_paragraph()
    run = p.add_run("Heading: ")
    run.bold = True
    p.add_run("How to take LUMIVEX®")

    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Lumvecitinib 6 mg should be taken once daily, with or without food. The tablet should be "
        "swallowed whole with water.⁴\n\n"
        "No dose titration is required. Treatment may be started at the full therapeutic dose of 6 mg "
        "from Day 1.⁴\n\n"
        "If a dose is missed, the patient should take it as soon as they remember, unless it is almost "
        "time for the next dose. A double dose should not be taken to make up for a missed dose.⁴"
    )

    add_separator(doc)

    # Section 3 — Monitoring
    add_heading(doc, "Section 3 — Baseline and ongoing monitoring (two-column)", level=3, color=BRAND_COLOUR)
    p = doc.add_paragraph()
    run = p.add_run("Block: columns-teaser")
    run.bold = True

    doc.add_paragraph()
    add_image_with_caption(doc, "columns-monitoring.jpeg", "Monitoring", width=Inches(3.5))

    p = doc.add_paragraph()
    run = p.add_run("Heading: ")
    run.bold = True
    p.add_run("Monitoring recommendations")

    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Prior to initiation: Evaluate for tuberculosis infection. Perform complete blood count "
        "(including absolute lymphocyte count, absolute neutrophil count, haemoglobin) and liver "
        "function tests. Ensure vaccinations are up to date, including herpes zoster vaccination "
        "where appropriate.⁴\n\n"
        "During treatment: Monitor complete blood count and liver function tests periodically. Assess "
        "lipid parameters 12 weeks after initiation. Monitor for signs and symptoms of infection.⁴\n\n"
        "Interruption: If a serious infection develops, interrupt treatment until the infection is "
        "controlled. Do not initiate treatment in patients with active serious infections.⁴"
    )

    add_separator(doc)

    # Section 4 — Combination therapy
    add_heading(doc, "Section 4 — Use with other treatments (centred text) | highlighted background", level=3, color=BRAND_COLOUR)
    p = doc.add_paragraph()
    run = p.add_run("Block: introduction")
    run.bold = True
    run2 = p.add_run("  |  Section metadata: Style: highlight")
    run2.font.color.rgb = GREY_TEXT

    p = doc.add_paragraph()
    run = p.add_run("Heading: ")
    run.bold = True
    p.add_run("Use with other psoriasis treatments")

    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Lumvecitinib can be used as monotherapy or in combination with topical therapies (corticosteroids, "
        "vitamin D analogues). It is not recommended in combination with biological immunomodulators or "
        "other potent systemic immunosuppressants (e.g. ciclosporin, methotrexate at immunosuppressive "
        "doses) due to the possibility of additive immunosuppression. Avoid concomitant use with strong "
        "CYP3A4 inducers (e.g. rifampicin, phenytoin, carbamazepine, St John's Wort).⁴"
    )

    add_separator(doc)

    # Accordion + metadata
    add_heading(doc, "Section 5 — Prescribing information footer", level=3, color=BRAND_COLOUR)
    add_body(doc, "Block: accordion  |  Expandable: PI | AE Reporting | References", italic=True)

    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run("Page metadata")
    run.bold = True
    run.font.color.rgb = AZ_MAGENTA
    add_body(doc, "Title: Dosing | LUMIVEX® (lumvecitinib) | Administration & Monitoring | AstraZeneca UK")
    add_body(doc, "Description: Dosing and administration guidance for LUMIVEX® (lumvecitinib) 6 mg once-daily oral tablet, including monitoring recommendations and concomitant therapy guidance for plaque psoriasis.")

    doc.add_page_break()

    # =====================================================================
    # PAGE 5: MECHANISM OF ACTION
    # =====================================================================
    add_heading(doc, "PAGE 5: Mechanism of Action", level=2, color=AZ_MAGENTA)
    p = doc.add_paragraph()
    run = p.add_run("URL path: /lumivex/mechanism-of-action")
    run.bold = True

    add_separator(doc)

    # Section 1 — Hero
    add_heading(doc, "Section 1 — Hero (full-width image with text overlay)", level=3, color=BRAND_COLOUR)
    p = doc.add_paragraph()
    run = p.add_run("Block: hero-teaser")
    run.bold = True
    doc.add_paragraph()
    add_image_with_caption(doc, "hero-moa.jpeg", "Hero — Mechanism of Action", width=Inches(5.5))

    p = doc.add_paragraph()
    run = p.add_run("Heading: ")
    run.bold = True
    p.add_run("How LUMIVEX® works")

    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Lumvecitinib is a selective allosteric TYK2 inhibitor that targets the pseudokinase (JH2) "
        "domain — blocking the IL-23, IL-12, and type I IFN signalling pathways that drive "
        "psoriatic inflammation, while preserving JAK1/2/3-mediated immune homeostasis.⁴"
    )

    add_separator(doc)

    # Section 2 — Disease pathway
    add_heading(doc, "Section 2 — The psoriatic inflammatory cascade (two-column) | light background", level=3, color=BRAND_COLOUR)
    p = doc.add_paragraph()
    run = p.add_run("Block: columns-teaser")
    run.bold = True
    run2 = p.add_run("  |  Section metadata: Style: light")
    run2.font.color.rgb = GREY_TEXT

    doc.add_paragraph()
    add_image_with_caption(doc, "psoriatic-inflammation.jpeg", "Psoriatic inflammation", width=Inches(3.5))

    p = doc.add_paragraph()
    run = p.add_run("Heading: ")
    run.bold = True
    p.add_run("The psoriatic inflammatory cascade")

    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Plaque psoriasis is driven by a dysregulated immune response in which dendritic cells produce "
        "IL-23, activating T-helper 17 (Th17) cells to release IL-17A, IL-17F, and IL-22. These "
        "cytokines drive keratinocyte hyperproliferation, neutrophil recruitment, and the characteristic "
        "epidermal thickening, scaling, and erythema of psoriatic plaques. IL-12 further promotes Th1 "
        "cell differentiation and IFN-γ production, amplifying the inflammatory loop.⁴"
    )

    add_separator(doc)

    # Section 3 — TYK2/IL-23 cascade
    add_heading(doc, "Section 3 — The IL-23/TYK2 signalling axis (two-column)", level=3, color=BRAND_COLOUR)
    p = doc.add_paragraph()
    run = p.add_run("Block: columns-teaser")
    run.bold = True

    doc.add_paragraph()
    add_image_with_caption(doc, "tyk2-il23-cascade.jpeg", "TYK2/IL-23 cascade", width=Inches(3.5))

    p = doc.add_paragraph()
    run = p.add_run("Heading: ")
    run.bold = True
    p.add_run("TYK2: a central kinase in psoriatic signalling")

    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "TYK2 is an intracellular kinase that mediates signal transduction downstream of the IL-23 "
        "receptor (paired with JAK2), the IL-12 receptor (paired with JAK2), and type I interferon "
        "receptors (paired with JAK1). When IL-23 binds its receptor, TYK2 phosphorylates STAT3, "
        "driving Th17 cell differentiation and IL-17 production — the central effector axis in "
        "plaque psoriasis. TYK2 genetic loss-of-function variants in humans are associated with "
        "protection from psoriasis, confirming TYK2 as a validated therapeutic target.⁴"
    )

    add_separator(doc)

    # Section 4 — Lumivex mechanism
    add_heading(doc, "Section 4 — Selective allosteric TYK2 inhibition (two-column) | highlighted background", level=3, color=BRAND_COLOUR)
    p = doc.add_paragraph()
    run = p.add_run("Block: columns-teaser")
    run.bold = True
    run2 = p.add_run("  |  Section metadata: Style: highlight")
    run2.font.color.rgb = GREY_TEXT

    doc.add_paragraph()
    add_image_with_caption(doc, "lumivex-blockade.jpeg", "Lumivex mechanism", width=Inches(3.5))

    p = doc.add_paragraph()
    run = p.add_run("Heading: ")
    run.bold = True
    p.add_run("How lumvecitinib selectively targets TYK2")

    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "Lumvecitinib binds to the pseudokinase (JH2) regulatory domain of TYK2, stabilising the "
        "enzyme in an inactive conformation. This allosteric mechanism is fundamentally different "
        "from ATP-competitive JAK inhibitors that bind the catalytic (JH1) domain shared across "
        "all four JAK family members.⁴\n\n"
        "Because the JH2 domain is structurally unique to TYK2, lumvecitinib achieves >100-fold "
        "selectivity for TYK2 over JAK1, JAK2, and JAK3. This preserves JAK1-mediated cytokine "
        "signalling (e.g. IL-6, IFN-γ receptor), JAK2-mediated haematopoiesis (erythropoietin, "
        "thrombopoietin), and JAK3-mediated lymphocyte development — explaining the absence of "
        "dose-dependent cytopenias and the favourable tolerability profile observed in the "
        "LUMINANCE programme.¹⁻⁴"
    )

    add_separator(doc)

    # Accordion + metadata
    add_heading(doc, "Section 5 — Prescribing information footer", level=3, color=BRAND_COLOUR)
    add_body(doc, "Block: accordion  |  Expandable: PI | AE Reporting | References", italic=True)

    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run("Page metadata")
    run.bold = True
    run.font.color.rgb = AZ_MAGENTA
    add_body(doc, "Title: Mechanism of Action | LUMIVEX® (lumvecitinib) | TYK2 Inhibition | AstraZeneca UK")
    add_body(doc, "Description: Understand how LUMIVEX® (lumvecitinib) works — selective allosteric TYK2 inhibition targeting the IL-23/Th17 axis in plaque psoriasis while preserving JAK1/2/3-mediated immune homeostasis.")

    doc.add_page_break()

    # =====================================================================
    # PAGE 6: RESOURCES
    # =====================================================================
    add_heading(doc, "PAGE 6: Resources", level=2, color=AZ_MAGENTA)
    p = doc.add_paragraph()
    run = p.add_run("URL path: /lumivex/resources")
    run.bold = True

    add_separator(doc)

    # Section 1 — Title
    add_heading(doc, "Section 1 — Page header (text only, no image)", level=3, color=BRAND_COLOUR)
    p = doc.add_paragraph()
    run = p.add_run("Block: title")
    run.bold = True

    p = doc.add_paragraph()
    run = p.add_run("Heading: ")
    run.bold = True
    p.add_run("Resources")

    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run("Access prescribing guides, patient materials, and clinical data summaries to support your practice.")

    add_separator(doc)

    # Section 2 — Resource cards
    add_heading(doc, "Section 2 — Three resource cards (equal columns) | light background", level=3, color=BRAND_COLOUR)
    p = doc.add_paragraph()
    run = p.add_run("Block: cards-teaser")
    run.bold = True
    run2 = p.add_run("  |  Section metadata: Style: light")
    run2.font.color.rgb = GREY_TEXT

    # Card 1
    doc.add_paragraph()
    add_image_with_caption(doc, "card-prescribing.jpeg", "Prescribing guide", width=Inches(3))
    p = doc.add_paragraph()
    run = p.add_run("Card heading: ")
    run.bold = True
    p.add_run("Prescribing guide")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "A concise guide covering indication, dosing, contraindications, monitoring requirements, "
        "and key safety information for LUMIVEX®. Designed for quick reference in clinical practice."
    )
    p = doc.add_paragraph()
    run = p.add_run("Card link: ")
    run.bold = True
    p.add_run("Download prescribing guide → /lumivex/resources")

    add_separator(doc)

    # Card 2
    add_image_with_caption(doc, "card-patient-guide.jpeg", "Patient guide", width=Inches(3))
    p = doc.add_paragraph()
    run = p.add_run("Card heading: ")
    run.bold = True
    p.add_run("Patient guide")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "A patient-friendly guide explaining how to take LUMIVEX®, what to expect during the first "
        "weeks of treatment, and when to contact their healthcare professional. Available to share "
        "during consultations."
    )
    p = doc.add_paragraph()
    run = p.add_run("Card link: ")
    run.bold = True
    p.add_run("Download patient guide → /lumivex/resources")

    add_separator(doc)

    # Card 3
    add_image_with_caption(doc, "card-clinical-data.jpeg", "Clinical data summary", width=Inches(3))
    p = doc.add_paragraph()
    run = p.add_run("Card heading: ")
    run.bold = True
    p.add_run("LUMINANCE clinical data summary")
    p = doc.add_paragraph()
    run = p.add_run("Card body: ")
    run.bold = True
    p.add_run(
        "A comprehensive summary of key efficacy and safety data from the LUMINANCE-1, LUMINANCE-2, "
        "and LUMINANCE-3 studies, including primary and secondary endpoint results and long-term data."
    )
    p = doc.add_paragraph()
    run = p.add_run("Card link: ")
    run.bold = True
    p.add_run("Download clinical data summary → /lumivex/resources")

    add_separator(doc)

    # Section 3 — Contact
    add_heading(doc, "Section 3 — Medical information contact (two-column) | highlighted background", level=3, color=BRAND_COLOUR)
    p = doc.add_paragraph()
    run = p.add_run("Block: columns-teaser")
    run.bold = True
    run2 = p.add_run("  |  Section metadata: Style: highlight")
    run2.font.color.rgb = GREY_TEXT

    doc.add_paragraph()
    add_image_with_caption(doc, "contact-support.jpeg", "Medical information", width=Inches(3.5))

    p = doc.add_paragraph()
    run = p.add_run("Heading: ")
    run.bold = True
    p.add_run("Need further information?")

    p = doc.add_paragraph()
    run = p.add_run("Body text: ")
    run.bold = True
    p.add_run(
        "For medical information enquiries about LUMIVEX® (lumvecitinib), please contact AstraZeneca "
        "Medical Information:\n\n"
        "Online: contactazmedical.astrazeneca.com\n"
        "Telephone: 0800 783 0033\n\n"
        "Our medical information team is available to support healthcare professionals with clinical "
        "questions, requests for published data, and product-related enquiries."
    )

    add_separator(doc)

    # Accordion + metadata
    add_heading(doc, "Section 4 — Prescribing information footer", level=3, color=BRAND_COLOUR)
    add_body(doc, "Block: accordion  |  Expandable: PI | AE Reporting | References", italic=True)

    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run("Page metadata")
    run.bold = True
    run.font.color.rgb = AZ_MAGENTA
    add_body(doc, "Title: Resources | LUMIVEX® (lumvecitinib) | Prescribing & Patient Guides | AstraZeneca UK")
    add_body(doc, "Description: Download prescribing guides, patient materials, and clinical data summaries for LUMIVEX® (lumvecitinib) to support clinical decision-making in moderate-to-severe plaque psoriasis.")

    doc.add_page_break()

    # =========================================================================
    # 10. FOOTER CONTENT
    # =========================================================================
    add_heading(doc, "10. Footer Content", level=1, color=AZ_MAGENTA)

    footer_rows = [
        ("Row 1 — Brand", "AstraZeneca logo | GB-94281 | DOP: March 2026 | © 2026 AstraZeneca. All rights reserved."),
        ("Row 2 — Site links", "Efficacy | Safety | Dosing | Mechanism of Action | Resources"),
        ("Row 3 — Regulatory links", "Report Adverse Event (https://yellowcard.mhra.gov.uk/) | Medical Information (https://contactazmedical.astrazeneca.com/) | Privacy Policy (https://www.astrazeneca.co.uk/our-company/privacy-notice.html) | Terms of Use (https://www.astrazeneca.co.uk/our-company/terms-of-use.html) | Accessibility (https://www.astrazeneca.co.uk/accessibility.html)"),
        ("Row 4 — Date", "Date of Preparation: March 2026"),
    ]
    for label, val in footer_rows:
        p = doc.add_paragraph()
        run_b = p.add_run(f"{label}: ")
        run_b.bold = True
        run_v = p.add_run(val)
        run_v.font.size = Pt(10)

    add_separator(doc)

    # =========================================================================
    # 11. IMAGE ASSETS
    # =========================================================================
    add_heading(doc, "11. Image Assets", level=1, color=AZ_MAGENTA)

    add_body(doc, f"All images are available on CDN at {CDN_BASE}/")
    doc.add_paragraph()

    image_assets = [
        ("1", "hero-home.jpeg", "1440×810", "Home — hero"),
        ("2", "hero-efficacy.jpeg", "1440×810", "Efficacy — hero"),
        ("3", "hero-moa.jpeg", "1440×810", "Mechanism of Action — hero"),
        ("4", "card-efficacy.jpeg", "800×600", "Home — benefit card"),
        ("5", "card-safety.jpeg", "800×600", "Home — benefit card"),
        ("6", "card-dosing.jpeg", "800×600", "Home — benefit card"),
        ("7", "columns-moa.jpeg", "800×600", "Home — MoA teaser"),
        ("8", "tab-luminance1.jpeg", "800×600", "Efficacy — LUMINANCE-1 tab"),
        ("9", "tab-luminance2.jpeg", "800×600", "Efficacy — LUMINANCE-2 tab"),
        ("10", "columns-longterm.jpeg", "800×600", "Efficacy — long-term data"),
        ("11", "card-infections.jpeg", "800×600", "Safety — infection card"),
        ("12", "card-selectivity.jpeg", "800×600", "Safety — selectivity card"),
        ("13", "card-longterm-safety.jpeg", "800×600", "Safety — long-term card"),
        ("14", "columns-special-pops.jpeg", "800×600", "Safety — special populations"),
        ("15", "columns-admin.jpeg", "800×600", "Dosing — administration"),
        ("16", "columns-monitoring.jpeg", "800×600", "Dosing — monitoring"),
        ("17", "psoriatic-inflammation.jpeg", "800×600", "MoA — disease pathway"),
        ("18", "tyk2-il23-cascade.jpeg", "800×600", "MoA — TYK2 cascade"),
        ("19", "lumivex-blockade.jpeg", "800×600", "MoA — drug mechanism"),
        ("20", "card-prescribing.jpeg", "800×600", "Resources — prescribing guide"),
        ("21", "card-patient-guide.jpeg", "800×600", "Resources — patient guide"),
        ("22", "card-clinical-data.jpeg", "800×600", "Resources — clinical data"),
        ("23", "contact-support.jpeg", "800×600", "Resources — contact"),
    ]

    add_table(doc,
        ["#", "Filename", "Dimensions", "CDN URL", "Used on"],
        [(n, fn, dim, f"{CDN_BASE}/{fn}", usage) for n, fn, dim, usage in image_assets]
    )

    doc.add_paragraph()
    add_body(doc, f"Shared assets (also on CDN):")
    add_body(doc, f"• AstraZeneca logo: {CDN_BASE}/astrazeneca-logo.png")
    add_body(doc, f"• Search icon: {CDN_BASE}/search.svg")

    doc.add_paragraph()
    doc.add_paragraph()

    # Final footer
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("GB-94281 | DOP: March 2026 | © 2026 AstraZeneca. All rights reserved.")
    run.font.size = Pt(8)
    run.font.color.rgb = GREY_TEXT

    # Save
    doc.save(OUTPUT_PATH)
    print(f"DOCX saved to: {OUTPUT_PATH}")
    print(f"File size: {os.path.getsize(OUTPUT_PATH):,} bytes")


if __name__ == "__main__":
    build_document()
