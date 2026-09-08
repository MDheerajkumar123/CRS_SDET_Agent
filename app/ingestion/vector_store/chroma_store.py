from pathlib import Path

import chromadb

from ..chunking.models import DocumentChunk


class ChromaVectorStore:



    def __init__(
        self,
        persist_directory: str = "data/chroma",
        collection_name: str = "crs_documents",
    ):
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.client = chromadb.PersistentClient(
            path=str(self.persist_directory)
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def add_chunks(
        self,
        chunks: list[DocumentChunk],
        embeddings: list[list[float]],
    ) -> None:

        if len(chunks) != len(embeddings):
            raise ValueError(
                "Number of chunks must match number of embeddings."
            )

        if not chunks:
            return

        # Remove existing records with the same chunk IDs.
        chunk_ids = [
            chunk.chunk_id
            for chunk in chunks
        ]

        existing = self.collection.get(
            ids=chunk_ids,
        )

        existing_ids = existing.get("ids", [])

        if existing_ids:
            self.collection.delete(
                ids=existing_ids,
            )

        self.collection.add(
            ids=chunk_ids,
            embeddings=embeddings,
            documents=[
                chunk.content
                for chunk in chunks
            ],
            metadatas=[
                {
                    "document_name": chunk.document_name,
                    "section_id": chunk.section_id,
                    "section_title": chunk.section_title,
                    "page_number": (
                        chunk.page_number
                        if chunk.page_number is not None
                        else -1
                    ),
                    "source_path": (
                        chunk.source_reference.source_path
                        if chunk.source_reference
                        else ""
                    ),
                }
                for chunk in chunks
            ],
        )

    def count(self) -> int:
        return self.collection.count()
    def search(
        self,
        query_embedding: list[float],
        n_results: int = 5,
    ) -> dict:
        if not query_embedding:
            raise ValueError(
                "Query embedding cannot be empty."
            )

        if n_results <= 0:
            raise ValueError(
                "n_results must be greater than 0."
            )

        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )
