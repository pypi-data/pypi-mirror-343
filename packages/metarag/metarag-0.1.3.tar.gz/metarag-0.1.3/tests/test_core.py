from metarag import MetaRAG

def test_basic_query():
    paths = ["VectorDB_Paper.pdf"]
    rag = MetaRAG(paths)
    res = rag.query("What is Vector DB?")
    assert "aggregated_response" in res
    assert isinstance(res["aggregated_response"], str)