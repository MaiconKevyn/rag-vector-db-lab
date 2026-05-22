# RAG Vector DB Lab LinkedIn Readiness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Evolve `rag-vector-db-lab` from a clean educational demo into a reproducible, evidence-backed RAG/vector-database benchmark project suitable for a strong LinkedIn technical showcase.

**Architecture:** Keep the current local-first package structure and add a thin evaluation layer around it. The core RAG pipeline remains in `src/rag_lab/`; benchmark datasets, runs, and reports live under `evaluation/` and `experiments/`; CI gains a real Qdrant integration smoke test while Pinecone remains supported through explicit environment variables.

**Tech Stack:** Python 3.11+, `pytest`, `ruff`, `typer`, `rich`, `pydantic-settings`, `fastembed`, `qdrant-client`, `pinecone`, Docker Compose, GitHub Actions, MkDocs Material.

---

## Current State Summary

The repository already has:

- `src/rag_lab/`: document loading, chunking, embeddings, pipeline orchestration, evaluation metrics, and vector store adapters.
- `scripts/ingest.py`, `scripts/query.py`, `scripts/evaluate.py`: runnable CLI entrypoints.
- `docker-compose.yml`: local Qdrant runtime.
- `docs/assets/rag-pipeline-overview.svg`: scientific-style pipeline overview image.
- `.github/workflows/ci.yml`: lint, unit tests, and MkDocs strict build.
- `README.md`: quickstart and project overview.

The main gap is evidence. The project has a good architecture for a lab, but it does not yet persist benchmark results, measure latency, run a real Qdrant smoke test in CI, or present a public results snapshot.

## Target File Structure Additions

```text
rag-vector-db-lab/
├── evaluation/
│   └── datasets/
│       └── rag_lab_questions.jsonl
├── experiments/
│   ├── reports/
│   │   └── latest.md
│   └── results/
│       └── latest.json
├── scripts/
│   └── benchmark.py
├── src/
│   └── rag_lab/
│       ├── benchmark.py
│       └── reporting.py
└── tests/
    ├── test_benchmark.py
    ├── test_cli_smoke.py
    ├── test_reporting.py
    └── test_vectorstores_hardening.py
```

## Task 1: Create A Real Evaluation Dataset

**Files:**
- Create: `evaluation/datasets/rag_lab_questions.jsonl`
- Create: `tests/test_benchmark.py`

- [ ] **Step 1: Create dataset directory**

```bash
mkdir -p evaluation/datasets
```

- [ ] **Step 2: Add a 20-question JSONL dataset**

Create `evaluation/datasets/rag_lab_questions.jsonl` with one JSON object per line:

