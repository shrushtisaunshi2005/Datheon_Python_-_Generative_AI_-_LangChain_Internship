
import csv
from pathlib import Path

import pandas as pd
from docx import Document as WordDocument
from pptx import Presentation
from pypdf import PdfReader

from langchain_core.documents import Document


SUPPORTED_EXTENSIONS = {
    ".pdf", ".docx", ".txt", ".md", ".xlsx", ".csv", ".pptx"
}


def load_document(file_path: str) -> list[Document]:
    """Load a supported file and preserve useful source metadata."""

    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"Document not found: {path}")

    extension = path.suffix.lower()
    filename = path.name
    documents = []

    if extension == ".pdf":
        reader = PdfReader(str(path))

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            if text.strip():
                documents.append(
                    Document(
                        page_content=text,
                        metadata={"source": filename, "page": page_number},
                    )
                )

    elif extension == ".docx":
        word_doc = WordDocument(str(path))
        parts = [
            paragraph.text.strip()
            for paragraph in word_doc.paragraphs
            if paragraph.text.strip()
        ]

        for table_index, table in enumerate(word_doc.tables, start=1):
            for row in table.rows:
                values = [cell.text.strip() for cell in row.cells]
                if any(values):
                    parts.append(" | ".join(values))

        text = "\n".join(parts)
        if text.strip():
            documents.append(
                Document(
                    page_content=text,
                    metadata={"source": filename, "page": None},
                )
            )

    elif extension in {".txt", ".md"}:
        text = path.read_text(encoding="utf-8-sig")
        if text.strip():
            documents.append(
                Document(
                    page_content=text,
                    metadata={"source": filename, "page": None},
                )
            )

    elif extension == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.reader(file))

        text = "\n".join(" | ".join(row) for row in rows if any(row))
        if text.strip():
            documents.append(
                Document(
                    page_content=text,
                    metadata={"source": filename, "page": None},
                )
            )

    elif extension == ".xlsx":
        workbook = pd.ExcelFile(path)
        for sheet_name in workbook.sheet_names:
            dataframe = pd.read_excel(workbook, sheet_name=sheet_name)
            text = (
                f"Worksheet: {sheet_name}\n"
                + dataframe.fillna("").to_csv(index=False)
            )
            if text.strip():
                documents.append(
                    Document(
                        page_content=text,
                        metadata={
                            "source": filename,
                            "page": None,
                            "sheet": sheet_name,
                        },
                    )
                )

    elif extension == ".pptx":
        presentation = Presentation(str(path))
        for slide_number, slide in enumerate(presentation.slides, start=1):
            parts = []
            for shape in slide.shapes:
                if getattr(shape, "has_text_frame", False):
                    value = shape.text.strip()
                    if value:
                        parts.append(value)

                if getattr(shape, "has_table", False):
                    for row in shape.table.rows:
                        parts.append(
                            " | ".join(cell.text.strip() for cell in row.cells)
                        )

            text = "\n".join(parts)
            if text.strip():
                documents.append(
                    Document(
                        page_content=text,
                        metadata={"source": filename, "page": slide_number},
                    )
                )

    else:
        supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
        raise ValueError(
            f"Unsupported file type: {extension or '(no extension)'}. "
            f"Supported formats: {supported}"
        )

    if not documents:
        raise ValueError(f"No readable text found in {filename}.")

    return documents


def load_documents(file_paths: list[str]) -> list[Document]:
    """Load multiple supported documents."""

    all_documents = []

    for file_path in file_paths:
        all_documents.extend(load_document(file_path))

    if not all_documents:
        raise ValueError("No readable documents were found.")

    return all_documents
