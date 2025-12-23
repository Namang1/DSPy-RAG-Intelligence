import dspy
from typing import List, Dict, Any
from app.core.parsers.toon_parser import ToonParser
try:
    from baml_client import b
    from baml_client.types import FinalAnswer
except ImportError:
    b = None
    FinalAnswer = None

class AnswerGenerator(dspy.Module):
    """
    Generates an answer based on the user query and retrieved context.
    Supports 'text' (default), 'toon', or 'baml' output formats.
    """
    def __init__(self, output_format: str = "text"):
        super().__init__()
        self.output_format = output_format
        
        if self.output_format == "baml":
            if b is None:
                raise ImportError("BAML client not found. Please run 'baml generate'.")
            # BAML handles the prompt/signature internally via the .baml files
            self.prog = None 
        elif self.output_format == "toon":
            # Signature for TOON structure
            # We define a custom signature class to add a docstring description
            class ToonSignature(dspy.Signature):
                """
                Generate the answer in TOON (Token-Oriented Object Notation) format.
                
                Format Rules:
                - Scalars: key: value
                - Arrays: key[count]: item1, item2
                
                Example:
                answer: DSPy is a framework.
                confidence: 0.95
                sources[2]: dspy_docs, milvus_docs

                IMPORTANT: You MUST use the exact keys: 'answer', 'confidence', and 'sources'.
                """
                context = dspy.InputField()
                question = dspy.InputField()
                answer_toon = dspy.OutputField(desc="The output using ONLY the keys: answer, confidence, sources")

            self.prog = dspy.ChainOfThought(ToonSignature)
        else:
            self.prog = dspy.ChainOfThought("context, question -> answer, confidence")

    def forward(self, context: List[str], question: str):
        # Join context list into a single string for valid input
        context_str = "\n\n".join(context)
        
        if self.output_format == "baml":
            # Call BAML generated function
            # Note: synchronous call for now
            response: FinalAnswer = b.GenerateAnswer(question=question, context=context_str)
            
            # Map BAML typed output to dspy.Prediction
            return dspy.Prediction(
                answer=response.answer,
                confidence=str(response.confidence), # Format string for consistency
                sources=[s.name for s in response.sources],
                raw_baml=response
            )

        if self.output_format == "toon":
            # Prompt engineering to encourage TOON
            dsp_prediction = self.prog(
                context=context_str, 
                question=question
            )
            # Parse TOON
            parsed = ToonParser.parse(dsp_prediction.answer_toon)
            
            # Map back to standard prediction fields
            return dspy.Prediction(
                answer=parsed.get("answer", dsp_prediction.answer_toon),
                confidence=parsed.get("confidence", "0.0"),
                sources=parsed.get("sources", []),
                raw_toon=dsp_prediction.answer_toon
            )
        else:
            return self.prog(context=context_str, question=question)
