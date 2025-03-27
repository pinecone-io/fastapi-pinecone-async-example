from pinecone import Pinecone
from api.config import settings

pc = Pinecone(api_key=settings.pinecone_api_key)

def get_pinecone_index():
    return pc.IndexAsyncio(host=settings.pinecone_index_host)