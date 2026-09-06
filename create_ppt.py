
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor


# =========================================================
# CIVICEYE AI — PREMIUM COMPETITION PRESENTATION
# =========================================================

prs = Presentation()

prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)


# =========================================================
# COLORS
# =========================================================

BG = RGBColor(245, 247, 255)
DARK = RGBColor(27, 31, 50)
PURPLE = RGBColor(91, 76, 220)
BLUE = RGBColor(57, 168, 255)
WHITE = RGBColor(255, 255, 255)
GREY = RGBColor(100, 106, 125)
LIGHT = RGBColor(232, 235, 248)
GREEN = RGBColor(40, 180, 120)


# =========================================================
# HELPERS
# =========================================================

def add_text(
    slide,
    text,
    x,
    y,
    w,
    h,
    size=18,
    color=DARK,
    bold=False,
    align=PP_ALIGN.LEFT
):

    box = slide.shapes.add_textbox(
        Inches(x),
        Inches(y),
        Inches(w),
        Inches(h)
    )

    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE

    p = tf.paragraphs[0]

    p.text = text
    p.font.name = "Aptos"
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.alignment = align

    return box


def add_card(
    slide,
    x,
    y,
    w,
    h,
    fill=WHITE,
    radius=True
):

    shape_type = (
        MSO_SHAPE.ROUNDED_RECTANGLE
        if radius
        else MSO_SHAPE.RECTANGLE
    )

    card = slide.shapes.add_shape(
        shape_type,
        Inches(x),
        Inches(y),
        Inches(w),
        Inches(h)
    )

    card.fill.solid()
    card.fill.fore_color.rgb = fill

    card.line.color.rgb = LIGHT

    return card


def add_background(slide):

    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = BG


def add_header(slide, title, number):

    add_text(
        slide,
        title,
        0.7,
        0.35,
        9.5,
        0.55,
        size=25,
        color=DARK,
        bold=True
    )

    add_text(
        slide,
        f"CIVICEYE AI   •   {number}/7",
        10.4,
        0.38,
        2.2,
        0.35,
        size=10,
        color=GREY,
        bold=True,
        align=PP_ALIGN.RIGHT
    )


def add_footer(slide):

    add_text(
        slide,
        "Smart AI Solution for a Cleaner Sri Lanka 🇱🇰",
        0.7,
        7.05,
        7.5,
        0.25,
        size=9,
        color=GREY
    )


# =========================================================
# SLIDE 1 — COVER
# =========================================================

slide = prs.slides.add_slide(prs.slide_layouts[6])

add_background(slide)


# Decorative shapes

circle = slide.shapes.add_shape(
    MSO_SHAPE.OVAL,
    Inches(9.6),
    Inches(-1.0),
    Inches(5.0),
    Inches(5.0)
)

circle.fill.solid()
circle.fill.fore_color.rgb = RGBColor(226, 222, 255)
circle.line.fill.background()


circle2 = slide.shapes.add_shape(
    MSO_SHAPE.OVAL,
    Inches(-1.3),
    Inches(5.4),
    Inches(4.0),
    Inches(4.0)
)

circle2.fill.solid()
circle2.fill.fore_color.rgb = RGBColor(222, 239, 255)
circle2.line.fill.background()


add_text(
    slide,
    "👁️",
    0.9,
    1.15,
    1.0,
    1.0,
    size=42,
    align=PP_ALIGN.CENTER
)

add_text(
    slide,
    "CivicEye AI",
    1.8,
    1.18,
    7.0,
    0.8,
    size=40,
    color=DARK,
    bold=True
)

add_text(
    slide,
    "Smart AI Solution for a Cleaner Sri Lanka 🇱🇰",
    1.85,
    2.05,
    7.5,
    0.55,
    size=21,
    color=PURPLE,
    bold=True
)

add_text(
    slide,
    "AI-powered public issue reporting and management platform",
    1.85,
    2.7,
    7.0,
    0.7,
    size=18,
    color=GREY
)


# Feature pills

pills = [
    ("🤖 AI Analysis", 1.85),
    ("📍 Smart Location", 4.15),
    ("🏛️ Authority Workflow", 6.55)
]

for text, x in pills:

    add_card(
        slide,
        x,
        3.75,
        2.1,
        0.55,
        WHITE
    )

    add_text(
        slide,
        text,
        x + 0.05,
        3.82,
        2.0,
        0.35,
        size=10,
        color=DARK,
        bold=True,
        align=PP_ALIGN.CENTER
    )


