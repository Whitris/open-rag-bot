def extract_text_from_txt(file_path: str) -> tuple[str, str]:
    with open(file_path, encoding="utf-8") as f:
        lines = f.readlines()
    title = ""
    for line in lines:
        if line.strip():
            title = line.strip()
            break
    text = "".join(lines)
    return text, title
