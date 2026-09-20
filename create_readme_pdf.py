from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import mm
import os
import re


# ============================================================
# CIVICEYE AI — README PDF
# FIXED 11-PAGE COMPETITION DOCUMENT
# ============================================================

OUTPUT_FILE = "CivicEye_AI_README.pdf"

PAGE_W, PAGE_H = A4


# ============================================================
# COLORS
# ============================================================

NAVY = HexColor("#0B192C")
BLUE = HexColor("#0084FF")
CYAN = HexColor("#00D2FF")
ICE = HexColor("#F8FAFC")
LIGHT = HexColor("#E2E8F0")
TEXT = HexColor("#111827")
MUTED = HexColor("#64748B")
WHITE = colors.white
SOFT_BLUE = HexColor("#EAF5FF")
SOFT_CYAN = HexColor("#ECFEFF")


# ============================================================
# FONT
# ============================================================

FONT_REGULAR = "Helvetica"
FONT_BOLD = "Helvetica-Bold"

font_candidates = [
    ("Inter", r"C:\Windows\Fonts\Inter-Regular.ttf",
     r"C:\Windows\Fonts\Inter-Bold.ttf"),
    ("Montserrat", r"C:\Windows\Fonts\Montserrat-Regular.ttf",
     r"C:\Windows\Fonts\Montserrat-Bold.ttf"),
    ("Roboto", r"C:\Windows\Fonts\Roboto-Regular.ttf",
     r"C:\Windows\Fonts\Roboto-Bold.ttf"),
]

for name, regular, bold in font_candidates:
    if os.path.exists(regular) and os.path.exists(bold):
        pdfmetrics.registerFont(TTFont(name, regular))
        pdfmetrics.registerFont(TTFont(name + "-Bold", bold))
        FONT_REGULAR = name
        FONT_BOLD = name + "-Bold"
        break


# ============================================================
# STYLES
# ============================================================

BODY = ParagraphStyle(
    "CE_BODY",
    fontName=FONT_REGULAR,
    fontSize=8.2,
    leading=11.0,
    textColor=TEXT,
    alignment=TA_LEFT,
    spaceAfter=4,
)

BODY_SMALL = ParagraphStyle(
    "CE_BODY_SMALL",
    fontName=FONT_REGULAR,
    fontSize=7.7,
    leading=9.7,
    textColor=TEXT,
)

BODY_TIGHT = ParagraphStyle(
    "CE_BODY_TIGHT",
    fontName=FONT_REGULAR,
    fontSize=7.9,
    leading=9.7,
    textColor=TEXT,
)

BULLET = ParagraphStyle(
    "CE_BULLET",
    fontName=FONT_REGULAR,
    fontSize=7.9,
    leading=10.0,
    textColor=TEXT,
    leftIndent=8,
    firstLineIndent=-6,
    spaceAfter=2,
)

SUBHEAD = ParagraphStyle(
    "CE_SUBHEAD",
    fontName=FONT_BOLD,
    fontSize=9.0,
    leading=11,
    textColor=NAVY,
    spaceAfter=3,
)

FEATURE_HEAD = ParagraphStyle(
    "CE_FEATURE_HEAD",
    fontName=FONT_BOLD,
    fontSize=8.5,
    leading=10,
    textColor=NAVY,
    spaceAfter=2,
)

FLOW_TEXT = ParagraphStyle(
    "CE_FLOW_TEXT",
    fontName=FONT_BOLD,
    fontSize=7.8,
    leading=9.3,
    textColor=NAVY,
    alignment=TA_CENTER,
)

CODE_TEXT = ParagraphStyle(
    "CE_CODE_TEXT",
    fontName="Courier",
    fontSize=7.4,
    leading=9.2,
    textColor=NAVY,
)


# ============================================================
# BASIC HELPERS
# ============================================================

def para(c, text, x, y, width, style=BODY):
    """
    Draw a Paragraph with its top-left corner at x,y.
    Returns the new y position.
    """
    text = text.strip()
    if not text:
        return y

    p = Paragraph(text, style)
    w, h = p.wrap(width, PAGE_H)
    p.drawOn(c, x, y - h)
    return y - h


def line(c, x1, y1, x2, y2, color=LIGHT, width=0.7):
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.line(x1, y1, x2, y2)


def rounded_box(c, x, y, w, h, fill=WHITE, stroke=LIGHT, radius=5):
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.setLineWidth(0.7)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=1)


def section_header(c, number, title, y, subtitle=None):
    """
    Returns y below header.
    """
    x = 18 * mm

    # Number badge
    c.setFillColor(BLUE)
    c.roundRect(x, y - 10 * mm, 13 * mm, 9 * mm, 3 * mm, fill=1, stroke=0)

    c.setFillColor(WHITE)
    c.setFont(FONT_BOLD, 9)
    c.drawCentredString(
        x + 6.5 * mm,
        y - 7.1 * mm,
        f"{number:02d}"
    )

    # Heading
    c.setFillColor(NAVY)
    c.setFont(FONT_BOLD, 15)
    c.drawString(x + 17 * mm, y - 6.8 * mm, title)

    # Accent line
    line(
        c,
        x + 17 * mm,
        y - 11.5 * mm,
        PAGE_W - 18 * mm,
        y - 11.5 * mm,
        BLUE,
        1.0
    )

    new_y = y - 17 * mm

    if subtitle:
        new_y = para(
            c,
            subtitle,
            x,
            new_y,
            PAGE_W - 36 * mm,
            BODY
        ) - 2 * mm

    return new_y


