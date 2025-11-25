"""
Memory Graph module for LifeUnity AI Cognitive Twin System.
Manages cognitive memory using embeddings and graph relationships.
"""

import json
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from pathlib import Path
import networkx as nx
import streamlit as st

from app.utils.embedder import get_embedder
from app.utils.logger import get_logger
from app.utils.preprocess import clean_text

logger = get_logger("MemoryGraph")


class MemoryGraph:
    """Memory graph manager using embeddings and graph structure."""
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize memory graph.
        
        Args:
            data_dir: Directory to store memory data
        """
        self.data_dir = Path(data_dir)
        self._storage_available = False
        try:
            self.data_dir.mkdir(exist_ok=True)
            self._storage_available = True
        except (OSError, PermissionError):
            # Storage not available (e.g., on Streamlit Cloud)
            logger.warning("Data directory not writable. Memory persistence disabled.")
        
        self.memory_file = self.data_dir / "memory_graph.json"
        self.embedder = get_embedder()
        self.graph = nx.Graph()
        
        self.memories = self._load_memories()
        self._build_graph()
        
        logger.info("MemoryGraph initialized")
    
    def _load_memories(self) -> List[Dict]:
        """Load memories from file."""
        if not self._storage_available:
            return []
        try:
            if self.memory_file.exists():
                with open(self.memory_file, 'r') as f:
                    memories = json.load(f)
                logger.info(f"Loaded {len(memories)} memories")
                return memories
            else:
                return []
        except Exception as e:
            logger.error(f"Error loading memories: {str(e)}", exc_info=True)
            return []
    
    def _save_memories(self):
        """Save memories to file."""
        if not self._storage_available:
            logger.debug("Storage not available, skipping memory save")
            return
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.memories, f, indent=2)
            logger.debug(f"Saved {len(self.memories)} memories")
        except Exception as e:
            logger.error(f"Error saving memories: {str(e)}", exc_info=True)
    
    def _build_graph(self):
        """Build graph from memories."""
        self.graph.clear()
        
        for memory in self.memories:
            memory_id = memory['id']
            self.graph.add_node(
                memory_id,
                content=memory['content'],
                timestamp=memory['timestamp'],
                tags=memory.get('tags', [])
            )
        
        # Add edges based on similarity
        if len(self.memories) > 1:
            self._connect_similar_memories()
    
    def _connect_similar_memories(self, threshold: float = 0.7):
        """
        Connect similar memories with edges.
        
        Args:
            threshold: Similarity threshold for creating edges
        """
        try:
            # Get all memory contents and embeddings
            contents = [m['content'] for m in self.memories]
            embeddings = self.embedder.embed_text(contents)
            
            # Compute pairwise similarities
            for i in range(len(self.memories)):
                for j in range(i + 1, len(self.memories)):
                    # Compute cosine similarity
                    similarity = np.dot(embeddings[i], embeddings[j]) / (
                        np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[j])
                    )
                    
                    if similarity >= threshold:
                        self.graph.add_edge(
                            self.memories[i]['id'],
                            self.memories[j]['id'],
                            weight=float(similarity)
                        )
            
            logger.debug(f"Connected memories with {self.graph.number_of_edges()} edges")
            
        except Exception as e:
            logger.error(f"Error connecting memories: {str(e)}", exc_info=True)
    
    def add_memory(
        self,
        content: str,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict] = None
    ) -> int:
        """
        Add a new memory to the graph.
        
        Args:
            content: Memory content
            tags: Optional tags
            metadata: Optional metadata
            
        Returns:
            Memory ID
        """
        content = clean_text(content)
        
        if not content:
            logger.warning("Cannot add empty memory")
            return -1
        
        try:
            # Generate embedding
            embedding = self.embedder.embed_text(content)[0]
            
            # Create memory record
            memory_id = len(self.memories) + 1
            memory = {
                'id': memory_id,
                'content': content,
                'embedding': embedding.tolist(),
                'timestamp': datetime.now().isoformat(),
                'tags': tags or [],
                'metadata': metadata or {}
            }
            
            self.memories.append(memory)
            self._save_memories()
            
            # Add to graph
            self.graph.add_node(
                memory_id,
                content=content,
                timestamp=memory['timestamp'],
                tags=tags or []
            )
            
            # Connect to similar memories
            self._connect_new_memory(memory_id, embedding)
            
            logger.info(f"Added memory ID: {memory_id}")
            return memory_id
            
        except Exception as e:
            logger.error(f"Error adding memory: {str(e)}", exc_info=True)
            return -1
    
    def _connect_new_memory(self, memory_id: int, embedding: np.ndarray, threshold: float = 0.7):
        """
        Connect a new memory to similar existing memories.
        
        Args:
            memory_id: ID of the new memory
            embedding: Embedding of the new memory
            threshold: Similarity threshold
        """
        try:
            for memory in self.memories[:-1]:  # Exclude the new memory itself
                other_embedding = np.array(memory['embedding'])
                
                # Compute cosine similarity
                similarity = np.dot(embedding, other_embedding) / (
                    np.linalg.norm(embedding) * np.linalg.norm(other_embedding)
                )
                
                if similarity >= threshold:
                    self.graph.add_edge(
                        memory_id,
                        memory['id'],
                        weight=float(similarity)
                    )
        
        except Exception as e:
            logger.error(f"Error connecting new memory: {str(e)}", exc_info=True)
    
    def search_memories(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Search for memories similar to a query.
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of similar memories
        """
        if not self.memories:
            return []
        
        try:
            # Embed query
            query_embedding = self.embedder.embed_text(query)[0]
            
            # Compute similarities
            similarities = []
            for memory in self.memories:
                memory_embedding = np.array(memory['embedding'])
                similarity = np.dot(query_embedding, memory_embedding) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(memory_embedding)
                )
                
                similarities.append({
                    'id': memory['id'],
                    'content': memory['content'],
                    'similarity': float(similarity),
                    'timestamp': memory['timestamp'],
                    'tags': memory.get('tags', [])
                })
            
            # Sort by similarity
            similarities.sort(key=lambda x: x['similarity'], reverse=True)
            
            return similarities[:top_k]
            
        except Exception as e:
            logger.error(f"Error searching memories: {str(e)}", exc_info=True)
            return []
    
    def get_related_memories(self, memory_id: int, max_depth: int = 2) -> List[int]:
        """
        Get memories related to a specific memory.
        
        Args:
            memory_id: ID of the memory
            max_depth: Maximum depth for graph traversal
            
        Returns:
            List of related memory IDs
        """
        try:
            if memory_id not in self.graph:
                return []
            
            # Use BFS to find related memories
            related = []
            visited = set()
            queue = [(memory_id, 0)]
            
            while queue:
                current_id, depth = queue.pop(0)
                
                if current_id in visited or depth > max_depth:
                    continue
                
                visited.add(current_id)
                
                if current_id != memory_id:
                    related.append(current_id)
                
                # Add neighbors
                for neighbor in self.graph.neighbors(current_id):
                    if neighbor not in visited:
                        queue.append((neighbor, depth + 1))
            
            return related
            
        except Exception as e:
            logger.error(f"Error getting related memories: {str(e)}", exc_info=True)
            return []
    
    def get_memory_clusters(self) -> List[List[int]]:
        """
        Get clusters of related memories.
        
        Returns:
            List of memory clusters (each cluster is a list of memory IDs)
        """
        try:
            if self.graph.number_of_nodes() == 0:
                return []
            
            # Find connected components
            components = list(nx.connected_components(self.graph))
            
            return [list(component) for component in components]
            
        except Exception as e:
            logger.error(f"Error getting memory clusters: {str(e)}", exc_info=True)
            return []
    
    def get_graph_stats(self) -> Dict:
        """
        Get statistics about the memory graph.
        
        Returns:
            Dictionary with graph statistics
        """
        return {
            'total_memories': len(self.memories),
            'total_connections': self.graph.number_of_edges(),
            'num_clusters': len(self.get_memory_clusters()),
            'avg_connections': (
                2 * self.graph.number_of_edges() / self.graph.number_of_nodes()
                if self.graph.number_of_nodes() > 0 else 0
            )
        }
    
    def get_all_memories(self) -> List[Dict]:
        """Get all memories."""
        return self.memories
    
    def delete_memory(self, memory_id: int) -> bool:
        """
        Delete a memory.
        
        Args:
            memory_id: ID of memory to delete
            
        Returns:
            True if deleted, False otherwise
        """
        try:
            # Remove from memories list
            self.memories = [m for m in self.memories if m['id'] != memory_id]
            
            # Remove from graph
            if memory_id in self.graph:
                self.graph.remove_node(memory_id)
            
            self._save_memories()
            logger.info(f"Deleted memory ID: {memory_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting memory: {str(e)}", exc_info=True)
            return False


# Global memory graph instance
_memory_graph = None


@st.cache_resource
def get_memory_graph() -> MemoryGraph:
    """
    Get or create a cached memory graph instance.
    
    Returns:
        MemoryGraph instance
    """
    return MemoryGraph()
