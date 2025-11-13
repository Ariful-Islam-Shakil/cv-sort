import os
from typing import List
import pdfplumber
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io
import json
from loguru import logger

def extract_pdf_links(pdf_path):
    """
    Extracts hyperlinks from a PDF using PyMuPDF.
    Returns a list of (page_number, link_text, uri) tuples.
    """
    links = []
    try:
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"File not found: {pdf_path}")

        # Open the PDF
        with fitz.open(pdf_path) as doc:
            for page_num, page in enumerate(doc, start=1):
                for link in page.get_links():
                    uri = link.get("uri", None)
                    if uri:
                        # You can also try to extract nearby text (optional)
                        rect = fitz.Rect(link["from"])
                        text = page.get_textbox(rect).strip()
                        # links.append((page_num, text, uri))
                        links.append(uri)
                        # logger.error(uri, "\n\n")

        return links

    except Exception as e:
        print(f"Error reading links from {pdf_path}: {e}")
        return []

def extract_text_pdfplumber(pdf_path: str) -> str:
    """Try extracting text using pdfplumber (works for text-based PDFs)."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        if text.strip():
            logger.info(f"Extracted text using pdfplumber from {pdf_path}")
        return text.strip()
    except Exception:
        return ""


def extract_text_pymupdf(pdf_path: str) -> str:
    """Try extracting text using PyMuPDF."""
    try:
        text = ""
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text("text")  # text extraction
        if text.strip():
            logger.info(f"Extracted text using PyMuPDF from {pdf_path}")
        return text.strip()
    except Exception:
        return ""


def extract_text_ocr(pdf_path: str) -> str:
    """
    Extract text from scanned PDFs using OCR (Tesseract).
    Handles low-DPI and image-based pages better.
    """
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page_num, page in enumerate(doc, start=1):
                # Render page at higher resolution (DPI ~300)
                zoom = 3  # 3x zoom = about 300 DPI
                mat = fitz.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat)

                # Convert to PIL Image
                img = Image.open(io.BytesIO(pix.tobytes("png")))

                # Run OCR
                extracted = pytesseract.image_to_string(img, lang="eng")

                if extracted.strip():
                    text += f"\n--- Page {page_num} ---\n{extracted.strip()}\n"

        return text.strip()
    except Exception as e:
        print(f"OCR failed for {pdf_path}: {e}")
        return ""


def read_cv_info(folder_path: str) -> List[str]:
    """Read all PDFs (including nested) and extract text from each."""
    all_texts = []
    links = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_path = os.path.join(root, file)
                link = extract_pdf_links(pdf_path)
                links.append(link)
                text = extract_text_pdfplumber(pdf_path)
                if not text:  # fallback to PyMuPDF
                    text = extract_text_pymupdf(pdf_path)
                if not text:  # final fallback using OCR
                    text = extract_text_ocr(pdf_path)
                if not text:
                    logger.warning(f"No text extracted from {pdf_path}")

                all_texts.append(str( file + " : \n" + text ) if text else f"[No readable text in {file}]")
    # logger.error(f"\n\nExtracted links are: {links}\n\n")
    # save_cv_data_to_json(links, "/Users/mdarifulislamshakil/ztrios/cv-sort/extracted_links.json")
    return all_texts

def save_cv_data_to_json(cv_texts: List[str], output_path: str):
    """
    Save extracted CV text data to a JSON file.

    Args:
        cv_texts: List of strings (each string = text from one CV)
        output_path: File path where JSON will be saved
    """
    try:
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Save as JSON
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(cv_texts, f, ensure_ascii=False, indent=4)

        print(f"✅ CV data successfully saved to: {output_path}")
    except Exception as e:
        print(f"❌ Error saving CV data: {e}")



if __name__ == "__main__":
    folder = "/Users/mdarifulislamshakil/ztrios/cv-sort/AI-Intern-9-Nov-2025"
    output_json = "/Users/mdarifulislamshakil/ztrios/cv-sort/cv_data.json"
    cv_texts = read_cv_info(folder)
    print(f"Extracted {len(cv_texts)} CVs")
    print(len(cv_texts[0]))  # print first 500 chars of first CV
    save_cv_data_to_json(cv_texts, output_json)