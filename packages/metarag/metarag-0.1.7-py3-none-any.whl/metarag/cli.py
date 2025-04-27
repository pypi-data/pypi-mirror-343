import argparse
import os
from dotenv import load_dotenv

# ✅ This ensures .env is loaded before anything else
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=os.path.abspath(env_path))
from metarag import MetaRAG

def main():
    if not os.getenv("GROQ_API_KEY"):
        print("❌ GROQ_API_KEY is missing. Please set it in a .env file or your environment variables.")
        exit(1)

    parser = argparse.ArgumentParser(description="MetaRAG: Multi-LLM RAG with cosine similarity aggregation.")
    parser.add_argument('--pdf', type=str, required=True, help='Path to the PDF file.')
    parser.add_argument('--query', type=str, required=True, help='The query to ask.')

    args = parser.parse_args()

    print("[INFO] Loading MetaRAG...")
    rag = MetaRAG([args.pdf])

    print(f"[INFO] Querying: {args.query}")
    result = rag.query(args.query)

    print("\n=== Aggregated Response ===")
    print(result["aggregated_response"])
