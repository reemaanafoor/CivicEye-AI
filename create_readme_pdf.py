
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle,
    HRFlowable,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os


# ============================================================
# CIVICEYE AI
# PREMIUM PROJECT DOCUMENTATION
# ============================================================

OUTPUT = "Documentation/README.pdf"

os.makedirs("Documentation", exist_ok=True)


# ============================================================
# FONTS
# ============================================================

regular_font = r"C:\Windows\Fonts\segoeui.ttf"
bold_font = r"C:\Windows\Fonts\segoeuib.ttf"

if os.path.exists(regular_font):
    pdfmetrics.registerFont(TTFont("CivicRegular", regular_font))
else:
    pdfmetrics.registerFont(TTFont("CivicRegular", r"C:\Windows\Fonts\arial.ttf"))

if os.path.exists(bold_font):
    pdfmetrics.registerFont(TTFont("CivicBold", bold_font))
else:
    pdfmetrics.registerFont(TTFont("CivicBold", r"C:\Windows\Fonts\arialbd.ttf"))


# ============================================================
# COLORS
# ============================================================

NAVY = colors.HexColor("#15182B")
PURPLE = colors.HexColor("#6254E7")
BLUE = colors.HexColor("#3C9FE8")
CYAN = colors.HexColor("#35B8C7")

GREEN = colors.HexColor("#25B77A")
ORANGE = colors.HexColor("#F19A43")
RED = colors.HexColor("#DF5C68")

TEXT = colors.HexColor("#303447")
MUTED = colors.HexColor("#73788C")

WHITE = colors.white
BACKGROUND = colors.HexColor("#F6F7FC")
LIGHT = colors.HexColor("#EEF0FA")
BORDER = colors.HexColor("#DDE1EC")


# ============================================================
# DOCUMENT
# ============================================================

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=15 * mm,
    rightMargin=15 * mm,
    topMargin=16 * mm,
    bottomMargin=18 * mm,
    title="CivicEye AI - Project Documentation",
    author="CivicEye AI",
)


# ============================================================
# STYLES
# ============================================================

cover_title = ParagraphStyle(
    "CoverTitle",
    fontName="CivicBold",
    fontSize=34,
    leading=40,
    alignment=TA_CENTER,
    textColor=NAVY,
)

cover_subtitle = ParagraphStyle(
    "CoverSubtitle",
    fontName="CivicRegular",
    fontSize=11,
    leading=17,
    alignment=TA_CENTER,
    textColor=MUTED,
)

cover_tag = ParagraphStyle(
    "CoverTag",
    fontName="CivicBold",
    fontSize=10,
    leading=14,
    alignment=TA_CENTER,
    textColor=PURPLE,
)

body = ParagraphStyle(
    "Body",
    fontName="CivicRegular",
    fontSize=8.7,
    leading=13,
    textColor=TEXT,
    spaceAfter=5,
)

small = ParagraphStyle(
    "Small",
    fontName="CivicRegular",
    fontSize=7.8,
    leading=11,
    textColor=TEXT,
)

small_bold = ParagraphStyle(
    "SmallBold",
    fontName="CivicBold",
    fontSize=8,
    leading=11,
    textColor=NAVY,
)

center = ParagraphStyle(
    "Center",
    fontName="CivicRegular",
    fontSize=8,
    leading=12,
    alignment=TA_CENTER,
    textColor=TEXT,
)

muted_center = ParagraphStyle(
    "MutedCenter",
    fontName="CivicRegular",
    fontSize=7.5,
    leading=10,
    alignment=TA_CENTER,
    textColor=MUTED,
)

quote = ParagraphStyle(
    "Quote",
    fontName="CivicBold",
    fontSize=10.5,
    leading=15,
    alignment=TA_CENTER,
    textColor=PURPLE,
)


# ============================================================
# PAGE HEADER / FOOTER
# ============================================================

