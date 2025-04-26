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
## Pre-requisites
Load your GROQ_API_KEY to the project from https://console.groq.com/keys and follow the sample example shown below.
## Example Usage (Local PC)
```python
import metarag
from dotenv import load_dotenv
load_dotenv()  
def test_metarag_functionality():
    
    document_paths = ["VectorDB_Paper.pdf"]  

    rag_instance = metarag.MetaRAG(document_paths=document_paths)

    query = "What is the methodology in 5 lines like a professor and extract 5 keywords?"

    result = rag_instance.run(query)

    print(f"Aggregated Response: {result}")

if __name__ == "__main__":
    test_metarag_functionality()

```
## On Google Colab
```
import metarag
import os

os.environ["GROQ_API_KEY"]="groq_api_key"

    
document_paths = ["/content/VectorDB_Paper.pdf"]  

rag_instance = metarag.MetaRAG(document_paths=document_paths)

query = "What is the methodology in 5 lines like a professor and extract 5 keywords?"

result = rag_instance.run(query)

print(f"Aggregated Response: {result}")


```
## Requirements
Python 3.8+

## License
MIT License - see LICENSE file for details.

## Author
**Nisharg Nargund**  
Founder @OpenRAG
