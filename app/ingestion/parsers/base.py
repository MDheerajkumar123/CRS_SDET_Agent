from abc import ABC, abstractmethod

from app.ingestion.models.document import ParsedDocument


class BaseDocumentParser(ABC):

    @abstractmethod
    def parse(self, file_path: str) -> ParsedDocument:
        """
        Parse a document and return a common ParsedDocument representation.
        """
        pass
