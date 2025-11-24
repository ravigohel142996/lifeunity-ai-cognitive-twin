"""
Embedding utilities for LifeUnity AI Cognitive Twin System.
Provides text embedding functionality using Sentence-BERT.
"""

import numpy as np
from typing import List, Union
from app.utils.logger import get_logger

logger = get_logger("Embedder")

# Try to import ML libraries, handle gracefully if not available
try:
    from sentence_transformers import SentenceTransformer
    import torch
    SENTENCE_TRANSFORMERS_AVAILABLE = True
    logger.info("Sentence-Transformers loaded successfully")
except ImportError as e:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    logger.warning(f"Sentence-Transformers not available: {e}. Using simple fallback embeddings.")


class TextEmbedder:
    """Text embedding handler using Sentence-BERT or simple fallback."""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize the text embedder.
        
        Args:
            model_name: Name of the sentence-transformers model
        """
        self.model_name = model_name
        self.model = None
        self.embedding_dim = None
        self.use_simple_embeddings = not SENTENCE_TRANSFORMERS_AVAILABLE
        if self.use_simple_embeddings:
            self.embedding_dim = 384  # Match standard model size
            logger.info("Using simple hash-based embeddings (fallback mode)")
        else:
            logger.info(f"Initializing TextEmbedder with model: {model_name}")
    
    def _simple_hash_embedding(self, text: str) -> np.ndarray:
        """
        Create a simple hash-based embedding for demo purposes.
        This is a fallback when sentence-transformers is not available.
        
        Args:
            text: Text to embed
            
        Returns:
            Numpy array embedding
        """
        import hashlib
        # Use hash of text to generate pseudo-random but deterministic embedding
        text_hash = hashlib.md5(text.encode()).hexdigest()
        # Convert hex to numbers
        seed = int(text_hash[:8], 16)
        np.random.seed(seed)
        # Generate random embedding
        embedding = np.random.randn(self.embedding_dim)
        # Normalize
        embedding = embedding / np.linalg.norm(embedding)
        return embedding.astype(np.float32)
    
    def load_model(self):
        """Load the sentence transformer model."""
        if self.use_simple_embeddings:
            logger.info("Using simple embeddings (fallback mode)")
            return
            
        try:
            if self.model is None:
                logger.info(f"Loading model: {self.model_name}")
                self.model = SentenceTransformer(self.model_name)
                # Get embedding dimension
                self.embedding_dim = self.model.get_sentence_embedding_dimension()
                logger.info(f"Model loaded successfully. Embedding dim: {self.embedding_dim}")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}", exc_info=True)
            logger.warning("Falling back to simple embeddings")
            self.use_simple_embeddings = True
            self.embedding_dim = 384
    
    def embed_text(self, text: Union[str, List[str]]) -> np.ndarray:
        """
        Generate embeddings for text.
        
        Args:
            text: Single text string or list of text strings
            
        Returns:
            Numpy array of embeddings
        """
        # Handle single string
        is_single = isinstance(text, str)
        if is_single:
            text = [text]
        
        # Use simple embeddings if sentence-transformers not available
        if self.use_simple_embeddings:
            embeddings = np.array([self._simple_hash_embedding(t) for t in text])
            logger.debug(f"Generated simple embeddings for {len(text)} texts")
            return embeddings[0] if is_single else embeddings
        
        # Load model if not loaded
        if self.model is None:
            self.load_model()
        
        try:
            # Generate embeddings using sentence-transformers
            embeddings = self.model.encode(
                text,
                convert_to_numpy=True,
                show_progress_bar=False
            )
            
            logger.debug(f"Generated embeddings for {len(text)} texts")
            return embeddings
            
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}", exc_info=True)
            # Fallback to simple embeddings
            logger.warning("Falling back to simple embeddings")
            embeddings = np.array([self._simple_hash_embedding(t) for t in text])
            return embeddings[0] if is_single else embeddings
    
    def compute_similarity(self, text1: str, text2: str) -> float:
        """
        Compute cosine similarity between two texts.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score (0-1)
        """
        try:
            embeddings = self.embed_text([text1, text2])
            
            # Compute cosine similarity
            similarity = np.dot(embeddings[0], embeddings[1]) / (
                np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
            )
            
            return float(similarity)
            
        except Exception as e:
            logger.error(f"Error computing similarity: {str(e)}", exc_info=True)
            return 0.0
    
    def find_most_similar(
        self,
        query: str,
        candidates: List[str],
        top_k: int = 5
    ) -> List[tuple]:
        """
        Find most similar texts to a query.
        
        Args:
            query: Query text
            candidates: List of candidate texts
            top_k: Number of top results to return
            
        Returns:
            List of (index, text, similarity_score) tuples
        """
        try:
            # Embed query and candidates
            query_embedding = self.embed_text(query)
            candidate_embeddings = self.embed_text(candidates)
            
            # Compute similarities
            similarities = []
            for idx, candidate_emb in enumerate(candidate_embeddings):
                similarity = np.dot(query_embedding[0], candidate_emb) / (
                    np.linalg.norm(query_embedding[0]) * np.linalg.norm(candidate_emb)
                )
                similarities.append((idx, candidates[idx], float(similarity)))
            
            # Sort by similarity (descending)
            similarities.sort(key=lambda x: x[2], reverse=True)
            
            return similarities[:top_k]
            
        except Exception as e:
            logger.error(f"Error finding similar texts: {str(e)}", exc_info=True)
            return []


# Global embedder instance
_embedder = None


def get_embedder(model_name: str = 'all-MiniLM-L6-v2') -> TextEmbedder:
    """
    Get or create a global embedder instance.
    
    Args:
        model_name: Name of the sentence-transformers model
        
    Returns:
        TextEmbedder instance
    """
    global _embedder
    if _embedder is None:
        _embedder = TextEmbedder(model_name)
    return _embedder
