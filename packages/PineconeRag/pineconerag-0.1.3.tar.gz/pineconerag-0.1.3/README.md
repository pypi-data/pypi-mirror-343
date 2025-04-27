# Pinecone RAG

A Python package for working with Pinecone in RAG (Retrieval-Augmented Generation) applications.

## Installation

```bash
pip install pinecone-rag
```

## Usage

```python
from PineconeRag import PineconeRAG

# Initialize the RAG client
rag = PineconeRAG(
    api_key="your-api-key",  # or set PINECONE_API_KEY env var
    index_name="rag-768"     # optional, defaults to "rag-768"
)

# Define a callback function (optional)
def process_match(match):
    print(f"Found match with score: {match['score']}")
    print(f"Text: {match['metadata']['original_text']}")

# Query Pinecone
results = rag.query(
    namespace="your-namespace",
    text="your query text",
    top_k=3,
    include_metadata=True,  # optional, defaults to True
    callback=process_match,  # optional callback
    debug=True  # optional debug mode
)
```

## Publishing to PyPI

```bash
python3 -m pip install --upgrade build
python3 -m build
python3 -m twine upload --repository pypi dist/*
```