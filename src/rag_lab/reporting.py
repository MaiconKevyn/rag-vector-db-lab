from pathlib import Path

from rag_lab.benchmark import BenchmarkRun


def render_markdown_report(run: BenchmarkRun) -> str:
    lines = [
        "# RAG Vector DB Lab Benchmark Report",
        "",
        (
            "This report is generated from a reproducible benchmark run using the same "
            "corpus, chunking strategy, embedding model, and retrieval metrics."
        ),
        "",
        "## Summary",
        "",
        "| Store | Items | Mean recall@k | Mean MRR | Mean latency ms | P95 latency ms |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
        (
            f"| {run.store} | {run.item_count} | {run.mean_recall_at_k:.3f} | "
            f"{run.mean_reciprocal_rank:.3f} | {run.mean_latency_ms:.1f} | "
            f"{run.p95_latency_ms:.1f} |"
        ),
        "",
        "## Per-question Results",
        "",
        "| ID | Difficulty | Topic | Recall@k | MRR | Latency ms | Retrieved ids |",
        "| --- | --- | --- | ---: | ---: | ---: | --- |",
    ]
    for result in run.results:
        lines.append(
            f"| {result.id} | {result.difficulty} | {result.topic} | "
            f"{result.recall_at_k:.3f} | {result.reciprocal_rank:.3f} | "
            f"{result.latency_ms:.1f} | {', '.join(result.retrieved_ids)} |"
        )
    lines.append("")
    return "\n".join(lines)


def write_markdown_report(run: BenchmarkRun, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown_report(run), encoding="utf-8")
