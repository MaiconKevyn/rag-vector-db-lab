from pathlib import Path

from rag_lab.documents import load_markdown_documents


def test_load_markdown_documents_reads_files(tmp_path: Path) -> None:
    doc = tmp_path / "qdrant.md"
    doc.write_text("# Qdrant\n\nVector database local.", encoding="utf-8")

    documents = load_markdown_documents(tmp_path)

    assert len(documents) == 1
    assert documents[0].id == "qdrant"
    assert documents[0].metadata["source"] == "qdrant.md"
    assert "Vector database local" in documents[0].text
