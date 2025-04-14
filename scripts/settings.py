import os
from dotenv import load_dotenv

load_dotenv(override=True)

class Settings:
    def __init__(self):
        self.pinecone_api_key = os.getenv('PINECONE_API_KEY')
        self.pinecone_dense_index_name = os.getenv('PINECONE_DENSE_INDEX_NAME')
        self.pinecone_sparse_index_name = os.getenv('PINECONE_SPARSE_INDEX_NAME')
        self.pinecone_namespace = os.getenv('PINECONE_NAMESPACE')

        # Dataset to load
        self.dataset = "GEM/sportsett_basketball"
        self.dataset_split = "test"
        self.field_name_to_chunk = "target"
        
        # Embedding model names
        self.dense_embedding_model = "llama-text-embed-v2"
        self.sparse_embedding_model = "pinecone-sparse-english-v0"

settings = Settings() 