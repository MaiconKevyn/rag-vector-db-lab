from time import sleep

from pinecone import Pinecone, ServerlessSpec

from rag_lab.vectorstores.base import SearchResult, VectorRecord, VectorStoreError


class PineconeVectorStore:
    def __init__(
        self,
        index_name: str,
        api_key: str,
        dimensions: int,
        cloud: str,
        region: str,
    ) -> None:
        self.pc = Pinecone(api_key=api_key)
        self.index_name = index_name
        existing_indexes = self.pc.list_indexes().names()
        if index_name not in existing_indexes:
            self.pc.create_index(
                name=index_name,
                dimension=dimensions,
                metric="cosine",
                spec=ServerlessSpec(cloud=cloud, region=region),
            )
            attempts = 0
            while not self.pc.describe_index(index_name).status["ready"]:
                attempts += 1
                if attempts > 60:
                    raise VectorStoreError(f"Pinecone index did not become ready: {index_name}")
                sleep(1)
        self.index = self.pc.Index(index_name)

    def upsert(self, records: list[VectorRecord]) -> None:
        self.index.upsert(
            vectors=[
                {
                    "id": record.id,
                    "values": record.vector,
                    "metadata": {"text": record.text, **record.metadata},
                }
                for record in records
            ]
        )

    def search(self, vector: list[float], top_k: int = 5) -> list[SearchResult]:
        response = self.index.query(vector=vector, top_k=top_k, include_metadata=True)
        return [
            SearchResult(
                id=str(match["id"]),
                text=str(match.get("metadata", {}).get("text", "")),
                score=float(match["score"]),
                metadata={
                    key: str(value)
                    for key, value in match.get("metadata", {}).items()
                    if key != "text"
                },
            )
            for match in response["matches"]
        ]
