import io
import re
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

# ── Colour Palette ──────────────────────────────────────────────────────────
PRIMARY      = colors.HexColor("#1E3A5F")
SECONDARY    = colors.HexColor("#2563EB")
ACCENT       = colors.HexColor("#059669")
GOLD         = colors.HexColor("#D97706")
LIGHT_BG     = colors.HexColor("#F0F4FF")
LIGHT_GREEN  = colors.HexColor("#ECFDF5")
LIGHT_GOLD   = colors.HexColor("#FFFBEB")
BORDER_COLOR = colors.HexColor("#CBD5E1")
TEXT_DARK    = colors.HexColor("#1E293B")
TEXT_MUTED   = colors.HexColor("#64748B")
WHITE        = colors.white
RED_ALERT    = colors.HexColor("#DC2626")


def _styles():
    base = getSampleStyleSheet()

    def add(name, **kw):
        if name not in base:
            base.add(ParagraphStyle(name=name, **kw))
        return base[name]

    add("CoverTitle",
        fontName="Helvetica-Bold", fontSize=28, textColor=WHITE,
        alignment=TA_CENTER, spaceAfter=8)
    add("CoverSubtitle",
        fontName="Helvetica", fontSize=14, textColor=colors.HexColor("#BFDBFE"),
        alignment=TA_CENTER, spaceAfter=6)
    add("CoverStudent",
        fontName="Helvetica-Bold", fontSize=18, textColor=GOLD,
        alignment=TA_CENTER, spaceAfter=4)
    add("SectionHeading",
        fontName="Helvetica-Bold", fontSize=15, textColor=WHITE,
        spaceAfter=10, spaceBefore=16, leading=20)
    add("SubHeading",
        fontName="Helvetica-Bold", fontSize=12, textColor=PRIMARY,
        spaceAfter=6, spaceBefore=10)
    add("Body",
        fontName="Helvetica", fontSize=10, textColor=TEXT_DARK,
        spaceAfter=5, leading=15, alignment=TA_JUSTIFY)
    add("BulletItem",
        fontName="Helvetica", fontSize=10, textColor=TEXT_DARK,
        spaceAfter=3, leading=14, leftIndent=14, bulletIndent=4)
    add("SmallMuted",
        fontName="Helvetica", fontSize=9, textColor=TEXT_MUTED,
        spaceAfter=3)
    add("Bold10",
        fontName="Helvetica-Bold", fontSize=10, textColor=TEXT_DARK,
        spaceAfter=4)
    add("Link",
        fontName="Helvetica", fontSize=9, textColor=SECONDARY,
        spaceAfter=3)
    add("AlertText",
        fontName="Helvetica-Bold", fontSize=10, textColor=RED_ALERT,
        spaceAfter=4)
    add("GreenText",
        fontName="Helvetica-Bold", fontSize=10, textColor=ACCENT,
        spaceAfter=4)
    return base


# ── Helpers ──────────────────────────────────────────────────────────────────

def _section_header(title: str, color=SECONDARY) -> list:
    """Blue/green banner with white title text."""
    table = Table([[Paragraph(title, _styles()["SectionHeading"])]],
                  colWidths=[170 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), color),
        ("ROUNDEDCORNERS", [6]),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING",   (0, 0), (-1, -1), 12),
    ]))
    return [Spacer(1, 6), table, Spacer(1, 8)]


def _info_box(text: str, bg=LIGHT_BG) -> list:
    """Coloured info box."""
    table = Table([[Paragraph(text, _styles()["Body"])]],
                  colWidths=[170 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("ROUNDEDCORNERS", [4]),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
    ]))
    return [table, Spacer(1, 6)]


def _two_col_table(rows: list) -> Table:
    """Key-value two-column table."""
    t = Table(rows, colWidths=[60 * mm, 110 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (0, -1), LIGHT_BG),
        ("FONTNAME",      (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME",      (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE",      (0, 0), (-1, -1), 10),
        ("TEXTCOLOR",     (0, 0), (0, -1), PRIMARY),
        ("TEXTCOLOR",     (1, 0), (1, -1), TEXT_DARK),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("GRID",          (0, 0), (-1, -1), 0.3, BORDER_COLOR),
    ]))
    return t


def _parse_guidance(guidance_text: str) -> dict:
    """
    Split raw LLM output into named sections using ## headings.
    Returns dict: {section_title: section_body_text}
    """
    sections = {}
    current = "Introduction"
    buf = []
    for line in guidance_text.splitlines():
        if line.startswith("## "):
            if buf:
                sections[current] = "\n".join(buf).strip()
            current = line[3:].strip()
            buf = []
        else:
            buf.append(line)
    if buf:
        sections[current] = "\n".join(buf).strip()
    return sections


