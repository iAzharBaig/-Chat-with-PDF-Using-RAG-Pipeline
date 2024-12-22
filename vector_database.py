from typing import List, Dict, Any
import numpy as np
from embedding import embedding_model

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0
    return np.dot(a, b) / (norm_a * norm_b)

class VectorDatabase:
    def __init__(self):
        self.vector_database: List[Dict[str, Any]] = []
        self.is_initialized = False

    def store_embeddings(self, chunks: List[str], embeddings: np.ndarray) -> None:
        if not chunks or not embeddings.size:
            raise ValueError("Empty chunks or embeddings")
        if len(chunks) != len(embeddings):
            raise ValueError("Chunks and embeddings must have same length")
            
        for chunk, embedding in zip(chunks, embeddings):
            self.vector_database.append({
                'chunk': chunk,
                'embedding': embedding
            })
        self.is_initialized = True

    def similarity_search(self, query: str, top_k: int = 5) -> List[str]:
        if not self.is_initialized:
            raise RuntimeError("Vector database not initialized")
            
        try:
            query_embedding = embedding_model.encode([query])[0]
            similarities = []
            
            for entry in self.vector_database:
                similarity = cosine_similarity(query_embedding, entry['embedding'])
                similarities.append((similarity, entry['chunk']))
                
            similarities.sort(reverse=True, key=lambda x: x[0])
            return [chunk for _, chunk in similarities[:top_k]]
        except Exception as e:
            raise Exception(f"Error in similarity search: {str(e)}")

# Initialize global instance
vector_db = VectorDatabase()

def store_embeddings(chunks: List[str], embeddings: np.ndarray) -> None:
    vector_db.store_embeddings(chunks, embeddings)

def similarity_search(query: str, top_k: int = 5) -> List[str]:
    return vector_db.similarity_search(query, top_k)