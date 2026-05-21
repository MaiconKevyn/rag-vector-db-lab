import typer
from rich.console import Console
from rich.table import Table

from rag_lab.evaluation import recall_at_k, reciprocal_rank
from rag_lab.pipeline import query_documents

app = typer.Typer(no_args_is_help=True)
console = Console()

EVAL_SET = [
    {"question": "qual vector database roda localmente?", "expected_ids": ["qdrant"]},
    {"question": "qual vector database e cloud gerenciado?", "expected_ids": ["pinecone"]},
    {"question": "o que significa retrieval augmented generation?", "expected_ids": ["rag-basics"]},
]


@app.command()
def main(
    store: str = typer.Option("qdrant", "--store"),
    top_k: int = typer.Option(3, "--top-k"),
) -> None:
    table = Table(title=f"Evaluation for {store}")
    table.add_column("question")
    table.add_column("recall@k")
    table.add_column("mrr")
    recalls: list[float] = []
    reciprocal_ranks: list[float] = []
    for item in EVAL_SET:
        results = query_documents(store_name=store, question=item["question"], top_k=top_k)
        retrieved_ids = [result.metadata.get("document_id", result.id) for result in results]
        recall = recall_at_k(item["expected_ids"], retrieved_ids, k=top_k)
        rank = reciprocal_rank(item["expected_ids"], retrieved_ids)
        recalls.append(recall)
        reciprocal_ranks.append(rank)
        table.add_row(item["question"], f"{recall:.2f}", f"{rank:.2f}")
    table.add_row(
        "mean",
        f"{sum(recalls) / len(recalls):.2f}",
        f"{sum(reciprocal_ranks) / len(reciprocal_ranks):.2f}",
    )
    console.print(table)


if __name__ == "__main__":
    app()
