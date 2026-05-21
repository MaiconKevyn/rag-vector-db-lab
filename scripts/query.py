import typer
from rich.console import Console
from rich.table import Table

from rag_lab.pipeline import query_documents

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command()
def main(
    question: str,
    store: str = typer.Option("qdrant", "--store"),
    top_k: int = typer.Option(5, "--top-k"),
) -> None:
    results = query_documents(store_name=store, question=question, top_k=top_k)
    table = Table(title=f"Results from {store}")
    table.add_column("score")
    table.add_column("source")
    table.add_column("text")
    for result in results:
        table.add_row(f"{result.score:.4f}", result.metadata.get("source", ""), result.text[:160])
    console.print(table)


if __name__ == "__main__":
    app()
