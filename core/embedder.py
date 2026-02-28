import os
from sentence_transformers import SentenceTransformer

class Embedder:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Embedder, cls).__new__(cls)
            # Load the all-MiniLM-L6-v2 model (Dimension 384)
            cls._instance.model = SentenceTransformer('all-MiniLM-L6-v2')
        return cls._instance

    def embed(self, texts):
        """
        Generates embeddings for a list of strings or a single string.
        """
        return self.model.encode(texts)