def _render_text_section(text: str, styles) -> list:
    """
    Convert raw section text into Platypus flowables.
    Handles ### subheadings, - bullets, plain paragraphs.
    """
    story = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            story.append(Spacer(1, 4))
        elif stripped.startswith("### "):
            story.append(Paragraph(stripped[4:], styles["SubHeading"]))
        elif stripped.startswith("#### "):
            story.append(Paragraph(stripped[5:], styles["Bold10"]))
        elif stripped.startswith(("- ", "* ", "• ")):
            story.append(Paragraph("• " + stripped[2:], styles["BulletItem"]))
        elif stripped.startswith(("**", "__")) and stripped.endswith(("**", "__")):
            story.append(Paragraph(stripped.strip("*_"), styles["Bold10"]))
        else:
            clean = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", stripped)
            story.append(Paragraph(clean, styles["Body"]))
    return story


# ── Cover Page ────────────────────────────────────────────────────────────────

def _cover_page(profile: dict, styles) -> list:
    story = []

    # Header banner
    header = Table([
        [Paragraph("🎓  CAREER GUIDANCE REPORT", styles["CoverTitle"])],
        [Paragraph("Personalised Career Roadmap", styles["CoverSubtitle"])],
        [Paragraph(f"Prepared for: {profile.get('name', 'Student')}", styles["CoverStudent"])],
    ], colWidths=[170 * mm])
    header.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PRIMARY),
        ("TOPPADDING",    (0, 0), (-1, -1), 16),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 16),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("ROUNDEDCORNERS", [8]),
    ]))
    story.append(header)
    story.append(Spacer(1, 20))

    # Profile summary card
    level = profile.get("level", "")
    stream = profile.get("stream", "N/A")
    rows = [
        ["Education Level", level],
    ]
    if level == "Inter Completed":
        rows.append(["Stream", stream])
    rows += [
        ["Marks / Percentage", f"{profile.get('marks', '')}%"],
        ["District", profile.get("district", "")],
        ["State", profile.get("state", "")],
        ["Caste Category", profile.get("caste", "")],
        ["Family Annual Income", f"Rs {profile.get('income', '')}"],
        ["Gender", profile.get("gender", "")],
        ["Report Generated", datetime.now().strftime("%d %B %Y — %I:%M %p")],
    ]
    story.append(Paragraph("Student Profile Summary", styles["SubHeading"]))
    story.append(_two_col_table(rows))
    story.append(Spacer(1, 12))

    # Interests
    interests = profile.get("interests", [])
    if interests:
        story.append(Paragraph("Interests & Aptitudes", styles["SubHeading"]))
        interest_text = "  •  ".join(interests)
        story += _info_box(interest_text, LIGHT_BG)

    # Disclaimer
    story.append(Spacer(1, 16))
    disclaimer = (
        "<b>Note:</b> This report is AI-generated based on your profile and live data. "
        "Always verify exam dates and eligibility from official websites before applying. "
        "Career guidance is based on current trends — actual outcomes depend on individual effort and preparation."
    )
    story += _info_box(disclaimer, LIGHT_GOLD)
    story.append(PageBreak())
    return story


# ── Main Generator ────────────────────────────────────────────────────────────