def footer(c, page_no):
    c.setStrokeColor(LIGHT)
    c.setLineWidth(0.6)
    c.line(
        18 * mm,
        13 * mm,
        PAGE_W - 18 * mm,
        13 * mm
    )

    c.setFillColor(MUTED)
    c.setFont(FONT_REGULAR, 7)

    c.drawString(
        18 * mm,
        8 * mm,
        "CivicEye AI · YCS 2026 · Sri Lanka"
    )

    c.drawRightString(
        PAGE_W - 18 * mm,
        8 * mm,
        f"Page {page_no} of 11"
    )


def top_title(c, text, y=277 * mm):
    c.setFillColor(NAVY)
    c.setFont(FONT_BOLD, 15)
    c.drawString(18 * mm, y, text)

    line(
        c,
        18 * mm,
        y - 4 * mm,
        PAGE_W - 18 * mm,
        y - 4 * mm,
        BLUE,
        1
    )

    return y - 10 * mm


# ============================================================
# FLOWCHART
# ============================================================

def draw_vertical_flow(
    c,
    steps,
    x,
    top_y,
    width,
    box_h=10 * mm,
    gap=5 * mm,
    font_style=FLOW_TEXT
):
    current_y = top_y

    for i, step in enumerate(steps):

        box_y = current_y - box_h

        rounded_box(
            c,
            x,
            box_y,
            width,
            box_h,
            fill=SOFT_BLUE,
            stroke=HexColor("#B9DDFB"),
            radius=4
        )

        p = Paragraph(step, font_style)
        pw, ph = p.wrap(width - 8 * mm, box_h)
        p.drawOn(
            c,
            x + 4 * mm,
            box_y + (box_h - ph) / 2
        )

        current_y = box_y

        if i < len(steps) - 1:
            arrow_x = x + width / 2

            c.setStrokeColor(BLUE)
            c.setFillColor(BLUE)
            c.setLineWidth(1.2)

            c.line(
                arrow_x,
                current_y,
                arrow_x,
                current_y - gap + 1.5 * mm
            )

            c.line(
                arrow_x,
                current_y - gap + 1.5 * mm,
                arrow_x - 1.5 * mm,
                current_y - gap + 3 * mm
            )

            c.line(
                arrow_x,
                current_y - gap + 1.5 * mm,
                arrow_x + 1.5 * mm,
                current_y - gap + 3 * mm
            )

            current_y -= gap

    return current_y


def draw_horizontal_arrow(c, x, y, width):
    c.setStrokeColor(BLUE)
    c.setFillColor(BLUE)
    c.setLineWidth(1.2)

    c.line(x, y, x + width - 4 * mm, y)

    c.line(
        x + width - 7 * mm,
        y + 2 * mm,
        x + width - 2 * mm,
        y
    )

    c.line(
        x + width - 7 * mm,
        y - 2 * mm,
        x + width - 2 * mm,
        y
    )


# ============================================================
# WORKFLOW COLUMN
# ============================================================

def workflow_column(
    c,
    title,
    steps,
    x,
    top_y,
    width
):
    c.setFillColor(NAVY)
    c.setFont(FONT_BOLD, 10)
    c.drawString(x, top_y, title)

    y = top_y - 7 * mm

    box_h = 8.7 * mm

    for i, step in enumerate(steps):

        rounded_box(
            c,
            x,
            y - box_h,
            width,
            box_h,
            fill=ICE,
            stroke=LIGHT,
            radius=3
        )

        p = Paragraph(
            step,
            ParagraphStyle(
                "CE_FLOW_COLUMN",
                parent=FLOW_TEXT,
                fontSize=7.1,
                leading=8.2,
            )
        )

        pw, ph = p.wrap(width - 5 * mm, box_h)
        p.drawOn(
            c,
            x + 2.5 * mm,
            y - box_h + (box_h - ph) / 2
        )

        y -= box_h

        if i < len(steps) - 1:
            c.setStrokeColor(BLUE)
            c.setLineWidth(0.8)

            cx = x + width / 2

            c.line(
                cx,
                y,
                cx,
                y - 3 * mm
            )

            c.line(
                cx,
                y - 3 * mm,
                cx - 1.2 * mm,
                y - 1.5 * mm
            )

            c.line(
                cx,
                y - 3 * mm,
                cx + 1.2 * mm,
                y - 1.5 * mm
            )

            y -= 4 * mm

    return y


# ============================================================
# PAGE 1 — COVER
# ============================================================

