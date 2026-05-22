# RAG Vector DB Lab Benchmark Report

This report is generated from a reproducible benchmark run using the same corpus, chunking strategy, embedding model, and retrieval metrics.

## Summary

| Store | Items | Mean recall@k | Mean MRR | Mean latency ms | P95 latency ms |
| --- | ---: | ---: | ---: | ---: | ---: |
| qdrant | 20 | 0.975 | 0.975 | 173.8 | 186.7 |

## Per-question Results

| ID | Difficulty | Topic | Recall@k | MRR | Latency ms | Retrieved ids |
| --- | --- | --- | ---: | ---: | ---: | --- |
| qdrant-local-runtime | easy | qdrant | 1.000 | 1.000 | 234.7 | qdrant, aws-bedrock, pinecone |
| qdrant-collections | easy | qdrant | 1.000 | 1.000 | 157.7 | qdrant, aws-bedrock, pinecone |
| qdrant-hnsw | medium | qdrant | 1.000 | 1.000 | 184.5 | qdrant, pinecone, aws-bedrock |
| qdrant-payload-filter | medium | qdrant | 1.000 | 1.000 | 160.2 | qdrant, rag-basics, aws-bedrock |
| qdrant-best-fit | medium | qdrant | 1.000 | 1.000 | 164.4 | qdrant, rag-basics, aws-bedrock |
| pinecone-managed | easy | pinecone | 1.000 | 0.500 | 156.3 | qdrant, pinecone, aws-bedrock |
| pinecone-serverless | medium | pinecone | 1.000 | 1.000 | 157.3 | pinecone, qdrant, rag-basics |
| pinecone-namespaces | medium | pinecone | 1.000 | 1.000 | 160.2 | pinecone, rag-basics, qdrant |
| pinecone-api-key | easy | pinecone | 1.000 | 1.000 | 168.6 | pinecone, qdrant, aws-bedrock |
| pinecone-best-fit | medium | pinecone | 1.000 | 1.000 | 181.5 | pinecone, aws-bedrock, qdrant |
| rag-definition | easy | rag | 1.000 | 1.000 | 181.3 | rag-basics, aws-bedrock, qdrant |
| rag-retriever | easy | rag | 1.000 | 1.000 | 166.0 | rag-basics, aws-bedrock, pinecone |
| rag-failure-modes | medium | rag | 1.000 | 1.000 | 186.7 | rag-basics, aws-bedrock, pinecone |
| rag-grounding | medium | rag | 1.000 | 1.000 | 176.4 | rag-basics, aws-bedrock, pinecone |
| bedrock-role | easy | bedrock | 1.000 | 1.000 | 182.3 | aws-bedrock, rag-basics, qdrant |
| bedrock-not-vector-db | medium | bedrock | 1.000 | 1.000 | 163.5 | aws-bedrock, qdrant, pinecone |
| compare-local-cloud | hard | comparison | 1.000 | 1.000 | 159.3 | pinecone, qdrant, aws-bedrock |
| compare-metadata-filter | hard | comparison | 0.500 | 1.000 | 181.3 | qdrant, rag-basics, aws-bedrock |
| compare-operational-risk | hard | comparison | 1.000 | 1.000 | 172.7 | pinecone, qdrant, aws-bedrock |
| compare-provider-dependency | hard | comparison | 1.000 | 1.000 | 181.0 | pinecone, aws-bedrock, qdrant |
