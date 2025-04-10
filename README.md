# Using the Pinecone Python SDK with Asyncio support

This is a sample app to demonstrate how to use the [Pinecone Python SDK](https://docs.pinecone.io/reference/python-sdk) with [asyncio](https://docs.python.org/3/library/asyncio.html) support. This is a simple Next.js app with a FastAPI backend.

## Getting started

### Prerequisites

- A Pinecone account. Create your free account [here](https://app.pinecone.io/?sessionType=signup) if you don't already have one.
- A Pinecone API key by following [these steps](https://docs.pinecone.io/guides/projects/manage-api-keys#create-an-api-key).
- Python 3.12 or higher.
- [Node.js](https://nodejs.org/) 20 or higher.

### Setup

#### Setup environment

Set up your custom environment variables by copying the `.env.example` file in the project root and replacing with your environment values.

#### Install Node dependencies

```bash
npm install
```

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

#### Create indexes load data

TODO

### Run the app

```bash
npm run dev
```

Head over to [http://localhost:3000](http://localhost:3000) to view the app.

The FastApi server will be running on [http://127.0.0.1:8000](http://127.0.0.1:8000).