def page_1(c):

    # Background
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    # Decorative cyan shapes
    c.setFillColor(HexColor("#12345A"))
    c.circle(PAGE_W - 15 * mm, PAGE_H - 20 * mm, 42 * mm, fill=1, stroke=0)

    c.setFillColor(HexColor("#0F2A49"))
    c.circle(12 * mm, 30 * mm, 38 * mm, fill=1, stroke=0)

    # Eye icon
    cx = PAGE_W / 2
    cy = 205 * mm

    c.setStrokeColor(CYAN)
    c.setLineWidth(4)

    c.bezier(
        cx - 24 * mm, cy,
        cx - 12 * mm, cy + 16 * mm,
        cx + 12 * mm, cy + 16 * mm,
        cx + 24 * mm, cy
    )

    c.bezier(
        cx - 24 * mm, cy,
        cx - 12 * mm, cy - 16 * mm,
        cx + 12 * mm, cy - 16 * mm,
        cx + 24 * mm, cy
    )

    c.setFillColor(CYAN)
    c.circle(cx, cy, 7 * mm, fill=1, stroke=0)

    c.setFillColor(NAVY)
    c.circle(cx, cy, 3 * mm, fill=1, stroke=0)

    # Title
    c.setFillColor(WHITE)
    c.setFont(FONT_BOLD, 31)
    c.drawCentredString(
        cx,
        155 * mm,
        "CIVICEYE AI"
    )

    c.setFillColor(CYAN)
    c.setFont(FONT_BOLD, 13)
    c.drawCentredString(
        cx,
        143 * mm,
        "YCS 2026"
    )

    c.setFillColor(WHITE)
    c.setFont(FONT_REGULAR, 11)
    c.drawCentredString(
        cx,
        134 * mm,
        "AI-Powered Civic Issue Reporting Platform"
    )

    c.setFillColor(HexColor("#B8D9F5"))
    c.setFont(FONT_REGULAR, 10)
    c.drawCentredString(
        cx,
        124 * mm,
        "Sri Lanka"
    )

    # Bottom badge
    rounded_box(
        c,
        cx - 34 * mm,
        45 * mm,
        68 * mm,
        12 * mm,
        fill=HexColor("#102A49"),
        stroke=HexColor("#25547C"),
        radius=6
    )

    c.setFillColor(WHITE)
    c.setFont(FONT_REGULAR, 8.5)
    c.drawCentredString(
        cx,
        49.5 * mm,
        "Competition Prototype · YCS 2026"
    )

    c.setFillColor(HexColor("#9BB8D4"))
    c.setFont(FONT_REGULAR, 7.5)
    c.drawCentredString(
        cx,
        27 * mm,
        "CivicEye AI · YCS 2026 · Sri Lanka"
    )


# ============================================================
# PAGE 2 — SECTIONS 1 + 2
# ============================================================

def page_2(c):

    y = 277 * mm

    y = section_header(c, 1, "PROJECT OVERVIEW", y)

    overview = [
        "CivicEye AI is an AI-assisted civic issue reporting and "
        "monitoring web application developed as a competition "
        "prototype for YCS 2026.",

        "The platform is designed to help citizens report common "
        "public issues such as road damage, garbage, water leaks, "
        "and faulty street lights through a structured digital "
        "workflow.",

        "Citizens can submit issue information including an image, "
        "issue type, description, and location. The system then "
        "performs AI-assisted analysis using programmed rules and "
        "keyword matching to support issue categorization, priority "
        "assessment, and authority recommendation.",

        "The platform also demonstrates duplicate detection, "
        "citizen notifications, report tracking, resolution "
        "verification, and an administrator dashboard."
    ]

    for p in overview:
        y = para(c, p, 18 * mm, y, PAGE_W - 36 * mm, BODY)
        y -= 1.5 * mm

    rounded_box(
        c,
        18 * mm,
        y - 23 * mm,
        PAGE_W - 36 * mm,
        20 * mm,
        fill=SOFT_CYAN,
        stroke=HexColor("#A5EAF2"),
        radius=5
    )

    y = para(
        c,
        "<b>Prototype Scope:</b> CivicEye AI is a prototype and is "
        "not currently connected to an official Municipal Council, "
        "government authority, emergency service, or production "
        "government database.",
        23 * mm,
        y - 6 * mm,
        PAGE_W - 46 * mm,
        BODY_TIGHT
    )

    y -= 12 * mm

    y = section_header(c, 2, "PROBLEM", y)

    problem = (
        "Public issues such as damaged roads, garbage accumulation, "
        "water leaks, and faulty street lights require an organized "
        "way for citizens to report them and for responsible "
        "authorities to monitor them."
    )

    y = para(c, problem, 18 * mm, y, PAGE_W - 36 * mm, BODY)

    y -= 1 * mm

    y = para(
        c,
        "<b>Traditional reporting processes may involve difficulties such as:</b>",
        18 * mm,
        y,
        PAGE_W - 36 * mm,
        BODY
    )

    bullets = [
        "Unclear reporting channels",
        "Incomplete complaint information",
        "Difficulty identifying the relevant authority",
        "Repeated or duplicate complaints",
        "Limited visibility of complaint progress",
        "Difficulty identifying higher-priority issues",
        "Language barriers for some citizens",
    ]

    for item in bullets:
        y = para(
            c,
            f"• {item}",
            21 * mm,
            y,
            PAGE_W - 42 * mm,
            BULLET
        )

    y -= 1 * mm

    para(
        c,
        "CivicEye AI addresses these challenges through a structured "
        "digital reporting workflow that combines citizen input, "
        "AI-assisted analysis, location information, priority "
        "assessment, authority recommendation, duplicate detection, "
        "notifications, and report tracking.",
        18 * mm,
        y,
        PAGE_W - 36 * mm,
        BODY_TIGHT
    )

    footer(c, 2)


