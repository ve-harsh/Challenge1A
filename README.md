# 🧠 Adobe Round 1A – PDF Structure Extractor

This project extracts the **title** and **structured headings (H1–H3)** from PDF files using PyMuPDF and spaCy. It processes documents offline and returns a clean, hierarchical outline in the required JSON format.

---

## 📦 Requirements Used

### Python Libraries (`requirements.txt`)
| Library         | Purpose |
|----------------|---------|
| `PyMuPDF`      | Fast PDF parsing and layout access (text, font sizes, positions) |
| `pdfminer.six` | Optional backup parser for deeper analysis (not mandatory) |
| `spaCy`        | NLP engine for sentence structure and language understanding |
| `numpy`        | Used for heading classification logic (based on layout patterns) |
| `langdetect`   | Detects primary language of each document |

> All dependencies are CPU-friendly and <200MB combined size.

---

## 🐳 Docker Environment

### Dockerfile Highlights

- Uses `python:3.10-slim` base image
- Installs minimal system dependencies (`poppler-utils`, `libgl1`, etc.)
- Downloads English spaCy model (`en_core_web_sm`)
- Copies all files and runs `main.py`
- Creates `/input` and `/output` folders inside container




## ✅ Output Format

Each `.pdf` file is converted to a `.json` file using this structure:


{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}


##🧠 Approach
The solution balances layout-based heuristics with lightweight NLP. Here's a breakdown:

🔹 Title Extraction
Extracted from the first page

Picks the longest meaningful line (with >5 words) that likely represents the title

🔹 Heading Detection
Each page is scanned for potential headings

A combination of font size, text casing, and line structure is used

The heading level (H1, H2, H3) is assigned based on:

Font size (relative across document)

Common heading patterns (1., 1.1, ending with :)

Text formatting (UPPERCASE, Title Case)

🔹 Language Detection (Internal Use)
Uses langdetect to identify the primary language

Not included in output but available if needed for multilingual filtering


### Build Docker Image

```bash
docker build --platform linux/amd64 -t adobe-pdf-extractor .
