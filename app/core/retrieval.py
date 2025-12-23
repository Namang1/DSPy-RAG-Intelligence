import dspy
from app.infrastructure.milvus_client import MilvusClient
from typing import List, Dict

class RetrieveEvidence(dspy.Module):
    """
    Retrieves evidence from Milvus based on the search query.
    """
    def __init__(self, milvus_client: MilvusClient, k: int = 5):
        super().__init__()
        self.milvus_client = milvus_client
        self.k = k

    def forward(self, search_query: str) -> dspy.Prediction:
        """
        Returns a dspy.Prediction containing a list of 'passages' (dicts with text/source).
        """
        results = self.milvus_client.search(search_query, top_k=self.k)
        
        # Format for DSPy usage
        passages = []
        for res in results:
            passages.append(f"[{res['source']}] {res['text']}")
            
        return dspy.Prediction(passages=passages, raw_results=results)
