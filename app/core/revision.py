import dspy
from typing import List

class RevisionAgent(dspy.Module):
    """
    Refines the answer based on the critic's feedback.
    """
    def __init__(self):
        super().__init__()
        self.prog = dspy.ChainOfThought("question, context, past_answer, critique -> revised_answer")

    def forward(self, question: str, context: List[str], past_answer: str, critique: str):
        context_str = "\n\n".join(context)
        return self.prog(
            question=question,
            context=context_str,
            past_answer=past_answer,
            critique=critique
        )
