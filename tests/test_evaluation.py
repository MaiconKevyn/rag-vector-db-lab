from rag_lab.evaluation import reciprocal_rank, recall_at_k


def test_recall_at_k_returns_one_when_expected_id_is_present() -> None:
    assert recall_at_k(["qdrant"], ["pinecone", "qdrant"], k=2) == 1.0


def test_reciprocal_rank_uses_first_relevant_position() -> None:
    assert reciprocal_rank(["qdrant"], ["pinecone", "qdrant"]) == 0.5