# ============================================================
# PAGE 3 — SECTION 3
# ============================================================

def page_3(c):

    y = 277 * mm

    y = section_header(c, 3, "PROPOSED SOLUTION", y)

    y = para(
        c,
        "CivicEye AI provides a single web-based platform where "
        "citizens can create and monitor civic issue reports.",
        18 * mm,
        y,
        PAGE_W - 36 * mm,
        BODY
    )

    y -= 2 * mm

    c.setFillColor(MUTED)
    c.setFont(FONT_BOLD, 8)
    c.drawString(18 * mm, y, "THE GENERAL WORKFLOW IS:")

    y -= 7 * mm

    steps = [
        "Citizen",
        "Create Report",
        "Upload Image + Enter Issue Details",
        "AI-Assisted Analysis",
        "Issue Categorization",
        "Priority Assessment",
        "Authority Recommendation",
        "Report Tracking",
        "Notifications",
        "Resolution Verification",
    ]

    draw_vertical_flow(
        c,
        steps,
        55 * mm,
        y,
        100 * mm,
        box_h=10.5 * mm,
        gap=4.5 * mm
    )

    bottom_y = 43 * mm

    rounded_box(
        c,
        18 * mm,
        bottom_y,
        PAGE_W - 36 * mm,
        25 * mm,
        fill=ICE,
        stroke=LIGHT,
        radius=5
    )

    para(
        c,
        "The system is designed to make the reporting process more "
        "structured while providing administrators with a dashboard "
        "for monitoring submitted reports.",
        24 * mm,
        bottom_y + 18 * mm,
        PAGE_W - 48 * mm,
        BODY
    )

    footer(c, 3)


# ============================================================
# PAGE 4 — SECTION 4
# ============================================================

