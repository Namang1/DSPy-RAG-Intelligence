import dspy
from app.infrastructure.milvus_client import MilvusClient
from app.core.query_understanding import QueryUnderstanding
from app.core.retrieval import RetrieveEvidence
from app.core.ranker import EvidenceRanker
from app.core.generation import AnswerGenerator
from app.pipeline.critic_loop import MultiAgentCriticLoop
from app.config import Config

class RAGPipeline(dspy.Module):
    def __init__(self, output_format: str = "text"):
        super().__init__()
        
        # Initialize Milvus
        self.milvus_client = MilvusClient()
        
        # Initialize Modules
        self.understand = QueryUnderstanding()
        self.retrieve = RetrieveEvidence(self.milvus_client, k=10) # Logically retrieve more to rank
        self.rank = EvidenceRanker()
        self.generate = AnswerGenerator(output_format=output_format)
        self.critic_loop = MultiAgentCriticLoop()
        
        # Configure DSPy LM
        # We need to set this up globally or pass it in. For now, setting globally in main.
        
    def forward(self, user_query: str):
        # 1. Understand Query
        understanding = self.understand(user_query=user_query)
        search_query = understanding.search_query
        
        print(f"Original Query: {user_query}")
        print(f"Deep Search Query: {search_query}")
        print(f"Intent: {understanding.intent}")
        
        # 2. Retrieve Evidence
        retrieval = self.retrieve(search_query=search_query)
        raw_context = retrieval.passages
        
        # 3. Rank Evidence
        ranked_res = self.rank(question=user_query, contexts=raw_context)
        # Using the output of the ranker. Assuming ranker returns a list or re-ordered string.
        # For this implementation, we'll assume the ranker returns a prediction that we need to parse 
        # or we just take the top 5 from the context if the ranker just scores them.
        # But 'EvidenceRanker' implementation currently returns a ChainOfThought prediction.
        # We'll use the raw context for now as a fallback if ranker output isn't a clean list, 
        # but ideally we pass 'ranked_res.ranked_contexts'.
        # Let's trust the ranker to give us a good string or list. 
        # For strict typing, we might parse it, but for now let's pass it as context.
        context = [str(ranked_res.ranked_contexts)] 
        
        # 4. Generate Initial Answer
        generation = self.generate(context=context, question=user_query)
        initial_answer = generation.answer
        
        # 5. Critic Loop (Self-Correction)
        # We only run this if the output format is 'text' for now, 
        # as complex struct format might break the critic logic or need a specialized critic.
        # But let's try to run it generally.
        critic_result = self.critic_loop(
            question=user_query,
            context=context,
            initial_answer=initial_answer
        )
        final_answer = critic_result.final_answer
        critic_history = critic_result.history
        
        # If we are in TOON/BAML mode, we might want to re-parse the *final* answer 
        # (since revision might have messed up the format key/values if not instructed well)
        # But for Phase 6, let's assume the reviser keeps the format or we just output text for the loop.
        
        return dspy.Prediction(
            answer=final_answer,
            confidence=generation.confidence, # Keep initial confidence or update?
            context=context,
            understanding=understanding,
            critic_history=critic_history
        )
