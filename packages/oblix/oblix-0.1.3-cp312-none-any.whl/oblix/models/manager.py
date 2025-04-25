# oblix/models/manager.py
import logging
import httpx
import asyncio
from typing import Dict, List, Optional, Any, Tuple

from .base import BaseModel, ModelType
from .factory import ModelFactory, ModelCreationError
from .validation import ValidationResult
from .supported_models import (
    SUPPORTED_OPENAI_MODELS,
    SUPPORTED_CLAUDE_MODELS,
    get_supported_models,
    is_model_supported
)

logger = logging.getLogger(__name__)

class ModelManager:
    """
    Central manager for all model-related operations.
    
    Provides a unified interface for:
    - Listing available models across providers
    - Model validation
    - Model registration and initialization
    - Model lifecycle management
    - Configuration persistence
    
    This manager acts as a layer between applications and the underlying
    model implementations, providing a clean API and centralized logic.
    """
    
    def __init__(self, config_manager=None):
        """
        Initialize the model manager.
        
        Args:
            config_manager: Optional configuration manager to use for persistence
                           If not provided, models will only be stored in memory
        """
        self.models = {}
        self.factory = ModelFactory()
        self.config_manager = config_manager
        
    async def list_ollama_models(self) -> List[str]:
        """
        Get list of locally available Ollama models.
        
        Returns:
            List of available model names or empty list if Ollama is not available
        """
        try:
            # Try connecting to Ollama's API (default is http://localhost:11434)
            async with httpx.AsyncClient(timeout=2.0) as client:
                response = await client.get("http://localhost:11434/api/tags")
                
                if response.status_code == 200:
                    models = response.json().get("models", [])
                    return [model.get("name") for model in models]
                else:
                    return []
        except (httpx.ConnectError, httpx.ReadTimeout, httpx.ConnectTimeout):
            # Connection failed
            return []
        except Exception as e:
            logger.error(f"Error connecting to Ollama: {e}")
            return []
    
    def get_openai_models(self) -> List[Dict[str, str]]:
        """
        Return a list of recommended OpenAI models.
        
        Returns:
            List of model configurations
        """
        return SUPPORTED_OPENAI_MODELS
    
    def get_claude_models(self) -> List[Dict[str, str]]:
        """
        Return a list of recommended Claude models.
        
        Returns:
            List of model configurations
        """
        return SUPPORTED_CLAUDE_MODELS
    
    async def list_available_models(self) -> Dict[str, List]:
        """
        List all available models across all providers.
        
        Returns:
            Dictionary mapping provider type to list of available models
        """
        models = {
            "ollama": await self.list_ollama_models(),
            "openai": [model["name"] for model in self.get_openai_models()],
            "claude": [model["name"] for model in self.get_claude_models()]
        }
        
        # If a config manager is available, also include configured models
        if self.config_manager:
            configured_models = self.config_manager.list_models()
            # Merge with available models
            for model_type, model_names in configured_models.items():
                if model_type in models:
                    # Add only unique models
                    models[model_type] = list(set(models[model_type] + model_names))
                else:
                    models[model_type] = model_names
        
        return models
    
    def get_model_details(self, model_type: str, model_name: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific model.
        
        Args:
            model_type: Type of model (e.g., 'openai', 'claude')
            model_name: Name of the model
            
        Returns:
            Dictionary of model details or None if not found
        """
        # Check in supported models
        supported_models = get_supported_models(model_type)
        for model in supported_models:
            if model["name"] == model_name:
                return model
        
        # If not found but it's a configured model, return basic info
        if self.config_manager:
            model_config = self.config_manager.get_model(model_type, model_name)
            if model_config:
                return {
                    "name": model_config.name,
                    "type": model_config.type.value,
                    "description": "Custom configured model"
                }
        
        return None
    
    async def register_model(self, 
                           model_type: str, 
                           model_name: str, 
                           api_key: Optional[str] = None,
                           endpoint: Optional[str] = None,
                           auto_initialize: bool = True,
                           **kwargs) -> Tuple[bool, Optional[str], Optional[BaseModel]]:
        """
        Register and optionally initialize a model.
        
        Args:
            model_type: Type of model (e.g., 'openai', 'claude', 'ollama')
            model_name: Name of the model
            api_key: API key for cloud-based models (OpenAI, Claude)
            endpoint: Custom endpoint URL (mainly for Ollama models)
            auto_initialize: Whether to initialize the model immediately
            **kwargs: Additional model-specific parameters
            
        Returns:
            Tuple containing:
            - Success flag
            - Error message (if any)
            - Initialized model instance (if successful and auto_initialize=True)
        """
        try:
            # Prepare model configuration
            config = {
                'type': ModelType(model_type),
                'name': model_name,
                **kwargs
            }
            
            if api_key:
                config['api_key'] = api_key
            
            if endpoint:
                config['endpoint'] = endpoint
                
            # Save to config manager if available
            if self.config_manager:
                self.config_manager.add_model(model_type, model_name, endpoint, api_key)
            
            if auto_initialize:
                # Create and initialize the model
                model = await self.factory.create_model(config)
                
                if model:
                    # Store in memory
                    model_id = f"{model_type}:{model_name}"
                    self.models[model_id] = model
                    
                    return True, None, model
            else:
                # Just validate the config without initializing
                validation_result = await self.factory.validator.validate_model_config(config)
                if validation_result.is_valid:
                    return True, None, None
                else:
                    error_messages = "; ".join([f"{error.error_type.value}: {error.message}" 
                                              for error in validation_result.errors])
                    return False, error_messages, None
                
        except ModelCreationError as e:
            logger.error(f"Model creation failed: {e}")
            if e.validation_result:
                errors = "; ".join([f"{error.error_type.value}: {error.message}" 
                                  for error in e.validation_result.errors])
                return False, errors, None
            return False, str(e), None
            
        except Exception as e:
            logger.error(f"Unexpected error registering model: {e}")
            return False, str(e), None
    
    async def initialize_model(self, model_type: str, model_name: str) -> Tuple[bool, Optional[str], Optional[BaseModel]]:
        """
        Initialize a previously registered model.
        
        Args:
            model_type: Type of model
            model_name: Name of the model
            
        Returns:
            Tuple containing:
            - Success flag
            - Error message (if any)
            - Initialized model instance (if successful)
        """
        model_id = f"{model_type}:{model_name}"
        
        # Check if already initialized
        if model_id in self.models:
            return True, None, self.models[model_id]
        
        # Get configuration from config manager
        if self.config_manager:
            model_config = self.config_manager.get_model(model_type, model_name)
            if model_config:
                config = {
                    'type': ModelType(model_config.type.value),
                    'name': model_config.name
                }
                
                if model_config.api_key:
                    config['api_key'] = model_config.api_key
                
                if model_config.endpoint:
                    config['endpoint'] = model_config.endpoint
                    
                try:
                    # Create and initialize the model
                    model = await self.factory.create_model(config)
                    
                    if model:
                        # Store in memory
                        self.models[model_id] = model
                        return True, None, model
                        
                except ModelCreationError as e:
                    logger.error(f"Model initialization failed: {e}")
                    if e.validation_result:
                        errors = "; ".join([f"{error.error_type.value}: {error.message}" 
                                          for error in e.validation_result.errors])
                        return False, errors, None
                    return False, str(e), None
                    
                except Exception as e:
                    logger.error(f"Unexpected error initializing model: {e}")
                    return False, str(e), None
        
        return False, f"Model {model_id} not registered", None
    
    def get_model(self, model_type: str, model_name: str) -> Optional[BaseModel]:
        """
        Get an initialized model by type and name.
        
        Args:
            model_type: Type of model
            model_name: Name of the model
            
        Returns:
            Initialized model instance or None if not found
        """
        model_id = f"{model_type}:{model_name}"
        return self.models.get(model_id)
    
    async def unregister_model(self, model_type: str, model_name: str) -> bool:
        """
        Unregister and cleanup a model.
        
        Args:
            model_type: Type of model
            model_name: Name of the model
            
        Returns:
            True if successful, False otherwise
        """
        model_id = f"{model_type}:{model_name}"
        
        # Cleanup if initialized
        if model_id in self.models:
            model = self.models[model_id]
            
            # Call cleanup methods if available
            try:
                if hasattr(model, 'cleanup') and callable(model.cleanup):
                    await model.cleanup()
                elif hasattr(model, 'close') and callable(model.close):
                    await model.close()
            except Exception as e:
                logger.warning(f"Error cleaning up model {model_id}: {e}")
            
            # Remove from memory
            del self.models[model_id]
        
        # Remove from config if available
        if self.config_manager:
            self.config_manager.remove_model(model_type, model_name)
        
        return True
    
    async def cleanup(self):
        """
        Cleanup all models and resources.
        
        Should be called when shutting down the application.
        """
        # Cleanup all models
        for model_id, model in list(self.models.items()):
            try:
                if hasattr(model, 'cleanup') and callable(model.cleanup):
                    await model.cleanup()
                elif hasattr(model, 'close') and callable(model.close):
                    await model.close()
            except Exception as e:
                logger.warning(f"Error cleaning up model {model_id}: {e}")
        
        # Clear models dictionary
        self.models.clear()
        
        # Cleanup factory
        await self.factory.cleanup()