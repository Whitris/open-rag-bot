import logging
from collections.abc import Callable
from pathlib import Path

from tqdm import tqdm

from src.data.docx import extract_text_from_docx
from src.data.pdf import extract_text_from_pdf
from src.data.txt import extract_text_from_txt
from src.data.utils import split_text_into_chunks

extractors: dict[str, Callable[[str], str]] = {
    ".pdf": extract_text_from_pdf,
    ".txt": extract_text_from_txt,
    ".docx": extract_text_from_docx,
}


def get_all_files(root_dir: str, extensions=None) -> list[str]:
    if extensions is None:
        extensions = list(extractors.keys())
    return [
        str(p)
        for ext in extensions
        for p in Path(root_dir).rglob(f"*{ext}")
        if "_new" not in p.name and "_temp" not in p.name
    ]


def process_files(file_paths: list[str], chunk_size: int = 500, max_files: int = -1) -> list[dict]:
    processed_chunks = []
    for i, path in tqdm(
        enumerate(file_paths[:max_files]),
        desc="File processing",
        total=len(file_paths) if max_files == -1 else max_files,
    ):
        if 0 < max_files <= i:
            break
        ext = Path(path).suffix.lower()
        extractor = extractors.get(ext)
        if not extractor:
            logging.warning(f"Nessun extractor per {path}")
            continue
        try:
            result = extractor(path)
            if isinstance(result, tuple):
                text, title = result
            else:
                text, title = result, ""
            chunks = split_text_into_chunks(text, chunk_size)
            for chunk in chunks:
                processed_chunks.append(
                    {"filename": Path(path).name, "title": title, "text": chunk}
                )
        except Exception as e:
            logging.warning(f"Errore nel file {path}: {type(e).__name__}: {e}")
    return processed_chunks
