from pathlib import Path

from pypdf import PdfReader
from docx import Document as DocxDocument


def extract_text_from_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n\n".join(pages)


def extract_text_from_docx(file_path: str) -> str:
    document = DocxDocument(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            paragraphs.append(paragraph.text)

    return "\n".join(paragraphs)


def extract_text_from_txt(file_path: str) -> str:
    return Path(file_path).read_text(
        encoding="utf-8"
    )


def extract_text(
    file_path: str,
    file_type: str
) -> str:

    if file_type == "pdf":
        return extract_text_from_pdf(file_path)

    if file_type == "docx":
        return extract_text_from_docx(file_path)

    if file_type == "txt":
        return extract_text_from_txt(file_path)

    raise ValueError(
        f"Unsupported file type: {file_type}"
    )