MetaRAG is a Python framework for multi-model Retrieval-Augmented Generation. It queries multiple LLMs in parallel, scores the responses based on cosine similarity with the context, and aggregates the top responses for a more accurate and comprehensive answer.

## Features
- 🔍 Multi-LLM querying using Groq's LLMs (LLaMA3, Gemma, etc.)
- 🤝 Cosine similarity scoring of responses
- 🧠 Top-k response aggregation
- 📄 Works with PDFs and plain text
- ⚡ Fast execution with thread pooling

## Installation
```bash
pip install metarag
```

## Example Usage
```python
from metarag import MetaRAG

rag = MetaRAG(["VectorDB_Paper.pdf"])
result = rag.query("Explain the abstract in simple terms")
print(result["aggregated_response"])
```

## Requirements
Python 3.8+

## License
MIT License - see LICENSE file for details.

## Author
**Nisharg Nargund**  
Founder @OpenRAG
