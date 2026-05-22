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
