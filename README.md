# My CV Generator

Python script that generates my professional CV as PDF in both Turkish and English.

## Structure

```
mycv/
├── assets/
│   └── photo.jpg          # Profile photo (circular crop applied automatically)
├── output/
│   ├── cv_tr.pdf           # Generated - Turkish version
│   └── cv_en.pdf           # Generated - English version
├── generate.py             # CV generator script
└── README.md
```

## Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- Windows (uses Calibri font from `C:\Windows\Fonts`)

## Usage

```bash
# With uv (no virtual env needed)
uv run --with reportlab --with pypdf generate.py

# Or with pip
pip install reportlab pypdf
python generate.py
```

Both `output/cv_tr.pdf` and `output/cv_en.pdf` will be generated.

## Customization

Edit `generate.py` to update:

| What | Where |
|---|---|
| **Colors** | `BG_DARK`, `ACCENT_GOLD`, `ACCENT_BLUE` etc. at the top |
| **Work experience** | `create_tr()` / `create_en()` - `m_work()` calls |
| **Projects** | `m_project()` calls |
| **Education** | `m_edu()` calls |
| **Skills** | `sb_skills_compact()` calls in sidebar |
| **Contact info** | `sb_contact()` calls in sidebar |
| **Photo** | Replace `assets/photo.jpg` |

## Template

Dark navy sidebar with gold accents. Calibri font for full Turkish character support.