def page_4(c):

    y = 277 * mm

    y = section_header(c, 4, "MAIN FEATURES", y)

    features = [
        (
            "4.1 AI-Assisted Issue Categorization",
            "The system analyzes the submitted issue information using "
            "programmed rules and keyword matching to determine the "
            "likely issue category.",
            "Supported example categories include: Road Damage · Garbage · "
            "Water Leak · Faulty Street Light"
        ),
        (
            "4.2 Image-Based Reporting",
            "Citizens can upload an image related to the reported issue. "
            "The image provides supporting visual information for the "
            "submitted complaint.",
            "The current prototype does not use a trained computer-vision "
            "model for image classification."
        ),
        (
            "4.3 Location Support",
            "Citizens can enter or capture the location associated with "
            "the reported issue.",
            "Browser geolocation functionality depends on browser support "
            "and user permission."
        ),
        (
            "4.4 Priority Assessment",
            "The system provides an AI-assisted priority assessment based "
            "on programmed rules and issue information.",
            "This is intended to demonstrate how reports could be "
            "prioritized in a future production system."
        ),
        (
            "4.5 Authority Recommendation",
            "Based on the issue category, the system can recommend a "
            "relevant authority for the reported issue.",
            "This recommendation is part of the prototype workflow and "
            "does not directly submit complaints to government authorities."
        ),
        (
            "4.6 Multilingual Interaction",
            "The platform is designed to support English, Tamil, and "
            "Sinhala user interaction.",
            "Voice recognition functionality depends on browser support "
            "and user permissions."
        ),
    ]

    col_x = [18 * mm, 108 * mm]
    col_w = 82 * mm

    for index, feature in enumerate(features):

        col = index % 2

        if col == 0:
            y_row = y

        x = col_x[col]

        rounded_box(
            c,
            x,
            y_row - 34 * mm,
            col_w,
            31 * mm,
            fill=WHITE,
            stroke=LIGHT,
            radius=5
        )

        c.setFillColor(BLUE)
        c.circle(
            x + 6 * mm,
            y_row - 7 * mm,
            2.2 * mm,
            fill=1,
            stroke=0
        )

        para(
            c,
            feature[0],
            x + 11 * mm,
            y_row - 4.5 * mm,
            col_w - 15 * mm,
            FEATURE_HEAD
        )

        yy = y_row - 12 * mm

        yy = para(
            c,
            feature[1],
            x + 5 * mm,
            yy,
            col_w - 10 * mm,
            BODY_SMALL
        )

        para(
            c,
            feature[2],
            x + 5 * mm,
            yy - 1.5 * mm,
            col_w - 10 * mm,
            BODY_SMALL
        )

        if col == 1:
            y -= 37 * mm

    # Lower features 4.7 - 4.12
    lower = [
        ("4.7 Duplicate Detection",
         "The backend checks submitted reports for potentially matching "
         "existing reports using relevant report information such as "
         "issue type and location. This helps demonstrate how repeated "
         "complaints could be identified."),
        ("4.8 Citizen Notifications",
         "Citizens can receive notifications related to report activity "
         "and status changes."),
        ("4.9 Admin Alerts",
         "The administrator interface supports monitoring of relevant "
         "report activity."),
        ("4.10 Report Tracking",
         "Citizens can view submitted reports and monitor their current "
         "status."),
        ("4.11 Resolution Verification",
         "The prototype provides a citizen-facing resolution verification "
         "interaction after an issue is marked as solved."),
        ("4.12 Administrator Dashboard",
         "Administrators can review submitted reports and update their "
         "status."),
    ]

    # Compact two-column lower cards
    for i, (head, desc) in enumerate(lower):

        col = i % 2

        if col == 0:
            y -= 3 * mm
            row_y = y

        x = col_x[col]

        rounded_box(
            c,
            x,
            row_y - 19 * mm,
            col_w,
            17 * mm,
            fill=ICE,
            stroke=LIGHT,
            radius=4
        )

        yy = para(
            c,
            head,
            x + 4 * mm,
            row_y - 4 * mm,
            col_w - 8 * mm,
            FEATURE_HEAD
        )

        para(
            c,
            desc,
            x + 4 * mm,
            yy - 1 * mm,
            col_w - 8 * mm,
            BODY_SMALL
        )

        if col == 1:
            y = row_y - 21 * mm

    # Status flow
    y -= 4 * mm

    c.setFillColor(MUTED)
    c.setFont(FONT_BOLD, 7.5)
    c.drawString(18 * mm, y, "EXAMPLE STATUS FLOW")

    y -= 8 * mm

    statuses = ["Pending", "Processing", "Solved"]

    sx = 42 * mm
    sw = 38 * mm

    for i, status in enumerate(statuses):

        rounded_box(
            c,
            sx + i * 48 * mm,
            y - 9 * mm,
            sw,
            9 * mm,
            fill=SOFT_BLUE,
            stroke=HexColor("#B9DDFB"),
            radius=4
        )

        c.setFillColor(NAVY)
        c.setFont(FONT_BOLD, 7.5)
        c.drawCentredString(
            sx + i * 48 * mm + sw / 2,
            y - 5.8 * mm,
            status
        )

        if i < 2:
            draw_horizontal_arrow(
                c,
                sx + i * 48 * mm + sw + 2 * mm,
                y - 4.5 * mm,
                8 * mm
            )

    footer(c, 4)


# ============================================================
# PAGE 5 — SECTION 5
# ============================================================

def page_5(c):

    y = 277 * mm

    y = section_header(c, 5, "USER WORKFLOW", y)

    citizen_steps = [
        "Open CivicEye AI.",
        "Login as a citizen.",
        "Open the Citizen Portal.",
        "Select Report New Issue.",
        "Upload an issue image.",
        "Select the issue type.",
        "Enter a description.",
        "Enter or capture the location.",
        "Submit the complaint.",
        "View the AI-assisted analysis result.",
        "Open the Citizen Dashboard.",
        "Check the submitted report and notification.",
    ]

    admin_steps = [
        "Open Admin Login.",
        "Open the Admin Dashboard.",
        "Review submitted reports.",
        "Open a report.",
        "Review the report information.",
        "Change the status from Pending to Processing.",
        "Change the status from Processing to Solved.",
        "Verify the updated status and generated notifications.",
    ]

    margin = 18 * mm
    gap = 7 * mm
    col_w = (PAGE_W - 2 * margin - gap) / 2

    workflow_column(
        c,
        "Citizen Workflow",
        citizen_steps,
        margin,
        y,
        col_w
    )

    workflow_column(
        c,
        "Admin Workflow",
        admin_steps,
        margin + col_w + gap,
        y,
        col_w
    )

    footer(c, 5)


# ============================================================
# PAGE 6 — SECTION 6
# ============================================================

