from dataclasses import dataclass

from app.ingestion.embeddings.embedding_service import EmbeddingService
from app.ingestion.vector_store.chroma_store import ChromaVectorStore


@dataclass
class RetrievedContext:
    content: str
    source_document: str
    source_path: str
    section_id: str
    section_title: str
    page_number: int | None
    distance: float


class CRSRetriever:

    def __init__(
        self,
        embedding_service: EmbeddingService | None = None,
        vector_store: ChromaVectorStore | None = None,
    ):
        self.embedding_service = (
            embedding_service or EmbeddingService()
        )

        self.vector_store = (
            vector_store or ChromaVectorStore()
        )

    def search(
        self,
        query: str,
        n_results: int = 5,
    ) -> list[RetrievedContext]:

        if not query or not query.strip():
            raise ValueError(
                "Search query cannot be empty."
            )

        query_embedding = self.embedding_service.embed_text(
            query
        )

        results = self.vector_store.search(
            query_embedding=query_embedding,
            n_results=n_results,
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        contexts = []

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances,
        ):
            page_number = metadata.get("page_number")

            if page_number == -1:
                page_number = None

            contexts.append(
                RetrievedContext(
                    content=document,
                    source_document=metadata.get(
                        "document_name",
                        "",
                    ),
                    source_path=metadata.get(
                        "source_path",
                        "",
                    ),
                    section_id=metadata.get(
                        "section_id",
                        "",
                    ),
                    section_title=metadata.get(
                        "section_title",
                        "",
                    ),
                    page_number=page_number,
                    distance=distance,
                )
            )

        return contexts
