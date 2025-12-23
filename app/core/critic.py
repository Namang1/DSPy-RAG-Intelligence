import dspy
from typing import List

class CriticAgent(dspy.Module):
    """
    Analyzes the answer for logical fallacies, contradictions, and missing information.
    """
    def __init__(self):
        super().__init__()
        self.prog = dspy.ChainOfThought("question, context, answer -> critique, score, passed")

    def forward(self, question: str, context: List[str], answer: str):
        context_str = "\n\n".join(context)
        return self.prog(question=question, context=context_str, answer=answer)
