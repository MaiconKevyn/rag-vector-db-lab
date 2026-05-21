# Lab 03: Comparar resultados

Use este lab depois de indexar o mesmo corpus em Qdrant e Pinecone.

```bash
python -m pip install -e ".[dev,docs]"
docker compose up -d qdrant
python scripts/ingest.py --store qdrant --docs data/sample_docs
python scripts/query.py --store qdrant "quando usar qdrant em rag?"
python scripts/evaluate.py --store qdrant
cp .env.example .env
python scripts/ingest.py --store pinecone --docs data/sample_docs
python scripts/query.py --store pinecone "quando usar pinecone em rag?"
python scripts/evaluate.py --store pinecone
mkdocs serve
```

Compare recall, MRR, latencia percebida, esforco operacional e facilidade de configurar filtros por metadados.
