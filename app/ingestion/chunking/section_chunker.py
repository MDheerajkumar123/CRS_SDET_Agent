from ..models.document import ParsedDocument
from .models import DocumentChunk
from ..models.source import SourceReference

class SectionChunker:

    def __init__(
        self,
        max_chunk_size: int = 1200,
        overlap: int = 150,
    ):
        if max_chunk_size <= 0:
            raise ValueError(
                "max_chunk_size must be greater than 0."
            )

        if overlap < 0:
            raise ValueError(
                "overlap cannot be negative."
            )

        if overlap >= max_chunk_size:
            raise ValueError(
                "overlap must be smaller than max_chunk_size."
            )

        self.max_chunk_size = max_chunk_size
        self.overlap = overlap

    def chunk(self, document: ParsedDocument) -> list[DocumentChunk]:
        chunks = []
        chunk_counter = 1

        for section in document.sections:
            content = section.content.strip()

            if not content:
                continue

            start = 0
            content_length = len(content)

            while start < content_length:
                end = min(
                    start + self.max_chunk_size,
                    content_length,
                )

                chunk_text = content[start:end].strip()

                if chunk_text:
                    chunks.append(
                        DocumentChunk(
                            chunk_id=f"CHUNK-{chunk_counter:04d}",
                            document_name=document.document_name,
                            section_id=section.section_id,
                            section_title=section.title,
                            content=chunk_text,
                            page_number=section.page_number,
                            source_reference=SourceReference(
                                document_name=document.document_name,
                                source_path=document.source_path,
                                section_id=section.section_id,
                                section_title=section.title,
                                page_number=section.page_number,
                                source_text=chunk_text,
                            ),
                        )
                    )

                    chunk_counter += 1

                if end >= content_length:
                    break

                start = end - self.overlap

        return chunks