def draw_page(canvas, document):

    canvas.saveState()

    # Top accent
    canvas.setFillColor(PURPLE)
    canvas.rect(
        0,
        A4[1] - 3.5 * mm,
        A4[0],
        3.5 * mm,
        fill=1,
        stroke=0,
    )

    # Footer line
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.5)

    canvas.line(
        15 * mm,
        11 * mm,
        195 * mm,
        11 * mm,
    )

    # Footer
    canvas.setFont("CivicRegular", 7)
    canvas.setFillColor(MUTED)

    canvas.drawString(
        15 * mm,
        6.5 * mm,
        "CivicEye AI  |  YCS 2026  |  Sri Lanka",
    )

    canvas.drawRightString(
        195 * mm,
        6.5 * mm,
        f"Page {document.page} of 5",
    )

    canvas.restoreState()


# ============================================================
# SECTION HEADER
# ============================================================

def section_header(number, title, subtitle):

    number_box = Table(
        [
            [
                Paragraph(
                    f"<font color='#FFFFFF'><b>{number}</b></font>",
                    center,
                )
            ]
        ],
        colWidths=[13 * mm],
        rowHeights=[13 * mm],
    )

    number_box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), PURPLE),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )

    title_block = Paragraph(
        f"<font size='17' color='#15182B'><b>{title}</b></font>"
        f"<br/>"
        f"<font size='8' color='#73788C'>{subtitle}</font>",
        body,
    )

    layout = Table(
        [[number_box, title_block]],
        colWidths=[15 * mm, 165 * mm],
    )

    layout.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )

    return layout


# ============================================================
# PREMIUM CARD
# ============================================================

def card(title, text, accent=PURPLE):

    table = Table(
        [
            [
                Paragraph(
                    f"<font color='{accent}'><b>{title}</b></font>"
                    f"<br/><br/>{text}",
                    body,
                )
            ]
        ],
        colWidths=[180 * mm],
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), WHITE),
                ("BOX", (0, 0), (-1, -1), 0.6, BORDER),
                ("LINEBEFORE", (0, 0), (0, 0), 3, accent),
                ("LEFTPADDING", (0, 0), (-1, -1), 11),
                ("RIGHTPADDING", (0, 0), (-1, -1), 11),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    return table


# ============================================================
# BULLET
# ============================================================

def bullet(text):

    return Paragraph(
        f"<font color='#6254E7'><b>•</b></font>  {text}",
        body,
    )


# ============================================================
# STORY
# ============================================================

story = []


# ============================================================
# PAGE 1
# PREMIUM COVER
# ============================================================

story.extend(
    [
        Spacer(1, 12 * mm),

        Paragraph(
            "CIVICEYE AI",
            ParagraphStyle(
                "Brand",
                fontName="CivicBold",
                fontSize=10,
                leading=14,
                alignment=TA_CENTER,
                textColor=PURPLE,
            ),
        ),

        Spacer(1, 5 * mm),

        Paragraph("CivicEye AI", cover_title),

        Spacer(1, 4 * mm),

        Paragraph(
            "AI-Powered Public Issue Reporting &amp; Monitoring",
            cover_subtitle,
        ),

        Spacer(1, 4 * mm),

        Paragraph(
            "Smart Digital Solution for Public Issue Management",
            cover_tag,
        ),

        Spacer(1, 8 * mm),

        HRFlowable(
            width="30%",
            thickness=1.2,
            color=PURPLE,
            hAlign="CENTER",
        ),

        Spacer(1, 8 * mm),

        Paragraph(
            "<b>YOUNG COMPUTER SCIENTIST COMPETITION 2026</b>",
            center,
        ),

        Spacer(1, 3 * mm),

        Paragraph(
            "National-Level School ICT Championship",
            muted_center,
        ),

        Paragraph(
            "Sri Lanka",
            muted_center,
        ),

        Spacer(1, 10 * mm),
    ]
)


# Cover cards

cover_cards = []

cover_items = [
    (
        "AI ANALYSIS",
        "AI-assisted processing of public issue reports.",
        PURPLE,
    ),
    (
        "SMART LOCATION",
        "Location information supports accurate reporting.",
        BLUE,
    ),
    (
        "MONITORING",
        "Structured reporting and administrative review.",
        GREEN,
    ),
]

for title, text, accent in cover_items:

    item = Table(
        [
            [
                Paragraph(
                    f"<font color='{accent}'><b>{title}</b></font>"
                    f"<br/><br/>{text}",
                    small,
                )
            ]
        ],
        colWidths=[55 * mm],
        rowHeights=[34 * mm],
    )

    item.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), WHITE),
                ("BOX", (0, 0), (-1, -1), 0.6, BORDER),
                ("LINEABOVE", (0, 0), (-1, 0), 2.5, accent),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    cover_cards.append(item)


