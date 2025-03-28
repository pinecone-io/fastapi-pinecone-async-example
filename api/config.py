from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    pinecone_dense_index_host: str
    pinecone_sparse_index_host: str
    pinecone_namespace: str
    pinecone_top_k: int
    pinecone_api_key: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()