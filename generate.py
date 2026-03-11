#!/usr/bin/env python3
"""
CV Generator - Dark Navy Sidebar Template
Generates TR and EN versions of the CV as PDF.

Usage:
    uv run --with reportlab --with pypdf generate.py
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader, PdfWriter
from pathlib import Path
import os

# ─── Paths ───────────────────────────────────────────────────────────────────
PROJECT_DIR = Path(__file__).parent
ASSETS_DIR = PROJECT_DIR / "assets"
OUTPUT_DIR = PROJECT_DIR / "output"
PHOTO_PATH = ASSETS_DIR / "photo.jpg"

OUTPUT_DIR.mkdir(exist_ok=True)

# ─── Fonts (Calibri - Turkish character support) ─────────────────────────────
FONT_DIR = r"C:\Windows\Fonts"
pdfmetrics.registerFont(TTFont("Calibri", os.path.join(FONT_DIR, "calibri.ttf")))
pdfmetrics.registerFont(TTFont("Calibri-Bold", os.path.join(FONT_DIR, "calibrib.ttf")))
pdfmetrics.registerFont(TTFont("Calibri-Italic", os.path.join(FONT_DIR, "calibrii.ttf")))
pdfmetrics.registerFont(TTFont("Calibri-BoldItalic", os.path.join(FONT_DIR, "calibriz.ttf")))

F = "Calibri"
FB = "Calibri-Bold"
FI = "Calibri-Italic"

# ─── Layout ──────────────────────────────────────────────────────────────────
WIDTH, HEIGHT = A4
SIDEBAR_W = 68 * mm
SIDEBAR_PAD = 8 * mm
MAIN_LEFT = SIDEBAR_W + 10 * mm
MAIN_RIGHT = WIDTH - 12 * mm
MAIN_W = MAIN_RIGHT - MAIN_LEFT

# ─── Colors ──────────────────────────────────────────────────────────────────
BG_DARK = HexColor("#1B2838")
BG_DARK_LIGHT = HexColor("#243447")
ACCENT_GOLD = HexColor("#D4A843")
ACCENT_BLUE = HexColor("#5B9BD5")
TEXT_WHITE = HexColor("#EAEAEA")
TEXT_WHITE_DIM = HexColor("#B0B8C4")
TEXT_DARK = HexColor("#1A1A1A")
TEXT_MED = HexColor("#444444")
TEXT_LIGHT = HexColor("#777777")
SECTION_LINE = HexColor("#DDDDDD")


# ═══════════════════════════════════════════════════════════════════════════════
# Drawing Helpers
# ═══════════════════════════════════════════════════════════════════════════════

def wrap_text(c, x, y, text, font, size, max_width, line_h=3.4 * mm):
    c.setFont(font, size)
    words = text.split(" ")
    line = ""
    for word in words:
        test = (line + " " + word).strip()
        if c.stringWidth(test, font, size) <= max_width:
            line = test
        else:
            c.drawString(x, y, line)
            y -= line_h
            line = word
    if line:
        c.drawString(x, y, line)
        y -= line_h
    return y


# ─── Sidebar ─────────────────────────────────────────────────────────────────

def draw_sidebar(c):
    c.setFillColor(BG_DARK)
    c.rect(0, 0, SIDEBAR_W, HEIGHT, fill=1, stroke=0)


def draw_photo(c, y):
    cx = SIDEBAR_W / 2
    radius = 22 * mm
    c.setStrokeColor(ACCENT_GOLD)
    c.setLineWidth(1.5)
    c.circle(cx, y - radius, radius + 1.5, fill=0, stroke=1)
    if PHOTO_PATH.exists():
        c.saveState()
        p = c.beginPath()
        p.circle(cx, y - radius, radius)
        p.close()
        c.clipPath(p, stroke=0)
        c.drawImage(str(PHOTO_PATH), cx - radius, y - 2 * radius,
                     width=2 * radius, height=2 * radius,
                     preserveAspectRatio=True, anchor='c')
        c.restoreState()
    return y - 2 * radius - 6 * mm


def sb_divider(c, y):
    y -= 1 * mm
    c.setStrokeColor(BG_DARK_LIGHT)
    c.setLineWidth(0.5)
    c.line(SIDEBAR_PAD, y, SIDEBAR_W - SIDEBAR_PAD, y)
    return y - 4 * mm


def sb_section(c, y, title):
    y -= 2 * mm
    c.setFont(FB, 8)
    c.setFillColor(ACCENT_GOLD)
    c.drawString(SIDEBAR_PAD, y, title.upper())
    y -= 3 * mm
    c.setStrokeColor(ACCENT_GOLD)
    c.setLineWidth(0.6)
    c.line(SIDEBAR_PAD, y, SIDEBAR_PAD + 15 * mm, y)
    return y - 4 * mm


def sb_contact(c, y, label, value):
    c.setFont(FB, 6.5)
    c.setFillColor(TEXT_WHITE_DIM)
    c.drawString(SIDEBAR_PAD, y, label.upper())
    y -= 3 * mm
    c.setFont(F, 7)
    c.setFillColor(TEXT_WHITE)
    c.drawString(SIDEBAR_PAD, y, value)
    return y - 4 * mm


def sb_skills_compact(c, y, title, items):
    c.setFont(FB, 7)
    c.setFillColor(TEXT_WHITE)
    c.drawString(SIDEBAR_PAD, y, title)
    y -= 3.2 * mm
    sw = SIDEBAR_W - 2 * SIDEBAR_PAD
    c.setFillColor(TEXT_WHITE_DIM)
    text = " \u00b7 ".join(items)
    y = wrap_text(c, SIDEBAR_PAD, y, text, F, 6.5, sw, 3 * mm)
    return y - 1.5 * mm


def sb_language(c, y, lang, level, filled):
    c.setFont(F, 7)
    c.setFillColor(TEXT_WHITE)
    c.drawString(SIDEBAR_PAD, y, f"{lang}")
    lw = c.stringWidth(lang + "  ", F, 7)
    c.setFont(F, 6.5)
    c.setFillColor(TEXT_WHITE_DIM)
    c.drawString(SIDEBAR_PAD + lw, y, f"({level})")
    y -= 4 * mm
    dot_r = 2.2
    for i in range(5):
        dx = SIDEBAR_PAD + i * (dot_r * 2 + 3)
        c.setFillColor(ACCENT_GOLD if i < filled else BG_DARK_LIGHT)
        c.circle(dx + dot_r, y + dot_r / 2, dot_r, fill=1, stroke=0)
    return y - 5 * mm


# ─── Main Panel ──────────────────────────────────────────────────────────────

def m_section(c, y, title, first=False):
    if not first:
        y -= 5 * mm
    c.setFont(FB, 11.5)
    c.setFillColor(BG_DARK)
    c.drawString(MAIN_LEFT, y, title.upper())
    y -= 3.5 * mm
    c.setStrokeColor(ACCENT_GOLD)
    c.setLineWidth(1.5)
    c.line(MAIN_LEFT, y, MAIN_LEFT + 22 * mm, y)
    c.setStrokeColor(SECTION_LINE)
    c.setLineWidth(0.3)
    c.line(MAIN_LEFT + 22 * mm, y, MAIN_RIGHT, y)
    return y - 5 * mm


def m_work(c, y, title, company, date, bullets=None):
    c.setFont(FB, 9)
    c.setFillColor(TEXT_DARK)
    c.drawString(MAIN_LEFT, y, title)
    c.setFont(F, 7.5)
    c.setFillColor(ACCENT_BLUE)
    c.drawRightString(MAIN_RIGHT, y, date)
    y -= 4 * mm
    c.setFont(F, 8)
    c.setFillColor(TEXT_LIGHT)
    c.drawString(MAIN_LEFT, y, company)
    y -= 3.5 * mm
    if bullets:
        indent = MAIN_LEFT + 3 * mm
        for b in bullets:
            c.setFont(F, 7)
            c.setFillColor(TEXT_MED)
            c.drawString(MAIN_LEFT, y, "\u2022")
            y = wrap_text(c, indent, y, b, F, 7, MAIN_W - 3 * mm, 3.2 * mm)
            y -= 0.5 * mm
    return y - 2.5 * mm


def m_project(c, y, name, subtitle, techs, features, lang="tr"):
    tech_label = "Teknolojiler: " if lang == "tr" else "Technologies: "
    feat_label = "\u00d6zellikler: " if lang == "tr" else "Features: "

    c.setFont(FB, 9)
    c.setFillColor(TEXT_DARK)
    c.drawString(MAIN_LEFT, y, name)
    y -= 4 * mm
    c.setFont(FI, 7.5)
    c.setFillColor(TEXT_LIGHT)
    c.drawString(MAIN_LEFT, y, subtitle)
    y -= 4 * mm

    c.setFont(FB, 7)
    c.setFillColor(TEXT_DARK)
    c.drawString(MAIN_LEFT, y, tech_label)
    tw = c.stringWidth(tech_label, FB, 7)
    c.setFillColor(TEXT_MED)
    y = wrap_text(c, MAIN_LEFT + tw, y, techs, F, 7, MAIN_W - tw, 3.2 * mm)
    y -= 0.5 * mm
    c.setFont(FB, 7)
    c.setFillColor(TEXT_DARK)
    c.drawString(MAIN_LEFT, y, feat_label)
    fw = c.stringWidth(feat_label, FB, 7)
    c.setFillColor(TEXT_MED)
    y = wrap_text(c, MAIN_LEFT + fw, y, features, F, 7, MAIN_W - fw, 3.2 * mm)
    return y - 3 * mm


def m_edu(c, y, degree, school, date):
    c.setFont(FB, 9)
    c.setFillColor(TEXT_DARK)
    c.drawString(MAIN_LEFT, y, degree)
    c.setFont(F, 7.5)
    c.setFillColor(ACCENT_BLUE)
    c.drawRightString(MAIN_RIGHT, y, date)
    y -= 4 * mm
    c.setFont(FI, 7.5)
    c.setFillColor(TEXT_LIGHT)
    c.drawString(MAIN_LEFT, y, school)
    return y - 5 * mm


# ═══════════════════════════════════════════════════════════════════════════════
# Crop helper
# ═══════════════════════════════════════════════════════════════════════════════

def crop_pdf(path, content_bottom):
    """Remove white space below content."""
    reader = PdfReader(path)
    writer = PdfWriter()
    page = reader.pages[0]
    page.mediabox.lower_left = (0, content_bottom)
    writer.add_page(page)
    with open(path, "wb") as f:
        writer.write(f)


# ═══════════════════════════════════════════════════════════════════════════════
# CV Content - Turkish
# ═══════════════════════════════════════════════════════════════════════════════

def create_tr():
    out = str(OUTPUT_DIR / "cv_tr.pdf")
    c = canvas.Canvas(out, pagesize=A4)
    c.setTitle("Mustafa Akba\u015f - CV")

    draw_sidebar(c)
    sy = HEIGHT - 14 * mm
    sy = draw_photo(c, sy)

    # Name
    c.setFont(FB, 13)
    c.setFillColor(white)
    c.drawCentredString(SIDEBAR_W / 2, sy, "MUSTAFA AKBAŞ")
    sy -= 4.5 * mm
    c.setFont(F, 6.5)
    c.setFillColor(ACCENT_GOLD)
    c.drawCentredString(SIDEBAR_W / 2, sy, "Full Stack Developer | Game Dev | AI Engineer")
    sy -= 2 * mm

    sy = sb_divider(c, sy)

    # Contact
    sy = sb_section(c, sy, "İletişim")
    sy = sb_contact(c, sy, "Telefon", "(+90) 544 247 34 43")
    sy = sb_contact(c, sy, "E-posta", "mustafa@akbas.net")
    sy = sb_contact(c, sy, "Web", "mustafa.akbas.net")
    sy = sb_contact(c, sy, "GitHub", "github.com/makbash")
    sy = sb_contact(c, sy, "Konum", "\u0130stanbul, T\u00fcrkiye")

    # Skills
    sy = sb_section(c, sy, "Beceriler")
    sy = sb_skills_compact(c, sy, "Backend", ["NodeJS", "PHP", "Python", "C++", "FastAPI"])
    sy = sb_skills_compact(c, sy, "Frontend", ["React", "TypeScript", "JavaScript", "Angular"])
    sy = sb_skills_compact(c, sy, "Veritaban\u0131", ["PostgreSQL", "MySQL", "MongoDB", "Redis"])
    sy = sb_skills_compact(c, sy, "AI / ML", ["PyTorch", "HuggingFace", "Stable Diffusion", "ControlNet"])
    sy = sb_skills_compact(c, sy, "Oyun", ["UE5", "C++", "Blueprint", "Niagara"])

    # Languages
    sy = sb_section(c, sy, "Diller")
    sy = sb_language(c, sy, "T\u00fcrk\u00e7e", "Anadil", 5)
    sy = sb_language(c, sy, "\u0130ngilizce", "Orta", 3)

    # === MAIN ===
    my = HEIGHT - 16 * mm

    c.setFont(F, 8)
    c.setFillColor(TEXT_MED)
    summary = (
        "2010'dan bu yana profesyonel olarak yaz\u0131l\u0131m geli\u015ftirme yapmaktay\u0131m. "
        "Java ile ba\u015flayan ser\u00fcvenim PHP, NodeJS ve ReactJS ile devam etmi\u015ftir. "
        "Web geli\u015ftirmenin yan\u0131 s\u0131ra C++ ve Unreal Engine ile oyun geli\u015ftirme, "
        "Python ve PyTorch ile yapay zeka projeleri \u00fczerinde \u00e7al\u0131\u015fmaktay\u0131m."
    )
    my = wrap_text(c, MAIN_LEFT, my, summary, F, 8, MAIN_W, 3.4 * mm)
    my -= 3 * mm

    my = m_section(c, my, "\u0130\u015f Deneyimi", first=True)
    my = m_work(c, my, "Yaz\u0131l\u0131m Geli\u015ftirici", "Icrypex Bili\u015fim A.\u015e. - \u0130stanbul - Full Stack", "Ocak 2022 - Halen", [
        "Kripto para borsas\u0131 backend ve frontend geli\u015ftirme",
        "React, NodeJS ve mikroservis mimarisi ile \u00f6l\u00e7eklenebilir sistemler",
        "REST API tasar\u0131m\u0131, veritaban\u0131 optimizasyonu ve performans iyile\u015ftirmeleri",
    ])
    my = m_work(c, my, "Yaz\u0131l\u0131m Geli\u015ftirici", "Digidea Dijital - \u0130stanbul - Full Stack", "Aral\u0131k 2017 - Ocak 2022", [
        "Kurumsal web uygulamalar\u0131 ve e-ticaret platformlar\u0131 geli\u015ftirme",
        "PHP, NodeJS, React ve Angular ile \u00e7oklu proje y\u00f6netimi",
    ])
    my = m_work(c, my, "Yaz\u0131l\u0131m Geli\u015ftirici / Kurucu", "Avrasya Dijital - \u0130stanbul - Full Stack", "Nisan 2015 - Aral\u0131k 2017", [
        "Dijital ajans kurulumu ve m\u00fc\u015fteri projelerinin u\u00e7tan u\u00e7a y\u00f6netimi",
        "Web uygulama geli\u015ftirme, SEO ve dijital pazarlama \u00e7\u00f6z\u00fcmleri",
    ])
    my = m_work(c, my, "Yaz\u0131l\u0131m Geli\u015ftirici", "BRD - \u0130stanbul - Full Stack", "Ekim 2010 - Mart 2014", [
        "Java ve PHP tabanl\u0131 kurumsal yaz\u0131l\u0131m geli\u015ftirme",
        "Veritaban\u0131 tasar\u0131m\u0131 ve sistem entegrasyonlar\u0131",
    ])

    my = m_section(c, my, "Ki\u015fisel Projeler")
    my = m_project(c, my,
        "Maystro - Generative AI Creative Platform",
        "Yapay zeka destekli g\u00f6rsel ve video \u00fcretim platformu",
        "Python, FastAPI, React, TypeScript, PostgreSQL, PyTorch, HuggingFace, Stable Diffusion, ControlNet, LoRA",
        "AI g\u00f6rsel \u00fcretimi, inpainting/outpainting, node tabanl\u0131 i\u015f ak\u0131\u015f\u0131 edit\u00f6r\u00fc (104+ node), video st\u00fcdyosu, karakter st\u00fcdyosu, \u00e7oklu kullan\u0131c\u0131 deste\u011fi")
    my = m_project(c, my,
        "SurvivalCraft - Multiplayer Survival Oyunu",
        "Unreal Engine 5.6 ile geli\u015ftirilen multiplayer hayatta kalma oyunu",
        "C++, Unreal Engine 5.6, Blueprint, Steam Multiplayer (AdvancedSessions), Niagara VFX",
        "Yap\u0131 sistemi, envanter ve crafting, sava\u015f sistemi, hayvan evcille\u015ftirme ve binme, dinamik hava/mevsim sistemi, kabile sistemi, kay\u0131t/y\u00fckleme, FPS/TPS kamera")

    my = m_section(c, my, "E\u011fitim")
    my = m_edu(c, my, "Yaz\u0131l\u0131m M\u00fchendisli\u011fi", "Netkent Akdeniz Ara\u015ft\u0131rma ve Bilim \u00dcniversitesi", "2022 - 2026")
    my = m_edu(c, my, "Bilgisayar Programc\u0131l\u0131\u011f\u0131", "Gaziosmanpa\u015fa \u00dcniversitesi, Tokat", "2008 - 2010")
    my = m_edu(c, my, "Orman M\u00fchendisli\u011fi", "\u0130stanbul \u00dcniversitesi", "2004 - 2008")

    # Crop & save
    bottom_margin = 10 * mm
    content_bottom = min(my, sy) - bottom_margin
    c.save()
    crop_pdf(out, content_bottom)
    print(f"TR: {out}")


# ═══════════════════════════════════════════════════════════════════════════════
# CV Content - English
# ═══════════════════════════════════════════════════════════════════════════════

def create_en():
    out = str(OUTPUT_DIR / "cv_en.pdf")
    c = canvas.Canvas(out, pagesize=A4)
    c.setTitle("Mustafa Akbaş - CV")

    draw_sidebar(c)
    sy = HEIGHT - 14 * mm
    sy = draw_photo(c, sy)

    # Name
    c.setFont(FB, 13)
    c.setFillColor(white)
    c.drawCentredString(SIDEBAR_W / 2, sy, "MUSTAFA AKBAŞ")
    sy -= 4.5 * mm
    c.setFont(F, 6.5)
    c.setFillColor(ACCENT_GOLD)
    c.drawCentredString(SIDEBAR_W / 2, sy, "Full Stack Developer | Game Dev | AI Engineer")
    sy -= 2 * mm

    sy = sb_divider(c, sy)

    # Contact
    sy = sb_section(c, sy, "Contact")
    sy = sb_contact(c, sy, "Phone", "(+90) 544 247 34 43")
    sy = sb_contact(c, sy, "Email", "mustafa@akbas.net")
    sy = sb_contact(c, sy, "Web", "mustafa.akbas.net")
    sy = sb_contact(c, sy, "GitHub", "github.com/makbash")
    sy = sb_contact(c, sy, "Location", "Istanbul, Turkey")

    # Skills
    sy = sb_section(c, sy, "Skills")
    sy = sb_skills_compact(c, sy, "Backend", ["NodeJS", "PHP", "Python", "C++", "FastAPI"])
    sy = sb_skills_compact(c, sy, "Frontend", ["React", "TypeScript", "JavaScript", "Angular"])
    sy = sb_skills_compact(c, sy, "Database", ["PostgreSQL", "MySQL", "MongoDB", "Redis"])
    sy = sb_skills_compact(c, sy, "AI / ML", ["PyTorch", "HuggingFace", "Stable Diffusion", "ControlNet"])
    sy = sb_skills_compact(c, sy, "Game Dev", ["UE5", "C++", "Blueprint", "Niagara"])

    # Languages
    sy = sb_section(c, sy, "Languages")
    sy = sb_language(c, sy, "Turkish", "Native", 5)
    sy = sb_language(c, sy, "English", "Intermediate", 3)

    # === MAIN ===
    my = HEIGHT - 16 * mm

    c.setFont(F, 8)
    c.setFillColor(TEXT_MED)
    summary = (
        "Professional software developer since 2010. Started with Java, "
        "then expanded to PHP, NodeJS and ReactJS. Beyond web development, "
        "I work on game development with C++ and Unreal Engine, as well as "
        "AI projects using Python and PyTorch."
    )
    my = wrap_text(c, MAIN_LEFT, my, summary, F, 8, MAIN_W, 3.4 * mm)
    my -= 3 * mm

    my = m_section(c, my, "Work Experience", first=True)
    my = m_work(c, my, "Software Developer", "Icrypex Bilisim A.S. - Istanbul - Full Stack", "Jan 2022 - Present", [
        "Cryptocurrency exchange backend and frontend development",
        "Scalable systems with React, NodeJS and microservice architecture",
        "REST API design, database optimization and performance improvements",
    ])
    my = m_work(c, my, "Software Developer", "Digidea Digital - Istanbul - Full Stack", "Dec 2017 - Jan 2022", [
        "Enterprise web applications and e-commerce platform development",
        "Multi-project management with PHP, NodeJS, React and Angular",
    ])
    my = m_work(c, my, "Software Developer / Founder", "Avrasya Digital - Istanbul - Full Stack", "Apr 2015 - Dec 2017", [
        "Digital agency setup and end-to-end client project management",
        "Web application development, SEO and digital marketing solutions",
    ])
    my = m_work(c, my, "Software Developer", "BRD - Istanbul - Full Stack", "Oct 2010 - Mar 2014", [
        "Enterprise software development with Java and PHP",
        "Database design and system integrations",
    ])

    my = m_section(c, my, "Personal Projects")
    my = m_project(c, my,
        "Maystro - Generative AI Creative Platform",
        "AI-powered image and video generation platform",
        "Python, FastAPI, React, TypeScript, PostgreSQL, PyTorch, HuggingFace, Stable Diffusion, ControlNet, LoRA",
        "AI image generation, inpainting/outpainting, node-based workflow editor (104+ nodes), video studio, character studio, multi-user support",
        lang="en")
    my = m_project(c, my,
        "SurvivalCraft - Multiplayer Survival Game",
        "Multiplayer survival game built with Unreal Engine 5.6",
        "C++, Unreal Engine 5.6, Blueprint, Steam Multiplayer (AdvancedSessions), Niagara VFX",
        "Building system, inventory and crafting, combat system (melee/ranged), animal taming and riding, dynamic weather/season system, tribe system, save/load, FPS/TPS camera",
        lang="en")

    my = m_section(c, my, "Education")
    my = m_edu(c, my, "Software Engineering", "Netkent Mediterranean Research and Science University", "2022 - 2026")
    my = m_edu(c, my, "Computer Programming", "Gaziosmanpasa University, Tokat", "2008 - 2010")
    my = m_edu(c, my, "Forest Engineering", "Istanbul University", "2004 - 2008")

    # Crop & save
    bottom_margin = 10 * mm
    content_bottom = min(my, sy) - bottom_margin
    c.save()
    crop_pdf(out, content_bottom)
    print(f"EN: {out}")


# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    create_tr()
    create_en()
    print("Done!")
