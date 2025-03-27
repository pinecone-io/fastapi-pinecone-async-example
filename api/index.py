from fastapi import FastAPI, HTTPException
from pinecone import SearchQuery
from api import deps
from api.config import settings

app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")

@app.get("/api/search")
async def search(text_query: str = None):
    if not text_query or not text_query.strip():
        raise HTTPException(status_code=422, detail="Text query cannot be empty")
    
    response = await query_index(text_query)
    list_of_hits = response.result.hits
    
    results = [{
        "_id": hit['_id'],
        "score": hit['_score'],
        "chunk_text": hit['fields']['chunk_text'],
    } for hit in list_of_hits]

    return {"results": results}

async def query_index(text_query: str):
    async with deps.get_pinecone_index() as idx:
        response = await idx.search_records(
            namespace=settings.pinecone_namespace,
            query=SearchQuery(
                inputs={
                    "text": text_query,
                },
                top_k=settings.pinecone_top_k,
            ),
        )

    return response
    