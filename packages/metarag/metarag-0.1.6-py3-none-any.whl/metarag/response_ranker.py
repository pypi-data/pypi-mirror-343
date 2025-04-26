
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class ResponseRanker:
    def __init__(self, embeddings):
        self.embeddings = embeddings

    def score(self, context, responses, top_k=3):
        context_embedding = self.embeddings.embed_query(context)
        scored = []
        for r in responses:
            try:
                resp_embedding = self.embeddings.embed_query(r["response"])
                score = cosine_similarity(
                    np.array(context_embedding).reshape(1, -1),
                    np.array(resp_embedding).reshape(1, -1)
                )[0][0]
            except Exception as e:
                print(f"Error scoring model {r['model']}: {e}")
                score = -1
            scored.append({**r, "score": score})

        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]