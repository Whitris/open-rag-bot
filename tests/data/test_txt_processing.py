import pytest

from open_rag_bot.data.txt import extract_text_from_txt


@pytest.fixture
def sample_txt(tmp_path):
    path = tmp_path / "test.txt"
    path.write_text("Title line\nSome other content\nAnother line")
    return str(path)


def test_extract_text_and_title_from_txt(sample_txt):
    text, title = extract_text_from_txt(sample_txt)
    assert "Title line" in text
    assert title == "Title line"


def test_extract_text_and_title_from_txt_skip_empty(tmp_path):
    path = tmp_path / "empty_lines.txt"
    path.write_text("\n\nMain Title\nSecond line")
    text, title = extract_text_from_txt(str(path))
    assert "Main Title" in text
    assert title == "Main Title"
