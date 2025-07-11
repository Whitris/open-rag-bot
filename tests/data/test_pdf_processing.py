import fitz
import pikepdf
import pytest

from src.data.pdf import (
    clean_pdf,
    clean_pdf_with_mupdf,
    ensure_dir,
    extract_text_from_pdf,
    extract_title_from_first_page,
    extract_title_from_metadata,
    extract_title_from_text,
)


@pytest.fixture
def sample_pdf(tmp_path):
    path = tmp_path / "test.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "PDF Main Title", fontsize=20)
    page.insert_text((72, 120), "Some body text.")
    doc.save(str(path))
    doc.close()
    return str(path)


def test_ensure_dir(tmp_path):
    d = tmp_path / "subdir" / "nested"
    ensure_dir(d)
    assert d.exists()
    assert d.is_dir()


def test_clean_pdf_with_mupdf(sample_pdf, tmp_path):
    out = tmp_path / "out.pdf"
    clean_pdf_with_mupdf(sample_pdf, str(out))
    assert out.exists()
    assert out.stat().st_size > 0


def test_clean_pdf_fallback(sample_pdf, tmp_path, mocker):
    import pikepdf

    mocker.patch(
        "src.data.pdf.clean_pdf_with_pikepdf",
        side_effect=pikepdf.PdfError("pikepdf fail"),
    )
    out = tmp_path / "test_new.pdf"
    result = clean_pdf(sample_pdf, output_dir=tmp_path)
    assert out.name in result


def test_extract_text_from_pdf_title_and_text(sample_pdf):
    # Test che estrae testo e titolo da un PDF di esempio
    text, title = extract_text_from_pdf(sample_pdf)
    assert "PDF Main Title" in text
    assert title == "PDF Main Title"  # Titolo dovrebbe essere il primo heading grande


def test_extract_text_from_pdf_fallback_title(tmp_path):
    path = tmp_path / "plain.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 120), "Fallback title")
    page.insert_text((72, 140), "This is content")
    doc.save(str(path))
    doc.close()
    text, title = extract_text_from_pdf(str(path))
    assert "Fallback title" in text
    assert title == "Fallback title"


def test_extract_title_from_metadata_with_title(tmp_path):
    # Crea un PDF temporaneo con titolo
    pdf_path = tmp_path / "has_title.pdf"
    with pikepdf.new() as pdf:
        pdf.docinfo["/Title"] = "Test PDF Title"
        pdf.save(str(pdf_path))
    title = extract_title_from_metadata(str(pdf_path))
    assert title == "Test PDF Title"


def test_extract_title_from_metadata_no_title(tmp_path):
    pdf_path = tmp_path / "no_title.pdf"
    with pikepdf.new() as pdf:
        pdf.save(str(pdf_path))
    title = extract_title_from_metadata(str(pdf_path))
    assert title == ""


def test_extract_title_from_first_page_with_text(tmp_path):
    pdf_path = tmp_path / "first_page.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "The Main Title", fontsize=24)
    doc.save(str(pdf_path))
    doc.close()
    title = extract_title_from_first_page(str(pdf_path))
    assert "The Main Title" in title


def test_extract_title_from_first_page_empty(tmp_path):
    pdf_path = tmp_path / "empty.pdf"
    doc = fitz.open()
    doc.new_page()
    doc.save(str(pdf_path))
    doc.close()
    title = extract_title_from_first_page(str(pdf_path))
    assert title == ""


def test_extract_title_from_text_basic():
    text = "\nTitle line\n\nOther content\n"
    title = extract_title_from_text(text)
    assert title == "Title line"


def test_extract_title_from_text_multiple_lines():
    text = "\nFirst\nSecond\n\nBody"
    title = extract_title_from_text(text)
    assert title == "First Second"


def test_extract_title_from_text_empty():
    assert extract_title_from_text("") == ""


def test_extract_text_from_pdf_full(tmp_path):
    # Prepara un PDF con PyMuPDF e pikepdf, scrivi titolo sia come metadata che come testo
    pdf_path = tmp_path / "test_full.pdf"
    import fitz
    import pikepdf

    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Portfolio Test Title", fontsize=20)
    doc.save(str(pdf_path))
    doc.close()
    # Set metadata
    with pikepdf.open(str(pdf_path)) as pdf:
        pdf.docinfo["/Title"] = "Portfolio Test Title"
        temp_pdf_path = tmp_path / "temp.pdf"
        pdf.save(str(temp_pdf_path))
    # Sovrascrivi il file originale
    import os

    os.replace(str(temp_pdf_path), str(pdf_path))

    text, title = extract_text_from_pdf(str(pdf_path))
    assert "Portfolio Test Title" in text
    assert title == "Portfolio Test Title"
