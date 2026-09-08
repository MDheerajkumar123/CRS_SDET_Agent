from pathlib import Path

from pypdf import PdfReader

from .base import BaseDocumentParser
from ..models.document import ParsedDocument, DocumentSection


class PdfParser(BaseDocumentParser):

    def parse(self, file_path: str) -> ParsedDocument:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"PDF file not found: {file_path}"
            )

        if path.suffix.lower() != ".pdf":
            raise ValueError(
                f"Expected a PDF file, got: {path.suffix}"
            )

        reader = PdfReader(file_path)

        sections = []
        full_text_parts = []

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            text = text.strip()

            if not text:
                continue

            section = DocumentSection(
                section_id=f"SEC-{len(sections) + 1:03d}",
                title=f"Page {page_number}",
                content=text,
                page_number=page_number,
            )

            sections.append(section)
            full_text_parts.append(text)

        full_text = "\n\n".join(full_text_parts)

        return ParsedDocument(
            document_name=path.name,
            document_type="pdf",
            source_path=str(path),
            full_text=full_text,
            sections=sections,
        )
