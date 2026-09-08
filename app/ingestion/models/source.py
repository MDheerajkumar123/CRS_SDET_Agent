from dataclasses import dataclass


@dataclass
class SourceReference:
    document_name: str
    source_path: str
    section_id: str
    section_title: str
    page_number: int | None = None
    source_text: str = ""
