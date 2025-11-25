"""
Embedding utilities for LifeUnity AI Cognitive Twin System.
Provides text embedding functionality using Sentence-BERT or TfidfVectorizer fallback.
"""

import hashlib
import os
import numpy as np
from typing import List, Union, Tuple
import streamlit as st

# Disable TensorFlow imports to prevent compatibility issues on Python 3.13.
# These environment variables only affect the transformers/sentence-transformers
# library behavior and do not impact other parts of the application.
# - USE_TORCH: Forces transformers to use PyTorch instead of TensorFlow
# - TRANSFORMERS_NO_TF: Disables TensorFlow-specific imports in transformers
os.environ.setdefault('USE_TORCH', '1')
os.environ.setdefault('TRANSFORMERS_NO_TF', '1')

from utils.logger import get_logger

logger = get_logger("Embedder")

# Flag for availability - always True with fallback (no warnings)
SENTENCE_TRANSFORMERS_AVAILABLE = True

# Try to import ML libraries
_SENTENCE_TRANSFORMERS_LOADED = False
_SKLEARN_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer
    _SENTENCE_TRANSFORMERS_LOADED = True
    logger.info("Sentence-Transformers loaded successfully")
except ImportError:
    logger.info("Sentence-Transformers not available (not installed), using TF-IDF fallback")
except ValueError:
    # ValueError: TensorFlow compatibility issues (e.g., on Python 3.13)
    logger.info("Sentence-Transformers not available (TensorFlow compatibility error), using TF-IDF fallback")

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.decomposition import TruncatedSVD
    _SKLEARN_AVAILABLE = True
except ImportError:
    logger.info("Scikit-learn not available for TF-IDF fallback")


class TfidfEmbedder:
    """
    TF-IDF based text embedder as fallback when Sentence-Transformers not available.
    Produces consistent, deterministic embeddings that support similarity search.
    """
    
    def __init__(self, embedding_dim: int = 384):
        """
        Initialize TF-IDF embedder.
        
        Args:
            embedding_dim: Target embedding dimension
        """
        self.embedding_dim = embedding_dim
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            stop_words='english',
            lowercase=True
        )
        self.svd = TruncatedSVD(n_components=min(embedding_dim, 100))
        self.is_fitted = False
        self.corpus = []
        
    def _create_base_embedding(self, text: str) -> np.ndarray:
        """
        Create a base embedding using character-level features.
        This ensures we always get valid embeddings even for new texts.
        
        Args:
            text: Input text
            
        Returns:
            Base embedding vector
        """
        # Create deterministic embedding based on text characteristics
        text_lower = text.lower()
        
        # Character frequency features
        char_freq = np.zeros(26)
        for char in text_lower:
            if 'a' <= char <= 'z':
                char_freq[ord(char) - ord('a')] += 1
        
        # Normalize
        if np.sum(char_freq) > 0:
            char_freq = char_freq / np.sum(char_freq)
        
        # Word-level features
        words = text_lower.split()
        word_count = len(words)
        avg_word_len = np.mean([len(w) for w in words]) if words else 0
        
        # Extend to target dimension using repetition and variation
        base = np.concatenate([
            char_freq,  # 26 dims
            [word_count / 100, avg_word_len / 10],  # 2 dims
        ])
        
        # Extend to full dimension
        extended = np.zeros(self.embedding_dim)
        for i in range(self.embedding_dim):
            idx = i % len(base)
            # Add variation based on position
            extended[i] = base[idx] * (1 + 0.1 * np.sin(i * 0.1))
        
        # Normalize
        norm = np.linalg.norm(extended)
        if norm > 0:
            extended = extended / norm
        
        return extended.astype(np.float32)
    
    def fit(self, texts: List[str]):
        """
        Fit the TF-IDF vectorizer on a corpus.
        
        Args:
            texts: List of texts to fit on
        """
        if not texts:
            return
        
        self.corpus.extend(texts)
        
        try:
            # Fit TF-IDF
            tfidf_matrix = self.vectorizer.fit_transform(self.corpus)
            
            # Fit SVD for dimensionality reduction
            n_components = min(self.svd.n_components, tfidf_matrix.shape[1] - 1, tfidf_matrix.shape[0] - 1)
            if n_components > 0:
                self.svd.n_components = n_components
                self.svd.fit(tfidf_matrix)
                self.is_fitted = True
        except Exception as e:
            logger.debug(f"TF-IDF fitting error: {e}")
            self.is_fitted = False
    
    def embed(self, texts: Union[str, List[str]]) -> np.ndarray:
        """
        Generate embeddings for texts.
        
        Args:
            texts: Single text or list of texts
            
        Returns:
            Embeddings array
        """
        if isinstance(texts, str):
            texts = [texts]
        
        embeddings = []
        
        for text in texts:
            # Add to corpus for future fitting
            if text not in self.corpus:
                self.corpus.append(text)
            
            if self.is_fitted:
                try:
                    # Transform using fitted TF-IDF
                    tfidf_vec = self.vectorizer.transform([text])
                    # Apply SVD
                    reduced = self.svd.transform(tfidf_vec)[0]
                    # Pad to target dimension
                    embedding = np.zeros(self.embedding_dim)
                    embedding[:len(reduced)] = reduced
                    # Normalize
                    norm = np.linalg.norm(embedding)
                    if norm > 0:
                        embedding = embedding / norm
                    embeddings.append(embedding.astype(np.float32))
                except Exception:
                    # Fallback to base embedding
                    embeddings.append(self._create_base_embedding(text))
            else:
                # Use base embedding
                embeddings.append(self._create_base_embedding(text))
        
        return np.array(embeddings)


