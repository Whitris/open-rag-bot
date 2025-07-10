import logging
import tempfile
from pathlib import Path

import fitz
import pikepdf
from pdfminer.high_level import extract_text

from src.data.utils import ensure_dir


def clean_pdf(file_path: str, output_dir: str = "new_docs") -> str:
    ensure_dir(output_dir)
    file_name = Path(file_path).stem + "_new.pdf"
    output_path = Path(output_dir) / file_name

    try:
        clean_pdf_with_pikepdf(file_path, output_path)
    except pikepdf.PdfError:
        clean_pdf_with_mupdf(file_path, output_path)
    except Exception as e:
        logging.error(f"Errore inaspettato su {file_path}: {e}")
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
    """
    1. Pulisce il PDF (con PikePDF o MuPDF)
    2. Estrae testo e titolo dal PDF pulito
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        cleaned_pdf = clean_pdf(file_path, temp_dir)
        text = extract_text(cleaned_pdf)

    title = ""
    try:
        with pikepdf.open(cleaned_pdf) as pdf:
            docinfo = pdf.docinfo
            if docinfo and docinfo.get("/Title"):
                title = str(docinfo.get("/Title")).strip()
    except Exception:
        pass

    if not title:
        try:
            doc = fitz.open(cleaned_pdf)
            if doc.page_count > 0:
                page = doc[0]
                blocks = page.get_text("blocks")
                blocks = sorted(blocks, key=lambda b: b[1])
                for b in blocks:
                    line = b[4].strip()
                    if line:
                        title = line
                        break
                doc.close()
        except Exception:
            pass

    if not title:
        lines = [line.strip() for line in text.replace("\r", "\n").split("\n")]
        buffer = []
        for line in lines:
            if line:
                buffer.append(line)
            elif buffer:
                break
        title = " ".join(buffer) if buffer else ""

    return text, title