```jsonl
{"id":"qdrant-local-runtime","question":"qual vector database roda localmente com docker compose?","expected_ids":["qdrant"],"difficulty":"easy","topic":"qdrant"}
{"id":"qdrant-collections","question":"onde o qdrant organiza vetores e metadados?","expected_ids":["qdrant"],"difficulty":"easy","topic":"qdrant"}
{"id":"qdrant-hnsw","question":"qual tecnologia de indexacao o qdrant usa para busca vetorial aproximada?","expected_ids":["qdrant"],"difficulty":"medium","topic":"qdrant"}
{"id":"qdrant-payload-filter","question":"qual recurso do qdrant permite filtrar por source ou document_id?","expected_ids":["qdrant"],"difficulty":"medium","topic":"qdrant"}
{"id":"qdrant-best-fit","question":"quando qdrant e uma boa escolha para um time de rag?","expected_ids":["qdrant"],"difficulty":"medium","topic":"qdrant"}
{"id":"pinecone-managed","question":"qual vector database cloud gerenciado aparece no laboratorio?","expected_ids":["pinecone"],"difficulty":"easy","topic":"pinecone"}
{"id":"pinecone-serverless","question":"qual recurso do pinecone evita gerenciar servidores de busca vetorial?","expected_ids":["pinecone"],"difficulty":"medium","topic":"pinecone"}
{"id":"pinecone-namespaces","question":"qual conceito do pinecone separa conjuntos de vetores dentro do mesmo index?","expected_ids":["pinecone"],"difficulty":"medium","topic":"pinecone"}
{"id":"pinecone-api-key","question":"qual configuracao e obrigatoria para usar pinecone no laboratorio?","expected_ids":["pinecone"],"difficulty":"easy","topic":"pinecone"}
{"id":"pinecone-best-fit","question":"quando pinecone e uma boa escolha para prototipos cloud?","expected_ids":["pinecone"],"difficulty":"medium","topic":"pinecone"}
{"id":"rag-definition","question":"o que significa retrieval augmented generation?","expected_ids":["rag-basics"],"difficulty":"easy","topic":"rag"}
{"id":"rag-retriever","question":"qual parte do rag encontra chunks relevantes antes da geracao?","expected_ids":["rag-basics"],"difficulty":"easy","topic":"rag"}
{"id":"rag-failure-modes","question":"quais falhas podem acontecer em um pipeline rag?","expected_ids":["rag-basics"],"difficulty":"medium","topic":"rag"}
{"id":"rag-grounding","question":"como o rag ajuda a fundamentar respostas em contexto recuperado?","expected_ids":["rag-basics"],"difficulty":"medium","topic":"rag"}
{"id":"bedrock-role","question":"qual papel o aws bedrock pode cumprir em um sistema rag?","expected_ids":["aws-bedrock"],"difficulty":"easy","topic":"bedrock"}
{"id":"bedrock-not-vector-db","question":"por que bedrock nao substitui qdrant ou pinecone como vector database?","expected_ids":["aws-bedrock"],"difficulty":"medium","topic":"bedrock"}
{"id":"compare-local-cloud","question":"compare qdrant local com pinecone cloud para operacao de rag","expected_ids":["qdrant","pinecone"],"difficulty":"hard","topic":"comparison"}
{"id":"compare-metadata-filter","question":"quais stores no laboratorio suportam filtros por metadados?","expected_ids":["qdrant","pinecone"],"difficulty":"hard","topic":"comparison"}
{"id":"compare-operational-risk","question":"qual e o risco operacional principal de qdrant self-hosted versus pinecone?","expected_ids":["qdrant","pinecone"],"difficulty":"hard","topic":"comparison"}
{"id":"compare-provider-dependency","question":"qual opcao aumenta dependencia de provedor cloud gerenciado?","expected_ids":["pinecone"],"difficulty":"hard","topic":"comparison"}
```

- [ ] **Step 3: Write failing dataset loader tests**

Create `tests/test_benchmark.py`:

```python
from pathlib import Path

from rag_lab.benchmark import load_eval_dataset


def test_load_eval_dataset_reads_jsonl_items(tmp_path: Path) -> None:
    dataset = tmp_path / "questions.jsonl"
    dataset.write_text(
        '{"id":"one","question":"quando usar qdrant?","expected_ids":["qdrant"],'
        '"difficulty":"easy","topic":"qdrant"}\n',
        encoding="utf-8",
    )

    items = load_eval_dataset(dataset)

    assert len(items) == 1
    assert items[0].id == "one"
    assert items[0].expected_ids == ["qdrant"]
    assert items[0].difficulty == "easy"
    assert items[0].topic == "qdrant"


def test_load_eval_dataset_rejects_missing_expected_ids(tmp_path: Path) -> None:
    dataset = tmp_path / "questions.jsonl"
    dataset.write_text(
        '{"id":"bad","question":"sem expected ids","expected_ids":[],'
        '"difficulty":"easy","topic":"qdrant"}\n',
        encoding="utf-8",
    )

    try:
        load_eval_dataset(dataset)
    except ValueError as exc:
        assert "expected_ids" in str(exc)
    else:
        raise AssertionError("Expected ValueError for empty expected_ids")
```

- [ ] **Step 4: Run tests and confirm failure**

```bash
pytest tests/test_benchmark.py -q
```

Expected: fails with `ModuleNotFoundError: No module named 'rag_lab.benchmark'`.

- [ ] **Step 5: Commit dataset and failing tests only after red is observed**

Do not commit red tests by themselves. Proceed directly to Task 2 implementation before committing.

## Task 2: Add Benchmark Data Models And Metrics Aggregation

**Files:**
- Create: `src/rag_lab/benchmark.py`
- Modify: `tests/test_benchmark.py`

- [ ] **Step 1: Implement dataset and result models**

Create `src/rag_lab/benchmark.py`:

