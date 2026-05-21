# Embeddings

Embeddings transformam texto em vetores numericos. Textos semanticamente parecidos devem ficar proximos no espaco vetorial.

O laboratorio usa `fastembed` com o modelo configurado em `RAG_LAB_EMBEDDING_MODEL`. O valor padrao e `BAAI/bge-small-en-v1.5`, uma opcao pequena e pratica para labs locais.

Ao comparar bancos vetoriais, mantenha o mesmo modelo de embedding para todos os stores. Trocar o modelo muda a distribuicao dos vetores e invalida comparacoes diretas de recall ou ranking.
