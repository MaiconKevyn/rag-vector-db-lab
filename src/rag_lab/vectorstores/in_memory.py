from math import sqrt

from rag_lab.vectorstores.base import SearchResult, VectorRecord


def cosine_similarity(left: list[float], right: list[float]) -> float:
    dot = sum(a * b for a, b in zip(left, right, strict=True))
    left_norm = sqrt(sum(a * a for a in left))
    right_norm = sqrt(sum(b * b for b in right))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return dot / (left_norm * right_norm)


class InMemoryVectorStore:
    def __init__(self) -> None:
        self.records: list[VectorRecord] = []

    def upsert(self, records: list[VectorRecord]) -> None:
        incoming_ids = {record.id for record in records}
        self.records = [record for record in self.records if record.id not in incoming_ids]
        self.records.extend(records)

    def search(self, vector: list[float], top_k: int = 5) -> list[SearchResult]:
        scored = [
            SearchResult(
                id=record.id,
                text=record.text,
                score=cosine_similarity(vector, record.vector),
                metadata=record.metadata,
            )
            for record in self.records
        ]
        return sorted(scored, key=lambda result: result.score, reverse=True)[:top_k]
