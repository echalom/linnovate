from transformers import pipeline
import numpy as np

class LLMClient:
    def __init__(self):
        self.pipeline = pipeline("feature-extraction", model="sentence-transformers/all-MiniLM-L6-v2")

    def generate_embedding(self, text):
        embedding = self.pipeline(text)
        return np.mean(embedding[0], axis=0)

    def generate_summary(self, text):
        return f"Summary: {text[:100]}..."