cover_table = Table(
    [cover_cards],
    colWidths=[60 * mm, 60 * mm, 60 * mm],
)

cover_table.setStyle(
    TableStyle(
        [
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 2),
            ("RIGHTPADDING", (0, 0), (-1, -1), 2),
        ]
    )
)

story.append(cover_table)

story.extend(
    [
        Spacer(1, 11 * mm),

        card(
            "PROJECT INFORMATION",
            "<b>Project Name:</b> CivicEye AI<br/>"
            "<b>Competition:</b> Young Computer Scientist (YCS) 2026<br/>"
            "<b>Project Type:</b> AI-Powered Web Application<br/>"
            "<b>Country:</b> Sri Lanka",
            PURPLE,
        ),

        Spacer(1, 9 * mm),

        Paragraph(
            "REPORT  |  ANALYSE  |  CONNECT  |  RESOLVE",
            quote,
        ),

        Spacer(1, 3 * mm),

        Paragraph(
            "PREMIUM PROJECT DOCUMENTATION",
            muted_center,
        ),

        PageBreak(),
    ]
)


# ============================================================
# PAGE 2
# OVERVIEW / PROBLEM / SOLUTION
# ============================================================

story.extend(
    [
        section_header(
            "01",
            "Project Overview",
            "A centralized digital approach to public issue reporting",
        ),

        Spacer(1, 5 * mm),

        Paragraph(
            "CivicEye AI is an AI-powered web application designed to "
            "help citizens report and monitor public issues in their "
            "communities. The platform provides a structured digital "
            "workflow for submitting information about problems such "
            "as road damage, garbage issues, water leakage and "
            "street-light problems.",
            body,
        ),

        Paragraph(
            "Users can submit an image, select an issue type, provide "
            "a description and specify the location. The system then "
            "presents useful analysis information including confidence, "
            "priority, recommended authority, duplicate complaint "
            "status and report status.",
            body,
        ),

        Spacer(1, 4 * mm),

        section_header(
            "02",
            "The Problem",
            "Challenges in conventional public issue reporting",
        ),

        Spacer(1, 4 * mm),
    ]
)


problem_rows = [
    [
        Paragraph("<b>01</b>", center),
        Paragraph(
            "<b>Reporting Difficulty</b><br/>"
            "Citizens may not have a simple centralized platform "
            "for reporting different types of public issues.",
            small,
        ),
    ],
    [
        Paragraph("<b>02</b>", center),
        Paragraph(
            "<b>Authority Identification</b><br/>"
            "Citizens may not know which authority is responsible "
            "for handling a particular public issue.",
            small,
        ),
    ],
    [
        Paragraph("<b>03</b>", center),
        Paragraph(
            "<b>Repeated Complaints</b><br/>"
            "Multiple reports describing the same issue can make "
            "complaint organization more difficult.",
            small,
        ),
    ],
    [
        Paragraph("<b>04</b>", center),
        Paragraph(
            "<b>Monitoring Challenges</b><br/>"
            "Public issue information can be difficult to organize "
            "for administrative review and follow-up.",
            small,
        ),
    ],
]

problem_table = Table(
    problem_rows,
    colWidths=[18 * mm, 162 * mm],
)

problem_table.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (0, -1), LIGHT),
            ("BACKGROUND", (1, 0), (1, -1), WHITE),
            ("BOX", (0, 0), (-1, -1), 0.6, BORDER),
            ("INNERGRID", (0, 0), (-1, -1), 0.4, BORDER),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ]
    )
)

story.append(problem_table)

story.extend(
    [
        Spacer(1, 7 * mm),

        section_header(
            "03",
            "CivicEye AI Solution",
            "From citizen report to structured administrative information",
        ),

        Spacer(1, 4 * mm),

        card(
            "CITIZEN REPORTING",
            "Upload an image, select an issue, add a description "
            "and provide the location of the public problem.",
            PURPLE,
        ),

        Spacer(1, 3 * mm),

        card(
            "AI-ASSISTED PROCESSING",
            "Submitted information is processed and displayed as "
            "a structured analysis result for easier understanding.",
            BLUE,
        ),

        Spacer(1, 3 * mm),

        card(
            "ADMINISTRATIVE MONITORING",
            "Administrators can review submitted reports, locations, "
            "priority, status and other relevant information.",
            GREEN,
        ),

        Spacer(1, 6 * mm),

        Paragraph(
            "ONE PLATFORM  |  ONE WORKFLOW  |  SMARTER MONITORING",
            quote,
        ),

        PageBreak(),
    ]
)


