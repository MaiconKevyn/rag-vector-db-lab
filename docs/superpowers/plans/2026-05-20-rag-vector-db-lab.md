# RAG Vector DB Lab Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild this repository as a hands-on RAG laboratory that teaches, runs, and compares vector databases, starting with Qdrant and Pinecone.

**Architecture:** Replace the current AWS/serverless PDF pipeline with a local-first Python package, runnable CLI labs, and a static documentation site. The core package owns document loading, chunking, embeddings, retrieval, and evaluation; vector database integrations live behind a small adapter interface so Pinecone and Qdrant can be compared with the same corpus and queries.

**Tech Stack:** Python 3.11+, `pytest`, `ruff`, `pydantic-settings`, `typer`, `rich`, `fastembed`, `qdrant-client`, `pinecone`, Docker Compose for local Qdrant, and MkDocs Material for documentation.

---

## Target Repository Name

- Local directory: `/home/maiconkevyn/PycharmProjects/rag-vector-db-lab`
- GitHub repository: `MaiconKevyn/rag-vector-db-lab`
- Python package: `rag_lab`
- Documentation title: `RAG Vector DB Lab`

## Files To Remove

Remove the current AWS-specific implementation because it will not be reused:

- `.github/workflows/deploy.yml`
- `SETUP.md`
- `app.py`
- `configure_s3_trigger.py`
- `create_s3_folders.py`
- `setup_complete_pipeline.py`
- `template.yaml`
- `test_pipeline.py`
- `lambdas/`
- `state_machines/`
- `templates/`

Keep and rewrite:

- `.gitignore`
- `README.md`
- `.env.example`

## Target File Structure

```text
rag-vector-db-lab/
├── .env.example
├── .github/workflows/ci.yml
├── .gitignore
├── README.md
├── docker-compose.yml
├── mkdocs.yml
├── pyproject.toml
├── data/
│   └── sample_docs/
│       ├── aws-bedrock.md
│       ├── pinecone.md
│       ├── qdrant.md
│       └── rag-basics.md
├── docs/
│   ├── index.md
│   ├── concepts/
│   │   ├── chunking.md
│   │   ├── embeddings.md
│   │   └── retrieval-evaluation.md
│   ├── labs/
│   │   ├── 01-local-qdrant.md
│   │   ├── 02-pinecone-cloud.md
│   │   └── 03-compare-results.md
│   └── vector-databases/
│       ├── comparison.md
│       ├── pinecone.md
│       └── qdrant.md
├── scripts/
│   ├── evaluate.py
│   ├── ingest.py
│   └── query.py
├── src/
│   └── rag_lab/
│       ├── __init__.py
│       ├── chunking.py
│       ├── config.py
│       ├── documents.py
│       ├── embeddings.py
│       ├── evaluation.py
│       ├── pipeline.py
│       └── vectorstores/
│           ├── __init__.py
│           ├── base.py
│           ├── in_memory.py
│           ├── pinecone_store.py
│           └── qdrant_store.py
└── tests/
    ├── test_chunking.py
    ├── test_documents.py
    ├── test_evaluation.py
    └── test_in_memory_pipeline.py
```

## Task 1: Repository Reset And Metadata

**Files:**
- Delete: AWS/serverless files listed in "Files To Remove"
- Modify: `README.md`
- Modify: `.gitignore`
- Modify: `.env.example`
- Create: `pyproject.toml`
- Create: `.github/workflows/ci.yml`

- [ ] **Step 1: Remove the legacy AWS implementation**

Run:

```bash
rm -rf \
  .github/workflows/deploy.yml \
  SETUP.md \
  app.py \
  configure_s3_trigger.py \
  create_s3_folders.py \
  setup_complete_pipeline.py \
  template.yaml \
  test_pipeline.py \
  lambdas \
  state_machines \
  templates
```

Expected: `git status --short` shows the deleted legacy files.

- [ ] **Step 2: Create the project metadata**

Create `pyproject.toml`:

