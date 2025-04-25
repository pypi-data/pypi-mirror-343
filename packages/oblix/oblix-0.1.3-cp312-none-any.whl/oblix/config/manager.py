# oblix/config/manager.py
from pathlib import Path
import yaml
from typing import Dict, Any, Optional
import logging
import os
from dataclasses import dataclass
from enum import Enum

from oblix.models.base import ModelType

logger = logging.getLogger(__name__)

class ModelConfigType(str, Enum):
    OLLAMA = "ollama"
    OPENAI = "openai"
    CLAUDE = "claude"
    CUSTOM = "custom"

@dataclass
class ModelConfig:
    """
    Represents a configuration for a specific model
    """
    name: str
    type: ModelConfigType
    endpoint: Optional[str] = None
    api_key: Optional[str] = None

class ConfigManager:
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize Configuration Manager
        
        :param config_path: Path to configuration file
        """
        # Ensure config path is set with a default
        if config_path is None:
            # Create default config directory if it doesn't exist
            default_config_dir = os.path.join(os.path.expanduser("~"), ".oblix")
            os.makedirs(default_config_dir, exist_ok=True)
            config_path = os.path.join(default_config_dir, "config.yaml")
        
        # Ensure the config file exists
        self.config_path = Path(config_path)
        if not self.config_path.exists():
            self._create_default_config()
        
        # Store for model configurations
        self.models: Dict[str, ModelConfig] = {}
        
        # Store for API key
        self.api_key: Optional[str] = None
        
        # Load existing configuration
        self._load_config()

    def _create_default_config(self):
        """
        Create a default configuration file if it doesn't exist
        """
        try:
            # Create an empty configuration structure
            default_config = {
                'models': {
                    model_type.value: [] 
                    for model_type in ModelConfigType 
                    if model_type != ModelConfigType.CUSTOM
                }
            }
            
            # Write default configuration
            with open(self.config_path, 'w') as f:
                yaml.safe_dump(default_config, f, default_flow_style=False)
            
            logger.info(f"Created default configuration at {self.config_path}")
        
        except Exception as e:
            logger.error(f"Error creating default config: {e}")
            raise

    def _load_config(self):
        """
        Load configuration from YAML file
        """
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f) or {}
            
            # Load API key if available
            self.api_key = config.get('api_key')
            
            # Load model configurations
            models_config = config.get('models', {})
            for model_type, models in models_config.items():
                if not isinstance(models, list):
                    models = [models]
                
                for model in models:
                    # Handle different configuration formats
                    if isinstance(model, str):
                        # Simple format: just model name
                        self.add_model(model_type, model)
                    elif isinstance(model, dict):
                        # Detailed format with additional config
                        self.add_model(
                            model_type,
                            model.get('name'),
                            endpoint=model.get('endpoint'),
                            api_key=model.get('api_key')
                        )
        
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            # Fallback to creating a default config if loading fails
            self._create_default_config()

    def add_model(self, 
                  model_type: str, 
                  model_name: str, 
                  endpoint: Optional[str] = None, 
                  api_key: Optional[str] = None):
        """
        Add or update a model configuration
        
        :param model_type: Type of model (ollama, openai, claude, etc.)
        :param model_name: Name of the model
        :param endpoint: Optional endpoint URL
        :param api_key: Optional API key
        """
        try:
            # Validate and normalize model type
            model_type = model_type.lower()
            
            # Explicitly handle all known model types
            valid_types = [t.value for t in ModelConfigType]
            if model_type not in valid_types:
                # Try to map or fallback to custom if not found
                type_mapping = {
                    'ollama': ModelConfigType.OLLAMA,
                    'openai': ModelConfigType.OPENAI,
                    'claude': ModelConfigType.CLAUDE
                }
                model_type = type_mapping.get(model_type, ModelConfigType.CUSTOM).value
            
            # Create model configuration
            model_config = ModelConfig(
                name=model_name,
                type=ModelConfigType(model_type),
                endpoint=endpoint,
                api_key=api_key
            )
            
            # Store model configuration
            model_id = f"{model_type}:{model_name}"
            self.models[model_id] = model_config
            
            # Update configuration file
            self._update_config_file()
            
            logger.debug(f"Added model configuration: {model_id}")
        
        except Exception as e:
            logger.error(f"Error adding model {model_name}: {e}")

    def _update_config_file(self):
        """
        Update the configuration file with current model configurations
        """
        try:
            # Load existing config to get any non-model settings (like api_key)
            existing_config = {}
            if self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    existing_config = yaml.safe_load(f) or {}
            
            # Start with existing config to preserve api_key and other settings
            config = existing_config.copy()
            
            # Update or create models section
            config['models'] = {}
            
            # Organize models by type
            for model_id, model_config in self.models.items():
                model_type = model_config.type.value
                
                if model_type not in config['models']:
                    config['models'][model_type] = []
                
                # Prepare model entry
                model_entry = {'name': model_config.name}
                if model_config.endpoint:
                    model_entry['endpoint'] = model_config.endpoint
                if model_config.api_key:
                    model_entry['api_key'] = model_config.api_key
                
                config['models'][model_type].append(model_entry)
            
            # Ensure api_key is in the config if it's set in memory
            if self.api_key:
                config['api_key'] = self.api_key
            
            # Write updated configuration
            with open(self.config_path, 'w') as f:
                yaml.safe_dump(config, f, default_flow_style=False)
            
            logger.info("Configuration file updated with model settings")
        
        except Exception as e:
            logger.error(f"Error updating config file: {e}")

    def get_model(self, model_type: str, model_name: str) -> Optional[ModelConfig]:
        """
        Retrieve a specific model configuration
        
        :param model_type: Type of model
        :param model_name: Name of the model
        :return: Model configuration or None
        """
        model_id = f"{model_type}:{model_name}"
        return self.models.get(model_id)

    def list_models(self) -> Dict[str, list]:
        """
        List all configured models
        
        :return: Dictionary of model types and their names
        """
        result = {}
        for model_id, config in self.models.items():
            model_type = config.type.value
            if model_type not in result:
                result[model_type] = []
            result[model_type].append(config.name)
        return result

    def remove_model(self, model_type: str, model_name: str):
        """
        Remove a model configuration
        
        :param model_type: Type of model
        :param model_name: Name of the model
        """
        try:
            model_id = f"{model_type}:{model_name}"
            if model_id in self.models:
                del self.models[model_id]
                self._update_config_file()
                logger.info(f"Removed model configuration: {model_id}")
        
        except Exception as e:
            logger.error(f"Error removing model {model_name}: {e}")
            
    def set_api_key(self, api_key: str):
        """
        Save the Oblix API key to the configuration file
        
        :param api_key: The API key to save
        """
        try:
            # Load existing config or create new one
            config = {}
            if self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    config = yaml.safe_load(f) or {}
            
            # Add or update API key
            config['api_key'] = api_key
            self.api_key = api_key
            
            # Write back to config file
            with open(self.config_path, 'w') as f:
                yaml.safe_dump(config, f, default_flow_style=False)
                
            logger.info("API key saved to configuration")
            
        except Exception as e:
            logger.error(f"Error saving API key: {e}")
            raise
            
    def get_api_key(self) -> Optional[str]:
        """
        Retrieve the stored Oblix API key
        
        :return: API key if available, None otherwise
        """
        return self.api_key