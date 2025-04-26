from metarag import MetaRAG

if __name__ == "__main__":
    paths = ["VectorDB_Paper.pdf"]
    rag = MetaRAG(paths)
    result = rag.query("Explain the abstract to a class 10 student in beginner friendly manner")
    print("\nAggregated Response:\n", result["aggregated_response"])