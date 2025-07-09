import pytest
import fitz
from src.data.pdf import (
    clean_pdf,
    clean_pdf_with_mupdf,
    extract_text_from_pdf,
    ensure_dir,
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
    assert d.exists() and d.is_dir()

def test_clean_pdf_with_mupdf(sample_pdf, tmp_path):
    out = tmp_path / "out.pdf"
    clean_pdf_with_mupdf(sample_pdf, str(out))
    assert out.exists() and out.stat().st_size > 0

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

