# Pinecone

Pinecone e um vector database cloud gerenciado. Ele remove grande parte do trabalho operacional de provisionar, atualizar e escalar a infraestrutura de busca vetorial.

## Managed indexes

Os vetores sao armazenados em indexes. No modo serverless, o index e criado com cloud, regiao, dimensao e metrica de similaridade. O laboratorio usa essas configuracoes a partir de variaveis `RAG_LAB_PINECONE_*`.

## Serverless deployment

Para usar Pinecone, configure uma API key e o nome do index:

```bash
cp .env.example .env
```

Depois preencha `RAG_LAB_PINECONE_API_KEY` e ajuste cloud, regiao ou index se necessario.

## Namespaces e filtros

Namespaces separam conjuntos de vetores dentro do mesmo index. Metadata filters permitem limitar a busca por campos como fonte, tipo de documento ou tenant.

## Quando usar

Pinecone e uma boa escolha quando voce quer operacao gerenciada, setup cloud rapido, escalabilidade sem administrar servidores e integracao direta com pipelines RAG em producao.