# ============================================================
# PAGE 3
# CORE FEATURES
# ============================================================

story.extend(
    [
        section_header(
            "04",
            "Core Features",
            "Key capabilities implemented in CivicEye AI",
        ),

        Spacer(1, 6 * mm),
    ]
)


features = [
    (
        "IMAGE-BASED REPORTING",
        "Upload an image representing the public issue.",
        PURPLE,
    ),
    (
        "ISSUE DESCRIPTION",
        "Provide detailed information about the reported problem.",
        BLUE,
    ),
    (
        "SMART LOCATION",
        "Enter or capture the location associated with a report.",
        GREEN,
    ),
    (
        "AI ANALYSIS",
        "Present AI-assisted analysis information for the report.",
        PURPLE,
    ),
    (
        "CONFIDENCE DISPLAY",
        "Show the confidence associated with the analysis result.",
        BLUE,
    ),
    (
        "PRIORITY DETECTION",
        "Classify reports into Normal, Medium, High or Emergency.",
        RED,
    ),
    (
        "AUTHORITY RECOMMENDATION",
        "Recommend an appropriate authority based on the issue.",
        GREEN,
    ),
    (
        "DUPLICATE DETECTION",
        "Identify potentially repeated complaints.",
        ORANGE,
    ),
    (
        "ADMIN DASHBOARD",
        "Provide administrators with a structured report view.",
        PURPLE,
    ),
    (
        "CITIZEN DASHBOARD",
        "Provide citizens with access to submitted information.",
        BLUE,
    ),
    (
        "STATUS TRACKING",
        "Display the current state of submitted reports.",
        GREEN,
    ),
    (
        "MULTILINGUAL INPUT",
        "Designed to support English, Tamil and Sinhala interaction.",
        ORANGE,
    ),
]


for index in range(0, len(features), 3):

    row = []

    for j in range(3):

        title, description, accent = features[index + j]

        feature_card = Table(
            [
                [
                    Paragraph(
                        f"<font color='{accent}'><b>{title}</b></font>"
                        f"<br/><br/>{description}",
                        small,
                    )
                ]
            ],
            colWidths=[57 * mm],
            rowHeights=[35 * mm],
        )

        feature_card.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), WHITE),
                    ("BOX", (0, 0), (-1, -1), 0.6, BORDER),
                    ("LINEABOVE", (0, 0), (-1, 0), 2.2, accent),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )

        row.append(feature_card)

    row_table = Table(
        [row],
        colWidths=[60 * mm, 60 * mm, 60 * mm],
    )

    row_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 2),
                ("RIGHTPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )

    story.append(row_table)
    story.append(Spacer(1, 4 * mm))


story.extend(
    [
        Spacer(1, 2 * mm),

        card(
            "FEATURE WORKFLOW",
            "<b>Report</b>  →  <b>Analyse</b>  →  <b>Prioritize</b>  →  "
            "<b>Recommend Authority</b>  →  <b>Check Duplicate</b>  →  "
            "<b>Track Status</b>  →  <b>Admin Review</b>",
            PURPLE,
        ),

        Spacer(1, 5 * mm),

        Paragraph(
            "CivicEye AI combines citizen-facing reporting tools "
            "with administrative monitoring features, creating a "
            "practical foundation for organized public issue management.",
            body,
        ),

        PageBreak(),
    ]
)


# ============================================================
# PAGE 4
# TECHNOLOGY / STRUCTURE / API
# ============================================================

story.extend(
    [
        section_header(
            "05",
            "Technology &amp; Architecture",
            "Technologies used to build the CivicEye AI application",
        ),

        Spacer(1, 5 * mm),
    ]
)


technology_table = Table(
    [
        [
            Paragraph("<b>FRONTEND</b>", small_bold),
            Paragraph(
                "HTML5  |  CSS3  |  JavaScript<br/>"
                "Responsive web interface and interactive components.",
                small,
            ),
        ],
        [
            Paragraph("<b>BACKEND</b>", small_bold),
            Paragraph(
                "Node.js  |  Express.js  |  Multer  |  CORS  |  dotenv<br/>"
                "Server-side report and upload handling.",
                small,
            ),
        ],
        [
            Paragraph("<b>DEPLOYMENT</b>", small_bold),
            Paragraph(
                "Frontend: Web-based interface<br/>"
                "Backend: Railway",
                small,
            ),
        ],
    ],
    colWidths=[38 * mm, 142 * mm],
)

technology_table.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (0, -1), LIGHT),
            ("BACKGROUND", (1, 0), (1, -1), WHITE),
            ("BOX", (0, 0), (-1, -1), 0.6, BORDER),
            ("INNERGRID", (0, 0), (-1, -1), 0.4, BORDER),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 9),
            ("RIGHTPADDING", (0, 0), (-1, -1), 9),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ]
    )
)

