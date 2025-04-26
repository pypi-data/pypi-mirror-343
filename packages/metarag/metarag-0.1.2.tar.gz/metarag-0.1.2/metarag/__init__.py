from .core import MetaRAG

def simple_query(query: str, docs: list[str]):
    rag = MetaRAG(document_paths=docs)
    return rag.run(query)
