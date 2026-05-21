from pathlib import Path

from rag_lab.chunking import chunk_text
from rag_lab.config import Settings
from rag_lab.documents import load_markdown_documents
from rag_lab.embeddings import DeterministicEmbedder, FastEmbedder
from rag_lab.vectorstores.base import SearchResult, VectorRecord, VectorStore
from rag_lab.vectorstores.in_memory import InMemoryVectorStore
from rag_lab.vectorstores.pinecone_store import PineconeVectorStore
from rag_lab.vectorstores.qdrant_store import QdrantVectorStore


def build_embedder(settings: Settings) -> FastEmbedder:
    return FastEmbedder(model_name=settings.embedding_model)


def infer_dimensions(embedder: FastEmbedder | DeterministicEmbedder) -> int:
    return len(embedder.embed(["dimension probe"])[0])


def build_records(
    docs_path: Path,
    embedder: FastEmbedder | DeterministicEmbedder,
) -> list[VectorRecord]:
    documents = load_markdown_documents(docs_path)
    chunk_ids: list[str] = []
    texts: list[str] = []
    metadata: list[dict[str, str]] = []
    for document in documents:
        for index, chunk in enumerate(chunk_text(document.text)):
            chunk_ids.append(f"{document.id}:{index}")
            texts.append(chunk)
            metadata.append(
                {
                    "document_id": document.id,
                    "source": document.metadata["source"],
                    "chunk_index": str(index),
                }
            )
    vectors = embedder.embed(texts)
    return [
        VectorRecord(id=chunk_id, text=text, vector=vector, metadata=meta)
        for chunk_id, text, vector, meta in zip(chunk_ids, texts, vectors, metadata, strict=True)
    ]


def build_store(store_name: str, settings: Settings, dimensions: int) -> VectorStore:
    normalized = store_name.lower().replace("_", "-")
    if normalized == "in-memory":
        return InMemoryVectorStore()
    if normalized == "qdrant":
        return QdrantVectorStore(
            collection=settings.collection,
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            dimensions=dimensions,
        )
    if normalized == "pinecone":
        if not settings.pinecone_api_key:
            raise ValueError("RAG_LAB_PINECONE_API_KEY is required for Pinecone")
        return PineconeVectorStore(
            index_name=settings.pinecone_index,
            api_key=settings.pinecone_api_key,
            dimensions=dimensions,
            cloud=settings.pinecone_cloud,
            region=settings.pinecone_region,
        )
    raise ValueError(f"Unsupported vector store: {store_name}")


def ingest_documents(store_name: str, docs_path: Path) -> int:
    settings = Settings(vector_store=store_name)
    embedder = build_embedder(settings)
    records = build_records(docs_path=docs_path, embedder=embedder)
    if not records:
        return 0
    store = build_store(store_name=store_name, settings=settings, dimensions=len(records[0].vector))
    store.upsert(records)
    return len(records)


def query_documents(store_name: str, question: str, top_k: int = 5) -> list[SearchResult]:
    settings = Settings(vector_store=store_name)
    embedder = build_embedder(settings)
    query_vector = embedder.embed([question])[0]
    store = build_store(store_name=store_name, settings=settings, dimensions=len(query_vector))
    return store.search(query_vector, top_k=top_k)