```toml
[project]
name = "rag-vector-db-lab"
version = "0.1.0"
description = "Hands-on RAG laboratory for comparing vector databases such as Qdrant and Pinecone."
requires-python = ">=3.11"
dependencies = [
  "fastembed>=0.4.2",
  "pinecone>=5.4.0",
  "pydantic-settings>=2.6.0",
  "qdrant-client>=1.12.0",
  "rich>=13.9.0",
  "typer>=0.12.5",
]

[project.optional-dependencies]
docs = [
  "mkdocs>=1.6.1",
  "mkdocs-material>=9.5.42",
]
dev = [
  "pytest>=8.3.3",
  "ruff>=0.7.1",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]
```

- [ ] **Step 3: Replace `.env.example`**

Create `.env.example`:

```bash
RAG_LAB_VECTOR_STORE=qdrant
RAG_LAB_COLLECTION=rag_lab_documents
RAG_LAB_EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
RAG_LAB_QDRANT_URL=http://localhost:6333
RAG_LAB_QDRANT_API_KEY=
RAG_LAB_PINECONE_API_KEY=
RAG_LAB_PINECONE_INDEX=rag-vector-db-lab
RAG_LAB_PINECONE_CLOUD=aws
RAG_LAB_PINECONE_REGION=us-east-1
```

- [ ] **Step 4: Replace `.gitignore`**

Create `.gitignore`:

```gitignore
.env
.venv/
__pycache__/
*.py[cod]
.pytest_cache/
.ruff_cache/
.coverage
htmlcov/
site/
dist/
build/
*.egg-info/
experiments/results/*.json
experiments/results/*.csv
.DS_Store
.idea/
.vscode/
```

- [ ] **Step 5: Create CI**

Create `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install
        run: |
          python -m pip install --upgrade pip
          python -m pip install -e ".[dev,docs]"
      - name: Lint
        run: ruff check .
      - name: Tests
        run: pytest -q
      - name: Docs build
        run: mkdocs build --strict
```

- [ ] **Step 6: Commit**

```bash
git add .
git commit -m "chore: reset project for rag vector db lab"
```

## Task 2: Static Documentation Site

**Files:**
- Create: `mkdocs.yml`
- Create: `docs/index.md`
- Create: `docs/vector-databases/qdrant.md`
- Create: `docs/vector-databases/pinecone.md`
- Create: `docs/vector-databases/comparison.md`
- Create: `docs/concepts/chunking.md`
- Create: `docs/concepts/embeddings.md`
- Create: `docs/concepts/retrieval-evaluation.md`
- Create: `docs/labs/01-local-qdrant.md`
- Create: `docs/labs/02-pinecone-cloud.md`
- Create: `docs/labs/03-compare-results.md`

- [ ] **Step 1: Create `mkdocs.yml`**

```yaml
site_name: RAG Vector DB Lab
site_description: Hands-on labs for learning and comparing vector databases in RAG systems.
theme:
  name: material
  language: pt-BR
  features:
    - navigation.sections
    - navigation.indexes
    - content.code.copy
markdown_extensions:
  - admonition
  - tables
  - toc:
      permalink: true
nav:
  - Inicio: index.md
  - Conceitos:
      - Chunking: concepts/chunking.md
      - Embeddings: concepts/embeddings.md
      - Avaliacao de retrieval: concepts/retrieval-evaluation.md
  - Vector Databases:
      - Comparacao: vector-databases/comparison.md
      - Qdrant: vector-databases/qdrant.md
      - Pinecone: vector-databases/pinecone.md
  - Labs:
      - Qdrant local: labs/01-local-qdrant.md
      - Pinecone cloud: labs/02-pinecone-cloud.md
      - Comparar resultados: labs/03-compare-results.md
```

- [ ] **Step 2: Create `docs/index.md`**

```markdown
# RAG Vector DB Lab

Este laboratorio mostra como construir, testar e comparar pipelines de Retrieval-Augmented Generation usando diferentes vector databases.

O fluxo base e sempre o mesmo:

1. carregar documentos pequenos de exemplo;
2. quebrar documentos em chunks;
3. gerar embeddings;
4. indexar em um vector database;
5. executar consultas;
6. medir qualidade e latencia.

Comece pelo lab de Qdrant local se quiser rodar tudo sem conta externa. Use o lab de Pinecone quando quiser comparar com uma opcao cloud gerenciada.
```

