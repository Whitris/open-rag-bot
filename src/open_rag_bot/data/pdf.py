import logging
import tempfile
from pathlib import Path

import fitz
import pikepdf
from pdfminer.high_level import extract_text

from open_rag_bot.data.utils import ensure_dir

logger = logging.getLogger(__name__)


def clean_pdf(file_path: str, output_dir: str = "new_docs") -> str:
    ensure_dir(output_dir)
    file_name = Path(file_path).stem + "_new.pdf"
    output_path = Path(output_dir) / file_name

    try:
        clean_pdf_with_pikepdf(file_path, output_path)
    except pikepdf.PdfError:
        clean_pdf_with_mupdf(file_path, output_path)
    except Exception:
        logger.exception(f"Unexpected error on {file_path}.")
        raise
    return str(output_path)


def clean_pdf_with_mupdf(file_path: str, output_path: str):
    doc = fitz.open(file_path)
    doc.save(output_path, garbage=4)
    doc.close()


def clean_pdf_with_pikepdf(file_path: str, output_path: str):
    with pikepdf.open(file_path) as pdf:
        with pdf.open_metadata() as meta:
            meta.clear()
        pdf.remove_unreferenced_resources()
        pdf.save(output_path)


def extract_text_from_pdf(file_path: str) -> tuple[str, str]:
    """Extract the main text and a best-effort title from a PDF."""
    with tempfile.TemporaryDirectory() as temp_dir:
        cleaned_pdf = clean_pdf(file_path, temp_dir)
        text = extract_text(cleaned_pdf)

    title = (
        extract_title_from_metadata(cleaned_pdf)
        or extract_title_from_first_page(cleaned_pdf)
        or extract_title_from_text(text)
    )
    return text, title


def extract_title_from_metadata(pdf_path: str) -> str:
    """Try to extract title from PDF metadata."""
    try:
        with pikepdf.open(pdf_path) as pdf:
            docinfo = pdf.docinfo
            if docinfo and docinfo.get("/Title"):
                return str(docinfo.get("/Title")).strip()
    except Exception:
        logger.debug(f"Error reading metadata for {pdf_path}.")
    return ""


def extract_title_from_first_page(pdf_path: str) -> str:
    """Try to extract a plausible title from the first page's visible text."""
    try:
        doc = fitz.open(pdf_path)
        if doc.page_count > 0:
            page = doc[0]
            blocks = page.get_text("blocks")
            blocks = sorted(blocks, key=lambda b: b[1])
            for b in blocks:
                line = b[4].strip()
                if line:
                    return line
        doc.close()
    except Exception:
        logger.debug(f"Error processing first page for {pdf_path}.")
    return ""


def extract_title_from_text(text: str) -> str:
    """Fallback: guess a title from the first non-empty lines of the extracted text."""
    lines = [line.strip() for line in text.replace("\r", "\n").split("\n")]
    buffer = []
    for line in lines:
        if line:
            buffer.append(line)
        elif buffer:
            break
    return " ".join(buffer) if buffer else ""
