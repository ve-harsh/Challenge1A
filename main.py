# main.py

import os
import fitz  # PyMuPDF
import spacy
import json
from pathlib import Path

INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"

nlp = spacy.load("en_core_web_sm")

def extract_outline_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    outline = {
        "Title": None,
        "Outline": []
    }

    title_found = False

    for page_num, page in enumerate(doc, start=1):
        text_blocks = page.get_text("dict")["blocks"]

        for block in text_blocks:
            if "lines" not in block:
                continue

            for line in block["lines"]:
                sentence = " ".join(span["text"] for span in line["spans"]).strip()

                if not sentence or len(sentence.split()) < 2:
                    continue

                doc_nlp = nlp(sentence)

                if not title_found and len(sentence.split()) > 5:
                    outline["Title"] = sentence
                    title_found = True
                    continue

                # Simpler heading heuristics based on entity labels and patterns
                if sentence.isupper() or sentence.istitle():
                    heading_level = detect_heading_level(sentence)
                    outline[""].append({
                        "level": heading_level,
                        "text": sentence,
                        "page": page_num
                    })

    return outline

def detect_heading_level(text):
    # Simple heuristic: based on length or keywords
    if len(text.split()) <= 2:
        return "H1"
    elif len(text.split()) <= 4:
        return "H2"
    else:
        return "H3"

def save_json(outline, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(outline, f, indent=2)

def main():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    for file_name in os.listdir(INPUT_FOLDER):
        if not file_name.endswith(".pdf"):
            continue

        pdf_path = os.path.join(INPUT_FOLDER, file_name)
        outline = extract_outline_from_pdf(pdf_path)

        output_json_path = os.path.join(OUTPUT_FOLDER, file_name.replace(".pdf", ".json"))
        save_json(outline, output_json_path)
        print(f"Processed: {file_name} -> {output_json_path}")

if __name__ == "__main__":
    main()