- [ ] **Step 3: Create vector database pages**

`docs/vector-databases/qdrant.md` must explain local Docker usage, collections, payload filters, HNSW indexing, and when Qdrant is a good fit.

`docs/vector-databases/pinecone.md` must explain managed indexes, serverless deployment, namespaces, metadata filters, API key setup, and when Pinecone is a good fit.

`docs/vector-databases/comparison.md` must include this table:

```markdown
| Criterio | Qdrant | Pinecone |
| --- | --- | --- |
| Modelo operacional | Local ou cloud | Cloud gerenciado |
| Melhor primeiro uso | Desenvolvimento local e controle fino | Prototipos cloud e operacao gerenciada |
| Setup local | Docker Compose | Nao aplicavel |
| Filtros por metadados | Sim | Sim |
| Custo inicial | Zero localmente | Depende do plano cloud |
| Risco principal | Operar infraestrutura propria em producao | Dependencia do provedor |
```

- [ ] **Step 4: Create lab pages with runnable commands**

Each lab page must include exact commands:

```bash
python -m pip install -e ".[dev,docs]"
docker compose up -d qdrant
python scripts/ingest.py --store qdrant --docs data/sample_docs
python scripts/query.py --store qdrant "quando usar qdrant em rag?"
python scripts/evaluate.py --store qdrant
mkdocs serve
```

For Pinecone, include:

```bash
cp .env.example .env
python scripts/ingest.py --store pinecone --docs data/sample_docs
python scripts/query.py --store pinecone "quando usar pinecone em rag?"
python scripts/evaluate.py --store pinecone
```

- [ ] **Step 5: Verify docs**

Run:

```bash
python -m pip install -e ".[docs]"
mkdocs build --strict
```

Expected: MkDocs builds `site/` without warnings or broken nav links.

- [ ] **Step 6: Commit**

```bash
git add mkdocs.yml docs
git commit -m "docs: add rag vector database guide"
```

## Task 3: Core RAG Domain Package

**Files:**
- Create: `src/rag_lab/__init__.py`
- Create: `src/rag_lab/config.py`
- Create: `src/rag_lab/documents.py`
- Create: `src/rag_lab/chunking.py`
- Create: `src/rag_lab/embeddings.py`
- Create: `tests/test_documents.py`
- Create: `tests/test_chunking.py`

- [ ] **Step 1: Write document and chunking tests**

Create `tests/test_documents.py`:

```python
from pathlib import Path

from rag_lab.documents import load_markdown_documents


def test_load_markdown_documents_reads_files(tmp_path: Path) -> None:
    doc = tmp_path / "qdrant.md"
    doc.write_text("# Qdrant\n\nVector database local.", encoding="utf-8")

    documents = load_markdown_documents(tmp_path)

    assert len(documents) == 1
    assert documents[0].id == "qdrant"
    assert documents[0].metadata["source"] == "qdrant.md"
    assert "Vector database local" in documents[0].text
```

Create `tests/test_chunking.py`:

```python
from rag_lab.chunking import chunk_text


def test_chunk_text_keeps_overlap() -> None:
    chunks = chunk_text("alpha beta gamma delta epsilon", chunk_size=3, overlap=1)

    assert chunks == ["alpha beta gamma", "gamma delta epsilon"]
```

- [ ] **Step 2: Run tests and confirm failure**

```bash
pytest tests/test_documents.py tests/test_chunking.py -q
```

Expected: import errors because `rag_lab.documents` and `rag_lab.chunking` do not exist yet.

- [ ] **Step 3: Implement documents**

Create `src/rag_lab/documents.py`:

```python
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
```

- [ ] **Step 4: Implement chunking**

Create `src/rag_lab/chunking.py`:

```python
def chunk_text(text: str, chunk_size: int = 180, overlap: int = 30) -> list[str]:
    words = text.split()
    if not words:
        return []
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks: list[str] = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunks.append(" ".join(words[start:end]))
        if end >= len(words):
            break
        start = end - overlap
    return chunks
```

