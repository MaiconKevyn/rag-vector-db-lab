from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from rag_lab.benchmark import run_benchmark, write_benchmark_json
from rag_lab.pipeline import query_documents
from rag_lab.reporting import write_markdown_report

app = typer.Typer(no_args_is_help=True)
console = Console()
DEFAULT_DATASET = Path("evaluation/datasets/rag_lab_questions.jsonl")
DEFAULT_OUTPUT = Path("experiments/results/latest.json")
DEFAULT_REPORT = Path("experiments/reports/latest.md")


@app.command()
def main(
    store: Annotated[str, typer.Option("--store")] = "qdrant",
    dataset: Annotated[Path, typer.Option("--dataset")] = DEFAULT_DATASET,
    output: Annotated[Path, typer.Option("--output")] = DEFAULT_OUTPUT,
    report: Annotated[Path, typer.Option("--report")] = DEFAULT_REPORT,
    top_k: Annotated[int, typer.Option("--top-k")] = 3,
) -> None:
    run = run_benchmark(store=store, dataset_path=dataset, top_k=top_k, query_fn=query_documents)
    write_benchmark_json(run, output)
    write_markdown_report(run, report)

    table = Table(title=f"Benchmark: {store}")
    table.add_column("items")
    table.add_column("mean recall@k")
    table.add_column("mean mrr")
    table.add_column("mean latency ms")
    table.add_column("p95 latency ms")
    table.add_row(
        str(run.item_count),
        f"{run.mean_recall_at_k:.3f}",
        f"{run.mean_reciprocal_rank:.3f}",
        f"{run.mean_latency_ms:.1f}",
        f"{run.p95_latency_ms:.1f}",
    )
    console.print(table)
    console.print(f"Wrote {output}")
    console.print(f"Wrote {report}")


if __name__ == "__main__":
    app()
