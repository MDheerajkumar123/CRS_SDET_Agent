from app.ingestion.chunking.models import DocumentChunk
from app.ingestion.chunking.section_chunker import SectionChunker
from app.ingestion.models.document import DocumentSection, ParsedDocument
from app.ingestion.vector_store.chroma_store import ChromaVectorStore
from app.analysis.retrieval.retriever import RetrievedContext
from app.analysis.services.requirement_analyzer import RequirementAnalyzer
from app.llm.models import LLMResponse


def test_search_filters_by_document_name(tmp_path):
    store = ChromaVectorStore(
        persist_directory=str(tmp_path / "chroma"),
        collection_name="test_documents",
    )

    store.collection.add(
        ids=["chunk-1", "chunk-2"],
        embeddings=[
            [1.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
        ],
        documents=[
            "Sample document content",
            "SmartBank document content",
        ],
        metadatas=[
            {
                "document_name": "Sample.docx",
                "section_id": "SEC-001",
                "section_title": "Sample",
                "page_number": -1,
                "source_path": "Sample.docx",
            },
            {
                "document_name": "SmartBank_BRD_ERD_AI_Practice_New.docx",
                "section_id": "SEC-001",
                "section_title": "SmartBank",
                "page_number": -1,
                "source_path": "SmartBank_BRD_ERD_AI_Practice_New.docx",
            },
        ],
    )

    results = store.search(
        query_embedding=[1.0, 0.0, 0.0],
        n_results=5,
        document_name="SmartBank_BRD_ERD_AI_Practice_New.docx",
    )

    assert len(results["documents"][0]) == 1
    assert (
        results["metadatas"][0][0]["document_name"]
        == "SmartBank_BRD_ERD_AI_Practice_New.docx"
    )


def _document(name: str, sections: list[str]) -> ParsedDocument:
    return ParsedDocument(
        document_name=name,
        document_type="txt",
        source_path=f"data/input/{name}",
        full_text="\n".join(sections),
        sections=[
            DocumentSection(
                section_id=f"SEC-{index:03d}",
                title=f"Section {index}",
                content=content,
            )
            for index, content in enumerate(sections, start=1)
        ],
    )


def _add(store: ChromaVectorStore, chunks: list[DocumentChunk]) -> None:
    store.add_chunks(
        chunks,
        embeddings=[[1.0, 0.0, 0.0] for _ in chunks],
    )


def test_chunk_ids_are_document_scoped_and_deterministic():
    chunker = SectionChunker()

    sample_chunks = chunker.chunk(_document("Sample.docx", ["same text"]))
    customer_chunks = chunker.chunk(_document("CustomerA.docx", ["same text"]))

    assert sample_chunks[0].chunk_id != customer_chunks[0].chunk_id
    assert sample_chunks[0].chunk_id == chunker.chunk(
        _document("Sample.docx", ["same text"])
    )[0].chunk_id


def test_reingestion_replaces_only_the_target_document(tmp_path):
    store = ChromaVectorStore(
        persist_directory=str(tmp_path / "chroma"),
        collection_name="document_reingestion",
    )
    chunker = SectionChunker()
    sample_chunks = chunker.chunk(
        _document("Sample.docx", ["sample section one", "sample section two"])
    )
    customer_chunks = chunker.chunk(
        _document("CustomerA.docx", ["customer section"])
    )

    _add(store, sample_chunks)
    _add(store, customer_chunks)
    assert store.count() == 3

    replacement = chunker.chunk(_document("Sample.docx", ["revised sample"]))
    _add(store, replacement)

    assert store.count() == 2
    sample_records = store.collection.get(
        where={"document_name": "Sample.docx"},
    )
    customer_records = store.collection.get(
        where={"document_name": "CustomerA.docx"},
    )
    assert sample_records["ids"] == [replacement[0].chunk_id]
    assert customer_records["ids"] == [customer_chunks[0].chunk_id]


def test_requirement_analyzer_filters_retrieval_by_document_name():
    class FakeRetriever:
        def __init__(self):
            self.received = None

        def search(self, **kwargs):
            self.received = kwargs
            return [
                RetrievedContext(
                    content="The system shall authenticate users.",
                    source_document="Sample.docx",
                    source_path="data/input/Sample.docx",
                    section_id="SEC-001",
                    section_title="Authentication",
                    page_number=None,
                    distance=0.0,
                )
            ]

    class FakeLLMManager:
        def generate(self, **_kwargs):
            return LLMResponse(
                content=(
                    '{"document_name":"Sample.docx",'
                    '"analysis_summary":"summary",'
                    '"requirements":[],"overall_confidence":1.0}'
                ),
                provider="gemini",
                model="test-model",
                task="crs_analyzer",
            )

    retriever = FakeRetriever()
    analyzer = RequirementAnalyzer(
        retriever=retriever,
        llm_manager=FakeLLMManager(),
    )

    analysis, _ = analyzer.analyze(
        document_name="Sample.docx",
        query="Identify requirements.",
    )

    assert analysis.document_name == "Sample.docx"
    assert retriever.received["document_name"] == "Sample.docx"
