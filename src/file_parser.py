from pathlib import Path

from pypdf import PdfReader
from docx import Document


def extract_text_from_file(file_path: str) -> str:
    """
    Extract text from TXT, PDF, or DOCX files.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    extension = path.suffix.lower()

    if extension == ".txt":
        return path.read_text(encoding="utf-8")

    if extension == ".pdf":
        reader = PdfReader(str(path))

        pages = []

        for page in reader.pages:
            text = page.extract_text()

            if text:
                pages.append(text)

        return "\n".join(pages)

    if extension == ".docx":
        document = Document(str(path))

        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        return "\n".join(paragraphs)

    raise ValueError(
        "Unsupported file type. Please use a .txt, .pdf, or .docx file."
    )
