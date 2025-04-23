def prepare_results(hits: list):
    return [{
        "_id": hit['_id'],
        "score": hit['_score'],
        "chunk_text": hit['fields']['chunk_text'],
    } for hit in hits]

def dedup_combined_results(combined_results: list):
    unique_records = {
        result['_id']: {
            "_id": result['_id'],
            "score": result['_score'],
            "chunk_text": result['fields']['chunk_text'],
        }
        for result in combined_results
    }
    
    return sorted(unique_records.values(), key=lambda x: x['score'], reverse=True)