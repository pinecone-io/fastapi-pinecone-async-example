from pinecone import Pinecone
from api.config import settings

pc = Pinecone(api_key=settings.pinecone_api_key)

def get_pinecone_dense_index():
    return pc.IndexAsyncio(host=settings.pinecone_dense_index_host)

def get_pinecone_sparse_index():
    return pc.IndexAsyncio(host=settings.pinecone_sparse_index_host)