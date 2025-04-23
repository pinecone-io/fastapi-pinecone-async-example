import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from api import deps
from api.config import settings
from api.util import prepare_results, dedup_combined_results

pinecone_indexes = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    pinecone_indexes["dense"] = deps.get_pinecone_dense_index()
    pinecone_indexes["sparse"] = deps.get_pinecone_sparse_index()

    yield

    await pinecone_indexes["dense"].close()
    await pinecone_indexes["sparse"].close()

app = FastAPI(lifespan=lifespan, docs_url="/api/docs", openapi_url="/api/openapi.json")

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
    return await pinecone_indexes['dense'].search_records(
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
    return await pinecone_indexes['sparse'].search_records(
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