```python
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from time import perf_counter
from typing import Callable

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
        retrieved_ids = [result.metadata.get("document_id", result.id).split(":")[0] for result in results]
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
```

- [ ] **Step 2: Extend tests for benchmark aggregation**

Append to `tests/test_benchmark.py`:

```python
from rag_lab.benchmark import run_benchmark
from rag_lab.vectorstores.base import SearchResult


def test_run_benchmark_computes_mean_metrics(tmp_path: Path) -> None:
    dataset = tmp_path / "questions.jsonl"
    dataset.write_text(
        "\n".join(
            [
                '{"id":"one","question":"qdrant?","expected_ids":["qdrant"],'
                '"difficulty":"easy","topic":"qdrant"}',
                '{"id":"two","question":"pinecone?","expected_ids":["pinecone"],'
                '"difficulty":"easy","topic":"pinecone"}',
            ]
        ),
        encoding="utf-8",
    )

    def fake_query(store: str, question: str, top_k: int) -> list[SearchResult]:
        assert store == "in-memory"
        assert top_k == 2
        if "qdrant" in question:
            return [SearchResult(id="qdrant:0", text="", score=1.0, metadata={"document_id": "qdrant"})]
        return [SearchResult(id="wrong:0", text="", score=1.0, metadata={"document_id": "wrong"})]

    run = run_benchmark("in-memory", dataset, top_k=2, query_fn=fake_query)

    assert run.item_count == 2
    assert run.mean_recall_at_k == 0.5
    assert run.mean_reciprocal_rank == 0.5
    assert run.mean_latency_ms >= 0
```

- [ ] **Step 3: Run tests**

```bash
pytest tests/test_benchmark.py -q
```

Expected: all benchmark tests pass.

- [ ] **Step 4: Run full test suite**

```bash
pytest -q
```

Expected: all tests pass.

- [ ] **Step 5: Commit**

```bash
git add evaluation/datasets/rag_lab_questions.jsonl src/rag_lab/benchmark.py tests/test_benchmark.py
git commit -m "feat: add benchmark dataset and metrics"
```

## Task 3: Add A Reproducible Benchmark CLI

**Files:**
- Create: `scripts/benchmark.py`
- Create: `tests/test_cli_smoke.py`
- Modify: `README.md`

- [ ] **Step 1: Write CLI smoke test**

Create `tests/test_cli_smoke.py`:

```python
from pathlib import Path


def test_benchmark_script_exists() -> None:
    script = Path("scripts/benchmark.py")

    assert script.exists()
    assert "run_benchmark" in script.read_text(encoding="utf-8")
```

- [ ] **Step 2: Run test and confirm failure**

```bash
pytest tests/test_cli_smoke.py -q
```

Expected: fails because `scripts/benchmark.py` does not exist.

- [ ] **Step 3: Create benchmark CLI**

Create `scripts/benchmark.py`:

```python
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from rag_lab.benchmark import run_benchmark, write_benchmark_json
from rag_lab.pipeline import query_documents

app = typer.Typer(no_args_is_help=True)
console = Console()
DEFAULT_DATASET = Path("evaluation/datasets/rag_lab_questions.jsonl")
DEFAULT_OUTPUT = Path("experiments/results/latest.json")


@app.command()
def main(
    store: Annotated[str, typer.Option("--store")] = "qdrant",
    dataset: Annotated[Path, typer.Option("--dataset")] = DEFAULT_DATASET,
    output: Annotated[Path, typer.Option("--output")] = DEFAULT_OUTPUT,
    top_k: Annotated[int, typer.Option("--top-k")] = 3,
) -> None:
    run = run_benchmark(store=store, dataset_path=dataset, top_k=top_k, query_fn=query_documents)
    write_benchmark_json(run, output)

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


if __name__ == "__main__":
    app()
```

- [ ] **Step 4: Add README command**

In `README.md`, add this under `## Validacao`:

```markdown
## Benchmark reproduzivel

```bash
docker compose up -d qdrant
python scripts/ingest.py --store qdrant --docs data/sample_docs
python scripts/benchmark.py --store qdrant --dataset evaluation/datasets/rag_lab_questions.jsonl
```
```

- [ ] **Step 5: Run CLI smoke test**

