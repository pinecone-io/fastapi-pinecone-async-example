from fastapi import FastAPI, HTTPException
from pinecone import SearchQuery
from api import deps
from api.config import settings

app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")

@app.get("/api/search/dense")
async def dense_search(text_query: str = None):
    if not text_query or not text_query.strip():
        raise HTTPException(status_code=422, detail="Text query cannot be empty")
    
    results = await query_dense_index(text_query)

    return {"results": results}

@app.get("/api/search/sparse")
async def sparse_search(text_query: str = None):
    if not text_query or not text_query.strip():
        raise HTTPException(status_code=422, detail="Text query cannot be empty")
    
    results = await query_sparse_index(text_query)
    
    return {"results": results}

@app.get("/api/search/hybrid")
async def hybrid_search(text_query: str = None):
    if not text_query or not text_query.strip():
        raise HTTPException(status_code=422, detail="Text query cannot be empty")
    
    dense_results, sparse_results, combined_results = await query_hybrid(text_query)    

    return {"dense_results": dense_results, "sparse_results": sparse_results, "results": combined_results}

async def query_hybrid(text_query: str):
    # First do dense search
    async with deps.get_pinecone_dense_index() as dense_idx:
        dense_response = await dense_idx.search_records(
            namespace=settings.pinecone_namespace,
            query=SearchQuery(
                inputs={
                    "text": text_query,
                },
                top_k=settings.pinecone_top_k,
            ),
            rerank={
                "model": "cohere-rerank-3.5",
                "rank_fields": ["chunk_text"]
            }
        )

    # Then do sparse search
    async with deps.get_pinecone_sparse_index() as sparse_idx:
        sparse_response = await sparse_idx.search_records(
            namespace=settings.pinecone_namespace,
            query=SearchQuery(
                inputs={
                    "text": text_query,
                },
                top_k=settings.pinecone_top_k,
            ),
            rerank={
                "model": "cohere-rerank-3.5",
                "rank_fields": ["chunk_text"]
            }
        )

    dense_results = prepare_results(dense_response.result.hits)
    sparse_results = prepare_results(sparse_response.result.hits)
    
    combined_results = dense_results + sparse_results
    deduped_results = dedup_combined_results(combined_results)

    return dense_results, sparse_results, deduped_results[:settings.pinecone_top_k]
        
async def query_dense_index(text_query: str):
    async with deps.get_pinecone_dense_index() as idx:
        response = await idx.search_records(
            namespace=settings.pinecone_namespace,
            query=SearchQuery(
                inputs={
                    "text": text_query,
                },
                top_k=settings.pinecone_top_k,
            ),
        )

# score here is semantic similarity score (cosine similarity)
# the reranker score is more about relevance to the query based on the reranker model - relevance score
    results = prepare_results(response.result.hits)
    
    return results

async def query_sparse_index(text_query: str):
    async with deps.get_pinecone_sparse_index() as idx:
        response = await idx.search_records(
            namespace=settings.pinecone_namespace,
            query=SearchQuery(
                inputs={
                    "text": text_query,
                },
                top_k=settings.pinecone_top_k,
            ),
        )

    results = prepare_results(response.result.hits)

    return results

def prepare_results(hits: list):
    return [{
        "_id": hit['_id'],
        "score": hit['_score'],
        "chunk_text": hit['fields']['chunk_text'],
    } for hit in hits]

def dedup_combined_results(combined_results: list):
    seen_ids = {}
    deduped_results = []
    
    # Keep first occurrence of each ID
    for result in combined_results:
        if result['_id'] not in seen_ids:
            seen_ids[result['_id']] = True
            deduped_results.append(result)
    
    return sorted(deduped_results, key=lambda x: x['score'], reverse=True)