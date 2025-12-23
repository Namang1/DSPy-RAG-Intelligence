from sentence_transformers import SentenceTransformer
from app.config import Config
from typing import List, Union
import numpy as np

class EmbeddingModel:
    def __init__(self, model_name: str = Config.EMBEDDING_MODEL_NAME):
        self.model = SentenceTransformer(model_name)

    def encode(self, texts: Union[str, List[str]]) -> List[List[float]]:
        """
        Generate embeddings for a single string or a list of strings.
        Returns a list of vectors (list of floats).
        """
        if isinstance(texts, str):
            texts = [texts]
            
        embeddings = self.model.encode(texts)
        # Convert numpy array to list of lists for Milvus
        return embeddings.tolist()
    
    @property
    def dimension(self) -> int:
        return self.model.get_sentence_embedding_dimension()
