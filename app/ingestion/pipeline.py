from dataclasses import dataclass

from .parsers.factory import DocumentParserFactory
from .cleaners.document_cleaner import DocumentCleaner
from .chunking.section_chunker import SectionChunker
from .embeddings.embedding_service import EmbeddingService
from .vector_store.chroma_store import ChromaVectorStore


@dataclass
class IngestionResult:
    document_name: str
    document_type: str
    sections: int
    chunks: int
    embeddings: int
    stored_records: int


class IngestionPipeline:

    def __init__(self):
        self.chunker = SectionChunker()
        self.embedding_service = EmbeddingService()
        self.vector_store = ChromaVectorStore()

    def ingest(self, file_path: str) -> IngestionResult:

        # 1. Parse
        parser = DocumentParserFactory.get_parser(file_path)
        document = parser.parse(file_path)

        # 2. Clean
        cleaned_document = DocumentCleaner.clean(document)

        # 3. Chunk
        chunks = self.chunker.chunk(cleaned_document)

        # 4. Generate embeddings
        embeddings = self.embedding_service.embed_texts(
            [chunk.content for chunk in chunks]
        )

        # 5. Store in ChromaDB
        self.vector_store.add_chunks(
            chunks,
            embeddings,
        )

        return IngestionResult(
            document_name=cleaned_document.document_name,
            document_type=cleaned_document.document_type,
            sections=len(cleaned_document.sections),
            chunks=len(chunks),
            embeddings=len(embeddings),
            stored_records=self.vector_store.count(),
        )