story.append(technology_table)

story.extend(
    [
        Spacer(1, 7 * mm),

        section_header(
            "06",
            "Project Structure",
            "Main files and folders used by the project",
        ),

        Spacer(1, 4 * mm),
    ]
)


structure_table = Table(
    [
        [
            Paragraph(
                "<b>FRONTEND</b><br/><br/>"
                "index.html<br/>"
                "login.html<br/>"
                "citizen.html<br/>"
                "admin.html<br/>"
                "report.html<br/>"
                "ai-processing.html<br/>"
                "script.js<br/>"
                "style.css",
                small,
            ),
            Paragraph(
                "<b>BACKEND</b><br/><br/>"
                "server.js<br/>"
                "package.json<br/>"
                "package-lock.json<br/><br/>"
                "<b>SUPPORT</b><br/><br/>"
                "uploads/<br/>"
                "Documentation/",
                small,
            ),
        ]
    ],
    colWidths=[89 * mm, 89 * mm],
)

structure_table.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, -1), WHITE),
            ("BOX", (0, 0), (-1, -1), 0.6, BORDER),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ]
    )
)

story.append(structure_table)

story.extend(
    [
        Spacer(1, 7 * mm),

        section_header(
            "07",
            "Backend API",
            "Core endpoints used by the web application",
        ),

        Spacer(1, 4 * mm),

        card(
            "GET /",
            "Backend health check used to verify that the CivicEye AI backend is running.",
            GREEN,
        ),

        Spacer(1, 2.5 * mm),

        card(
            "POST /upload",
            "Receives uploaded image and report information for processing.",
            BLUE,
        ),

        Spacer(1, 2.5 * mm),

        card(
            "GET /reports",
            "Returns submitted reports for administrative monitoring.",
            PURPLE,
        ),

        Spacer(1, 2.5 * mm),

        card(
            "DELETE /reports/:id",
            "Removes a selected report from the backend.",
            RED,
        ),

        PageBreak(),
    ]
)


# ============================================================
# PAGE 5
# TESTING / OBJECTIVES / FUTURE / CONCLUSION
# ============================================================

story.extend(
    [
        section_header(
            "08",
            "Testing &amp; Demonstration",
            "Recommended evaluation workflow for judges",
        ),

        Spacer(1, 4 * mm),
    ]
)


steps = [
    (
        "01",
        "OPEN REPORTING PAGE",
        "Open report.html and prepare a sample public issue report.",
        PURPLE,
    ),
    (
        "02",
        "CREATE A REPORT",
        "Upload an image, select an issue, add a description and provide the location.",
        BLUE,
    ),
    (
        "03",
        "SUBMIT REPORT",
        "Submit the report and allow CivicEye AI to process the information.",
        GREEN,
    ),
    (
        "04",
        "VIEW AI ANALYSIS",
        "Review issue, confidence, location, priority, authority, duplicate status and report status.",
        ORANGE,
    ),
    (
        "05",
        "ADMIN REVIEW",
        "Open admin.html to review the submitted report and its information.",
        PURPLE,
    ),
]


