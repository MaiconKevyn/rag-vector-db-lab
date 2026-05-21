# Chunking

Chunking e a etapa que transforma documentos longos em trechos menores antes da geracao de embeddings.

Chunks pequenos aumentam precisao local, mas podem perder contexto. Chunks grandes preservam contexto, mas podem misturar assuntos e piorar a busca. O overlap reaproveita algumas palavras do chunk anterior para reduzir cortes bruscos.

No laboratorio, o chunking base usa contagem de palavras:

```python
chunk_text(text, chunk_size=180, overlap=30)
```

Para comparar vector databases com justica, mantenha a mesma estrategia de chunking entre Qdrant e Pinecone.