```bash
pytest tests/test_cli_smoke.py -q
```

Expected: pass.

- [ ] **Step 6: Run local benchmark manually**

```bash
docker compose up -d qdrant
python scripts/ingest.py --store qdrant --docs data/sample_docs
python scripts/benchmark.py --store qdrant --dataset evaluation/datasets/rag_lab_questions.jsonl --output experiments/results/latest.json
docker compose down
```

Expected: command prints a benchmark table and writes `experiments/results/latest.json`.

- [ ] **Step 7: Commit**

```bash
git add README.md scripts/benchmark.py tests/test_cli_smoke.py experiments/results/latest.json
git commit -m "feat: add reproducible benchmark cli"
```

## Task 4: Generate A Markdown Benchmark Report

**Files:**
- Create: `src/rag_lab/reporting.py`
- Create: `tests/test_reporting.py`
- Create: `experiments/reports/latest.md`
- Modify: `scripts/benchmark.py`
- Modify: `README.md`

- [ ] **Step 1: Write failing report test**

Create `tests/test_reporting.py`:

```python
from rag_lab.benchmark import BenchmarkRun, QueryResult
from rag_lab.reporting import render_markdown_report


def test_render_markdown_report_contains_summary_table() -> None:
    run = BenchmarkRun(
        store="qdrant",
        top_k=3,
        dataset_path="evaluation/datasets/rag_lab_questions.jsonl",
        item_count=1,
        mean_recall_at_k=1.0,
        mean_reciprocal_rank=1.0,
        mean_latency_ms=12.5,
        p95_latency_ms=12.5,
        results=[
            QueryResult(
                id="qdrant-local-runtime",
                question="qual vector database roda localmente?",
                expected_ids=["qdrant"],
                retrieved_ids=["qdrant"],
                recall_at_k=1.0,
                reciprocal_rank=1.0,
                latency_ms=12.5,
                difficulty="easy",
                topic="qdrant",
            )
        ],
    )

    markdown = render_markdown_report(run)

    assert "# RAG Vector DB Lab Benchmark Report" in markdown
    assert "| Store | Items | Mean recall@k | Mean MRR | Mean latency ms | P95 latency ms |" in markdown
    assert "| qdrant | 1 | 1.000 | 1.000 | 12.5 | 12.5 |" in markdown
```

- [ ] **Step 2: Run test and confirm failure**

```bash
pytest tests/test_reporting.py -q
```

Expected: fails because `rag_lab.reporting` does not exist.

- [ ] **Step 3: Implement report rendering**

Create `src/rag_lab/reporting.py`:

```python
from pathlib import Path

from rag_lab.benchmark import BenchmarkRun


def render_markdown_report(run: BenchmarkRun) -> str:
    lines = [
        "# RAG Vector DB Lab Benchmark Report",
        "",
        "This report is generated from a reproducible benchmark run using the same corpus, chunking strategy, embedding model, and retrieval metrics.",
        "",
        "## Summary",
        "",
        "| Store | Items | Mean recall@k | Mean MRR | Mean latency ms | P95 latency ms |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
        (
            f"| {run.store} | {run.item_count} | {run.mean_recall_at_k:.3f} | "
            f"{run.mean_reciprocal_rank:.3f} | {run.mean_latency_ms:.1f} | {run.p95_latency_ms:.1f} |"
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
```

- [ ] **Step 4: Update benchmark CLI to write report**

Modify `scripts/benchmark.py`:

```python
from rag_lab.reporting import write_markdown_report

DEFAULT_REPORT = Path("experiments/reports/latest.md")
```

Add a `report` option:

```python
report: Annotated[Path, typer.Option("--report")] = DEFAULT_REPORT,
```

After `write_benchmark_json(run, output)`, add:

```python
write_markdown_report(run, report)
```

After printing the JSON output, add:

```python
console.print(f"Wrote {report}")
```

- [ ] **Step 5: Add README report link**

Add to `README.md`:

```markdown
## Resultados

- Relatorio mais recente: `experiments/reports/latest.md`
- Resultado bruto: `experiments/results/latest.json`
```

- [ ] **Step 6: Run tests**

```bash
pytest tests/test_reporting.py tests/test_benchmark.py -q
```

Expected: pass.

- [ ] **Step 7: Regenerate benchmark artifacts**