def page_6(c):

    y = 277 * mm

    y = section_header(c, 6, "TECHNOLOGIES USED", y)

    blocks = [
        (
            "Frontend",
            [
                "HTML5",
                "CSS3",
                "JavaScript",
            ],
        ),
        (
            "Backend",
            [
                "Node.js",
                "Express.js",
                "CORS",
                "Multer",
                "dotenv",
            ],
        ),
        (
            "Development and Deployment",
            [
                "Visual Studio Code",
                "Git / GitHub",
                "Vercel",
                "Railway",
            ],
        ),
        (
            "Browser-based capabilities",
            [
                "Geolocation API",
                "Web Speech / Voice Recognition support where available",
            ],
        ),
    ]

    box_w = 82 * mm
    box_h = 47 * mm

    positions = [
        (18 * mm, y - box_h),
        (108 * mm, y - box_h),
        (18 * mm, y - box_h - 55 * mm),
        (108 * mm, y - box_h - 55 * mm),
    ]

    for (title, items), (x, box_y) in zip(blocks, positions):

        rounded_box(
            c,
            x,
            box_y,
            box_w,
            box_h,
            fill=WHITE,
            stroke=LIGHT,
            radius=6
        )

        c.setFillColor(BLUE)
        c.rect(
            x,
            box_y + box_h - 2.5 * mm,
            box_w,
            2.5 * mm,
            fill=1,
            stroke=0
        )

        c.setFillColor(NAVY)
        c.setFont(FONT_BOLD, 10)
        c.drawString(
            x + 6 * mm,
            box_y + box_h - 10 * mm,
            title
        )

        yy = box_y + box_h - 18 * mm

        for item in items:
            yy = para(
                c,
                f"• {item}",
                x + 6 * mm,
                yy,
                box_w - 12 * mm,
                BODY
            )

    footer(c, 6)


# ============================================================
# PAGE 7 — SECTION 7
# ============================================================

def page_7(c):

    y = 277 * mm

    y = section_header(c, 7, "SYSTEM ARCHITECTURE", y)

    y = para(
        c,
        "The CivicEye AI prototype follows a frontend-backend architecture.",
        18 * mm,
        y,
        PAGE_W - 36 * mm,
        BODY
    )

    y -= 2 * mm

    architecture = [
        "Citizen / Admin",
        "Web Frontend",
        "JavaScript",
        "HTTP API",
        "Node.js + Express Backend",
        "Report Processing",
        "Duplicate Detection",
        "Notifications / Admin Alerts",
    ]

    draw_vertical_flow(
        c,
        architecture,
        51 * mm,
        y,
        108 * mm,
        box_h=11 * mm,
        gap=5 * mm
    )

    bottom_y = 39 * mm

    rounded_box(
        c,
        18 * mm,
        bottom_y,
        PAGE_W - 36 * mm,
        29 * mm,
        fill=ICE,
        stroke=LIGHT,
        radius=5
    )

    yy = bottom_y + 21 * mm

    yy = para(
        c,
        "The frontend communicates with the backend through HTTP API requests.",
        24 * mm,
        yy,
        PAGE_W - 48 * mm,
        BODY
    )

    para(
        c,
        "The backend handles report processing, duplicate detection, status "
        "management, notifications, and related application logic.",
        24 * mm,
        yy - 2 * mm,
        PAGE_W - 48 * mm,
        BODY
    )

    footer(c, 7)


# ============================================================
# PAGE 8 — SECTIONS 8 + 9
# ============================================================

def page_8(c):

    y = 277 * mm

    y = section_header(c, 8, "PROJECT STRUCTURE", y)

    y = para(
        c,
        "<b>Main frontend pages include:</b>",
        18 * mm,
        y,
        PAGE_W - 36 * mm,
        BODY
    )

    pages = [
        "index.html",
        "login.html",
        "citizen.html",
        "admin.html",
        "report.html",
        "ai-processing.html",
        "track.html",
        "profile.html",
        "settings.html",
        "notifications.html",
        "privacy.html",
    ]

    # Code-like grid
    start_x = 18 * mm
    start_y = y
    box_w = 55 * mm
    box_h = 8.5 * mm

    for i, item in enumerate(pages):

        col = i % 3
        row = i // 3

        x = start_x + col * 60 * mm
        yy = start_y - row * 11 * mm

        rounded_box(
            c,
            x,
            yy - box_h,
            box_w,
            box_h,
            fill=ICE,
            stroke=LIGHT,
            radius=3
        )

        c.setFillColor(NAVY)
        c.setFont("Courier", 7.4)
        c.drawString(
            x + 4 * mm,
            yy - 5.7 * mm,
            item
        )

    rows = (len(pages) + 2) // 3
    y = start_y - rows * 11 * mm - 3 * mm

    y = para(
        c,
        "<b>Supporting frontend files include:</b>",
        18 * mm,
        y,
        PAGE_W - 36 * mm,
        BODY
    )

    for item in ["script.js", "style.css", "images/"]:
        y = para(
            c,
            f"• {item}",
            21 * mm,
            y,
            PAGE_W - 42 * mm,
            BODY
        )

    y = para(
        c,
        "Backend files contain the Node.js and Express server, "
        "configuration, and supporting backend logic.",
        18 * mm,
        y - 1 * mm,
        PAGE_W - 36 * mm,
        BODY
    )

    y -= 3 * mm

    y = section_header(c, 9, "DEPLOYMENT", y)

    deployment = [
        (
            "Frontend",
            "The frontend can be deployed as a web application using Vercel."
        ),
        (
            "Backend",
            "The backend is deployed using Railway."
        ),
        (
            "API Communication",
            "The frontend communicates with the deployed backend through "
            "the configured backend API URL."
        ),
        (
            "PORT",
            "The backend uses the environment variable PORT when provided."
        ),
        (
            "Railway",
            "When deployed on Railway, the platform-provided port is used."
        ),
    ]

    for title, desc in deployment:
        rounded_box(
            c,
            18 * mm,
            y - 18 * mm,
            PAGE_W - 36 * mm,
            15 * mm,
            fill=WHITE,
            stroke=LIGHT,
            radius=4
        )

        c.setFillColor(BLUE)
        c.setFont(FONT_BOLD, 8)
        c.drawString(
            23 * mm,
            y - 6 * mm,
            title
        )

        para(
            c,
            desc,
            65 * mm,
            y - 4 * mm,
            PAGE_W - 88 * mm,
            BODY_SMALL
        )

        y -= 19 * mm

    footer(c, 8)