class TextEmbedder:
    """Text embedding handler using Sentence-BERT or TF-IDF fallback."""
    
    # Default embedding dimension
    DEFAULT_EMBEDDING_DIM = 384
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize the text embedder.
        
        Args:
            model_name: Name of the sentence-transformers model
        """
        self.model_name = model_name
        self.model = None
        self.embedding_dim = self.DEFAULT_EMBEDDING_DIM
        self.use_sentence_transformers = _SENTENCE_TRANSFORMERS_LOADED
        self.tfidf_embedder = None
        
        if not self.use_sentence_transformers:
            if _SKLEARN_AVAILABLE:
                self.tfidf_embedder = TfidfEmbedder(self.embedding_dim)
                logger.info("Using TF-IDF embeddings (sklearn fallback)")
            else:
                logger.info("Using simple character-based embeddings")
    
    def _normalize_text_input(self, text: Union[str, List[str]]) -> Tuple[List[str], bool]:
        """
        Normalize text input to always be a list.
        
        Args:
            text: Single text string or list of text strings
            
        Returns:
            Tuple of (text_list, is_single_input)
        """
        is_single = isinstance(text, str)
        text_list = [text] if is_single else text
        return text_list, is_single
    
    def _format_embeddings_output(self, embeddings: np.ndarray, is_single: bool) -> np.ndarray:
        """
        Format embeddings output based on input type.
        
        Args:
            embeddings: Array of embeddings
            is_single: Whether the original input was a single text
            
        Returns:
            Formatted embeddings
        """
        return embeddings[0] if is_single else embeddings
    
    def _simple_embedding(self, text: str) -> np.ndarray:
        """
        Create a simple deterministic embedding when no ML libraries available.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        # Use hash for deterministic pseudo-random embedding
        text_hash = hashlib.sha256(text.encode()).hexdigest()
        seed = int(text_hash[:16], 16)
        rng = np.random.default_rng(seed)
        
        embedding = rng.standard_normal(self.embedding_dim)
        embedding = embedding / np.linalg.norm(embedding)
        
        return embedding.astype(np.float32)
    
    @st.cache_resource
    def _load_sentence_transformer(_self, model_name: str):
        """Load sentence transformer model with caching."""
        if not _SENTENCE_TRANSFORMERS_LOADED:
            return None
        
        try:
            model = SentenceTransformer(model_name)
            logger.info(f"Loaded sentence transformer model: {model_name}")
            return model
        except Exception as e:
            logger.info(f"Could not load sentence transformer: {e}")
            return None
    
    def load_model(self):
        """Load the sentence transformer model."""
        if not self.use_sentence_transformers:
            return
            
        if self.model is None:
            self.model = self._load_sentence_transformer(self.model_name)
            if self.model is not None:
                self.embedding_dim = self.model.get_sentence_embedding_dimension()
            else:
                self.use_sentence_transformers = False
                if _SKLEARN_AVAILABLE:
                    self.tfidf_embedder = TfidfEmbedder(self.embedding_dim)
    
    def embed_text(self, text: Union[str, List[str]]) -> np.ndarray:
        """
        Generate embeddings for text.
        
        Args:
            text: Single text string or list of text strings
            
        Returns:
            Numpy array of embeddings
        """
        text_list, is_single = self._normalize_text_input(text)
        
        # Try sentence transformers first
        if self.use_sentence_transformers:
            if self.model is None:
                self.load_model()
            
            if self.model is not None:
                try:
                    embeddings = self.model.encode(
                        text_list,
                        convert_to_numpy=True,
                        show_progress_bar=False
                    )
                    logger.debug(f"Generated embeddings for {len(text_list)} texts")
                    return self._format_embeddings_output(embeddings, is_single)
                except Exception as e:
                    logger.debug(f"Sentence transformer error: {e}")
        
        # TF-IDF fallback
        if self.tfidf_embedder is not None:
            embeddings = self.tfidf_embedder.embed(text_list)
            logger.debug(f"Generated TF-IDF embeddings for {len(text_list)} texts")
            return self._format_embeddings_output(embeddings, is_single)
        
        # Simple fallback
        embeddings = np.array([self._simple_embedding(t) for t in text_list])
        logger.debug(f"Generated simple embeddings for {len(text_list)} texts")
        return self._format_embeddings_output(embeddings, is_single)
    
    def compute_similarity(self, text1: str, text2: str) -> float:
        """
        Compute cosine similarity between two texts.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score (-1 to 1)
        """
        try:
            embeddings = self.embed_text([text1, text2])
            
            similarity = np.dot(embeddings[0], embeddings[1]) / (
                np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
            )
            
            return float(similarity)
            
        except Exception as e:
            logger.error(f"Error computing similarity: {str(e)}")
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
            query_embedding = self.embed_text(query)
            candidate_embeddings = self.embed_text(candidates)
            
            similarities = []
            for idx, candidate_emb in enumerate(candidate_embeddings):
                similarity = np.dot(query_embedding, candidate_emb) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(candidate_emb)
                )
                similarities.append((idx, candidates[idx], float(similarity)))
            
            similarities.sort(key=lambda x: x[2], reverse=True)
            
            return similarities[:top_k]
            
        except Exception as e:
            logger.error(f"Error finding similar texts: {str(e)}")
            return []


# Global embedder instance
_embedder = None


@st.cache_resource
def get_embedder(model_name: str = 'all-MiniLM-L6-v2') -> TextEmbedder:
    """
    Get or create a cached embedder instance.
    
    Args:
        model_name: Name of the sentence-transformers model
        
    Returns:
        TextEmbedder instance
    """
    return TextEmbedder(model_name)
