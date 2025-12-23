import dspy
from app.core.generation import AnswerGenerator
from app.config import Config
import os

def check_baml():
    # Setup DSPy (mostly for consistency, BAML uses its own client config)
    lm = dspy.LM("openai/gpt-4o-mini", api_key=Config.OPENAI_API_KEY)
    dspy.configure(lm=lm)
    
    # Initialize Generator with BAML format
    print("Initializing AnswerGenerator with format='baml'...")
    generator = AnswerGenerator(output_format="baml")
    
    context = [
        "DSPy is a framework for programming with foundation models. It emphasizes programming over prompting.",
        "BAML (Better Agentic Markup Language) is a DSL for defining structured LLM outputs.",
        "Milvus is a vector database."
    ]
    question = "How does BAML differ from DSPy in purpose?"
    
    print(f"Question: {question}")
    print("Generating answer using BAML...")
    
    try:
        prediction = generator(context=context, question=question)
        
        print("\n--- Parsed Output (Tyepsafe!) ---")
        print(f"Answer: {prediction.answer}")
        print(f"Confidence: {prediction.confidence}")
        print(f"Sources: {prediction.sources}")
        
    except Exception as e:
        print(f"Error executing BAML generation: {e}")

if __name__ == "__main__":
    check_baml()
