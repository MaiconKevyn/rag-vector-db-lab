from rag_lab.vectorstores.base import VectorRecord
from rag_lab.vectorstores.in_memory import InMemoryVectorStore


def test_in_memory_store_returns_nearest_records() -> None:
    store = InMemoryVectorStore()
    store.upsert(
        [
            VectorRecord(id="qdrant", text="Qdrant runs locally", vector=[1.0, 0.0], metadata={}),
            VectorRecord(id="pinecone", text="Pinecone is managed", vector=[0.0, 1.0], metadata={}),
        ]
    )

    results = store.search([0.9, 0.1], top_k=1)

    assert results[0].id == "qdrant"
    assert results[0].score > 0.9
