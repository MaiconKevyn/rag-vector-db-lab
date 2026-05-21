# Avaliacao de retrieval

Avaliacao de retrieval mede se a busca retorna os documentos esperados para uma pergunta.

Este laboratorio usa duas metricas simples:

| Metrica | O que mede |
| --- | --- |
| Recall@k | Proporcao dos documentos esperados que aparecem nos primeiros `k` resultados |
| MRR | Quanto mais cedo aparece o primeiro resultado relevante |

Essas metricas nao substituem avaliacao humana, mas ajudam a comparar Qdrant e Pinecone com o mesmo corpus, as mesmas perguntas e os mesmos embeddings.
