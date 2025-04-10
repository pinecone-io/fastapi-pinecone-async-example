import asyncio
from fastapi import FastAPI, HTTPException
from api import deps
from api.config import settings

app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")

@app.get("/api/semantic-search")
async def semantic_search(text_query: str = None):
    if not text_query or not text_query.strip():
        raise HTTPException(status_code=422, detail="Text query cannot be empty")
    
    dense_response = await query_dense_index(text_query)
    results = prepare_results(dense_response.result.hits)

    return {"results": results}

@app.get("/api/lexical-search")
async def lexical_search(text_query: str = None):
    if not text_query or not text_query.strip():
        raise HTTPException(status_code=422, detail="Text query cannot be empty")
    
    sparse_response = await query_sparse_index(text_query)
    results = prepare_results(sparse_response.result.hits)
    
    return {"results": results}

@app.get("/api/cascading-retrieval")
async def cascading_retrieval(text_query: str = None):
    if not text_query or not text_query.strip():
        raise HTTPException(status_code=422, detail="Text query cannot be empty")
    
    dense_response, sparse_response = await asyncio.gather(
        query_dense_index(text_query, rerank=True),
        query_sparse_index(text_query, rerank=True)
    )

    combined_results = dense_response.result.hits + sparse_response.result.hits
    deduped_results = dedup_combined_results(combined_results)

    results = deduped_results[:settings.pinecone_top_k]

    return {"results": results}
        
async def query_dense_index(text_query: str, rerank: bool = False):
    async with deps.get_pinecone_dense_index() as idx:
        return await idx.search_records(
            namespace=settings.pinecone_namespace,
            query={
                "inputs": {
                    "text": text_query,
                },
                "top_k": settings.pinecone_top_k,
            },
            rerank={
                "model": "cohere-rerank-3.5",
                "rank_fields": ["chunk_text"]
            } if rerank else None
        )

async def query_sparse_index(text_query: str, rerank: bool = False):
    async with deps.get_pinecone_sparse_index() as idx:
        return await idx.search_records(
            namespace=settings.pinecone_namespace,
            query={
                "inputs":{
                    "text": text_query,
                },
                "top_k": settings.pinecone_top_k,
            },
            rerank={
                "model": "cohere-rerank-3.5",
                "rank_fields": ["chunk_text"]
            } if rerank else None
        )

def prepare_results(hits: list):
    return [{
        "_id": hit['_id'],
        "score": hit['_score'],
        "chunk_text": hit['fields']['chunk_text'],
    } for hit in hits]

def dedup_combined_results(combined_results: list):
    seen_ids = {}
    deduped_records = []
    
    # Keep first occurrence of each ID
    for result in combined_results:
        if result['_id'] not in seen_ids:
            seen_ids[result['_id']] = True
            record = {
                "_id": result['_id'],
                "score": result['_score'],
                "chunk_text": result['fields']['chunk_text'],
            }
            deduped_records.append(record)
    
    return sorted(deduped_records, key=lambda x: x['score'], reverse=True)