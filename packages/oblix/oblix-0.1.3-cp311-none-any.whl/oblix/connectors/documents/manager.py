# oblix/connectors/documents/manager.py
import os
import json
import uuid
import logging
import asyncio
from typing import Dict, List, Optional, Any, Union, Tuple, Set
from dataclasses import dataclass, field, asdict

from .processors import DocumentProcessor, TextChunker
from .storage import VectorStorage
from ...models.base import ModelType, EmbeddingModelType, BaseEmbeddingModel

logger = logging.getLogger(__name__)

@dataclass
class Document:
    """
    Represents a document with metadata and chunks.
    
    Attributes:
        id (str): Unique document identifier
        name (str): Document name
        source_path (str): Original document path
        chunks (List[str]): Text chunks from the document
        metadata (Dict[str, Any]): Additional document metadata
        embedding_status (str): Status of embedding process ('pending', 'complete', 'failed')
        workspaces (Set[str]): Set of workspace IDs this document belongs to
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    source_path: str = ""
    chunks: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    embedding_status: str = "pending"
    workspaces: Set[str] = field(default_factory=set)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        result = asdict(self)
        # Convert set to list for JSON serialization
        result['workspaces'] = list(self.workspaces)
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Document':
        """Create from dictionary after deserialization."""
        # Convert workspaces list back to set
        if 'workspaces' in data and isinstance(data['workspaces'], list):
            data['workspaces'] = set(data['workspaces'])
        return cls(**data)

@dataclass
class Workspace:
    """
    Represents a workspace containing documents.
    
    Attributes:
        id (str): Unique workspace identifier
        name (str): Workspace name
        description (str): Workspace description
        document_ids (Set[str]): Set of document IDs in this workspace
        metadata (Dict[str, Any]): Additional workspace metadata
        vector_store_path (str): Path to vector store file for this workspace
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    document_ids: Set[str] = field(default_factory=set)
    metadata: Dict[str, Any] = field(default_factory=dict)
    vector_store_path: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        result = asdict(self)
        # Convert set to list for JSON serialization
        result['document_ids'] = list(self.document_ids)
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Workspace':
        """Create from dictionary after deserialization."""
        # Convert document_ids list back to set
        if 'document_ids' in data and isinstance(data['document_ids'], list):
            data['document_ids'] = set(data['document_ids'])
        return cls(**data)

