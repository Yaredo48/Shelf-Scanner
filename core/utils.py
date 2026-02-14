from sentence_transformers import SentenceTransformer
import numpy as np

# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")  # lightweight model

# Generate embedding for a string (book title + description)
def get_book_embedding(text: str):
    return model.encode(text, normalize_embeddings=True)

# Cosine similarity
def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2)