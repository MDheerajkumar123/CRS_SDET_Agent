from sentence_transformers import SentenceTransformer


class EmbeddingService:

    def __init__(
        self,
        model_name: str = "BAAI/bge-small-en-v1.5",
    ):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def embed_text(self, text: str) -> list[float]:
        if not text or not text.strip():
            raise ValueError(
                "Cannot generate embedding for empty text."
            )

        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    def embed_texts(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        if not texts:
            return []

        if any(
            not text or not text.strip()
            for text in texts
        ):
            raise ValueError(
                "Cannot generate embeddings for empty text."
            )

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
        )

        return embeddings.tolist()

    def get_dimension(self) -> int:
        return self.model.get_embedding_dimension()
