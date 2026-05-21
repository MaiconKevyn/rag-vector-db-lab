from pathlib import Path

import typer
from rich.console import Console

from rag_lab.pipeline import ingest_documents

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command()
def main(
    store: str = typer.Option("qdrant", "--store"),
    docs: Path = typer.Option(Path("data/sample_docs"), "--docs"),
) -> None:
    count = ingest_documents(store_name=store, docs_path=docs)
    console.print(f"Indexed {count} chunks into {store}")


if __name__ == "__main__":
    app()