- [ ] **Step 5: Implement settings and embeddings**

Create `src/rag_lab/config.py`:

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    vector_store: str = "qdrant"
    collection: str = "rag_lab_documents"
    embedding_model: str = "BAAI/bge-small-en-v1.5"
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str | None = None
    pinecone_api_key: str | None = None
    pinecone_index: str = "rag-vector-db-lab"
    pinecone_cloud: str = "aws"
    pinecone_region: str = "us-east-1"

    model_config = SettingsConfigDict(env_prefix="RAG_LAB_", env_file=".env", extra="ignore")
```

Create `src/rag_lab/embeddings.py`:

```python
from collections.abc import Iterable
from hashlib import sha256
from random import Random

from fastembed import TextEmbedding


class FastEmbedder:
    def __init__(self, model_name: str) -> None:
        self.model = TextEmbedding(model_name=model_name)

    def embed(self, texts: Iterable[str]) -> list[list[float]]:
        return [list(vector) for vector in self.model.embed(list(texts))]


class DeterministicEmbedder:
    def __init__(self, dimensions: int = 16) -> None:
        self.dimensions = dimensions

    def embed(self, texts: Iterable[str]) -> list[list[float]]:
        vectors: list[list[float]] = []
        for text in texts:
            seed = int(sha256(text.encode("utf-8")).hexdigest(), 16)
            rng = Random(seed)
            vectors.append([rng.uniform(-1.0, 1.0) for _ in range(self.dimensions)])
        return vectors
```

- [ ] **Step 6: Run tests and commit**

```bash
pytest tests/test_documents.py tests/test_chunking.py -q
git add src/rag_lab tests
git commit -m "feat: add core rag document processing"
```

## Task 4: Vector Store Adapters

**Files:**
- Create: `src/rag_lab/vectorstores/base.py`
- Create: `src/rag_lab/vectorstores/in_memory.py`
- Create: `src/rag_lab/vectorstores/qdrant_store.py`
- Create: `src/rag_lab/vectorstores/pinecone_store.py`
- Create: `src/rag_lab/vectorstores/__init__.py`
- Create: `tests/test_in_memory_pipeline.py`

- [ ] **Step 1: Write adapter contract tests using in-memory store**

Create `tests/test_in_memory_pipeline.py`:

```python
from rag_lab.vectorstores.base import VectorRecord
from rag_lab.vectorstores.in_memory import InMemoryVectorStore


def test_in_memory_store_returns_nearest_records() -> None:
    store = InMemoryVectorStore()
    store.upsert(
        [
            VectorRecord(id="qdrant", text="Qdrant runs locally", vector=[1.0, 0.0], metadata={}),
            VectorRecord(id="pinecone", text="Pinecone is managed", vector=[0.0, 1.0], metadata={}),
        ]
    )

    results = store.search([0.9, 0.1], top_k=1)

    assert results[0].id == "qdrant"
    assert results[0].score > 0.9
```

- [ ] **Step 2: Run test and confirm failure**

```bash
pytest tests/test_in_memory_pipeline.py -q
```

Expected: import errors because vector store modules do not exist yet.

- [ ] **Step 3: Create the adapter interface**

Create `src/rag_lab/vectorstores/base.py`:

```python
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
```

- [ ] **Step 4: Create in-memory implementation**

Create `src/rag_lab/vectorstores/in_memory.py`:

```python
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
        self.records = [record for record in self.records if record.id not in {r.id for r in records}]
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
```

- [ ] **Step 5: Create Qdrant implementation**

Create `src/rag_lab/vectorstores/qdrant_store.py`:

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from rag_lab.vectorstores.base import SearchResult, VectorRecord


class QdrantVectorStore:
    def __init__(
        self,
        collection: str,
        url: str,
        api_key: str | None,
        dimensions: int,
    ) -> None:
        self.collection = collection
        self.client = QdrantClient(url=url, api_key=api_key)
        if not self.client.collection_exists(collection_name=collection):
            self.client.create_collection(
                collection_name=collection,
                vectors_config=VectorParams(size=dimensions, distance=Distance.COSINE),
            )

    def upsert(self, records: list[VectorRecord]) -> None:
        self.client.upsert(
            collection_name=self.collection,
            points=[
                PointStruct(
                    id=record.id,
                    vector=record.vector,
                    payload={"text": record.text, **record.metadata},
                )
                for record in records
            ],
        )

    def search(self, vector: list[float], top_k: int = 5) -> list[SearchResult]:
        response = self.client.query_points(
            collection_name=self.collection,
            query=vector,
            limit=top_k,
            with_payload=True,
        )
        return [
            SearchResult(
                id=str(point.id),
                text=str((point.payload or {}).get("text", "")),
                score=float(point.score),
                metadata={
                    key: str(value)
                    for key, value in (point.payload or {}).items()
                    if key != "text"
                },
            )
            for point in response.points
        ]
```

