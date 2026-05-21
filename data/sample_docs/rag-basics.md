# RAG basics

Retrieval-Augmented Generation, or RAG, combines retrieval, augmentation, and generation. The retriever finds relevant chunks from a knowledge base, the application adds those chunks to the prompt, and the language model generates an answer grounded in that retrieved context.

Common failure modes include missing the relevant document, retrieving a weak chunk, using stale source material, or generating an answer that ignores the retrieved evidence.
