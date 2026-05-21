# Qdrant

Qdrant e um vector database com boa experiencia local via Docker e API compativel com workloads de RAG. Ele organiza vetores em collections, cada uma com tamanho de vetor e metrica de distancia definidos no momento da criacao.

## Uso local

No laboratorio, Qdrant roda com Docker Compose:

```bash
docker compose up -d qdrant
```

A API HTTP fica disponivel em `http://localhost:6333`. Os scripts criam a collection configurada em `RAG_LAB_COLLECTION` quando ela ainda nao existe.

## Collections e payloads

Cada chunk indexado vira um ponto com:

- vetor numerico;
- texto original no payload;
- metadados como `source`, `document_id` e `chunk_index`.

Payload filters permitem restringir buscas por documento, fonte ou qualquer outro metadado salvo junto do vetor.

## HNSW

Qdrant usa HNSW para busca aproximada de vizinhos proximos. O indice oferece baixa latencia em colecoes grandes mantendo boa qualidade de recuperacao, e ainda permite ajustes finos quando a aplicacao precisa equilibrar velocidade e recall.

## Quando usar

Qdrant e uma boa escolha quando voce quer desenvolvimento local, controle de infraestrutura, filtros por metadados e uma transicao simples para self-hosted ou cloud.
