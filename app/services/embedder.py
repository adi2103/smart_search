from abc import ABC, abstractmethod
from sentence_transformers import SentenceTransformer
import numpy as np

class Embedder(ABC):
    @abstractmethod
    def encode(self, text: str) -> np.ndarray:
        pass

class LocalEmbedder(Embedder):
    def __init__(self):
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    
    def encode(self, text: str) -> np.ndarray:
        return self.model.encode(text, normalize_embeddings=True)

def get_embedder(provider: str = "local") -> Embedder:
    if provider == "local":
        return LocalEmbedder()
    raise ValueError(f"Unknown embedder provider: {provider}")
