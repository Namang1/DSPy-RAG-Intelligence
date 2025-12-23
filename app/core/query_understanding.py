import dspy

class QueryUnderstanding(dspy.Module):
    """
    Interprets user queries to extract intent, entities, and rewrite for better retrieval.
    """
    def __init__(self):
        super().__init__()
        self.prog = dspy.ChainOfThought("user_query -> search_query, intent, entities")

    def forward(self, user_query: str):
        return self.prog(user_query=user_query)
