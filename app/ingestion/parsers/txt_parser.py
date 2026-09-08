from pathlib import Path

from .base import BaseDocumentParser
from ..models.document import ParsedDocument, DocumentSection


class TxtParser(BaseDocumentParser):

    def parse(self, file_path: str) -> ParsedDocument:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"TXT file not found: {file_path}"
            )

        if path.suffix.lower() != ".txt":
            raise ValueError(
                f"Expected a TXT file, got: {path.suffix}"
            )

        text = path.read_text(
            encoding="utf-8"
        ).strip()

        section = DocumentSection(
            section_id="SEC-001",
            title="Document Content",
            content=text,
        )

        return ParsedDocument(
            document_name=path.name,
            document_type="txt",
            source_path=str(path),
            full_text=text,
            sections=[section],
        )
