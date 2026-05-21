# Lab 02: Pinecone cloud

Use este lab para comparar o mesmo corpus em um vector database cloud gerenciado.

```bash
python -m pip install -e ".[dev,docs]"
cp .env.example .env
python scripts/ingest.py --store pinecone --docs data/sample_docs
python scripts/query.py --store pinecone "quando usar pinecone em rag?"
python scripts/evaluate.py --store pinecone
mkdocs serve
```

Antes de rodar os scripts, preencha `RAG_LAB_PINECONE_API_KEY` no `.env`. Os demais valores podem ficar nos defaults durante o primeiro teste.
