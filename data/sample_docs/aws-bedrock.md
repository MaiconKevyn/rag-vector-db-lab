# AWS Bedrock

AWS Bedrock provides managed embedding and generation models. In a RAG system, Bedrock can generate embeddings for chunks and can also generate final answers after retrieval.

Bedrock is not a vector database by itself. It is usually paired with a retrieval store such as Qdrant, Pinecone, OpenSearch, or another vector search backend.
