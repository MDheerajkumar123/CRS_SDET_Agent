from dataclasses import dataclass

from ..models.source import SourceReference


@dataclass
class DocumentChunk:
    chunk_id: str
    document_name: str
    section_id: str
    section_title: str
    content: str
    page_number: int | None = None
    source_reference: SourceReference | None = None
