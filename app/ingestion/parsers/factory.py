from pathlib import Path

from .base import BaseDocumentParser
from .docx_parser import DocxParser
from .pdf_parser import PdfParser
from .txt_parser import TxtParser


class DocumentParserFactory:

    @staticmethod
    def get_parser(file_path: str) -> BaseDocumentParser:
        extension = Path(file_path).suffix.lower()

        if extension == ".docx":
            return DocxParser()

        if extension == ".pdf":
            return PdfParser()

        if extension == ".txt":
            return TxtParser()

        raise ValueError(
            f"Unsupported document type: {extension}"
        )
