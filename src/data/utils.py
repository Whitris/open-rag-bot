from pathlib import Path
import re


def ensure_dir(path: str | Path):
    Path(path).mkdir(parents=True, exist_ok=True)


def clean_text(text: str) -> str:
    text = re.sub(r"[^\x20-\x7Eàèéìòù]", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\b(pag(ina)?|page)\s*\d+\b", "", text, flags=re.IGNORECASE)

    return text.strip()


def split_text_into_chunks(text: str, chunk_size: int = 500) -> list[str]:
    words = text.split()
    chunks = []
    current_chunk = []
    for word in words:
        if len(" ".join(current_chunk + [word])) < chunk_size:
            current_chunk.append(word)
        else:
            cleaned = clean_text(" ".join(current_chunk))
            if len(cleaned) > 20:
                chunks.append(cleaned)
            current_chunk = [word]
    if current_chunk:
        cleaned = clean_text(" ".join(current_chunk))
        if len(cleaned) > 20:
            chunks.append(cleaned)
    return chunks