for number, title, description, accent in steps:

    step_table = Table(
        [
            [
                Paragraph(
                    f"<font color='{accent}'><b>{number}</b></font>",
                    center,
                ),
                Paragraph(
                    f"<b>{title}</b><br/>{description}",
                    small,
                ),
            ]
        ],
        colWidths=[18 * mm, 162 * mm],
    )

    step_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, 0), LIGHT),
                ("BACKGROUND", (1, 0), (1, 0), WHITE),
                ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    story.append(step_table)
    story.append(Spacer(1, 2.5 * mm))


story.extend(
    [
        Spacer(1, 3 * mm),

        section_header(
            "09",
            "Project Objectives",
            "What CivicEye AI aims to demonstrate",
        ),

        Spacer(1, 3 * mm),

        bullet("Encourage citizen participation in reporting public issues."),
        bullet("Use AI-assisted processing to organize submitted information."),
        bullet("Support public issue prioritization."),
        bullet("Identify potentially duplicate complaints."),
        bullet("Recommend a relevant authority."),
        bullet("Provide digital administrative monitoring."),

        Spacer(1, 4 * mm),

        section_header(
            "10",
            "Future Improvements",
            "Potential directions for further development",
        ),

        Spacer(1, 3 * mm),
    ]
)


future_table = Table(
    [
        [
            Paragraph(
                "<b>INTELLIGENCE</b><br/><br/>"
                "Advanced computer-vision issue detection<br/>"
                "Improved multilingual AI support<br/>"
                "Advanced analytics and prediction<br/>"
                "Smarter issue classification",
                small,
            ),
            Paragraph(
                "<b>CONNECTIVITY</b><br/><br/>"
                "Real-time authority notifications<br/>"
                "Interactive geographic issue maps<br/>"
                "Cloud database integration<br/>"
                "Integration with public-service authorities",
                small,
            ),
        ]
    ],
    colWidths=[89 * mm, 89 * mm],
)

future_table.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, -1), WHITE),
            ("BOX", (0, 0), (-1, -1), 0.6, BORDER),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 9),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ]
    )
)

story.append(future_table)

story.extend(
    [
        Spacer(1, 5 * mm),

        section_header(
            "11",
            "Conclusion",
            "A practical application of AI and web technologies",
        ),

        Spacer(1, 3 * mm),

        Paragraph(
            "CivicEye AI demonstrates how AI and web technologies can "
            "be combined to address real-world public-service challenges. "
            "By bringing citizen reporting, image uploads, location "
            "information, AI-assisted analysis, priority detection, "
            "duplicate detection, authority recommendation and "
            "administrative monitoring together, the platform provides "
            "a foundation for a more organized public issue reporting process.",
            body,
        ),

        Spacer(1, 5 * mm),
    ]
)


# ============================================================
# FINAL INFORMATION STRIP
# ============================================================

final_table = Table(
    [
        [
            Paragraph(
                "<b>CivicEye AI</b><br/>AI-Powered Web Application",
                center,
            ),
            Paragraph(
                "<b>YCS 2026</b><br/>Young Computer Scientist Competition",
                center,
            ),
            Paragraph(
                "<b>Sri Lanka</b><br/>National-Level ICT Championship",
                center,
            ),
        ]
    ],
    colWidths=[59 * mm, 59 * mm, 59 * mm],
)

final_table.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
            ("BOX", (0, 0), (-1, -1), 0.6, BORDER),
            ("INNERGRID", (0, 0), (-1, -1), 0.4, BORDER),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 9),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ]
    )
)

story.extend(
    [
        final_table,

        Spacer(1, 6 * mm),

        Paragraph(
            "REPORT  |  ANALYSE  |  CONNECT  |  RESOLVE",
            quote,
        ),

        Spacer(1, 2 * mm),

        Paragraph(
            "PROJECT DOCUMENTATION",
            muted_center,
        ),
    ]
)


# ============================================================
# BUILD PDF
# ============================================================

doc.build(
    story,
    onFirstPage=draw_page,
    onLaterPages=draw_page,
)


# ============================================================
# SUCCESS MESSAGE
# ============================================================

print()
print("================================================")
print("CIVICEYE AI PREMIUM README CREATED SUCCESSFULLY")
print("================================================")
print()
print("File: Documentation\\README.pdf")
print("Pages: 5")
print("Style: Premium")
print("Emoji: Disabled for PDF compatibility")
print()