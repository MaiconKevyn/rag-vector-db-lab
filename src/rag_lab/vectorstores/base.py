from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class VectorRecord:
    id: str
    text: str
    vector: list[float]
    metadata: dict[str, str]


@dataclass(frozen=True)
class SearchResult:
    id: str
    text: str
    score: float
    metadata: dict[str, str]


class VectorStore(Protocol):
    def upsert(self, records: list[VectorRecord]) -> None:
        raise NotImplementedError

    def search(self, vector: list[float], top_k: int = 5) -> list[SearchResult]:
        raise NotImplementedError


class VectorStoreError(RuntimeError):
    pass


def ensure_vector_dimensions(expected: int, actual: int, store_name: str) -> None:
    if expected != actual:
        raise VectorStoreError(
            f"{store_name} vector dimension mismatch: expected {expected}, got {actual}"
        )
