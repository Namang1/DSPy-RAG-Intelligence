import dspy
from app.core.parsers.toon_parser import ToonParser
from app.core.generation import AnswerGenerator
from app.config import Config
import os

def check_toon():
    # Setup DSPy
    lm = dspy.LM("openai/gpt-4o-mini", api_key=Config.OPENAI_API_KEY)
    dspy.configure(lm=lm)
    
    # Initialize Generator with TOON format
    generator = AnswerGenerator(output_format="toon")
    
    context = [
        "DSPy is a framework for programming with foundation models. It emphasizes programming over prompting.",
        "TOON (Token-Oriented Object Notation) is a compact format for LLM output."
    ]
    question = "What is the relationship between DSPy and TOON?"
    
    print(f"Question: {question}")
    print("Generating answer in TOON format...")
    
    # This might fail if the model doesn't know TOON or if we didn't give examples.
    # In a real DSPy optimization, we would bootstrap this.
    # For now, we rely on the model's ability to follow implicit instructions or we might need to add a signature/instruction.
    # NOTE: The current AnswerGenerator implementation just changes the output field name to 'answer_toon'. 
    # Validating if the model actually outputs legitimate TOON might require a more descriptive signature docstring or few-shot examples.
    
    prediction = generator(context=context, question=question)
    
    print("\n--- Raw Output ---")
    print(prediction.raw_toon)
    
    print("\n--- Parsed Output ---")
    print(f"Answer: {prediction.answer}")
    print(f"Confidence: {prediction.confidence}")
    print(f"Sources: {prediction.sources}")

if __name__ == "__main__":
    check_toon()
