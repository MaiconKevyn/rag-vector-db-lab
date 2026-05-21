from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    vector_store: str = "qdrant"
    collection: str = "rag_lab_documents"
    embedding_model: str = "BAAI/bge-small-en-v1.5"
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str | None = None
    pinecone_api_key: str | None = None
    pinecone_index: str = "rag-vector-db-lab"
    pinecone_cloud: str = "aws"
    pinecone_region: str = "us-east-1"

    model_config = SettingsConfigDict(env_prefix="RAG_LAB_", env_file=".env", extra="ignore")
