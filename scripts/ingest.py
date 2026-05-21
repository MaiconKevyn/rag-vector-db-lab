from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from rag_lab.pipeline import ingest_documents

app = typer.Typer(no_args_is_help=True)
console = Console()
DEFAULT_DOCS_PATH = Path("data/sample_docs")


@app.command()
def main(
    store: Annotated[str, typer.Option("--store")] = "qdrant",
    docs: Annotated[Path, typer.Option("--docs")] = DEFAULT_DOCS_PATH,
) -> None:
    count = ingest_documents(store_name=store, docs_path=docs)
    console.print(f"Indexed {count} chunks into {store}")


if __name__ == "__main__":
    app()
