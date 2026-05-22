from pathlib import Path

from rag_lab.benchmark import load_eval_dataset, run_benchmark
from rag_lab.vectorstores.base import SearchResult


def test_load_eval_dataset_reads_jsonl_items(tmp_path: Path) -> None:
    dataset = tmp_path / "questions.jsonl"
    dataset.write_text(
        '{"id":"one","question":"quando usar qdrant?","expected_ids":["qdrant"],'
        '"difficulty":"easy","topic":"qdrant"}\n',
        encoding="utf-8",
    )

    items = load_eval_dataset(dataset)

    assert len(items) == 1
    assert items[0].id == "one"
    assert items[0].expected_ids == ["qdrant"]
    assert items[0].difficulty == "easy"
    assert items[0].topic == "qdrant"


def test_load_eval_dataset_rejects_missing_expected_ids(tmp_path: Path) -> None:
    dataset = tmp_path / "questions.jsonl"
    dataset.write_text(
        '{"id":"bad","question":"sem expected ids","expected_ids":[],'
        '"difficulty":"easy","topic":"qdrant"}\n',
        encoding="utf-8",
    )

    try:
        load_eval_dataset(dataset)
    except ValueError as exc:
        assert "expected_ids" in str(exc)
    else:
        raise AssertionError("Expected ValueError for empty expected_ids")


def test_run_benchmark_computes_mean_metrics(tmp_path: Path) -> None:
    dataset = tmp_path / "questions.jsonl"
    dataset.write_text(
        "\n".join(
            [
                '{"id":"one","question":"qdrant?","expected_ids":["qdrant"],'
                '"difficulty":"easy","topic":"qdrant"}',
                '{"id":"two","question":"pinecone?","expected_ids":["pinecone"],'
                '"difficulty":"easy","topic":"pinecone"}',
            ]
        ),
        encoding="utf-8",
    )

    def fake_query(store: str, question: str, top_k: int) -> list[SearchResult]:
        assert store == "in-memory"
        assert top_k == 2
        if "qdrant" in question:
            return [SearchResult(id="qdrant:0", text="", score=1.0, metadata={"document_id": "qdrant"})]
        return [SearchResult(id="wrong:0", text="", score=1.0, metadata={"document_id": "wrong"})]

    run = run_benchmark("in-memory", dataset, top_k=2, query_fn=fake_query)

    assert run.item_count == 2
    assert run.mean_recall_at_k == 0.5
    assert run.mean_reciprocal_rank == 0.5
    assert run.mean_latency_ms >= 0
