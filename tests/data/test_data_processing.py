from pathlib import Path
import pandas as pd
import pytest

from src.data.data_processing import (
    clean_pdf,
    clean_pdf_with_mupdf,
    ensure_dir,
    get_all_pdf_files,
    process_pdfs,
    save_chunks_to_csv,
    split_text_into_chunks,
)


@pytest.fixture
def sample_pdf(tmp_path):
    path = tmp_path / "test.pdf"
    import fitz

    doc = fitz.open()
    doc.new_page()
    doc.save(str(path))
    doc.close()
    return str(path)


def test_ensure_dir(tmp_path):
    d = tmp_path / "subdir" / "nested"
    ensure_dir(d)
    assert d.exists() and d.is_dir()


def test_clean_pdf_with_mupdf(sample_pdf, tmp_path):
    out = tmp_path / "out.pdf"
    clean_pdf_with_mupdf(sample_pdf, str(out))
    assert out.exists() and out.stat().st_size > 0


def test_clean_pdf_fallback(sample_pdf, tmp_path, mocker):
    # Patching clean_pdf_with_pikepdf per simulare fallimento
    mocker.patch(
        "src.data.data_processing.clean_pdf_with_pikepdf",
        side_effect=RuntimeError("pikepdf fail"),
    )
    out = tmp_path / "test_new.pdf"
    result = clean_pdf(sample_pdf, output_dir=tmp_path)
    assert out.name in result


def test_split_text_into_chunks():
    text = " ".join(str(i) for i in range(100))
    chunks = split_text_into_chunks(text, chunk_size=50)
    assert all(len(c) <= 50 for c in chunks)


def test_get_all_pdf_files(tmp_path):
    pdf1 = tmp_path / "a.pdf"
    pdf1.write_text("dummy")
    temp = tmp_path / "a_new.pdf"
    temp.write_text("dummy")
    nested = tmp_path / "sub"
    nested.mkdir()
    nested_pdf = nested / "b.pdf"
    nested_pdf.write_text("dummy")
    files = get_all_pdf_files(str(tmp_path))

    assert str(pdf1) in files
    assert str(nested_pdf) in files
    assert not any("new" in f for f in files)


def test_process_and_save(tmp_path, sample_pdf, mocker):
    docs = tmp_path / "docs"
    docs.mkdir()
    p = docs / "test.pdf"
    p.write_bytes(Path(sample_pdf).read_bytes())

    # Patch extract_text_from_pdf per evitare dipendenze esterne
    mocker.patch(
        "src.data.data_processing.extract_text_from_pdf", return_value="word " * 300
    )
    chunks = process_pdfs([str(p)], chunk_size=100, max_files=1)
    assert len(chunks) >= 1

    out_csv = tmp_path / "out.csv"
    save_chunks_to_csv(chunks, str(out_csv))
    df = pd.read_csv(str(out_csv))
    assert not df.empty
    assert all("word" in txt for txt in df.text)
