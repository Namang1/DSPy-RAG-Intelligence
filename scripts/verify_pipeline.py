import dspy
from app.infrastructure.milvus_client import MilvusClient
from app.pipeline.rag_pipeline import RAGPipeline
from app.config import Config
import os

def setup_dspy():
    lm = dspy.LM("openai/gpt-4o-mini", api_key=Config.OPENAI_API_KEY)
    dspy.configure(lm=lm)

def index_sample_data():
    client = MilvusClient()
    
    # Sample Data
    documents = [
        "DSPy is a framework for programming with foundation models. It emphasizes programming over prompting.",
        "Milvus is a high-performance open-source vector database built for scalable similarity search.",
        "Retrieval-Augmented Generation (RAG) combines an information retrieval component with a text generator model.",
        "The self-optimizing system uses a critic loop to improve its own answers over time.",
        "Agency in AI refers to the capacity of an autonomous agent to act in an environment to achieve goals."
    ]
    sources = [
        "dspy_docs", "milvus_docs", "rag_overview", "system_design", "ai_concepts"
    ]
    
    client.insert_documents(documents, sources)

def run_verification():
    setup_dspy()
    
    # Index data first
    print("Indexing sample data...")
    index_sample_data()
    
    # Run Pipeline
    print("\nInitializing RAG Pipeline...")
    rag = RAGPipeline()
    
    query = "What is the core philosophy of DSPy compared to traditional prompting?"
    print(f"\nRunning Query: {query}")
    
    result = rag(user_query=query)
    
    print("\n--- Result ---")
    print(f"Answer: {result.answer}")
    print(f"Confidence: {result.confidence}")
    print("\n--- Evidence Used ---")
    for ctx in result.context:
        print(f"- {ctx}")

    # Verify Critic Loop
    print("\n\nTesting Multi-Agent Critic Loop...")
    from app.pipeline.critic_loop import MultiAgentCriticLoop
    
    critic_loop = MultiAgentCriticLoop(max_iterations=3)
    
    # Introduce a slight error in the answer to see if Critic catches it
    flawed_answer = "DSPy stands for Deep Super Python and it uses magic to prompt models."
    print(f"Initial Flawed Answer: {flawed_answer}")
    
    final_res = critic_loop(
        question=query,
        context=result.context,
        initial_answer=flawed_answer
    )
    
    print("\n--- Final Refined Answer ---")
    print(final_res.final_answer)
    print(f"Final Score: {final_res.final_score}")
    print("\nHistory:")
    for step in final_res.history:
        print(f"Iter {step['iteration']}: Score {step['score']} - {step['critique'][:50]}...")

if __name__ == "__main__":
    run_verification()
