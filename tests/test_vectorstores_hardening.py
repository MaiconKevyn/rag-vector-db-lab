from rag_lab.vectorstores.base import VectorStoreError, ensure_vector_dimensions


def test_ensure_vector_dimensions_rejects_mismatch() -> None:
    try:
        ensure_vector_dimensions(expected=3, actual=2, store_name="qdrant")
    except VectorStoreError as exc:
        assert "qdrant" in str(exc)
        assert "expected 3" in str(exc)
        assert "got 2" in str(exc)
    else:
        raise AssertionError("Expected VectorStoreError")


def test_ensure_vector_dimensions_accepts_match() -> None:
    ensure_vector_dimensions(expected=3, actual=3, store_name="qdrant")
