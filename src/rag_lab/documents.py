from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Document:
    id: str
    text: str
    metadata: dict[str, str]


def load_markdown_documents(path: Path) -> list[Document]:
    files = sorted(path.glob("*.md"))
    return [
        Document(
            id=file.stem,
            text=file.read_text(encoding="utf-8"),
            metadata={"source": file.name},
        )
        for file in files
    ]
