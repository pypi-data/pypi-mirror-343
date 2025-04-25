"""Embedding model implementations for the Oblix system.

This module provides concrete implementations of embedding models from
different providers:
- OpenAI
- Ollama
- HuggingFace
"""

import logging
from typing import List, Dict, Any, Optional

from .base import BaseEmbeddingModel, EmbeddingModelType

logger = logging.getLogger(__name__)

class OpenAIEmbeddingModel(BaseEmbeddingModel):
    """
    Embedding model implementation for OpenAI embeddings.
    
    Supported models:
    - text-embedding-3-small (1536 dimensions)
    - text-embedding-3-large (3072 dimensions)
    - text-embedding-ada-002 (1536 dimensions, legacy)
    """
    
    def __init__(self, model_name: str = "text-embedding-3-small", api_key: Optional[str] = None):
        """
        Initialize OpenAI embedding model.
        
        Args:
            model_name (str): OpenAI embedding model name
            api_key (Optional[str]): OpenAI API key
        """
        # Set embedding dimension based on model
        embedding_dim = 1536  # Default for most models
        if model_name == "text-embedding-3-large":
            embedding_dim = 3072
            
        super().__init__(
            model_type=EmbeddingModelType.OPENAI,
            model_name=model_name,
            embedding_dim=embedding_dim
        )
        self.api_key = api_key
        self.client = None
        
    async def initialize(self) -> bool:
        """Initialize the OpenAI embedding client."""
        try:
            import openai
            
            self.client = openai.AsyncClient(api_key=self.api_key)
            self.is_ready = True
            
            logger.debug(f"OpenAI embedding model {self.model_name} initialized")
            return True
            
        except ImportError:
            logger.error("OpenAI package not installed")
            return False
        except Exception as e:
            logger.error(f"Error initializing OpenAI embedding model: {e}")
            return False
            
    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using OpenAI API."""
        if not self.is_ready or not self.client:
            raise RuntimeError("OpenAI embedding model not initialized")
            
        try:
            response = await self.client.embeddings.create(
                model=self.model_name,
                input=texts
            )
            
            embeddings = [item.embedding for item in response.data]
            return embeddings
            
        except Exception as e:
            logger.error(f"Error generating OpenAI embeddings: {e}")
            return []
            
    async def shutdown(self) -> None:
        """Clean up OpenAI resources."""
        self.client = None
        self.is_ready = False


class OllamaEmbeddingModel(BaseEmbeddingModel):
    """
    Embedding model implementation for Ollama embeddings.
    
    Uses Ollama's embedding endpoint for local embedding generation.
    """
    
    def __init__(self, model_name: str = "nomic-embed-text", endpoint: str = "http://localhost:11434"):
        """
        Initialize Ollama embedding model.
        
        Args:
            model_name (str): Ollama model name
            endpoint (str): Ollama API endpoint
        """
        # Common embedding dimensions for Ollama models
        # These may vary by model, so we use a mapping
        embedding_dims = {
            "nomic-embed-text": 768,
            "all-minilm": 384,
            "mxbai-embed-large": 1024,
            "llama3-embed": 4096
        }
        
        embedding_dim = embedding_dims.get(model_name, 768)  # Default to 768 dimensions
            
        super().__init__(
            model_type=EmbeddingModelType.OLLAMA,
            model_name=model_name,
            embedding_dim=embedding_dim
        )
        self.endpoint = endpoint
        self.session = None
        
    async def initialize(self) -> bool:
        """Initialize the Ollama embedding client."""
        try:
            import aiohttp
            
            # Use a context manager session to ensure proper cleanup
            self._session_cleanup_callback = None
            self.session = aiohttp.ClientSession()
            
            # Register a cleanup callback on event loop close to ensure session is closed
            import asyncio
            loop = asyncio.get_event_loop()
            
            def cleanup_session():
                if self.session and not self.session.closed:
                    try:
                        # Create a new event loop for cleanup if needed
                        try:
                            loop = asyncio.get_event_loop()
                        except RuntimeError:
                            loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(loop)
                        
                        # Run the close coroutine in the loop
                        if loop.is_running():
                            loop.create_task(self.session.close())
                        else:
                            loop.run_until_complete(self.session.close())
                            
                        logger.debug("Closed Ollama session via cleanup callback")
                    except Exception as e:
                        logger.error(f"Error during Ollama session cleanup: {e}")
            
            # Register this to be called when garbage collected
            import weakref
            self._cleanup_ref = weakref.finalize(self, cleanup_session)
            
            self.is_ready = True
            
            logger.debug(f"Ollama embedding model {self.model_name} initialized with endpoint {self.endpoint}")
            return True
            
        except ImportError:
            logger.error("aiohttp package not installed")
            return False
        except Exception as e:
            logger.error(f"Error initializing Ollama embedding model: {e}")
            return False
            
    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using Ollama API."""
        if not self.is_ready or not self.session:
            raise RuntimeError("Ollama embedding model not initialized")
            
        import asyncio
        
        try:
            embeddings = []
            # Try to generate embeddings directly
            model_available = False
            model_check_done = False
            
            # Now generate embeddings
            for text in texts:
                # Skip if we've already determined the model isn't available
                if model_check_done and not model_available:
                    continue
                    
                async with self.session.post(
                    f"{self.endpoint}/api/embeddings",
                    json={"model": self.model_name, "prompt": text}
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        
                        # Check if the error is because the model doesn't exist
                        if "not found" in error_text and "try pulling it first" in error_text and not model_check_done:
                            model_check_done = True
                            model_available = False
                            
                            # Model doesn't exist, inform the user they need to download it
                            logger.error(f"The embedding model '{self.model_name}' is not available in Ollama")
                            logger.error(f"Please run the following command to download it:")
                            logger.error(f"    ollama pull {self.model_name}")
                            logger.error(f"After downloading, try again")
                            
                            # Return empty list since we can't proceed
                            return []
                            
                        else:
                            # Some other error occurred
                            logger.error(f"Ollama API error: {error_text}")
                            continue
                    else:
                        # If we get here, the model is available
                        if not model_check_done:
                            model_check_done = True
                            model_available = True
                            logger.info(f"Model {self.model_name} is available in Ollama")
                        
                        result = await response.json()
                        if "embedding" in result:
                            embeddings.append(result["embedding"])
                        else:
                            logger.error(f"No embedding in Ollama response: {result}")
                
            # If we couldn't use the model, return empty list
            if not model_available:
                return []
                        
            return embeddings
            
        except Exception as e:
            logger.error(f"Error generating Ollama embeddings: {e}")
            return []
            
    async def shutdown(self) -> None:
        """Clean up Ollama resources."""
        try:
            # Disable the finalizer since we're explicitly cleaning up
            if hasattr(self, '_cleanup_ref'):
                self._cleanup_ref.detach()
            
            # Close the session if it exists and isn't already closed
            if hasattr(self, 'session') and self.session and not self.session.closed:
                try:
                    await self.session.close()
                    logger.debug("Closed Ollama session")
                except Exception as e:
                    logger.error(f"Error closing Ollama session: {e}")
            
            # Clean up references    
            self.session = None
            self.is_ready = False
            
            logger.debug("Ollama embedding model shutdown complete")
        except Exception as e:
            logger.error(f"Error during Ollama shutdown: {e}")
            self.is_ready = False


class HuggingFaceEmbeddingModel(BaseEmbeddingModel):
    """
    Embedding model implementation for HuggingFace embeddings.
    
    Supports various sentence transformer models from HuggingFace.
    """
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2", 
                 api_key: Optional[str] = None, local: bool = True):
        """
        Initialize HuggingFace embedding model.
        
        Args:
            model_name (str): HuggingFace model name
            api_key (Optional[str]): HuggingFace API key (for API-based access)
            local (bool): Whether to use local model or API
        """
        # Common embedding dimensions for popular models
        embedding_dims = {
            "sentence-transformers/all-MiniLM-L6-v2": 384,
            "sentence-transformers/all-mpnet-base-v2": 768,
            "sentence-transformers/multi-qa-mpnet-base-dot-v1": 768,
            "sentence-transformers/paraphrase-multilingual-mpnet-base-v2": 768
        }
        
        embedding_dim = embedding_dims.get(model_name, 768)  # Default to 768 dimensions
            
        super().__init__(
            model_type=EmbeddingModelType.HUGGINGFACE,
            model_name=model_name,
            embedding_dim=embedding_dim
        )
        self.api_key = api_key
        self.local = local
        self.model = None
        self.client = None
        
    async def initialize(self) -> bool:
        """Initialize the HuggingFace embedding model."""
        try:
            if self.local:
                # Import locally for SentenceTransformer
                from sentence_transformers import SentenceTransformer
                import torch
                
                # Run on GPU if available
                device = "cuda" if torch.cuda.is_available() else "cpu"
                logger.debug(f"Loading HuggingFace model on {device}")
                
                self.model = SentenceTransformer(self.model_name, device=device)
                logger.debug(f"HuggingFace local embedding model {self.model_name} initialized")
            else:
                # Import for API access
                import huggingface_hub
                
                self.client = huggingface_hub.InferenceClient(token=self.api_key)
                logger.debug(f"HuggingFace API embedding model {self.model_name} initialized")
            
            self.is_ready = True
            return True
            
        except ImportError as e:
            logger.error(f"Required package not installed: {e}")
            return False
        except Exception as e:
            logger.error(f"Error initializing HuggingFace embedding model: {e}")
            return False
            
    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using HuggingFace."""
        if not self.is_ready:
            raise RuntimeError("HuggingFace embedding model not initialized")
            
        try:
            if self.local and self.model:
                # Convert tensors to list of floats
                import asyncio
                import torch
                
                def _embed():
                    embeddings = self.model.encode(texts)
                    # Handle both list of lists and torch tensor outputs
                    if isinstance(embeddings, torch.Tensor):
                        return embeddings.tolist()
                    elif isinstance(embeddings, list) and all(isinstance(e, list) for e in embeddings):
                        return embeddings
                    else:
                        return [embeddings.tolist()]
                
                # Run in a thread to avoid blocking
                loop = asyncio.get_event_loop()
                embeddings = await loop.run_in_executor(None, _embed)
                return embeddings
                
            elif self.client:
                # Use the HuggingFace Inference API
                embeddings = []
                for text in texts:
                    result = self.client.feature_extraction(text=text, model=self.model_name)
                    embeddings.append(result)
                return embeddings
            else:
                raise RuntimeError("No HuggingFace model or client available")
            
        except Exception as e:
            logger.error(f"Error generating HuggingFace embeddings: {e}")
            return []
            
    async def shutdown(self) -> None:
        """Clean up HuggingFace resources."""
        try:
            # Nothing to explicitly close for HuggingFace
            logger.debug("Shutting down HuggingFace embedding model")
            self.model = None
            self.client = None
            self.is_ready = False
        except Exception as e:
            logger.error(f"Error during HuggingFace shutdown: {e}")
            self.is_ready = False