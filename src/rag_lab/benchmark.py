from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import asdict, dataclass
from pathlib import Path
from time import perf_counter

from rag_lab.evaluation import recall_at_k, reciprocal_rank
from rag_lab.vectorstores.base import SearchResult


@dataclass(frozen=True)
class EvalItem:
    id: str
    question: str
    expected_ids: list[str]
    difficulty: str
    topic: str


@dataclass(frozen=True)
class QueryResult:
    id: str
    question: str
    expected_ids: list[str]
    retrieved_ids: list[str]
    recall_at_k: float
    reciprocal_rank: float
    latency_ms: float
    difficulty: str
    topic: str


@dataclass(frozen=True)
class BenchmarkRun:
    store: str
    top_k: int
    dataset_path: str
    item_count: int
    mean_recall_at_k: float
    mean_reciprocal_rank: float
    mean_latency_ms: float
    p95_latency_ms: float
    results: list[QueryResult]


def load_eval_dataset(path: Path) -> list[EvalItem]:
    items: list[EvalItem] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        payload = json.loads(line)
        item = EvalItem(
            id=str(payload["id"]),
            question=str(payload["question"]),
            expected_ids=[str(value) for value in payload["expected_ids"]],
            difficulty=str(payload["difficulty"]),
            topic=str(payload["topic"]),
        )
        if not item.expected_ids:
            raise ValueError(f"Line {line_number}: expected_ids must not be empty")
        items.append(item)
    if not items:
        raise ValueError(f"Dataset is empty: {path}")
    return items


def percentile(values: list[float], percentile_rank: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, round((percentile_rank / 100) * (len(ordered) - 1)))
    return ordered[index]


def run_benchmark(
    store: str,
    dataset_path: Path,
    top_k: int,
    query_fn: Callable[[str, str, int], list[SearchResult]],
) -> BenchmarkRun:
    items = load_eval_dataset(dataset_path)
    query_results: list[QueryResult] = []
    for item in items:
        started = perf_counter()
        results = query_fn(store, item.question, top_k)
        latency_ms = (perf_counter() - started) * 1000
        retrieved_ids = [
            result.metadata.get("document_id", result.id).split(":")[0] for result in results
        ]
        query_results.append(
            QueryResult(
                id=item.id,
                question=item.question,
                expected_ids=item.expected_ids,
                retrieved_ids=retrieved_ids,
                recall_at_k=recall_at_k(item.expected_ids, retrieved_ids, top_k),
                reciprocal_rank=reciprocal_rank(item.expected_ids, retrieved_ids),
                latency_ms=latency_ms,
                difficulty=item.difficulty,
                topic=item.topic,
            )
        )

    recalls = [result.recall_at_k for result in query_results]
    reciprocal_ranks = [result.reciprocal_rank for result in query_results]
    latencies = [result.latency_ms for result in query_results]
    return BenchmarkRun(
        store=store,
        top_k=top_k,
        dataset_path=str(dataset_path),
        item_count=len(query_results),
        mean_recall_at_k=sum(recalls) / len(recalls),
        mean_reciprocal_rank=sum(reciprocal_ranks) / len(reciprocal_ranks),
        mean_latency_ms=sum(latencies) / len(latencies),
        p95_latency_ms=percentile(latencies, 95),
        results=query_results,
    )


def write_benchmark_json(run: BenchmarkRun, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asdict(run), indent=2), encoding="utf-8")