- [ ] **Step 6: Create Pinecone implementation**

Create `src/rag_lab/vectorstores/pinecone_store.py`:

```python
from time import sleep

from pinecone import Pinecone, ServerlessSpec

from rag_lab.vectorstores.base import SearchResult, VectorRecord


class PineconeVectorStore:
    def __init__(
        self,
        index_name: str,
        api_key: str,
        dimensions: int,
        cloud: str,
        region: str,
    ) -> None:
        self.pc = Pinecone(api_key=api_key)
        self.index_name = index_name
        existing_indexes = self.pc.list_indexes().names()
        if index_name not in existing_indexes:
            self.pc.create_index(
                name=index_name,
                dimension=dimensions,
                metric="cosine",
                spec=ServerlessSpec(cloud=cloud, region=region),
            )
            while not self.pc.describe_index(index_name).status["ready"]:
                sleep(1)
        self.index = self.pc.Index(index_name)

    def upsert(self, records: list[VectorRecord]) -> None:
        self.index.upsert(
            vectors=[
                {
                    "id": record.id,
                    "values": record.vector,
                    "metadata": {"text": record.text, **record.metadata},
                }
                for record in records
            ]
        )

    def search(self, vector: list[float], top_k: int = 5) -> list[SearchResult]:
        response = self.index.query(vector=vector, top_k=top_k, include_metadata=True)
        return [
            SearchResult(
                id=str(match["id"]),
                text=str(match.get("metadata", {}).get("text", "")),
                score=float(match["score"]),
                metadata={
                    key: str(value)
                    for key, value in match.get("metadata", {}).items()
                    if key != "text"
                },
            )
            for match in response["matches"]
        ]
```

- [ ] **Step 7: Run tests and commit**

```bash
pytest tests/test_in_memory_pipeline.py -q
git add src/rag_lab/vectorstores tests/test_in_memory_pipeline.py
git commit -m "feat: add vector store adapters"
```

## Task 5: Ingestion, Query, And Evaluation CLI

**Files:**
- Create: `src/rag_lab/pipeline.py`
- Create: `src/rag_lab/evaluation.py`
- Create: `scripts/ingest.py`
- Create: `scripts/query.py`
- Create: `scripts/evaluate.py`
- Create: `data/sample_docs/rag-basics.md`
- Create: `data/sample_docs/qdrant.md`
- Create: `data/sample_docs/pinecone.md`
- Create: `data/sample_docs/aws-bedrock.md`
- Create: `tests/test_evaluation.py`

- [ ] **Step 1: Write evaluation tests**

Create `tests/test_evaluation.py`:

```python
from rag_lab.evaluation import reciprocal_rank, recall_at_k


def test_recall_at_k_returns_one_when_expected_id_is_present() -> None:
    assert recall_at_k(["qdrant"], ["pinecone", "qdrant"], k=2) == 1.0


def test_reciprocal_rank_uses_first_relevant_position() -> None:
    assert reciprocal_rank(["qdrant"], ["pinecone", "qdrant"]) == 0.5
```

- [ ] **Step 2: Implement evaluation metrics**

Create `src/rag_lab/evaluation.py`:

```python
def recall_at_k(expected_ids: list[str], retrieved_ids: list[str], k: int) -> float:
    if not expected_ids:
        return 0.0
    retrieved = set(retrieved_ids[:k])
    expected = set(expected_ids)
    return len(expected & retrieved) / len(expected)


def reciprocal_rank(expected_ids: list[str], retrieved_ids: list[str]) -> float:
    expected = set(expected_ids)
    for position, retrieved_id in enumerate(retrieved_ids, start=1):
        if retrieved_id in expected:
            return 1.0 / position
    return 0.0
```

- [ ] **Step 3: Implement pipeline orchestration**

Create `src/rag_lab/pipeline.py`:

```python
from pathlib import Path

from rag_lab.chunking import chunk_text
from rag_lab.config import Settings
from rag_lab.documents import load_markdown_documents
from rag_lab.embeddings import DeterministicEmbedder, FastEmbedder
from rag_lab.vectorstores.base import SearchResult, VectorRecord, VectorStore
from rag_lab.vectorstores.in_memory import InMemoryVectorStore
from rag_lab.vectorstores.pinecone_store import PineconeVectorStore
from rag_lab.vectorstores.qdrant_store import QdrantVectorStore


def build_embedder(settings: Settings) -> FastEmbedder:
    return FastEmbedder(model_name=settings.embedding_model)


def infer_dimensions(embedder: FastEmbedder | DeterministicEmbedder) -> int:
    return len(embedder.embed(["dimension probe"])[0])


def build_records(
    docs_path: Path,
    embedder: FastEmbedder | DeterministicEmbedder,
) -> list[VectorRecord]:
    documents = load_markdown_documents(docs_path)
    chunk_ids: list[str] = []
    texts: list[str] = []
    metadata: list[dict[str, str]] = []
    for document in documents:
        for index, chunk in enumerate(chunk_text(document.text)):
            chunk_ids.append(f"{document.id}:{index}")
            texts.append(chunk)
            metadata.append(
                {
                    "document_id": document.id,
                    "source": document.metadata["source"],
                    "chunk_index": str(index),
                }
            )
    vectors = embedder.embed(texts)
    return [
        VectorRecord(id=chunk_id, text=text, vector=vector, metadata=meta)
        for chunk_id, text, vector, meta in zip(chunk_ids, texts, vectors, metadata, strict=True)
    ]


def build_store(store_name: str, settings: Settings, dimensions: int) -> VectorStore:
    normalized = store_name.lower().replace("_", "-")
    if normalized == "in-memory":
        return InMemoryVectorStore()
    if normalized == "qdrant":
        return QdrantVectorStore(
            collection=settings.collection,
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            dimensions=dimensions,
        )
    if normalized == "pinecone":
        if not settings.pinecone_api_key:
            raise ValueError("RAG_LAB_PINECONE_API_KEY is required for Pinecone")
        return PineconeVectorStore(
            index_name=settings.pinecone_index,
            api_key=settings.pinecone_api_key,
            dimensions=dimensions,
            cloud=settings.pinecone_cloud,
            region=settings.pinecone_region,
        )
    raise ValueError(f"Unsupported vector store: {store_name}")


def ingest_documents(store_name: str, docs_path: Path) -> int:
    settings = Settings(vector_store=store_name)
    embedder = build_embedder(settings)
    records = build_records(docs_path=docs_path, embedder=embedder)
    if not records:
        return 0
    store = build_store(store_name=store_name, settings=settings, dimensions=len(records[0].vector))
    store.upsert(records)
    return len(records)


def query_documents(store_name: str, question: str, top_k: int = 5) -> list[SearchResult]:
    settings = Settings(vector_store=store_name)
    embedder = build_embedder(settings)
    query_vector = embedder.embed([question])[0]
    store = build_store(store_name=store_name, settings=settings, dimensions=len(query_vector))
    return store.search(query_vector, top_k=top_k)
```

- [ ] **Step 4: Create CLI scripts**

Create `scripts/ingest.py`:

```python
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
```

Create `scripts/query.py`:

```python
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
```

Create `scripts/evaluate.py`:

```python
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
```

Required commands:

```bash
python scripts/ingest.py --store qdrant --docs data/sample_docs
python scripts/query.py --store qdrant "o que e qdrant?"
python scripts/evaluate.py --store qdrant
```