# ============================================================
# PAGE 9 — SECTION 10
# ============================================================

def page_9(c):

    y = 277 * mm

    y = section_header(c, 10, "TESTING WORKFLOW", y)

    citizen_test = [
        "Open CivicEye AI.",
        "Select Citizen Login.",
        "Open the Citizen Portal.",
        "Select Report New Issue.",
        "Upload an issue image.",
        "Select the issue type.",
        "Enter a description.",
        "Enter or capture the location.",
        "Submit the complaint.",
        "View the AI-assisted analysis result.",
        "Open the Citizen Dashboard.",
        "Check the submitted report and notification.",
    ]

    duplicate_test = [
        "Submit a report with a specific issue type and location.",
        "Submit another report using the same issue type and location.",
        "The backend checks for an existing matching report.",
        "The second submission is identified as a duplicate.",
    ]

    admin_test = [
        "Open Admin Login.",
        "Open the Admin Dashboard.",
        "Review submitted reports.",
        "Open a report.",
        "Change the status from Pending to Processing.",
        "Change the status from Processing to Solved.",
        "Verify the updated status and generated notifications.",
    ]

    margin = 12 * mm
    gap = 5 * mm
    col_w = (PAGE_W - 2 * margin - 2 * gap) / 3

    workflow_column(
        c,
        "Citizen Report Test",
        citizen_test,
        margin,
        y,
        col_w
    )

    workflow_column(
        c,
        "Duplicate Detection Test",
        duplicate_test,
        margin + col_w + gap,
        y,
        col_w
    )

    workflow_column(
        c,
        "Admin Test",
        admin_test,
        margin + 2 * (col_w + gap),
        y,
        col_w
    )

    footer(c, 9)


# ============================================================
# PAGE 10 — SECTIONS 11 + 12
# ============================================================

def page_10(c):

    y = 277 * mm

    y = section_header(c, 11, "IMPORTANT PROTOTYPE LIMITATIONS", y)

    limitations = [
        (
            "Rule-Based AI",
            "The current AI-assisted analysis uses programmed rules and "
            "keyword matching. It does not currently use a trained "
            "machine-learning model or external AI API."
        ),
        (
            "Confidence Display",
            "The current prototype displays a predefined confidence value "
            "for demonstration purposes. It should not be interpreted "
            "as a statistically calibrated machine-learning confidence score."
        ),
        (
            "Data Storage",
            "Reports and notifications are currently stored in server "
            "memory. Therefore, the prototype does not provide permanent "
            "database storage."
        ),
        (
            "Authentication",
            "The current login system is designed for prototype "
            "demonstration and does not provide production-grade "
            "authentication."
        ),
        (
            "Resolution Verification",
            "The citizen resolution verification interface is currently "
            "a frontend prototype interaction and is not stored through "
            "a dedicated backend verification service."
        ),
        (
            "Browser Features",
            "Voice recognition and geolocation depend on browser support "
            "and user permissions."
        ),
    ]

    for title, desc in limitations:

        rounded_box(
            c,
            18 * mm,
            y - 24 * mm,
            PAGE_W - 36 * mm,
            21 * mm,
            fill=ICE,
            stroke=LIGHT,
            radius=5
        )

        yy = para(
            c,
            title,
            23 * mm,
            y - 4 * mm,
            PAGE_W - 46 * mm,
            FEATURE_HEAD
        )

        para(
            c,
            desc,
            23 * mm,
            yy - 1 * mm,
            PAGE_W - 46 * mm,
            BODY_SMALL
        )

        y -= 26 * mm

    y -= 1 * mm

    y = section_header(c, 12, "FUTURE IMPROVEMENTS", y)

    improvements = [
        "Trained machine-learning models",
        "Computer vision for image-based issue classification",
        "Permanent cloud database",
        "Secure user authentication",
        "Role-based access control",
        "Per-citizen report access",
        "Real-time authority communication",
        "Advanced GIS mapping",
        "Persistent resolution verification",
        "Advanced analytics and reporting",
        "Mobile application support",
        "Integration with relevant government authorities",
    ]

    for i, item in enumerate(improvements):

        col = i % 2

        if col == 0:
            row_y = y

        x = 18 * mm + col * 90 * mm

        rounded_box(
            c,
            x,
            row_y - 8 * mm,
            84 * mm,
            7 * mm,
            fill=WHITE,
            stroke=LIGHT,
            radius=3
        )

        c.setFillColor(BLUE)
        c.circle(
            x + 4 * mm,
            row_y - 4.5 * mm,
            1.2 * mm,
            fill=1,
            stroke=0
        )

        c.setFillColor(TEXT)
        c.setFont(FONT_REGULAR, 6.9)
        c.drawString(
            x + 8 * mm,
            row_y - 5.8 * mm,
            item
        )

        if col == 1:
            y = row_y - 10 * mm

    footer(c, 10)


