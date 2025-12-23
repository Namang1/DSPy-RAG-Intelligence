import json
import os
from typing import Dict, Any
from datetime import datetime

class FeedbackManager:
    """
    Manages human feedback data for DSPy optimization.
    Saves examples to a JSONL file that can be loaded as dspy.Example objects later.
    """
    def __init__(self, filepath: str = "data/feedback.jsonl"):
        self.filepath = filepath
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

    def save_feedback(self, question: str, initial_answer: str, corrected_answer: str, score: int, metadata: Dict[str, Any] = None):
        """
        Saves a feedback entry.
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "initial_answer": initial_answer,
            "corrected_answer": corrected_answer,
            "score": score,
            "metadata": metadata or {}
        }
        
        with open(self.filepath, "a") as f:
            f.write(json.dumps(entry) + "\n")
        
        print(f"Feedback saved to {self.filepath}: Score {score}/10")
            
    def load_examples(self):
        """
        Loads feedback as a list of dicts.
        """
        if not os.path.exists(self.filepath):
            return []
            
        examples = []
        with open(self.filepath, "r") as f:
            for line in f:
                if line.strip():
                    examples.append(json.loads(line))
        return examples
