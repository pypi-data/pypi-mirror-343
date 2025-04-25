"""
Factory for creating embedding model instances.

This module provides factory functions to create and validate embedding models
from different providers, similar to the model factory for LLMs.
"""

import logging
from typing import Dict, Any, Optional, List

from .base import EmbeddingModelType, BaseEmbeddingModel
from .embeddings import (
    OpenAIEmbeddingModel,
    OllamaEmbeddingModel,
    HuggingFaceEmbeddingModel
)

logger = logging.getLogger(__name__)

class EmbeddingModelCreationError(Exception):
    """
    Custom exception for embedding model creation errors.
    
    Attributes:
        message (str): Error message
    """
    def __init__(self, message: str):
        super().__init__(message)

class EmbeddingModelFactory:
    """
    Factory class for creating and validating embedding model instances.
    
    The EmbeddingModelFactory simplifies the creation and validation of 
    embedding model instances from configuration dictionaries. It ensures 
    consistent model initialization, validation, and error handling across 
    different embedding model types.
    
    Attributes:
        _default_models (Dict[EmbeddingModelType, str]): Default model names by type
    """
    
    def __init__(self):
        """Initialize the embedding model factory with default models."""
        self._default_models = {
            EmbeddingModelType.OPENAI: "text-embedding-3-small",
            EmbeddingModelType.OLLAMA: "nomic-embed-text",
            EmbeddingModelType.HUGGINGFACE: "sentence-transformers/all-MiniLM-L6-v2",
        }
    
    async def create_embedding_model(self, config: Dict[str, Any]) -> BaseEmbeddingModel:
        """
        Create and initialize an embedding model instance.
        
        This method handles the complete lifecycle of embedding model creation:
        1. Validates the configuration
        2. Creates the appropriate model instance based on type
        3. Initializes the model
        4. Handles errors at each stage
        
        Args:
            config: Embedding model configuration dictionary containing at minimum:
                - type: Model type (EmbeddingModelType or string)
                - name: Model name (optional, will use default if not provided)
                Additional provider-specific keys may be required:
                - api_key: For OpenAI and HuggingFace models
                - endpoint: For Ollama models (optional)
                - local: For HuggingFace models (optional)
        
        Returns:
            Initialized embedding model instance
        
        Raises:
            EmbeddingModelCreationError: If validation or initialization fails
        """
        try:
            # Get model type
            model_type_str = config.get('type')
            if not model_type_str:
                raise EmbeddingModelCreationError("Model type is required")
            
            # Convert string to enum if needed
            if isinstance(model_type_str, str):
                try:
                    model_type = EmbeddingModelType(model_type_str.lower())
                except ValueError:
                    raise EmbeddingModelCreationError(f"Unsupported embedding model type: {model_type_str}")
            else:
                model_type = model_type_str
            
            # Get model name (use default if not provided)
            model_name = config.get('name', self._default_models.get(model_type))
            if not model_name:
                raise EmbeddingModelCreationError(f"Model name is required for {model_type.value}")
            
            # Create the appropriate model instance
            if model_type == EmbeddingModelType.OPENAI:
                api_key = config.get('api_key')
                if not api_key:
                    raise EmbeddingModelCreationError("API key is required for OpenAI embedding models")
                
                model = OpenAIEmbeddingModel(
                    model_name=model_name,
                    api_key=api_key
                )
                

            elif model_type == EmbeddingModelType.OLLAMA:
                endpoint = config.get('endpoint', "http://localhost:11434")
                
                model = OllamaEmbeddingModel(
                    model_name=model_name,
                    endpoint=endpoint
                )
                
            elif model_type == EmbeddingModelType.HUGGINGFACE:
                api_key = config.get('api_key')
                local = config.get('local', True)
                
                model = HuggingFaceEmbeddingModel(
                    model_name=model_name,
                    api_key=api_key,
                    local=local
                )
                
            else:
                raise EmbeddingModelCreationError(f"Unsupported embedding model type: {model_type}")
            
            # Initialize the model
            if not await model.initialize():
                raise EmbeddingModelCreationError(f"Failed to initialize {model_type.value} embedding model: {model_name}")
            
            logger.debug(f"Successfully created and initialized {model_type.value} embedding model: {model_name}")
            
            return model
            
        except EmbeddingModelCreationError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error creating embedding model: {e}")
            raise EmbeddingModelCreationError(f"Unexpected error creating embedding model: {str(e)}")
    
    def get_default_model_name(self, model_type: EmbeddingModelType) -> str:
        """
        Get the default model name for a given embedding model type.
        
        Args:
            model_type (EmbeddingModelType): The embedding model type
            
        Returns:
            str: Default model name
        """
        return self._default_models.get(model_type, "")
    
    def get_supported_models(self) -> Dict[str, List[str]]:
        """
        Get a dictionary of supported embedding models by provider.
        
        Returns:
            Dict[str, List[str]]: Dictionary mapping provider names to lists of model names
        """
        return {
            EmbeddingModelType.OPENAI.value: [
                "text-embedding-3-small",
                "text-embedding-3-large",
                "text-embedding-ada-002"
            ],
            EmbeddingModelType.OLLAMA.value: [
                "nomic-embed-text",
                "all-minilm",
                "mxbai-embed-large",
                "llama3-embed"
            ],
            EmbeddingModelType.HUGGINGFACE.value: [
                "sentence-transformers/all-MiniLM-L6-v2",
                "sentence-transformers/all-mpnet-base-v2",
                "sentence-transformers/multi-qa-mpnet-base-dot-v1",
                "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
            ]
        }
    
    async def cleanup(self):
        """
        Clean up resources.
        
        This method should be called when the factory is no longer needed
        to ensure all resources are properly released.
        """
        pass  # No resources to clean up in the factory itself