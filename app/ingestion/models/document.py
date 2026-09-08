from dataclasses import dataclass, field
from typing import List


@dataclass
class DocumentSection:
    section_id: str
    title: str
    content: str
    page_number: int | None = None


@dataclass
class ParsedDocument:
    document_name: str
    document_type: str
    source_path: str
    full_text: str
    sections: List[DocumentSection] = field(default_factory=list)