add_card(
    slide,
    1.85,
    5.05,
    6.8,
    0.85,
    PURPLE
)

add_text(
    slide,
    "Young Computer Scientist (YCS) 2026",
    2.0,
    5.18,
    6.5,
    0.45,
    size=18,
    color=WHITE,
    bold=True,
    align=PP_ALIGN.CENTER
)

add_text(
    slide,
    "🇱🇰 AI Innovation Project",
    9.2,
    5.7,
    3.0,
    0.5,
    size=16,
    color=PURPLE,
    bold=True,
    align=PP_ALIGN.CENTER
)


# =========================================================
# SLIDE 2 — THE PROBLEM
# =========================================================

slide = prs.slides.add_slide(prs.slide_layouts[6])

add_background(slide)
add_header(slide, "🚨 The Public Issue Challenge", 2)

add_text(
    slide,
    "Public problems need a faster and more organized way to reach the right authority.",
    0.75,
    1.05,
    11.7,
    0.55,
    size=18,
    color=GREY
)


problems = [
    ("📸", "Difficult Reporting", "Citizens may struggle to report public problems efficiently."),
    ("⏳", "Slow Follow-up", "Reports can be difficult to monitor after submission."),
    ("🔁", "Repeated Complaints", "Similar complaints may be submitted multiple times."),
    ("❓", "Wrong Routing", "A report may need to reach the correct local authority.")
]

positions = [
    (0.8, 2.0),
    (6.75, 2.0),
    (0.8, 4.35),
    (6.75, 4.35)
]

for (icon, title, desc), (x, y) in zip(problems, positions):

    add_card(
        slide,
        x,
        y,
        5.75,
        1.85,
        WHITE
    )

    add_text(
        slide,
        icon,
        x + 0.25,
        y + 0.25,
        0.65,
        0.65,
        size=25,
        align=PP_ALIGN.CENTER
    )

    add_text(
        slide,
        title,
        x + 1.0,
        y + 0.2,
        4.3,
        0.4,
        size=17,
        color=DARK,
        bold=True
    )

    add_text(
        slide,
        desc,
        x + 1.0,
        y + 0.7,
        4.35,
        0.8,
        size=13,
        color=GREY
    )

add_footer(slide)


# =========================================================
# SLIDE 3 — SOLUTION + FEATURES
# =========================================================

slide = prs.slides.add_slide(prs.slide_layouts[6])

add_background(slide)
add_header(slide, "💡 Introducing CivicEye AI", 3)

add_text(
    slide,
    "One platform connecting citizens, AI-assisted analysis and authorities.",
    0.75,
    1.0,
    11.5,
    0.5,
    size=18,
    color=GREY
)


features = [
    ("🤖", "AI Issue Detection", "Identify and categorize reported issues."),
    ("📍", "Smart Location", "Capture where the issue was reported."),
    ("🔍", "Duplicate Detection", "Identify similar reports."),
    ("🚨", "Priority Classification", "Highlight issues needing faster attention."),
    ("🏛️", "Authority Recommendation", "Suggest the relevant authority."),
    ("🔄", "Status Tracking", "Monitor complaint progress."),
    ("✅", "Resolution Verification", "Allow citizens to verify resolution."),
    ("🎙️", "Multilingual Voice", "Support English, Tamil and Sinhala when available.")
]

x_positions = [0.75, 3.9, 7.05, 10.2]

for i, (icon, title, desc) in enumerate(features):

    row = i // 4
    col = i % 4

    x = x_positions[col]
    y = 1.8 + row * 2.3

    add_card(
        slide,
        x,
        y,
        2.75,
        1.9,
        WHITE
    )

    add_text(
        slide,
        icon,
        x + 0.15,
        y + 0.18,
        0.65,
        0.55,
        size=23,
        align=PP_ALIGN.CENTER
    )

    add_text(
        slide,
        title,
        x + 0.85,
        y + 0.18,
        1.7,
        0.65,
        size=13,
        color=DARK,
        bold=True
    )

    add_text(
        slide,
        desc,
        x + 0.2,
        y + 0.95,
        2.35,
        0.7,
        size=11,
        color=GREY,
        align=PP_ALIGN.LEFT
    )

add_footer(slide)


