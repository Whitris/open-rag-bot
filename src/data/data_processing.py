from pathlib import Path

import fitz
import pandas as pd
import pikepdf
from pdfminer.high_level import extract_text
from tqdm import tqdm


def ensure_dir(path: str | Path):
    Path(path).mkdir(parents=True, exist_ok=True)


def clean_pdf_with_pikepdf(file_path: str, output_path: str):
    with pikepdf.open(file_path) as pdf:
        with pdf.open_metadata() as meta:
            meta.clear()
        pdf.remove_unreferenced_resources()
        pdf.save(output_path)


def clean_pdf_with_mupdf(file_path: str, output_path: str):
    doc = fitz.open(file_path)
    doc.save(output_path, garbage=4)
    doc.close()


def clean_pdf(file_path: str, output_dir: str = "new_docs") -> str:
    ensure_dir(output_dir)
    file_name = Path(file_path).stem + "_new.pdf"
    output_path = Path(output_dir) / file_name

    try:
        clean_pdf_with_pikepdf(file_path, output_path)
    except Exception:
        clean_pdf_with_mupdf(file_path, output_path)

    return str(output_path)


def extract_text_from_pdf(file_path: str) -> str:
    return extract_text(file_path)


def split_text_into_chunks(text: str, chunk_size: int = 500) -> list[str]:
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        if len(" ".join(current_chunk + [word])) < chunk_size:
            current_chunk.append(word)
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def get_all_pdf_files(root_dir: str) -> list[str]:
    return [
        str(p)
        for p in Path(root_dir).rglob("*.pdf")
        if "_new" not in p.name and "_temp" not in p.name
    ]


def process_pdfs(
    pdf_paths: list[str], chunk_size: int = 500, max_files: int = -1
) -> list[str]:
    processed_chunks = []
    ensure_dir("new_docs")

    for i, path in enumerate(tqdm(pdf_paths, desc="Elaborazione file")):
        if 0 < max_files <= i:
            break
        try:
            cleaned_pdf = clean_pdf(path)
            text = extract_text_from_pdf(cleaned_pdf)
            chunks = split_text_into_chunks(text, chunk_size)
            processed_chunks.extend(chunks)
        except Exception as e:
            print(f"Errore nel file {path}: {e}")

    return processed_chunks


def save_chunks_to_csv(chunks: list[str], output_csv: str = "stuff.csv"):
    cleaned_chunks = [chunk.replace(",", " ") for chunk in chunks]
    df = pd.DataFrame(cleaned_chunks, columns=["text"])
    df.to_csv(output_csv, index=False)