# ============================================================
# PAGE 11 — SECTIONS 13 + 14
# ============================================================

def page_11(c):

    y = 277 * mm

    y = section_header(c, 13, "PROJECT OBJECTIVE", y)

    y = para(
        c,
        "The objective of CivicEye AI is to demonstrate how web "
        "technologies and AI-assisted decision logic can support more "
        "structured civic issue reporting and monitoring.",
        18 * mm,
        y,
        PAGE_W - 36 * mm,
        BODY
    )

    y -= 2 * mm

    y = para(
        c,
        "<b>The project focuses on:</b>",
        18 * mm,
        y,
        PAGE_W - 36 * mm,
        BODY
    )

    objective_items = [
        "Simplifying citizen reporting",
        "Organizing complaint information",
        "Supporting issue prioritization",
        "Reducing repeated complaints",
        "Recommending relevant authorities",
        "Improving complaint visibility",
        "Supporting multilingual interaction",
    ]

    for item in objective_items:
        y = para(
            c,
            f"• {item}",
            22 * mm,
            y,
            PAGE_W - 44 * mm,
            BULLET
        )

    y -= 5 * mm

    y = section_header(c, 14, "CONCLUSION", y)

    y = para(
        c,
        "CivicEye AI demonstrates a prototype workflow for digital "
        "civic issue reporting and monitoring.",
        18 * mm,
        y,
        PAGE_W - 36 * mm,
        BODY
    )

    y = para(
        c,
        "By combining a citizen-facing web interface, a Node.js backend, "
        "rule-based AI-assisted analysis, duplicate detection, authority "
        "recommendation, notifications, and an administrator dashboard, "
        "the project provides a foundation for a future intelligent "
        "civic management platform.",
        18 * mm,
        y - 1 * mm,
        PAGE_W - 36 * mm,
        BODY
    )

    rounded_box(
        c,
        18 * mm,
        62 * mm,
        PAGE_W - 36 * mm,
        31 * mm,
        fill=SOFT_CYAN,
        stroke=HexColor("#A5EAF2"),
        radius=6
    )

    para(
        c,
        "The current implementation is intentionally presented as a "
        "prototype, with future scope for machine learning, persistent "
        "databases, secure authentication, advanced mapping, and direct "
        "authority integration.",
        25 * mm,
        83 * mm,
        PAGE_W - 50 * mm,
        BODY
    )

    # Final project identity
    c.setFillColor(NAVY)
    c.setFont(FONT_BOLD, 12)
    c.drawCentredString(
        PAGE_W / 2,
        43 * mm,
        "CivicEye AI · YCS 2026 · Sri Lanka"
    )

    c.setFillColor(MUTED)
    c.setFont(FONT_REGULAR, 7.5)
    c.drawCentredString(
        PAGE_W / 2,
        35 * mm,
        "AI-Powered Civic Issue Reporting Platform"
    )

    footer(c, 11)


# ============================================================
# CREATE PDF
# ============================================================

def create_pdf():

    c = canvas.Canvas(
        OUTPUT_FILE,
        pagesize=A4
    )

    c.setTitle(
        "CivicEye AI — YCS 2026 Project README"
    )

    c.setAuthor(
        "CivicEye AI"
    )

    # Page 1
    page_1(c)
    c.showPage()

    # Page 2
    page_2(c)
    c.showPage()

    # Page 3
    page_3(c)
    c.showPage()

    # Page 4
    page_4(c)
    c.showPage()

    # Page 5
    page_5(c)
    c.showPage()

    # Page 6
    page_6(c)
    c.showPage()

    # Page 7
    page_7(c)
    c.showPage()

    # Page 8
    page_8(c)
    c.showPage()

    # Page 9
    page_9(c)
    c.showPage()

    # Page 10
    page_10(c)
    c.showPage()

    # Page 11
    page_11(c)
    c.showPage()

    c.save()

    print()
    print("=" * 60)
    print("CIVICEYE AI PDF CREATED SUCCESSFULLY")
    print("=" * 60)
    print(f"File: {OUTPUT_FILE}")
    print("Pages: 11")
    print("=" * 60)


if __name__ == "__main__":
    create_pdf()