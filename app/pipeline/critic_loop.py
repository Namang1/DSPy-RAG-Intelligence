import dspy
from app.core.critic import CriticAgent
from app.core.revision import RevisionAgent
from typing import List, Dict

class MultiAgentCriticLoop(dspy.Module):
    def __init__(self, max_iterations: int = 3):
        super().__init__()
        self.max_iterations = max_iterations
        self.critic = CriticAgent()
        self.reviser = RevisionAgent()

    def forward(self, question: str, context: List[str], initial_answer: str):
        current_answer = initial_answer
        history = []
        
        print(f"\n--- Starting Critic Loop (Max {self.max_iterations} iters) ---")
        
        for i in range(self.max_iterations):
            print(f"Iteration {i+1}: Critiquing...")
            
            # 1. Critique
            critique_res = self.critic(question=question, context=context, answer=current_answer)
            
            # Robust score parsing
            import re
            score_match = re.search(r"(\d+(\.\d+)?)", str(critique_res.score))
            score = float(score_match.group(1)) if score_match else 0.0
            
            history.append({
                "iteration": i+1,
                "answer": current_answer,
                "critique": critique_res.critique,
                "score": score,
                "passed": critique_res.passed
            })
            
            print(f"Critique: {critique_res.critique[:100]}...")
            print(f"Score: {score}/10")
            
            # Stop if the critic is happy (score > 8 or passed is True)
            if score >= 9.0 or str(critique_res.passed).lower() == "true":
                print("Critique passed! Stopping loop.")
                break
                
            # 2. Revise
            print("Revising...")
            revision_res = self.reviser(
                question=question, 
                context=context, 
                past_answer=current_answer, 
                critique=critique_res.critique
            )
            current_answer = revision_res.revised_answer
            
        return dspy.Prediction(
            final_answer=current_answer,
            history=history,
            final_score=score
        )
