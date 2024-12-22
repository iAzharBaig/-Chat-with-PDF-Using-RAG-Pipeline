from typing import List, Dict
import numpy as np
from collections import Counter
import math

class SimpleTfIdf:
    def __init__(self):
        self.vocabulary: Dict[str, int] = {}
        self.idf: Dict[str, float] = {}
        self.n_docs = 0
    
    def _tokenize(self, text: str) -> List[str]:
        # Simple tokenization by splitting on spaces and removing punctuation
        return ''.join(c.lower() if c.isalnum() else ' ' for c in text).split()
    
    def _compute_tf(self, text: str) -> Dict[str, float]:
        tokens = self._tokenize(text)
        count = Counter(tokens)
        # Normalize term frequencies
        total_words = len(tokens)
        return {word: freq/total_words for word, freq in count.items()}
    
    def fit_transform(self, texts: List[str]) -> np.ndarray:
        # Build vocabulary
        all_words = set()
        for text in texts:
            all_words.update(self._tokenize(text))
        self.vocabulary = {word: idx for idx, word in enumerate(sorted(all_words))}
        
        # Compute IDF
        self.n_docs = len(texts)
        doc_freq = Counter()
        for text in texts:
            unique_words = set(self._tokenize(text))
            for word in unique_words:
                doc_freq[word] += 1
        
        self.idf = {word: math.log(self.n_docs / (df + 1)) + 1 
                   for word, df in doc_freq.items()}
        
        return self.transform(texts)
    
    def transform(self, texts: List[str]) -> np.ndarray:
        vectors = np.zeros((len(texts), len(self.vocabulary)))
        for i, text in enumerate(texts):
            tf = self._compute_tf(text)
            for word, tf_val in tf.items():
                if word in self.vocabulary:
                    idx = self.vocabulary[word]
                    vectors[i, idx] = tf_val * self.idf.get(word, 0)
        # Normalize vectors
        norms = np.linalg.norm(vectors, axis=1)
        norms[norms == 0] = 1  # Avoid division by zero
        vectors = vectors / norms[:, np.newaxis]
        return vectors

class EmbeddingModel:
    def __init__(self):
        self.vectorizer = SimpleTfIdf()
        self.is_fitted = False

    def encode(self, texts: List[str]) -> np.ndarray:
        if not texts:
            raise ValueError("Empty text input")
        try:
            if not self.is_fitted:
                vectors = self.vectorizer.fit_transform(texts)
                self.is_fitted = True
            else:
                vectors = self.vectorizer.transform(texts)
            return vectors
        except Exception as e:
            raise Exception(f"Error generating embeddings: {str(e)}")

# Initialize global instance
embedding_model = EmbeddingModel()

def convert_to_embeddings(chunks: List[str]) -> np.ndarray:
    return embedding_model.encode(chunks)