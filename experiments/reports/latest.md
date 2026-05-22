# RAG Vector DB Lab Benchmark Report

This report is generated from a reproducible benchmark run using the same corpus, chunking strategy, embedding model, and retrieval metrics.

## Summary

| Store | Items | Mean recall@k | Mean MRR | Mean latency ms | P95 latency ms |
| --- | ---: | ---: | ---: | ---: | ---: |
| qdrant | 20 | 0.975 | 0.975 | 171.6 | 184.9 |

## Per-question Results

| ID | Difficulty | Topic | Recall@k | MRR | Latency ms | Retrieved ids |
| --- | --- | --- | ---: | ---: | ---: | --- |
| qdrant-local-runtime | easy | qdrant | 1.000 | 1.000 | 235.1 | qdrant, aws-bedrock, pinecone |
| qdrant-collections | easy | qdrant | 1.000 | 1.000 | 180.3 | qdrant, aws-bedrock, pinecone |
| qdrant-hnsw | medium | qdrant | 1.000 | 1.000 | 164.6 | qdrant, pinecone, aws-bedrock |
| qdrant-payload-filter | medium | qdrant | 1.000 | 1.000 | 163.9 | qdrant, rag-basics, aws-bedrock |
| qdrant-best-fit | medium | qdrant | 1.000 | 1.000 | 163.4 | qdrant, rag-basics, aws-bedrock |
| pinecone-managed | easy | pinecone | 1.000 | 0.500 | 176.5 | qdrant, pinecone, aws-bedrock |
| pinecone-serverless | medium | pinecone | 1.000 | 1.000 | 177.5 | pinecone, qdrant, rag-basics |
| pinecone-namespaces | medium | pinecone | 1.000 | 1.000 | 181.0 | pinecone, rag-basics, qdrant |
| pinecone-api-key | easy | pinecone | 1.000 | 1.000 | 177.7 | pinecone, qdrant, aws-bedrock |
| pinecone-best-fit | medium | pinecone | 1.000 | 1.000 | 179.7 | pinecone, aws-bedrock, qdrant |
| rag-definition | easy | rag | 1.000 | 1.000 | 160.2 | rag-basics, aws-bedrock, qdrant |
| rag-retriever | easy | rag | 1.000 | 1.000 | 156.4 | rag-basics, aws-bedrock, pinecone |
| rag-failure-modes | medium | rag | 1.000 | 1.000 | 154.0 | rag-basics, aws-bedrock, pinecone |
| rag-grounding | medium | rag | 1.000 | 1.000 | 164.8 | rag-basics, aws-bedrock, pinecone |
| bedrock-role | easy | bedrock | 1.000 | 1.000 | 153.5 | aws-bedrock, rag-basics, qdrant |
| bedrock-not-vector-db | medium | bedrock | 1.000 | 1.000 | 156.0 | aws-bedrock, qdrant, pinecone |
| compare-local-cloud | hard | comparison | 1.000 | 1.000 | 155.1 | pinecone, qdrant, aws-bedrock |
| compare-metadata-filter | hard | comparison | 0.500 | 1.000 | 184.9 | qdrant, rag-basics, aws-bedrock |
| compare-operational-risk | hard | comparison | 1.000 | 1.000 | 180.8 | pinecone, qdrant, aws-bedrock |
| compare-provider-dependency | hard | comparison | 1.000 | 1.000 | 167.1 | pinecone, aws-bedrock, qdrant |