# =========================================================
# SLIDE 4 — HOW IT WORKS
# =========================================================

slide = prs.slides.add_slide(prs.slide_layouts[6])

add_background(slide)
add_header(slide, "🔄 How CivicEye AI Works", 4)

add_text(
    slide,
    "A simple digital workflow turns a citizen report into a trackable public issue.",
    0.75,
    1.0,
    11.5,
    0.5,
    size=18,
    color=GREY
)


steps = [
    ("01", "📸", "REPORT", "Citizen submits image, description and location."),
    ("02", "🤖", "AI ANALYSIS", "System analyses and categorizes the issue."),
    ("03", "🚨", "PRIORITIZE", "Priority and duplicate information are generated."),
    ("04", "🏛️", "AUTHORITY", "Relevant authority can review the report."),
    ("05", "🔄", "MONITOR", "Status changes can be tracked by citizens."),
    ("06", "✅", "RESOLVE", "Citizen can verify the reported issue.")
]

for i, (num, icon, title, desc) in enumerate(steps):

    x = 0.7 + (i % 3) * 4.15
    y = 1.8 + (i // 3) * 2.45

    add_card(
        slide,
        x,
        y,
        3.7,
        1.95,
        WHITE
    )

    add_text(
        slide,
        num,
        x + 0.2,
        y + 0.2,
        0.5,
        0.35,
        size=11,
        color=PURPLE,
        bold=True
    )

    add_text(
        slide,
        icon,
        x + 0.65,
        y + 0.18,
        0.65,
        0.55,
        size=22,
        align=PP_ALIGN.CENTER
    )

    add_text(
        slide,
        title,
        x + 1.35,
        y + 0.2,
        2.0,
        0.4,
        size=14,
        color=DARK,
        bold=True
    )

    add_text(
        slide,
        desc,
        x + 0.25,
        y + 0.95,
        3.15,
        0.7,
        size=11,
        color=GREY
    )

add_footer(slide)


# =========================================================
# SLIDE 5 — TECHNOLOGY
# =========================================================

slide = prs.slides.add_slide(prs.slide_layouts[6])

add_background(slide)
add_header(slide, "💻 Technology & System Architecture", 5)

add_text(
    slide,
    "CivicEye AI combines a web frontend with a Node.js backend and API-based communication.",
    0.75,
    1.0,
    11.6,
    0.5,
    size=17,
    color=GREY
)


# Frontend

add_card(slide, 0.8, 1.9, 3.45, 3.65, WHITE)

add_text(
    slide,
    "🌐 FRONTEND",
    1.05,
    2.15,
    2.8,
    0.45,
    size=18,
    color=PURPLE,
    bold=True,
    align=PP_ALIGN.CENTER
)

add_text(
    slide,
    "HTML\nCSS\nJavaScript\nResponsive Web Interface",
    1.15,
    2.85,
    2.6,
    1.8,
    size=17,
    color=DARK,
    bold=True,
    align=PP_ALIGN.CENTER
)


# Backend

add_card(slide, 4.95, 1.9, 3.45, 3.65, WHITE)

add_text(
    slide,
    "⚙️ BACKEND",
    5.2,
    2.15,
    2.8,
    0.45,
    size=18,
    color=PURPLE,
    bold=True,
    align=PP_ALIGN.CENTER
)

add_text(
    slide,
    "Node.js\nExpress.js\nMulter\nREST APIs\nCORS + dotenv",
    5.2,
    2.8,
    2.9,
    2.1,
    size=16,
    color=DARK,
    bold=True,
    align=PP_ALIGN.CENTER
)


# Deployment

add_card(slide, 9.1, 1.9, 3.45, 3.65, WHITE)

add_text(
    slide,
    "🚀 DEPLOYMENT",
    9.35,
    2.15,
    2.95,
    0.45,
    size=18,
    color=PURPLE,
    bold=True,
    align=PP_ALIGN.CENTER
)

add_text(
    slide,
    "Web Frontend\n+\nRailway Backend\n+\nAPI Communication",
    9.35,
    2.85,
    2.9,
    1.9,
    size=16,
    color=DARK,
    bold=True,
    align=PP_ALIGN.CENTER
)


# Flow

add_card(
    slide,
    2.2,
    6.0,
    8.9,
    0.55,
    PURPLE
)

add_text(
    slide,
    "Citizen  →  Frontend  →  REST API  →  Backend  →  Admin",
    2.35,
    6.08,
    8.6,
    0.35,
    size=13,
    color=WHITE,
    bold=True,
    align=PP_ALIGN.CENTER
)

add_footer(slide)


# =========================================================
# SLIDE 6 — TESTING + IMPACT
# =========================================================

slide = prs.slides.add_slide(prs.slide_layouts[6])

add_background(slide)
add_header(slide, "🧪 Testing, Impact & Future", 6)


# Testing card

add_card(slide, 0.75, 1.25, 5.8, 4.9, WHITE)

add_text(
    slide,
    "🧪 TESTED",
    1.05,
    1.55,
    5.1,
    0.45,
    size=20,
    color=PURPLE,
    bold=True
)

tests = [
    "✅ Image upload & report submission",
    "✅ AI processing result display",
    "✅ Citizen report tracking",
    "✅ Admin dashboard workflow",
    "✅ Status update APIs",
    "✅ Report retrieval & management",
    "✅ Railway backend connection"
]

add_text(
    slide,
    "\n".join(tests),
    1.05,
    2.2,
    5.0,
    3.2,
    size=15,
    color=DARK
)


# Future card

add_card(slide, 6.8, 1.25, 5.8, 4.9, WHITE)

add_text(
    slide,
    "🔮 FUTURE IMPROVEMENTS",
    7.1,
    1.55,
    5.1,
    0.45,
    size=20,
    color=PURPLE,
    bold=True
)

future = [
    "🤖 More advanced AI models",
    "🗄️ Persistent production database",
    "🎙️ Improved multilingual voice input",
    "📊 Advanced analytics",
    "🔔 Real-time notifications",
    "🌍 Wider community deployment"
]

add_text(
    slide,
    "\n".join(future),
    7.1,
    2.2,
    5.0,
    3.2,
    size=15,
    color=DARK
)

add_footer(slide)


# =========================================================
# SLIDE 7 — PROJECT INFORMATION / CONCLUSION
# =========================================================

slide = prs.slides.add_slide(prs.slide_layouts[6])

add_background(slide)

add_text(
    slide,
    "👁️ CivicEye AI",
    0.8,
    0.75,
    11.7,
    0.7,
    size=34,
    color=DARK,
    bold=True,
    align=PP_ALIGN.CENTER
)

add_text(
    slide,
    "Building smarter communities through AI and digital reporting 🇱🇰",
    1.0,
    1.5,
    11.3,
    0.55,
    size=19,
    color=PURPLE,
    bold=True,
    align=PP_ALIGN.CENTER
)


# Main conclusion

add_card(
    slide,
    1.0,
    2.35,
    11.3,
    1.2,
    PURPLE
)

add_text(
    slide,
    "Report  •  Analyse  •  Prioritize  •  Connect  •  Resolve",
    1.25,
    2.62,
    10.8,
    0.6,
    size=21,
    color=WHITE,
    bold=True,
    align=PP_ALIGN.CENTER
)


# Project info cards

info = [
    ("Project Name", "CivicEye AI"),
    ("Competition", "Young Computer Scientist (YCS) 2026"),
    ("Project Type", "AI-Powered Web Application"),
    ("Country", "Sri Lanka 🇱🇰")
]

for i, (label, value) in enumerate(info):

    x = 1.0 + (i % 2) * 5.75
    y = 4.0 + (i // 2) * 1.25

    add_card(
        slide,
        x,
        y,
        5.35,
        0.95,
        WHITE
    )

    add_text(
        slide,
        label,
        x + 0.2,
        y + 0.12,
        1.7,
        0.3,
        size=11,
        color=GREY,
        bold=True
    )

    add_text(
        slide,
        value,
        x + 1.85,
        y + 0.1,
        3.2,
        0.55,
        size=14,
        color=DARK,
        bold=True,
        align=PP_ALIGN.RIGHT
    )


add_text(
    slide,
    "Thank You",
    4.0,
    6.65,
    5.3,
    0.45,
    size=20,
    color=PURPLE,
    bold=True,
    align=PP_ALIGN.CENTER
)


# =========================================================
# SAVE
# =========================================================

output_file = "CivicEye_AI_Premium_Final.pptx"

prs.save(output_file)

print()
print("==============================================")
print("CIVICEYE AI PREMIUM PPT CREATED! 🚀")
print("==============================================")
print()
print(f"File: {output_file}")
print()