- [ ] **Step 5: Add sample documents**

Create four short Markdown files under `data/sample_docs/` covering:

- `rag-basics.md`: retrieval, augmentation, generation, failure modes.
- `qdrant.md`: local setup, collections, payload filters, HNSW, use cases.
- `pinecone.md`: managed serverless indexes, namespaces, metadata filters, use cases.
- `aws-bedrock.md`: managed embedding and generation services, relation to RAG.

- [ ] **Step 6: Run tests and commit**

```bash
pytest -q
git add src/rag_lab scripts data/sample_docs tests/test_evaluation.py
git commit -m "feat: add rag lab cli workflows"
```

## Task 6: Local Qdrant Runtime

**Files:**
- Create: `docker-compose.yml`
- Modify: `docs/labs/01-local-qdrant.md`
- Modify: `README.md`

- [ ] **Step 1: Create Docker Compose**

Create `docker-compose.yml`:

```yaml
services:
  qdrant:
    image: qdrant/qdrant:v1.12.4
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - qdrant_storage:/qdrant/storage

volumes:
  qdrant_storage:
```

- [ ] **Step 2: Verify Qdrant lab**

Run:

```bash
docker compose up -d qdrant
python scripts/ingest.py --store qdrant --docs data/sample_docs
python scripts/query.py --store qdrant "qual vector database roda localmente?"
docker compose down
```

Expected: query returns a result whose source metadata is `qdrant.md`.

- [ ] **Step 3: Commit**

```bash
git add docker-compose.yml README.md docs/labs/01-local-qdrant.md
git commit -m "feat: add local qdrant lab runtime"
```

## Task 7: Documentation Polish And Final Validation

**Files:**
- Modify: `README.md`
- Modify: docs pages as needed

- [ ] **Step 1: Rewrite README as the repo entrypoint**

`README.md` must include:

```markdown
# RAG Vector DB Lab

Laboratorio pratico para aprender RAG comparando vector databases como Qdrant e Pinecone.

## Inicio rapido

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev,docs]"
docker compose up -d qdrant
python scripts/ingest.py --store qdrant --docs data/sample_docs
python scripts/query.py --store qdrant "quando usar qdrant?"
mkdocs serve
```

## Labs

- Qdrant local: `docs/labs/01-local-qdrant.md`
- Pinecone cloud: `docs/labs/02-pinecone-cloud.md`
- Comparacao: `docs/labs/03-compare-results.md`
```

- [ ] **Step 2: Run full validation**

```bash
ruff check .
pytest -q
mkdocs build --strict
```

Expected: all commands pass.

- [ ] **Step 3: Verify GitHub rename status**

Run:

```bash
git remote -v
gh auth status
```

If GitHub CLI is authenticated:

```bash
gh repo rename rag-vector-db-lab --repo MaiconKevyn/qa-on-aws --yes
git remote set-url origin https://github.com/MaiconKevyn/rag-vector-db-lab.git
```

If GitHub CLI is not authenticated, leave the remote unchanged and document the manual command:

```bash
gh auth login
gh repo rename rag-vector-db-lab --repo MaiconKevyn/qa-on-aws --yes
git remote set-url origin https://github.com/MaiconKevyn/rag-vector-db-lab.git
```

- [ ] **Step 4: Commit**

```bash
git add README.md docs
git commit -m "docs: finalize rag vector db lab guide"
```

## Acceptance Criteria

- The local project directory is named `rag-vector-db-lab`.
- The repository no longer contains the AWS Lambda/SAM/Flask implementation.
- `README.md` explains the new lab purpose and quickstart.
- MkDocs builds a documentation site with Qdrant, Pinecone, and comparison pages.
- Qdrant runs locally through Docker Compose.
- Pinecone is supported through environment variables without hardcoded secrets.
- The same CLI can ingest, query, and evaluate both Qdrant and Pinecone.
- Unit tests cover chunking, document loading, evaluation metrics, and adapter behavior.
- `ruff check .`, `pytest -q`, and `mkdocs build --strict` pass.
