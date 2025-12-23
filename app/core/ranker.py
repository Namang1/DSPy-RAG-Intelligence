import dspy
from typing import List

class EvidenceRanker(dspy.Module):
    """
    Ranks and filters retrieved evidence to select the most relevant chunks.
    """
    def __init__(self):
        super().__init__()
        self.prog = dspy.ChainOfThought("question, contexts -> ranked_contexts")

    def forward(self, question: str, contexts: List[str]):
        # Join contexts with indices for the LM to reference
        context_str = "\n".join([f"[{i}] {ctx}" for i, ctx in enumerate(contexts)])
        
        # The LM should output the list of selected/ranked evidence
        prediction = self.prog(question=question, contexts=context_str)
        
        # In a real scenario, we'd parse the output to select specific indices.
        # For this v1, we'll trust the LM's generated 'ranked_contexts' or just pass through if it's text.
        # Ideally, we want it to return a list of best chunks.
        
        return prediction
