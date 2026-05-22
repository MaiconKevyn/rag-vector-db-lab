import os
from pathlib import Path

import pytest

from rag_lab.pipeline import ingest_documents, query_documents


@pytest.mark.integration
def test_qdrant_ingest_and_query_returns_expected_source() -> None:
    if os.getenv("RAG_LAB_RUN_QDRANT_INTEGRATION") != "1":
        pytest.skip("set RAG_LAB_RUN_QDRANT_INTEGRATION=1 to run Qdrant integration test")

    count = ingest_documents(store_name="qdrant", docs_path=Path("data/sample_docs"))

    assert count > 0
    results = query_documents("qdrant", "qual vector database roda localmente?", top_k=1)
    assert results
    assert results[0].metadata["source"] == "qdrant.md"