def generate_pdf_report(guidance_data: dict) -> bytes:
    """
    Generate a complete PDF career guidance report.

    Args:
        guidance_data: dict with keys 'profile', 'guidance', 'profile_summary'

    Returns:
        PDF as bytes
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
        title="Career Guidance Report",
        author="Career Guidance Agent",
    )

    styles = _styles()
    profile = guidance_data.get("profile", {})
    guidance_text = guidance_data.get("guidance", "")

    story = []

    # ── Cover ────────────────────────────────────────────────────────────────
    story += _cover_page(profile, styles)

    # ── Parse guidance into sections ─────────────────────────────────────────
    sections = _parse_guidance(guidance_text)

    section_colors = {
        "SECTION 1": SECONDARY,
        "SECTION 2": colors.HexColor("#7C3AED"),
        "SECTION 3": ACCENT,
        "SECTION 4": colors.HexColor("#B45309"),
        "SECTION 5": colors.HexColor("#0891B2"),
        "SECTION 6": RED_ALERT,
        "SECTION 7": colors.HexColor("#059669"),
        "SECTION 8": PRIMARY,
    }

    # ── Introduction / pre-section content ───────────────────────────────────
    intro = sections.pop("Introduction", "").strip()
    if intro:
        story += _section_header("Career Guidance — Overview", SECONDARY)
        story += _render_text_section(intro, styles)
        story.append(Spacer(1, 10))

    # ── Remaining sections ────────────────────────────────────────────────────
    for title, body in sections.items():
        # Pick colour by section number keyword
        color = SECONDARY
        for k, c in section_colors.items():
            if k in title.upper():
                color = c
                break

        story += _section_header(title, color)
        story += _render_text_section(body, styles)
        story.append(Spacer(1, 8))

    # ── Footer page ───────────────────────────────────────────────────────────
    story.append(PageBreak())
    story += _section_header("Key Official Websites", PRIMARY)

    websites = [
        ("AP EAMCET", "sche.ap.gov.in"),
        ("TS EAMCET", "tsche.ac.in"),
        ("POLYCET AP", "polycetap.nic.in"),
        ("POLYCET TS", "polycetts.nic.in"),
        ("RGUKT / IIIT Basara", "rgukt.ac.in"),
        ("AP Scholarships (ePass)", "apepass.apcfss.in"),
        ("TS Scholarships (ePass)", "telanganaepass.cgg.gov.in"),
        ("National Scholarship Portal", "scholarships.gov.in"),
        ("APPSC", "appsc.gov.in"),
        ("TSPSC", "tspsc.gov.in"),
        ("SSC Jobs", "ssc.nic.in"),
        ("Railways Recruitment", "rrbapply.gov.in"),
        ("India Post GDS", "indiapost.gov.in"),
        ("NEET / JEE", "nta.ac.in"),
        ("JEE Main", "jeemain.nta.nic.in"),
        ("AP Police Recruitment", "slprb.ap.gov.in"),
        ("TS Police Recruitment", "tslprb.in"),
        ("Indian Army", "joinindianarmy.nic.in"),
        ("UPSC", "upsc.gov.in"),
        ("AP ITI Admissions", "apitiadmissions.nic.in"),
        ("TS ITI Admissions", "itits.telangana.gov.in"),
        ("APSSDC Skill Development", "apssdc.in"),
        ("TSSDC Skill Development", "tssdc.telangana.gov.in"),
        ("PMKVY", "pmkvyofficial.org"),
        ("CLAT (Law)", "consortiumofnlus.ac.in"),
        ("NALSAR Hyderabad", "nalsar.ac.in"),
        ("NIT Warangal", "nitw.ac.in"),
        ("IIT Hyderabad", "iith.ac.in"),
        ("Buddy4Study Scholarships", "buddy4study.com"),
    ]

    rows = [["Portal / Exam", "Website"]]
    for name, url in websites:
        rows.append([name, url])

    web_table = Table(rows, colWidths=[85 * mm, 85 * mm])
    web_table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR",     (0, 0), (-1, 0), WHITE),
        ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 9),
        ("FONTNAME",      (0, 1), (-1, -1), "Helvetica"),
        ("TEXTCOLOR",     (0, 1), (-1, -1), TEXT_DARK),
        ("TEXTCOLOR",     (1, 1), (1, -1), SECONDARY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
        ("GRID",          (0, 0), (-1, -1), 0.3, BORDER_COLOR),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
    ]))
    story.append(web_table)
    story.append(Spacer(1, 20))

    # Closing message
    closing = Table([[
        Paragraph(
            "Best of luck on your career journey! Remember — consistency beats talent. "
            "Start today, take one step at a time, and never stop learning. "
            "Your hard work will definitely pay off. 🌟",
            styles["Body"]
        )
    ]], colWidths=[170 * mm])
    closing.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GREEN),
        ("ROUNDEDCORNERS", [6]),
        ("TOPPADDING",    (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ("LEFTPADDING",   (0, 0), (-1, -1), 14),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 14),
        ("BOX", (0, 0), (-1, -1), 1, ACCENT),
    ]))
    story.append(closing)

    # ── Build PDF ─────────────────────────────────────────────────────────────
    def _header_footer(canvas, doc):
        canvas.saveState()
        # Header line
        canvas.setStrokeColor(SECONDARY)
        canvas.setLineWidth(1.5)
        canvas.line(18 * mm, A4[1] - 12 * mm, A4[0] - 18 * mm, A4[1] - 12 * mm)
        canvas.setFont("Helvetica-Bold", 8)
        canvas.setFillColor(PRIMARY)
        canvas.drawString(18 * mm, A4[1] - 10 * mm, "Career Guidance Report")
        canvas.drawRightString(
            A4[0] - 18 * mm, A4[1] - 10 * mm,
            f"{profile.get('name', 'Student')} | {profile.get('level', '')}"
        )
        # Footer line
        canvas.setStrokeColor(BORDER_COLOR)
        canvas.line(18 * mm, 12 * mm, A4[0] - 18 * mm, 12 * mm)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(TEXT_MUTED)
        canvas.drawString(18 * mm, 8 * mm, "Generated by Career Guidance Agent")
        canvas.drawRightString(
            A4[0] - 18 * mm, 8 * mm,
            f"Page {doc.page} | {datetime.now().strftime('%d %b %Y')}"
        )
        canvas.restoreState()

    doc.build(story, onFirstPage=_header_footer, onLaterPages=_header_footer)
    return buffer.getvalue()
