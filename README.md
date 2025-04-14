# Using the Pinecone with Asyncio support and FastAPI

This is a sample app to demonstrate how to use the [Pinecone Python SDK](https://docs.pinecone.io/reference/python-sdk) with [asyncio](https://docs.python.org/3/library/asyncio.html) support. This is a simple Next.js app with a FastAPI backend.

## Getting started

### Prerequisites

- A Pinecone account. Create your free account [here](https://app.pinecone.io/?sessionType=signup) if you don't already have one.
- A Pinecone API key by following [these steps](https://docs.pinecone.io/guides/projects/manage-api-keys#create-an-api-key).
- Python 3.12 or higher.
- [Node.js](https://nodejs.org/) 20 or higher.

### Setup

#### Create Python virtual environment

Create and activate a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Install Python dependencies

```bash
pip3 install -r requirements.txt
```

#### Create indexes and load data

If you don't have both a dense index and a sparse index loaded with your own data, you can load test data using the `load-data.py` in the `scripts` directory. This will create two indexes:

1. a dense index using NVIDIA's `llama-text-embed-v2`, a state-of-the-art embedding model available natively in Pinecone Inference
2. a sparse index using Pinecone's own `pinecone-sparse-english-v0` embedding model

Once the indexes are created, it will chunk and upsert data from a dataset on Huggingface, converting the text to dense vectors automatically using the hosted embedding model.

##### Setup the script environment

Set up your scripts environment variables by copying the `.env.example` file in the `scripts` directory to `.env` and replacing with your environment values.

##### Run the script

From the `scripts` directory, run:

```bash
python3 load-data.py
```

#### Setup the app environment

Set up your app environment variables by copying the `.env.example` file in the project root to `.env` and replacing with your environment values. You'll need to grab the index host URLs either from the [Pinecone console](https://app.pinecone.io/organizations/-/projects/-/indexes) or from the Pinecone API using `describe_index` as detailed [here](https://docs.pinecone.io/guides/data/target-an-index).

#### Install Node dependencies

From the project root, run:

```bash
npm install
```

### Run the app

From the project root, run:

```bash
npm run dev
```

Head over to [http://localhost:3000](http://localhost:3000) to view the app.

The FastAPI server will be running on [http://127.0.0.1:8000](http://127.0.0.1:8000).