```bash
docker compose up -d qdrant
python scripts/ingest.py --store qdrant --docs data/sample_docs
python scripts/benchmark.py --store qdrant --dataset evaluation/datasets/rag_lab_questions.jsonl --output experiments/results/latest.json --report experiments/reports/latest.md
docker compose down
```

Expected:
- `experiments/results/latest.json` exists.
- `experiments/reports/latest.md` exists.
- report contains summary and per-question result tables.

- [ ] **Step 8: Commit**

```bash
git add README.md scripts/benchmark.py src/rag_lab/reporting.py tests/test_reporting.py experiments/results/latest.json experiments/reports/latest.md
git commit -m "feat: generate benchmark reports"
```

## Task 5: Add Qdrant Integration Tests And CI Service

**Files:**
- Create: `tests/test_qdrant_integration.py`
- Modify: `.github/workflows/ci.yml`

- [ ] **Step 1: Write Qdrant integration test**

Create `tests/test_qdrant_integration.py`:

```python
import os
from pathlib import Path

import pytest

from rag_lab.pipeline import ingest_documents, query_documents


@pytest.mark.integration
def test_qdrant_ingest_and_query_returns_expected_source() -> None:
    if os.getenv("RAG_LAB_RUN_QDRANT_INTEGRATION") != "1":
        pytest.skip("set RAG_LAB_RUN_QDRANT_INTEGRATION=1 to run Qdrant integration test")

    count = ingest_documents(store_name="qdrant", docs_path=Path("data/sample_docs"))

    assert count > 0
    results = query_documents("qdrant", "qual vector database roda localmente?", top_k=1)
    assert results
    assert results[0].metadata["source"] == "qdrant.md"
```

- [ ] **Step 2: Run test without env and verify skip**

```bash
pytest tests/test_qdrant_integration.py -q
```

Expected: skipped.

- [ ] **Step 3: Run test with local Qdrant**

```bash
docker compose up -d qdrant
RAG_LAB_RUN_QDRANT_INTEGRATION=1 pytest tests/test_qdrant_integration.py -q
docker compose down
```

Expected: pass.

- [ ] **Step 4: Add Qdrant service to CI**

Modify `.github/workflows/ci.yml` job:

```yaml
    services:
      qdrant:
        image: qdrant/qdrant:v1.12.4
        ports:
          - 6333:6333
```

Add after `Tests`:

```yaml
      - name: Qdrant integration
        env:
          RAG_LAB_RUN_QDRANT_INTEGRATION: "1"
          RAG_LAB_QDRANT_URL: http://localhost:6333
        run: pytest tests/test_qdrant_integration.py -q
```

- [ ] **Step 5: Commit**

```bash
git add .github/workflows/ci.yml tests/test_qdrant_integration.py
git commit -m "ci: add qdrant integration test"
```

## Task 6: Harden Vector Store Adapters

**Files:**
- Modify: `src/rag_lab/vectorstores/base.py`
- Modify: `src/rag_lab/vectorstores/qdrant_store.py`
- Modify: `src/rag_lab/vectorstores/pinecone_store.py`
- Create: `tests/test_vectorstores_hardening.py`

- [ ] **Step 1: Write tests for dimension mismatch and Pinecone timeout**

Create `tests/test_vectorstores_hardening.py`:

```python
from rag_lab.vectorstores.base import VectorStoreError, ensure_vector_dimensions


def test_ensure_vector_dimensions_rejects_mismatch() -> None:
    try:
        ensure_vector_dimensions(expected=3, actual=2, store_name="qdrant")
    except VectorStoreError as exc:
        assert "qdrant" in str(exc)
        assert "expected 3" in str(exc)
        assert "got 2" in str(exc)
    else:
        raise AssertionError("Expected VectorStoreError")


def test_ensure_vector_dimensions_accepts_match() -> None:
    ensure_vector_dimensions(expected=3, actual=3, store_name="qdrant")
```

- [ ] **Step 2: Run test and confirm failure**

```bash
pytest tests/test_vectorstores_hardening.py -q
```

Expected: fails because `VectorStoreError` and `ensure_vector_dimensions` do not exist.

- [ ] **Step 3: Add shared vector store error helpers**

Append to `src/rag_lab/vectorstores/base.py`:

