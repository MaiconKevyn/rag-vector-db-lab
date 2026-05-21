from rag_lab.chunking import chunk_text


def test_chunk_text_keeps_overlap() -> None:
    chunks = chunk_text("alpha beta gamma delta epsilon", chunk_size=3, overlap=1)

    assert chunks == ["alpha beta gamma", "gamma delta epsilon"]