class DocumentManager:
    """
    Manages documents, workspaces, and vector embeddings.
    
    This class provides methods for:
    - Uploading and processing documents
    - Creating and managing workspaces
    - Embedding document chunks
    - Retrieving relevant document chunks for queries
    
    The DocumentManager integrates with SessionManager to enable
    document-grounded conversations.
    """
    
    def __init__(self, base_dir: Optional[str] = None):
        """
        Initialize document manager.
        
        Args:
            base_dir (Optional[str]): Base directory for storing documents and embeddings
        """
        # Ensure os module is available within this method
        import os
        
        # Use a default directory if not specified
        if base_dir is None:
            base_dir = os.path.join(
                os.path.expanduser("~"), 
                ".oblix", 
                "documents"
            )
        
        # Create directory structure
        self.base_dir = base_dir
        self.documents_dir = os.path.join(base_dir, "documents")
        self.workspaces_dir = os.path.join(base_dir, "workspaces")
        self.vector_stores_dir = os.path.join(base_dir, "vector_stores")
        
        for directory in [self.base_dir, self.documents_dir, self.workspaces_dir, self.vector_stores_dir]:
            os.makedirs(directory, exist_ok=True)
        
        # Initialize document processor
        self.processor = DocumentProcessor()
        
        # Initialize storage
        self.documents = {}  # doc_id -> Document
        self.workspaces = {}  # workspace_id -> Workspace
        self.vector_stores = {}  # workspace_id -> VectorStorage
        
        # Load existing data
        self._load_documents()
        self._load_workspaces()
        
    def _get_document_path(self, doc_id: str) -> str:
        """Get the path to a document JSON file."""
        import os
        return os.path.join(self.documents_dir, f"{doc_id}.json")
        
    def _get_workspace_path(self, workspace_id: str) -> str:
        """Get the path to a workspace JSON file."""
        import os
        return os.path.join(self.workspaces_dir, f"{workspace_id}.json")
        
    def _get_vector_store_path(self, workspace_id: str) -> str:
        """Get the path to a vector store file."""
        import os
        return os.path.join(self.vector_stores_dir, f"{workspace_id}.vstore")
        
    def _load_documents(self) -> None:
        """Load all documents from disk."""
        # Ensure os module is available
        import os
        
        try:
            for filename in os.listdir(self.documents_dir):
                if filename.endswith('.json'):
                    doc_id = filename[:-5]  # Remove .json extension
                    try:
                        with open(os.path.join(self.documents_dir, filename), 'r') as f:
                            data = json.load(f)
                            self.documents[doc_id] = Document.from_dict(data)
                    except Exception as e:
                        logger.error(f"Error loading document {doc_id}: {e}")
        except Exception as e:
            logger.error(f"Error loading documents: {e}")
            
    def _load_workspaces(self) -> None:
        """Load all workspaces from disk."""
        # Ensure os module is available
        import os
        
        try:
            for filename in os.listdir(self.workspaces_dir):
                if filename.endswith('.json'):
                    workspace_id = filename[:-5]  # Remove .json extension
                    try:
                        with open(os.path.join(self.workspaces_dir, filename), 'r') as f:
                            data = json.load(f)
                            self.workspaces[workspace_id] = Workspace.from_dict(data)
                    except Exception as e:
                        logger.error(f"Error loading workspace {workspace_id}: {e}")
        except Exception as e:
            logger.error(f"Error loading workspaces: {e}")
            
    def _save_document(self, doc_id: str) -> None:
        """Save a document to disk."""
        try:
            document = self.documents.get(doc_id)
            if not document:
                logger.warning(f"Cannot save document {doc_id}: not found")
                return
                
            with open(self._get_document_path(doc_id), 'w') as f:
                json.dump(document.to_dict(), f, indent=2)
        except Exception as e:
            logger.error(f"Error saving document {doc_id}: {e}")
            
    def _save_workspace(self, workspace_id: str) -> None:
        """Save a workspace to disk."""
        try:
            workspace = self.workspaces.get(workspace_id)
            if not workspace:
                logger.warning(f"Cannot save workspace {workspace_id}: not found")
                return
                
            with open(self._get_workspace_path(workspace_id), 'w') as f:
                json.dump(workspace.to_dict(), f, indent=2)
        except Exception as e:
            logger.error(f"Error saving workspace {workspace_id}: {e}")
            
    def _get_or_create_vector_store(self, workspace_id: str, embedding_client=None) -> VectorStorage:
        """
        Get or create a vector store for a workspace.
        
        Args:
            workspace_id (str): The workspace ID
            embedding_client (EmbeddingClient, optional): The embedding client to use for dimension info
            
        Returns:
            VectorStorage: The vector store for the workspace
        """
        # Ensure os module is available within this method
        import os
        
        if workspace_id not in self.vector_stores:
            # Get embedding dimension from client if available, otherwise use default
            embedding_dim = 1536  # Default to OpenAI dimension
            if embedding_client:
                embedding_dim = embedding_client.embedding_dimension
                
            logger.debug(f"Creating vector store with dimension {embedding_dim} for workspace {workspace_id}")
            
            # Create a new vector store
            vector_store = VectorStorage(backend="simple", embedding_dim=embedding_dim)
            
            # Try to load existing data if available
            vector_store_path = self._get_vector_store_path(workspace_id)
            if os.path.exists(vector_store_path):
                try:
                    vector_store.load(vector_store_path)
                    
                    # Validate that the loaded vector store has the expected dimension
                    # If dimensions don't match, this is likely due to a model change
                    if vector_store.embedding_dim != embedding_dim:
                        logger.warning(
                            f"Vector store dimension mismatch for workspace {workspace_id}: "
                            f"expected {embedding_dim}, got {vector_store.embedding_dim}. "
                            f"This may be due to switching embedding models. "
                            f"A new vector store will be created."
                        )
                        # Create a new vector store with the correct dimension
                        vector_store = VectorStorage(backend="simple", embedding_dim=embedding_dim)
                        
                except Exception as e:
                    logger.warning(f"Could not load vector store for workspace {workspace_id}: {e}")
            
            self.vector_stores[workspace_id] = vector_store
            
        return self.vector_stores[workspace_id]
        
    def upload_document(self, file_path: str, name: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Upload and process a document.
        
        Args:
            file_path (str): Path to the document file
            name (Optional[str]): Document name (defaults to filename)
            metadata (Optional[Dict[str, Any]]): Additional metadata
            
        Returns:
            str: Document ID
        """
        # Ensure os module is available within this method
        import os
        
        try:
            # Use filename as name if not provided
            if not name:
                name = os.path.basename(file_path)
                
            # Create document record
            doc_id = str(uuid.uuid4())
            document = Document(
                id=doc_id,
                name=name,
                source_path=file_path,
                metadata=metadata or {}
            )
            
            # Process document to extract text and chunk it with optimized parameters
            text = self.processor.process_document(file_path)
            document.chunks = self.processor.chunk_document(text, chunk_size=768, chunk_overlap=150)
            
            # Extract and store basic metadata for better retrieval
            try:
                # Add creation date to metadata
                import os
                from datetime import datetime
                document.metadata["creation_date"] = datetime.fromtimestamp(
                    os.path.getctime(file_path)
                ).isoformat()
                
                # Add file type to metadata
                document.metadata["file_type"] = os.path.splitext(file_path)[1].lower()
            except Exception as e:
                logger.warning(f"Could not extract additional metadata: {e}")
            
            # Store document
            self.documents[doc_id] = document
            self._save_document(doc_id)
            
            logger.info(f"Uploaded document {name} with ID {doc_id}")
            return doc_id
            
        except Exception as e:
            logger.error(f"Error uploading document: {e}")
            raise
            
    def get_document(self, doc_id: str) -> Optional[Document]:
        """
        Get a document by ID.
        
        Args:
            doc_id (str): Document ID
            
        Returns:
            Optional[Document]: Document if found, None otherwise
        """
        return self.documents.get(doc_id)
        
    def delete_document(self, doc_id: str) -> bool:
        """
        Delete a document and its embeddings.
        
        Args:
            doc_id (str): Document ID
            
        Returns:
            bool: True if document was deleted
        """
        # Ensure os module is available
        import os
        
        try:
            document = self.documents.get(doc_id)
            if not document:
                logger.warning(f"Cannot delete document {doc_id}: not found")
                return False
                
            # Remove from workspaces
            for workspace_id in document.workspaces:
                workspace = self.workspaces.get(workspace_id)
                if workspace:
                    workspace.document_ids.discard(doc_id)
                    self._save_workspace(workspace_id)
                    
                    # Remove from vector store if it exists
                    vector_store = self.vector_stores.get(workspace_id)
                    if vector_store:
                        # Delete all chunks
                        for i in range(len(document.chunks)):
                            chunk_id = f"{doc_id}_{i}"
                            vector_store.delete_document(chunk_id)
                        
                        # Save vector store
                        vector_store.save(self._get_vector_store_path(workspace_id))
            
            # Delete document file
            document_path = self._get_document_path(doc_id)
            if os.path.exists(document_path):
                os.remove(document_path)
                
            # Remove from memory
            del self.documents[doc_id]
            
            logger.info(f"Deleted document {doc_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting document {doc_id}: {e}")
            return False
            
    def create_workspace(self, name: str, description: str = "", metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Create a new workspace.
        
        Args:
            name (str): Workspace name
            description (str): Workspace description
            metadata (Optional[Dict[str, Any]]): Additional metadata
            
        Returns:
            str: Workspace ID
        """
        workspace_id = str(uuid.uuid4())
        workspace = Workspace(
            id=workspace_id,
            name=name,
            description=description,
            metadata=metadata or {},
            vector_store_path=self._get_vector_store_path(workspace_id)
        )
        
        self.workspaces[workspace_id] = workspace
        self._save_workspace(workspace_id)
        
        # Initialize vector store
        self._get_or_create_vector_store(workspace_id)
        
        logger.info(f"Created workspace {name} with ID {workspace_id}")
        return workspace_id
        
    def get_workspace(self, workspace_id: str) -> Optional[Workspace]:
        """
        Get a workspace by ID.
        
        Args:
            workspace_id (str): Workspace ID
            
        Returns:
            Optional[Workspace]: Workspace if found, None otherwise
        """
        return self.workspaces.get(workspace_id)
        
    def list_workspaces(self) -> List[Dict[str, Any]]:
        """
        List all workspaces.
        
        Returns:
            List[Dict[str, Any]]: List of workspace metadata
        """
        return [
            {
                "id": workspace.id,
                "name": workspace.name,
                "description": workspace.description,
                "document_count": len(workspace.document_ids)
            }
            for workspace in self.workspaces.values()
        ]
        
    async def update_workspace_embeddings(self, workspace_id: str, embedding_client, batch_size: int = 10) -> bool:
        """
        Re-embed all documents in a workspace with a new embedding model.
        
        This is useful when switching to a different embedding model with a different dimension.
        
        Args:
            workspace_id (str): Workspace ID
            embedding_client: Client for generating embeddings
            batch_size (int): Number of chunks to embed at once
            
        Returns:
            bool: True if all documents were re-embedded successfully
        """
        try:
            workspace = self.workspaces.get(workspace_id)
            if not workspace:
                logger.warning(f"Cannot update workspace {workspace_id} embeddings: workspace not found")
                return False
                
            # Get or create vector store with the new embedding dimension
            vector_store = self._get_or_create_vector_store(workspace_id, embedding_client)
            
            # Clear existing vector store data
            vector_store.clear()
            
            # Re-embed all documents in the workspace
            success = True
            for doc_id in workspace.document_ids:
                document = self.documents.get(doc_id)
                if not document:
                    logger.warning(f"Document {doc_id} not found in workspace {workspace_id}")
                    continue
                    
                # Mark document as embedding in progress
                document.embedding_status = "embedding"
                self._save_document(doc_id)
                
                # Process chunks in batches
                chunks = document.chunks
                num_chunks = len(chunks)
                embeddings_data = []
                
                for i in range(0, num_chunks, batch_size):
                    batch = chunks[i:i+batch_size]
                    
                    # Get embeddings for batch
                    batch_embeddings = await embedding_client.get_embeddings(batch)
                    
                    # Prepare data for vector storage
                    for j, embedding in enumerate(batch_embeddings):
                        chunk_idx = i + j
                        chunk_id = f"{doc_id}_{chunk_idx}"
                        chunk_text = chunks[chunk_idx]
                        
                        metadata = {
                            "doc_id": doc_id,
                            "doc_name": document.name,
                            "chunk_idx": chunk_idx,
                            "text": chunk_text
                        }
                        
                        embeddings_data.append((chunk_id, embedding, metadata))
                
                # Add embeddings to vector store
                vector_store.add_documents(embeddings_data)
                
                # Mark document as embedded
                document.embedding_status = "complete"
                self._save_document(doc_id)
                
            # Save vector store
            vector_store.save(self._get_vector_store_path(workspace_id))
            
            logger.info(f"Successfully updated embeddings for workspace {workspace_id}")
            return success
            
        except Exception as e:
            logger.error(f"Error updating workspace {workspace_id} embeddings: {e}")
            return False
        
    def delete_workspace(self, workspace_id: str) -> bool:
        """
        Delete a workspace and its vector store.
        
        Args:
            workspace_id (str): Workspace ID
            
        Returns:
            bool: True if workspace was deleted
        """
        # Ensure os module is available
        import os
        
        try:
            workspace = self.workspaces.get(workspace_id)
            if not workspace:
                logger.warning(f"Cannot delete workspace {workspace_id}: not found")
                return False
                
            # Update documents to remove workspace association
            for doc_id in workspace.document_ids:
                document = self.documents.get(doc_id)
                if document:
                    document.workspaces.discard(workspace_id)
                    self._save_document(doc_id)
            
            # Delete workspace file
            workspace_path = self._get_workspace_path(workspace_id)
            if os.path.exists(workspace_path):
                os.remove(workspace_path)
                
            # Delete vector store file
            vector_store_path = self._get_vector_store_path(workspace_id)
            if os.path.exists(vector_store_path):
                os.remove(vector_store_path)
                
            # Remove from memory
            if workspace_id in self.vector_stores:
                del self.vector_stores[workspace_id]
            
            del self.workspaces[workspace_id]
            
            logger.info(f"Deleted workspace {workspace_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting workspace {workspace_id}: {e}")
            return False
            
    def add_document_to_workspace(self, doc_id: str, workspace_id: str) -> bool:
        """
        Add a document to a workspace.
        
        Args:
            doc_id (str): Document ID
            workspace_id (str): Workspace ID
            
        Returns:
            bool: True if document was added
        """
        try:
            document = self.documents.get(doc_id)
            workspace = self.workspaces.get(workspace_id)
            
            if not document:
                logger.warning(f"Cannot add document {doc_id} to workspace: document not found")
                return False
                
            if not workspace:
                logger.warning(f"Cannot add document to workspace {workspace_id}: workspace not found")
                return False
                
            # Update associations
            document.workspaces.add(workspace_id)
            workspace.document_ids.add(doc_id)
            
            # Save changes
            self._save_document(doc_id)
            self._save_workspace(workspace_id)
            
            logger.info(f"Added document {doc_id} to workspace {workspace_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding document {doc_id} to workspace {workspace_id}: {e}")
            return False
            
    def remove_document_from_workspace(self, doc_id: str, workspace_id: str) -> bool:
        """
        Remove a document from a workspace.
        
        Args:
            doc_id (str): Document ID
            workspace_id (str): Workspace ID
            
        Returns:
            bool: True if document was removed
        """
        try:
            document = self.documents.get(doc_id)
            workspace = self.workspaces.get(workspace_id)
            
            if not document:
                logger.warning(f"Cannot remove document {doc_id} from workspace: document not found")
                return False
                
            if not workspace:
                logger.warning(f"Cannot remove document from workspace {workspace_id}: workspace not found")
                return False
                
            # Update associations
            document.workspaces.discard(workspace_id)
            workspace.document_ids.discard(doc_id)
            
            # Save changes
            self._save_document(doc_id)
            self._save_workspace(workspace_id)
            
            # Remove from vector store
            vector_store = self.vector_stores.get(workspace_id)
            if vector_store:
                # Delete all chunks
                for i in range(len(document.chunks)):
                    chunk_id = f"{doc_id}_{i}"
                    vector_store.delete_document(chunk_id)
                
                # Save vector store
                vector_store.save(self._get_vector_store_path(workspace_id))
            
            logger.info(f"Removed document {doc_id} from workspace {workspace_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error removing document {doc_id} from workspace {workspace_id}: {e}")
            return False
            
    async def embed_document(self, doc_id: str, workspace_id: str, embedding_client, batch_size: int = 10) -> bool:
        """
        Embed document chunks and add to vector store.
        
        Args:
            doc_id (str): Document ID
            workspace_id (str): Workspace ID
            embedding_client: Client for generating embeddings
            batch_size (int): Number of chunks to embed at once
            
        Returns:
            bool: True if embedding was successful
        """
        try:
            document = self.documents.get(doc_id)
            if not document:
                logger.warning(f"Cannot embed document {doc_id}: document not found")
                return False
                
            if workspace_id not in document.workspaces:
                logger.warning(f"Document {doc_id} is not in workspace {workspace_id}")
                return False
                
            # First get a sample embedding to check dimensions
            if len(document.chunks) > 0:
                sample_embedding = await embedding_client.get_embeddings([document.chunks[0]])
                if not sample_embedding or len(sample_embedding) == 0:
                    logger.error(f"Failed to get sample embedding for dimension check")
                    return False
                
                embedding_dim = len(sample_embedding[0])
                logger.info(f"Using embedding model with dimension {embedding_dim}")
            else:
                # No chunks to embed
                logger.warning(f"Document {doc_id} has no chunks to embed")
                return False
            
            # Get vector store with the appropriate embedding dimension
            vector_store = self._get_or_create_vector_store(workspace_id, embedding_client)
            
            # Verify that the vector store dimension matches the embedding dimension
            if vector_store.embedding_dim != embedding_dim:
                # Mismatch found - recreate the vector store with correct dimension
                logger.warning(f"Embedding dimension mismatch. Vector store has {vector_store.embedding_dim} " +
                             f"dimensions, but embedding model produces {embedding_dim} dimensions. " +
                             f"Re-creating vector store with correct dimensions.")
                
                # Create a new vector store with the correct dimension
                vector_store = VectorStorage(backend="simple", embedding_dim=embedding_dim)
                self.vector_stores[workspace_id] = vector_store
            
            # Mark document as embedding in progress
            document.embedding_status = "embedding"
            self._save_document(doc_id)
            
            # Process chunks in batches
            chunks = document.chunks
            num_chunks = len(chunks)
            embeddings_data = []
            
            for i in range(0, num_chunks, batch_size):
                batch = chunks[i:i+batch_size]
                
                # Get embeddings for batch
                batch_embeddings = await embedding_client.get_embeddings(batch)
                
                # Prepare data for vector storage
                for j, embedding in enumerate(batch_embeddings):
                    chunk_idx = i + j
                    chunk_id = f"{doc_id}_{chunk_idx}"
                    chunk_text = chunks[chunk_idx]
                    
                    metadata = {
                        "doc_id": doc_id,
                        "doc_name": document.name,
                        "chunk_idx": chunk_idx,
                        "text": chunk_text
                    }
                    
                    embeddings_data.append((chunk_id, embedding, metadata))
            
            # Add embeddings to vector store
            vector_store.add_documents(embeddings_data)
            
            # Save vector store
            vector_store.save(self._get_vector_store_path(workspace_id))
            
            # Mark document as embedded
            document.embedding_status = "complete"
            self._save_document(doc_id)
            
            logger.info(f"Embedded document {doc_id} in workspace {workspace_id}")
            
            # Ensure proper cleanup of embedding client resources
            if hasattr(embedding_client, 'embedding_model') and embedding_client.embedding_model:
                if hasattr(embedding_client.embedding_model, 'shutdown'):
                    try:
                        await embedding_client.embedding_model.shutdown()
                        logger.debug(f"Successfully shut down embedding model {embedding_client.embedding_model.model_name}")
                    except Exception as e:
                        logger.error(f"Error shutting down embedding model: {e}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error embedding document {doc_id} in workspace {workspace_id}: {e}")
            
            # Mark document as failed
            document = self.documents.get(doc_id)
            if document:
                document.embedding_status = "failed"
                self._save_document(doc_id)
                
            return False
            
    def _enhance_query(self, query: str) -> str:
        """
        Enhance a query to improve retrieval for factual information.
        
        Args:
            query (str): Original search query
            
        Returns:
            str: Enhanced query
        """
        import re
        
        # Check if the query is asking for dates
        if re.search(r'\b(date|when|time|day|month|year)\b', query.lower()):
            # Add date-related terms
            return f"{query} date time calendar year month day"
            
        # Check if query is asking for numerical information
        if re.search(r'\b(how many|count|total|number|amount)\b', query.lower()):
            # Add number-related terms
            return f"{query} number count quantity total"
            
        # Check if query is asking for locations
        if re.search(r'\b(where|location|place|country|city|address)\b', query.lower()):
            # Add location-related terms
            return f"{query} location place address city country state"
        
        # Check if query is asking for a list of items
        if re.search(r'\b(list|all|every|each)\b', query.lower()):
            # Add list-related terms
            return f"{query} list all every complete full"
            
        # No special enhancement needed
        return query
    
    async def search_workspace(self, workspace_id: str, query: str, embedding_client, top_k: int = 10) -> List[Dict[str, Any]]:
        """
        Search for relevant document chunks in a workspace.
        
        Args:
            workspace_id (str): Workspace ID
            query (str): Search query
            embedding_client: Client for generating embeddings
            top_k (int): Number of results to return (default increased to 10)
            
        Returns:
            List[Dict[str, Any]]: List of relevant document chunks
        """
        try:
            workspace = self.workspaces.get(workspace_id)
            if not workspace:
                logger.warning(f"Cannot search workspace {workspace_id}: workspace not found")
                return []
                
            # Get vector store with the appropriate embedding dimension
            vector_store = self._get_or_create_vector_store(workspace_id, embedding_client)
            
            # Enhance query for better semantic search
            enhanced_query = self._enhance_query(query)
            logger.info(f"Enhanced query from '{query}' to '{enhanced_query}'")
            
            # Get query embedding using enhanced query
            query_embedding = await embedding_client.get_embeddings([enhanced_query])
            if not query_embedding:
                logger.error(f"Failed to get query embedding for workspace {workspace_id}")
                return []
                
            # Search for similar chunks
            results = vector_store.search(query_embedding[0], top_k=top_k)
            
            # Format results
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "id": result["id"],
                    "score": result["score"],
                    "text": result["metadata"]["text"],
                    "doc_id": result["metadata"]["doc_id"],
                    "doc_name": result["metadata"]["doc_name"],
                    "chunk_idx": result["metadata"]["chunk_idx"]
                })
            
            # Ensure proper cleanup of embedding client resources
            if hasattr(embedding_client, 'embedding_model') and embedding_client.embedding_model:
                if hasattr(embedding_client.embedding_model, 'shutdown'):
                    try:
                        await embedding_client.embedding_model.shutdown()
                        logger.debug(f"Successfully shut down embedding model after search")
                    except Exception as e:
                        logger.error(f"Error shutting down embedding model: {e}")
                
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error searching workspace {workspace_id}: {e}")
            return []
            
    async def upload_process_and_embed_document(self, file_path: str, workspace_id: str = None, name: str = None, 
                                         embedding_client = None, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Upload, process, and optionally embed a document in a single workflow.
        
        This high-level method encapsulates the complete document ingestion workflow:
        1. Upload and process the document
        2. Add it to a workspace if provided
        3. Embed the document for vector search
        
        Args:
            file_path (str): Path to the document file
            workspace_id (str, optional): Workspace ID to add the document to
            name (str, optional): Document name (defaults to filename)
            embedding_client: Client for generating embeddings
            metadata (Dict[str, Any], optional): Additional metadata
            
        Returns:
            Dict[str, Any]: Result containing:
                - doc_id: Document ID
                - success: Overall success status
                - upload_success: Upload success status
                - workspace_success: Workspace addition success status (if workspace_id provided)
                - embedding_success: Embedding success status (if workspace_id provided)
                - error: Error message (if any)
        """
        # Ensure os module is available within this method
        import os
        
        result = {
            "doc_id": None,
            "success": False,
            "upload_success": False,
            "workspace_success": None,
            "embedding_success": None,
            "error": None
        }
        
        try:
            # Resolve absolute path
            abs_path = os.path.abspath(file_path)
            if not os.path.exists(abs_path):
                result["error"] = f"File not found: {abs_path}"
                return result
                
            # Upload and process document
            doc_id = self.upload_document(abs_path, name, metadata)
            result["doc_id"] = doc_id
            result["upload_success"] = True
            
            # Add to workspace if provided
            if workspace_id:
                workspace_success = self.add_document_to_workspace(doc_id, workspace_id)
                result["workspace_success"] = workspace_success
                
                # Embed document if workspace addition was successful
                if workspace_success and embedding_client:
                    embedding_success = await self.embed_document(doc_id, workspace_id, embedding_client)
                    result["embedding_success"] = embedding_success
                    
                    # Overall success depends on all steps succeeding
                    result["success"] = embedding_success
                else:
                    # If no embedding was requested, success depends on upload and workspace addition
                    result["success"] = workspace_success
            else:
                # If no workspace was provided, success depends only on upload
                result["success"] = True
                
            return result
            
        except Exception as e:
            logger.error(f"Error in document workflow: {e}")
            result["error"] = str(e)
            return result
            
    async def process_directory(self, directory_path: str, workspace_id: str = None, 
                               embedding_client = None, recursive: bool = True,
                               metadata: Optional[Dict[str, Any]] = None,
                               batch_size: int = 100,
                               exclude_patterns: List[str] = None) -> Dict[str, Any]:
        """
        Process all supported documents in a directory.
        
        This high-level method handles ingesting multiple documents from a directory:
        1. Creates a workspace if needed
        2. Finds all supported documents in the directory
        3. Processes and embeds each document
        4. Returns statistics and results
        
        Args:
            directory_path (str): Path to the directory of documents
            workspace_id (str, optional): Workspace ID to add documents to (creates a new one if None)
            embedding_client: Client for generating embeddings
            recursive (bool): Whether to process subdirectories recursively
            metadata (Dict[str, Any], optional): Additional metadata to add to all documents
            batch_size (int): Number of embeddings to process at once
            exclude_patterns (List[str], optional): Directory/file patterns to exclude (e.g., ["*.egg-info", ".git", "__pycache__"])
            
        Returns:
            Dict[str, Any]: Results containing:
                - workspace_id: ID of the workspace created or used
                - success: Overall success status
                - total_files: Total number of document files found
                - processed_files: Number of files successfully processed
                - documents: List of document processing results
                - error: Error message (if any)
        """
        # Ensure os module is available
        import os
        import asyncio
        
        result = {
            "workspace_id": workspace_id,
            "success": False,
            "total_files": 0,
            "processed_files": 0,
            "documents": [],
            "error": None
        }
        
        try:
            # Validate directory
            abs_dir_path = os.path.abspath(directory_path)
            if not os.path.exists(abs_dir_path):
                result["error"] = f"Directory not found: {abs_dir_path}"
                return result
            
            if not os.path.isdir(abs_dir_path):
                result["error"] = f"Not a directory: {abs_dir_path}"
                return result
            
            # Create workspace if needed
            if not workspace_id:
                dir_name = os.path.basename(abs_dir_path)
                workspace_id = self.create_workspace(
                    name=f"{dir_name} Workspace",
                    description=f"Documents from directory {abs_dir_path}",
                    metadata={"source_directory": abs_dir_path}
                )
                result["workspace_id"] = workspace_id
            
            # Find all supported documents
            supported_extensions = ('.pdf', '.txt', '.md', '.docx', '.csv', '.json', '.yml', '.yaml')
            all_files = []
            
            # Use default exclude patterns if none provided
            if exclude_patterns is None:
                exclude_patterns = [
                    "*.egg-info", "__pycache__", ".git", ".github", 
                    ".vscode", ".idea", "node_modules", "build", "dist"
                ]
                
            # Helper function to check if a path should be excluded
            def should_exclude(path):
                import fnmatch
                # Get the relative path from the base directory
                rel_path = os.path.relpath(path, abs_dir_path)
                
                # Check if any part of the path matches exclude patterns
                for pattern in exclude_patterns:
                    # Check each component of the path
                    path_parts = rel_path.split(os.sep)
                    for part in path_parts:
                        if fnmatch.fnmatch(part, pattern):
                            return True
                return False
            
            if recursive:
                # Walk through all subdirectories
                for root, dirs, files in os.walk(abs_dir_path):
                    # Filter out excluded directories
                    dirs[:] = [d for d in dirs if not should_exclude(os.path.join(root, d))]
                    
                    # Skip excluded directories
                    if should_exclude(root):
                        continue
                        
                    # Add matching files
                    for file in files:
                        file_path = os.path.join(root, file)
                        if not should_exclude(file_path) and file.lower().endswith(supported_extensions):
                            all_files.append(file_path)
            else:
                # Only look at the main directory
                for item in os.listdir(abs_dir_path):
                    file_path = os.path.join(abs_dir_path, item)
                    if os.path.isfile(file_path) and not should_exclude(file_path) and file_path.lower().endswith(supported_extensions):
                        all_files.append(file_path)
            
            result["total_files"] = len(all_files)
            
            if not all_files:
                result["error"] = f"No supported documents found in directory: {abs_dir_path}"
                return result
            
            # Process documents in parallel
            async def process_file(file_path):
                try:
                    # Create combined metadata
                    file_metadata = metadata.copy() if metadata else {}
                    file_metadata["source_directory"] = abs_dir_path
                    
                    # Process the document
                    return await self.upload_process_and_embed_document(
                        file_path=file_path,
                        workspace_id=workspace_id,
                        embedding_client=embedding_client,
                        metadata=file_metadata
                    )
                except Exception as e:
                    logger.error(f"Error processing file {file_path}: {e}")
                    return {
                        "file_path": file_path,
                        "success": False,
                        "error": str(e)
                    }
            
            # Process files in batches to avoid overwhelming the system
            MAX_CONCURRENT = min(os.cpu_count() * 2, 8)  # Limit concurrent tasks
            
            async def process_batch(batch):
                tasks = [process_file(file_path) for file_path in batch]
                return await asyncio.gather(*tasks)
            
            # Split files into batches
            batches = [all_files[i:i+MAX_CONCURRENT] for i in range(0, len(all_files), MAX_CONCURRENT)]
            
            # Process each batch
            all_results = []
            for batch in batches:
                batch_results = await process_batch(batch)
                all_results.extend(batch_results)
            
            # Count successful files
            successful_files = sum(1 for res in all_results if res.get("success", False))
            result["processed_files"] = successful_files
            result["documents"] = all_results
            result["success"] = successful_files > 0
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing directory {directory_path}: {e}")
            result["error"] = str(e)
            return result
            
    async def create_vector_search(self, query: str, workspace_id: str, embedding_client, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for relevant documents using vector similarity.
        
        This method creates a combined search API that:
        1. Generates an embedding for the query
        2. Searches the vector store for similar document chunks
        3. Returns formatted results with document context
        
        Args:
            query (str): The search query
            workspace_id (str): Workspace ID to search in
            embedding_client: Client for generating embeddings
            top_k (int): Number of results to return
            
        Returns:
            List[Dict[str, Any]]: Search results with document context
        """
        try:
            # Verify workspace exists
            workspace = self.get_workspace(workspace_id)
            if not workspace:
                logger.error(f"Workspace not found: {workspace_id}")
                return []
            
            # Get query embedding
            query_embeddings = await embedding_client.get_embeddings([query])
            if not query_embeddings or len(query_embeddings) == 0:
                logger.error("Failed to generate query embedding")
                return []
                
            query_embedding = query_embeddings[0]
            
            # Get vector store and search
            vector_store = self._get_or_create_vector_store(workspace_id, embedding_client)
            search_results = vector_store.search(query_embedding, top_k=top_k)
            
            # Format results
            formatted_results = []
            for result in search_results:
                formatted_results.append({
                    "id": result["id"],
                    "score": result["score"],
                    "text": result["metadata"]["text"],
                    "document": result["metadata"].get("name", "Unknown Document"),
                    "source": result["metadata"].get("file", "")
                })
                
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error in vector search: {e}")
            return []
            
    async def format_workspace_list(self, workspaces: List[Dict[str, Any]], 
                              truncate_description: int = 0) -> List[Dict[str, Any]]:
        """
        Format workspace list for display with optional field truncation.
        
        Args:
            workspaces (List[Dict[str, Any]]): List of workspaces from list_workspaces()
            truncate_description (int): Max length for description before truncating with ellipsis
            
        Returns:
            List[Dict[str, Any]]: Formatted workspace list
        """
        formatted = []
        
        for workspace in workspaces:
            formatted_workspace = workspace.copy()
            
            # Truncate description if requested
            if truncate_description > 0 and 'description' in workspace:
                desc = workspace['description']
                if len(desc) > truncate_description:
                    formatted_workspace['description'] = desc[:truncate_description] + '...'
                    
            formatted.append(formatted_workspace)
            
        return formatted
        
    async def format_document_list(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Format document list for display with consistent fields.
        
        Args:
            documents (List[Dict[str, Any]]): List of documents from get_documents_in_workspace()
            
        Returns:
            List[Dict[str, Any]]: Formatted document list with standardized fields
        """
        return documents  # Currently returned format is already appropriate
        
    async def get_document_chat_context(self, workspace_id: str, query: str, embedding_client, 
                                  max_tokens: int = 2000) -> str:
        """
        Search workspace and generate context for document-grounded chat.
        
        This high-level method combines search and context generation for document-grounded chat:
        1. Search the workspace for relevant documents
        2. Generate a formatted context from the search results
        
        Args:
            workspace_id (str): Workspace ID to search
            query (str): User query
            embedding_client: Client for generating embeddings
            max_tokens (int): Maximum token count for context
            
        Returns:
            str: Document context string ready for chat
        """
        try:
            # Verify workspace exists
            if workspace_id not in self.workspaces:
                logger.error(f"Workspace not found: {workspace_id}")
                return f"ERROR: Workspace {workspace_id} not found."
                
            # Verify embedding client is working
            try:
                test_embedding = await embedding_client.get_embeddings(["Test embedding functionality"])
                if not test_embedding or len(test_embedding) == 0:
                    logger.error("Embedding client failed to generate embeddings")
                    return "ERROR: Embedding client failed to generate embeddings."
            except Exception as e:
                logger.error(f"Embedding client error: {e}")
                return f"ERROR: Embedding client error: {e}"
            
            # Search for relevant documents
            search_results = await self.search_workspace(workspace_id, query, embedding_client)
            
            # Check if we got any results
            if not search_results:
                logger.info(f"No relevant documents found for query: {query}")
                return ""
            
            # Get context for chat
            context = self.get_relevant_context(workspace_id, search_results, max_tokens)
            
            return context
        
        except Exception as e:
            error_msg = f"Error getting document chat context: {e}"
            logger.error(error_msg)
            # Return a more informative error message instead of empty string
            return f"ERROR: {error_msg}"
            
    async def get_documents_in_workspace(self, workspace_id: str) -> List[Dict[str, Any]]:
        """
        Get all documents in a workspace.
        
        Args:
            workspace_id (str): Workspace ID
            
        Returns:
            List[Dict[str, Any]]: List of document metadata
        """
        try:
            workspace = self.workspaces.get(workspace_id)
            if not workspace:
                logger.warning(f"Cannot get documents in workspace {workspace_id}: workspace not found")
                return []
                
            results = []
            for doc_id in workspace.document_ids:
                document = self.documents.get(doc_id)
                if document:
                    results.append({
                        "id": document.id,
                        "name": document.name,
                        "chunk_count": len(document.chunks),
                        "embedding_status": document.embedding_status
                    })
                    
            return results
            
        except Exception as e:
            logger.error(f"Error getting documents in workspace {workspace_id}: {e}")
            return []
            
    def get_relevant_context(self, workspace_id: str, search_results: List[Dict[str, Any]], max_tokens: int = 2000) -> str:
        """
        Create a context string from search results.
        
        Args:
            workspace_id (str): Workspace ID
            search_results (List[Dict[str, Any]]): Search results from search_workspace
            max_tokens (int): Maximum approximate token count for context
            
        Returns:
            str: Document context string
        """
        try:
            if not search_results:
                return ""
                
            # Prepare context string
            context_parts = []
            total_chars = 0
            char_to_token_ratio = 4  # Approximate ratio of characters to tokens
            max_chars = max_tokens * char_to_token_ratio
            
            # Group results by document for better organization
            doc_groups = {}
            for result in search_results:
                doc_id = result.get("doc_id", "unknown")
                if doc_id not in doc_groups:
                    doc_groups[doc_id] = {
                        "name": result.get("doc_name", "Unknown Document"),
                        "results": []
                    }
                doc_groups[doc_id]["results"].append(result)
            
            # Identify factual content (dates, numbers, etc.) for higher priority
            import re
            date_pattern = re.compile(r'(\d{4}[-/\.]\d{1,2}[-/\.]\d{1,2}|\d{1,2}[-/\.]\d{1,2}[-/\.]\d{2,4})')
            
            # Function to check if text has factual content
            def has_facts(text):
                # Check for dates
                if date_pattern.search(text):
                    return True
                # Check for numbers that might be important (quantities, IDs, etc.)
                if re.search(r'\b\d{3,}\b', text):
                    return True
                return False
            
            # First pass: add content with factual information
            for doc_id, doc_info in doc_groups.items():
                doc_name = doc_info["name"]
                
                # Sort results by score and prioritize factual information
                sorted_results = sorted(doc_info["results"], 
                                       key=lambda x: (0 if has_facts(x.get("text", "")) else 1, 
                                                     -x.get("score", 0)))
                
                # Add a document header
                doc_header = f"Document: {doc_name}\n"
                
                # Process each chunk from this document
                for result in sorted_results:
                    text = result.get("text", "")
                    score = result.get("score", 0)
                    
                    part = f"Section (Relevance: {score:.2f}):\n{text}\n\n"
                    part_chars = len(part) + (len(doc_header) if doc_header else 0)
                    
                    # Check if adding this part would exceed the token limit
                    if total_chars + part_chars > max_chars:
                        continue
                    
                    # Add document header if this is the first chunk from this document
                    if doc_header:
                        context_parts.append(doc_header)
                        total_chars += len(doc_header)
                        doc_header = None  # Only add the header once
                    
                    context_parts.append(part)
                    total_chars += len(part)
            
            # Combine parts into final context
            context = "".join(context_parts)
            
            if context:
                context = f"### Relevant Document Sections:\n\n{context}"
                
                # Add a hint about factual information if detected
                if date_pattern.search(context):
                    context += "\n\nNote: The document contains date information that may be relevant to the query."
                
            return context
            
        except Exception as e:
            logger.error(f"Error creating context from search results: {e}")
            return ""

class EmbeddingClient:
    """
    Client for generating embeddings using various models.
    
    This class provides a unified interface for generating embeddings
    from different model providers. It uses the BaseEmbeddingModel interface
    to support multiple embedding model providers.
    """
    
    def __init__(self, embedding_model=None):
        """
        Initialize embedding client.
        
        Args:
            embedding_model: Instance of BaseEmbeddingModel or None
        """
        self.embedding_model = embedding_model
        
    async def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts using the configured embedding model.
        
        Args:
            texts (List[str]): List of text strings to embed
            
        Returns:
            List[List[float]]: List of embedding vectors
        """
        if not self.embedding_model:
            raise RuntimeError("No embedding model configured")
            
        if not self.embedding_model.is_ready:
            if not await self.embedding_model.initialize():
                raise RuntimeError(f"Failed to initialize embedding model {self.embedding_model}")
                
        return await self.embedding_model.generate_embeddings(texts)
        
    @property
    def embedding_dimension(self) -> int:
        """
        Get the dimension of embeddings produced by the configured model.
        
        Returns:
            int: Embedding dimension
        """
        if not self.embedding_model:
            # Default fallback dimension (OpenAI text-embedding-3-small)
            return 1536
            
        return self.embedding_model.embedding_dim