```python
class VectorStoreError(RuntimeError):
    pass


def ensure_vector_dimensions(expected: int, actual: int, store_name: str) -> None:
    if expected != actual:
        raise VectorStoreError(
            f"{store_name} vector dimension mismatch: expected {expected}, got {actual}"
        )
```

- [ ] **Step 4: Harden Qdrant collection dimension checks**

Modify `src/rag_lab/vectorstores/qdrant_store.py`:

```python
from rag_lab.vectorstores.base import SearchResult, VectorRecord, ensure_vector_dimensions
```

In `__init__`, after confirming the collection exists, retrieve config and validate dimension:

```python
        else:
            collection_info = self.client.get_collection(collection_name=collection)
            vector_config = collection_info.config.params.vectors
            ensure_vector_dimensions(
                expected=dimensions,
                actual=vector_config.size,
                store_name="qdrant",
            )
```

- [ ] **Step 5: Harden Pinecone readiness loop**

Modify `src/rag_lab/vectorstores/pinecone_store.py`:

```python
from rag_lab.vectorstores.base import SearchResult, VectorRecord, VectorStoreError
```

Replace the unbounded readiness loop:

```python
            attempts = 0
            while not self.pc.describe_index(index_name).status["ready"]:
                attempts += 1
                if attempts > 60:
                    raise VectorStoreError(f"Pinecone index did not become ready: {index_name}")
                sleep(1)
```

- [ ] **Step 6: Run tests**

```bash
pytest tests/test_vectorstores_hardening.py -q
pytest -q
```

Expected: all tests pass.

- [ ] **Step 7: Commit**

```bash
git add src/rag_lab/vectorstores/base.py src/rag_lab/vectorstores/qdrant_store.py src/rag_lab/vectorstores/pinecone_store.py tests/test_vectorstores_hardening.py
git commit -m "fix: harden vector store adapters"
```

## Task 7: Expand The Public Comparison Story

**Files:**
- Modify: `docs/vector-databases/comparison.md`
- Modify: `README.md`

- [ ] **Step 1: Expand comparison table**

In `docs/vector-databases/comparison.md`, replace the current table with:

```markdown
| Criterio | Qdrant | Pinecone |
| --- | --- | --- |
| Modelo de deploy | Local, self-hosted ou cloud | Cloud gerenciado |
| Open source | Sim, core OSS | Nao, plataforma proprietaria |
| Primeiro uso ideal | Desenvolvimento local e controle fino | Prototipos cloud e operacao gerenciada |
| Setup local | Docker Compose | Nao aplicavel |
| Filtros por metadados | Sim, payload filters | Sim, metadata filters |
| Hybrid search | Suportado por recursos de sparse/dense vectors | Suportado por recursos gerenciados da plataforma |
| Escala operacional | Depende da operacao do cluster | Gerenciada pelo provedor |
| SQL e joins | Nao e banco relacional | Nao e banco relacional |
| Esforco operacional | Medio em self-hosted, baixo em cloud | Baixo para o usuario da plataforma |
| Custo inicial | Zero localmente | Depende do plano cloud |
| Melhor fit | Times que querem controle, local-first e portabilidade | Times que querem gerenciado, velocidade cloud e menos operacao |
| Risco principal | Operar infraestrutura propria em producao | Dependencia do provedor |
```

- [ ] **Step 2: Add “What this proves” section to README**

Add after the pipeline image:

```markdown
## O que este lab prova

- Comparacao justa exige manter corpus, chunking, embeddings e metricas constantes.
- Qdrant permite validar o pipeline inteiro localmente antes de envolver cloud.
- Pinecone permite comparar a mesma interface contra uma opcao gerenciada.
- O valor do projeto esta no controle experimental: trocar o vector store sem trocar o pipeline.
```

- [ ] **Step 3: Add CI and benchmark badges**

Add below the title in `README.md`:

```markdown
[![CI](https://github.com/MaiconKevyn/rag-vector-db-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/MaiconKevyn/rag-vector-db-lab/actions/workflows/ci.yml)
```

- [ ] **Step 4: Run docs build**

```bash
mkdocs build --strict
```

Expected: build succeeds.

- [ ] **Step 5: Commit**

