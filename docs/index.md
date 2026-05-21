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
