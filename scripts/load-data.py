from pinecone import Pinecone
import time
from datasets import load_dataset
import nltk
from tqdm import tqdm
from settings import settings

def main():
    pc = Pinecone(api_key=settings.pinecone_api_key, source_tag="pinecone:fastapi_pinecone_async_example")

    dense_index = create_index(pc, settings.pinecone_dense_index_name, settings.dense_embedding_model)
    sparse_index = create_index(pc, settings.pinecone_sparse_index_name, settings.sparse_embedding_model)

    records = process_dataset(settings.dataset, settings.dataset_split, settings.field_name_to_chunk)
    
    upsert_data(dense_index, settings.pinecone_namespace, records)
    upsert_data(sparse_index, settings.pinecone_namespace, records)
    
    time.sleep(15)

    stats = dense_index.describe_index_stats()
    print("Dense index stats:", stats)

    stats = sparse_index.describe_index_stats()
    print("Sparse index stats:", stats)

def create_index(pc, index_name, embed_model):
    if not pc.has_index(index_name):
        pc.create_index_for_model(
            name=index_name,
            cloud="aws",
            region="us-east-1",
            embed={
                "model": embed_model,
                "field_map": {"text": "chunk_text"}
            }
        )

    return pc.Index(index_name)

def process_dataset(dataset, split_name, field_name_to_chunk):
    test_dataset = load_dataset(dataset, split=split_name)
    records = []
    
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')

    for item_id, item in enumerate(test_dataset):
        field_to_chunk = item[field_name_to_chunk]
        chunks = nltk.sent_tokenize(field_to_chunk)

        for chunk_id, chunk in enumerate(chunks):
            # print(f"item#{item_id}#{chunk_id},{chunk}")
            record = {
                "_id": f"item#{item_id}#{chunk_id}", 
                "chunk_text": chunk
            }
            records.append(record)
    return records

def upsert_data(index, namespace, records):
    # Batch size is limited by the embedding model limit and the API's upsert limit.
    batch_size = 96
    for i in tqdm(range(0, len(records), batch_size), desc="Upserting records to Pinecone"):
        batch = records[i:i + batch_size]
        try:
            index.upsert_records(namespace=namespace, records=batch)
        except Exception as e:
            print(f"Error upserting batch: {e}")
            print(f"Batch: {batch}")

if __name__ == "__main__":
    main()