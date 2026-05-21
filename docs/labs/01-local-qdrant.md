# Lab 01: Qdrant local

Use este lab para executar todo o pipeline sem conta externa.

```bash
python -m pip install -e ".[dev,docs]"
docker compose up -d qdrant
python scripts/ingest.py --store qdrant --docs data/sample_docs
python scripts/query.py --store qdrant "quando usar qdrant em rag?"
python scripts/evaluate.py --store qdrant
mkdocs serve
```

Ao final, a consulta deve retornar chunks vindos de `qdrant.md`.
