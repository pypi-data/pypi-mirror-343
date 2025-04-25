# oblix/connectors/documents/storage.py
import os
import json
import logging
import pickle
import numpy as np
from typing import Dict, List, Optional, Any, Union, Tuple, Callable
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class BaseVectorStorage(ABC):
    """
    Abstract base class for vector storage implementations.
    
    Vector storage systems store document embeddings and provide
    similarity search functionality for retrieval.
    """
    
    @abstractmethod
    def add_document(self, doc_id: str, embedding: List[float], metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Add a document embedding to the storage.
        
        Args:
            doc_id (str): Unique document identifier
            embedding (List[float]): Document embedding vector
            metadata (Optional[Dict[str, Any]]): Additional document metadata
        """
        pass
        
    @abstractmethod
    def add_documents(self, embeddings: List[Tuple[str, List[float], Dict[str, Any]]]) -> None:
        """
        Add multiple document embeddings to the storage.
        
        Args:
            embeddings (List[Tuple[str, List[float], Dict[str, Any]]]): List of 
                (doc_id, embedding, metadata) tuples
        """
        pass
        
    @abstractmethod
    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar documents.
        
        Args:
            query_embedding (List[float]): Query embedding vector
            top_k (int): Number of results to return
            
        Returns:
            List[Dict[str, Any]]: List of matching documents with scores
        """
        pass
        
    @abstractmethod
    def delete_document(self, doc_id: str) -> bool:
        """
        Delete a document from the storage.
        
        Args:
            doc_id (str): Document identifier to delete
            
        Returns:
            bool: True if document was deleted, False otherwise
        """
        pass
        
    @abstractmethod
    def save(self, file_path: str) -> None:
        """
        Save the vector storage to disk.
        
        Args:
            file_path (str): Path to save the storage
        """
        pass
        
    @abstractmethod
    def load(self, file_path: str) -> None:
        """
        Load the vector storage from disk.
        
        Args:
            file_path (str): Path to load the storage from
        """
        pass

class SimpleVectorStorage(BaseVectorStorage):
    """
    Simple in-memory vector storage with basic similarity search.
    
    This storage implementation keeps all vectors in memory and 
    performs brute-force similarity search. It's suitable for small to
    medium document collections but won't scale to very large datasets.
    """
    
    def __init__(self, embedding_dim: int = 768):
        """
        Initialize the simple vector storage.
        
        Args:
            embedding_dim (int): Dimension of embedding vectors
        """
        self.embedding_dim = embedding_dim
        self.doc_ids = []
        self.embeddings = []
        self.metadata = {}
        
    def add_document(self, doc_id: str, embedding: List[float], metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Add a document embedding to the storage.
        
        Args:
            doc_id (str): Unique document identifier
            embedding (List[float]): Document embedding vector
            metadata (Optional[Dict[str, Any]]): Additional document metadata
        """
        # Ensure embedding is the correct dimension
        if len(embedding) != self.embedding_dim:
            raise ValueError(f"Embedding dimension mismatch. Expected {self.embedding_dim}, got {len(embedding)}")
            
        # Add document
        self.doc_ids.append(doc_id)
        self.embeddings.append(embedding)
        self.metadata[doc_id] = metadata or {}
        
    def add_documents(self, embeddings: List[Tuple[str, List[float], Dict[str, Any]]]) -> None:
        """
        Add multiple document embeddings to the storage.
        
        Args:
            embeddings (List[Tuple[str, List[float], Dict[str, Any]]]): List of 
                (doc_id, embedding, metadata) tuples
        """
        for doc_id, embedding, metadata in embeddings:
            self.add_document(doc_id, embedding, metadata)
            
    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar documents using cosine similarity.
        
        Args:
            query_embedding (List[float]): Query embedding vector
            top_k (int): Number of results to return
            
        Returns:
            List[Dict[str, Any]]: List of matching documents with scores
        """
        if not self.embeddings:
            return []
            
        # Convert to numpy for faster computation
        query_vec = np.array(query_embedding)
        doc_vecs = np.array(self.embeddings)
        
        # Normalize vectors
        query_norm = np.linalg.norm(query_vec)
        if query_norm > 0:
            query_vec = query_vec / query_norm
            
        # Compute cosine similarities
        similarities = []
        for i, doc_vec in enumerate(doc_vecs):
            doc_norm = np.linalg.norm(doc_vec)
            if doc_norm > 0:
                doc_vec = doc_vec / doc_norm
            similarity = np.dot(query_vec, doc_vec)
            similarities.append((similarity, i))
            
        # Sort by similarity (descending)
        similarities.sort(reverse=True)
        
        # Return top-k results
        results = []
        for similarity, idx in similarities[:top_k]:
            doc_id = self.doc_ids[idx]
            results.append({
                "id": doc_id,
                "score": float(similarity),
                "metadata": self.metadata[doc_id]
            })
            
        return results
        
    def delete_document(self, doc_id: str) -> bool:
        """
        Delete a document from the storage.
        
        Args:
            doc_id (str): Document identifier to delete
            
        Returns:
            bool: True if document was deleted, False otherwise
        """
        if doc_id not in self.doc_ids:
            return False
            
        # Find index of document
        idx = self.doc_ids.index(doc_id)
        
        # Remove document
        del self.doc_ids[idx]
        del self.embeddings[idx]
        del self.metadata[doc_id]
        
        return True
        
    def save(self, file_path: str) -> None:
        """
        Save the vector storage to disk.
        
        Args:
            file_path (str): Path to save the storage
        """
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        data = {
            "embedding_dim": self.embedding_dim,
            "doc_ids": self.doc_ids,
            "embeddings": self.embeddings,
            "metadata": self.metadata
        }
        
        with open(file_path, 'wb') as f:
            pickle.dump(data, f)
            
    def load(self, file_path: str) -> None:
        """
        Load the vector storage from disk.
        
        Args:
            file_path (str): Path to load the storage from
        """
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
            
        self.embedding_dim = data["embedding_dim"]
        self.doc_ids = data["doc_ids"]
        self.embeddings = data["embeddings"]
        self.metadata = data["metadata"]
        
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the vector storage.
        
        Returns:
            Dict[str, Any]: Storage statistics
        """
        return {
            "document_count": len(self.doc_ids),
            "embedding_dimension": self.embedding_dim,
            "unique_ids": len(set(self.doc_ids))
        }

class VectorStorage:
    """
    Main vector storage interface with pluggable backends.
    
    This class provides a unified interface for vector storage operations
    and delegates to the configured backend implementation.
    """
    
    def __init__(self, backend: str = "simple", embedding_dim: int = 768, **kwargs):
        """
        Initialize vector storage with specified backend.
        
        Args:
            backend (str): Storage backend to use ('simple', 'faiss', etc.)
            embedding_dim (int): Dimension of embedding vectors
            **kwargs: Backend-specific configuration options
        """
        self.backend_type = backend
        self.embedding_dim = embedding_dim
        
        # Initialize backend
        if backend == "simple":
            self.backend = SimpleVectorStorage(embedding_dim=embedding_dim)
        else:
            try:
                # Dynamically try to load FAISS if requested
                if backend == "faiss":
                    import faiss
                    from .backends.faiss_backend import FaissVectorStorage
                    self.backend = FaissVectorStorage(embedding_dim=embedding_dim, **kwargs)
                else:
                    logger.warning(f"Unknown backend: {backend}, falling back to simple storage")
                    self.backend = SimpleVectorStorage(embedding_dim=embedding_dim)
            except ImportError:
                logger.warning(f"Failed to load backend: {backend}, falling back to simple storage")
                self.backend = SimpleVectorStorage(embedding_dim=embedding_dim)
                
    def add_document(self, doc_id: str, embedding: List[float], metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Add a document embedding to the storage.
        
        Args:
            doc_id (str): Unique document identifier
            embedding (List[float]): Document embedding vector
            metadata (Optional[Dict[str, Any]]): Additional document metadata
        """
        self.backend.add_document(doc_id, embedding, metadata)
        
    def add_documents(self, embeddings: List[Tuple[str, List[float], Dict[str, Any]]]) -> None:
        """
        Add multiple document embeddings to the storage.
        
        Args:
            embeddings (List[Tuple[str, List[float], Dict[str, Any]]]): List of 
                (doc_id, embedding, metadata) tuples
        """
        self.backend.add_documents(embeddings)
        
    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar documents.
        
        Args:
            query_embedding (List[float]): Query embedding vector
            top_k (int): Number of results to return
            
        Returns:
            List[Dict[str, Any]]: List of matching documents with scores
        """
        return self.backend.search(query_embedding, top_k)
        
    def delete_document(self, doc_id: str) -> bool:
        """
        Delete a document from the storage.
        
        Args:
            doc_id (str): Document identifier to delete
            
        Returns:
            bool: True if document was deleted, False otherwise
        """
        return self.backend.delete_document(doc_id)
        
    def save(self, file_path: str) -> None:
        """
        Save the vector storage to disk.
        
        Args:
            file_path (str): Path to save the storage
        """
        self.backend.save(file_path)
        
    def load(self, file_path: str) -> None:
        """
        Load the vector storage from disk.
        
        Args:
            file_path (str): Path to load the storage from
        """
        self.backend.load(file_path)
        
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the vector storage.
        
        Returns:
            Dict[str, Any]: Storage statistics
        """
        if hasattr(self.backend, 'get_stats'):
            return self.backend.get_stats()
        return {"backend": self.backend_type}