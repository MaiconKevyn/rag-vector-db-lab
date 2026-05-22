from uuid import NAMESPACE_URL, uuid5

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from rag_lab.vectorstores.base import SearchResult, VectorRecord, ensure_vector_dimensions


class QdrantVectorStore:
    def __init__(
        self,
        collection: str,
        url: str,
        api_key: str | None,
        dimensions: int,
    ) -> None:
        self.collection = collection
        self.client = QdrantClient(url=url, api_key=api_key)
        if not self.client.collection_exists(collection_name=collection):
            self.client.create_collection(
                collection_name=collection,
                vectors_config=VectorParams(size=dimensions, distance=Distance.COSINE),
            )
        else:
            collection_info = self.client.get_collection(collection_name=collection)
            vector_config = collection_info.config.params.vectors
            if isinstance(vector_config, dict):
                vector_size = next(iter(vector_config.values())).size
            else:
                vector_size = vector_config.size
            ensure_vector_dimensions(
                expected=dimensions,
                actual=vector_size,
                store_name="qdrant",
            )

    def upsert(self, records: list[VectorRecord]) -> None:
        self.client.upsert(
            collection_name=self.collection,
            points=[
                PointStruct(
                    id=str(uuid5(NAMESPACE_URL, record.id)),
                    vector=record.vector,
                    payload={"record_id": record.id, "text": record.text, **record.metadata},
                )
                for record in records
            ],
        )

    def search(self, vector: list[float], top_k: int = 5) -> list[SearchResult]:
        response = self.client.query_points(
            collection_name=self.collection,
            query=vector,
            limit=top_k,
            with_payload=True,
        )
        return [
            SearchResult(
                id=str((point.payload or {}).get("record_id", point.id)),
                text=str((point.payload or {}).get("text", "")),
                score=float(point.score),
                metadata={
                    key: str(value)
                    for key, value in (point.payload or {}).items()
                    if key not in {"record_id", "text"}
                },
            )
            for point in response.points
        ]
