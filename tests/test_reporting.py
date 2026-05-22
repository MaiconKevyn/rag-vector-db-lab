from rag_lab.benchmark import BenchmarkRun, QueryResult
from rag_lab.reporting import render_markdown_report


def test_render_markdown_report_contains_summary_table() -> None:
    run = BenchmarkRun(
        store="qdrant",
        top_k=3,
        dataset_path="evaluation/datasets/rag_lab_questions.jsonl",
        item_count=1,
        mean_recall_at_k=1.0,
        mean_reciprocal_rank=1.0,
        mean_latency_ms=12.5,
        p95_latency_ms=12.5,
        results=[
            QueryResult(
                id="qdrant-local-runtime",
                question="qual vector database roda localmente?",
                expected_ids=["qdrant"],
                retrieved_ids=["qdrant"],
                recall_at_k=1.0,
                reciprocal_rank=1.0,
                latency_ms=12.5,
                difficulty="easy",
                topic="qdrant",
            )
        ],
    )

    markdown = render_markdown_report(run)

    assert "# RAG Vector DB Lab Benchmark Report" in markdown
    assert "| Store | Items | Mean recall@k | Mean MRR | Mean latency ms | P95 latency ms |" in markdown
    assert "| qdrant | 1 | 1.000 | 1.000 | 12.5 | 12.5 |" in markdown