```bash
git add README.md docs/vector-databases/comparison.md
git commit -m "docs: strengthen vector database comparison"
```

## Task 8: Add A LinkedIn Publishing Kit

**Files:**
- Create: `docs/linkedin-post.md`
- Modify: `README.md`

- [ ] **Step 1: Create LinkedIn post draft**

Create `docs/linkedin-post.md`:

```markdown
# LinkedIn Post Draft

Construí um laboratório RAG local-first para comparar vector databases com controle experimental.

A ideia não é apenas rodar RAG. É conseguir responder perguntas como:

- O que muda quando troco Qdrant local por Pinecone cloud?
- Como mantenho corpus, chunking, embedding e métrica constantes?
- Qual é o impacto em recall@k, MRR e latência?

O projeto inclui:

- pipeline Python com document loading, chunking, embeddings e retrieval;
- interface comum `VectorStore` para Qdrant, Pinecone e in-memory;
- Qdrant local via Docker Compose;
- Pinecone via variáveis de ambiente, sem secrets hardcoded;
- benchmark reproduzível com dataset JSONL;
- relatório Markdown com recall@k, MRR e latência;
- CI com lint, testes, docs e smoke test de Qdrant;
- documentação MkDocs e SVG científico do fluxo.

Repo: https://github.com/MaiconKevyn/rag-vector-db-lab

O principal aprendizado: comparar vector databases exige controlar o experimento. Se corpus, chunking ou embedding mudam, você não está comparando o banco vetorial; está comparando pipelines diferentes.
```

- [ ] **Step 2: Link the post draft in README**

Add to `README.md`:

```markdown
## Material de divulgacao

- Draft para LinkedIn: `docs/linkedin-post.md`
```

- [ ] **Step 3: Commit**

```bash
git add README.md docs/linkedin-post.md
git commit -m "docs: add linkedin publishing kit"
```

## Task 9: Final Validation And Publish

**Files:**
- No new files required.

- [ ] **Step 1: Run local validation**

```bash
ruff check .
pytest -q
mkdocs build --strict
```

Expected:
- `ruff check .` prints `All checks passed!`
- `pytest -q` passes all tests.
- `mkdocs build --strict` exits with code 0.

- [ ] **Step 2: Run Qdrant benchmark one last time**

```bash
docker compose up -d qdrant
python scripts/ingest.py --store qdrant --docs data/sample_docs
python scripts/benchmark.py --store qdrant --dataset evaluation/datasets/rag_lab_questions.jsonl --output experiments/results/latest.json --report experiments/reports/latest.md
docker compose down
```

Expected:
- `experiments/results/latest.json` is updated.
- `experiments/reports/latest.md` is updated.
- Query count equals the dataset item count.

- [ ] **Step 3: Verify repository state**

```bash
git status --short
git log --oneline -n 8
```

Expected:
- `git status --short` is clean.
- Latest commits match Tasks 1-8.

- [ ] **Step 4: Push**

```bash
git push origin main
```

Expected: push succeeds and GitHub Actions runs on `main`.

- [ ] **Step 5: Verify GitHub Actions**

```bash
gh run list --limit 3
```

Expected: latest `CI` run completes with `success`.

## Acceptance Criteria

- `README.md` clearly explains the differentiator: controlled comparison of vector stores under the same RAG pipeline.
- `docs/assets/rag-pipeline-overview.svg` remains visible from README.
- `evaluation/datasets/rag_lab_questions.jsonl` contains at least 20 validated questions.
- `scripts/benchmark.py` runs Qdrant benchmark and writes JSON plus Markdown report.
- `experiments/results/latest.json` contains item-level and aggregate metrics.
- `experiments/reports/latest.md` contains summary and per-question benchmark tables.
- CI runs lint, unit tests, docs build, and Qdrant integration smoke test.
- Adapter hardening prevents silent dimension mismatch and unbounded Pinecone readiness waits.
- Docs include a stronger Qdrant vs Pinecone comparison table with deployment model, OSS status, hybrid search, metadata filtering, scale, SQL/joins, operational effort, and best fit.
- `docs/linkedin-post.md` provides a ready-to-edit LinkedIn post draft.
- `ruff check .`, `pytest -q`, and `mkdocs build --strict` pass locally.
- Latest GitHub Actions `CI` run succeeds after push.

