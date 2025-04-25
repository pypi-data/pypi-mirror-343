# oblix/client/base_client.py
import os
import sys
import asyncio
import logging
from typing import Dict, Any, Optional, Union, List

from ..models.base import BaseModel, ModelType
from ..models.factory import ModelFactory
from ..models.manager import ModelManager
from ..agents.base import BaseAgent
from ..agents.resource_monitor import ResourceMonitor
from ..agents.connectivity import BaseConnectivityAgent
from ..config.manager import ConfigManager
from ..sessions.manager import SessionManager
from ..core.execution import ExecutionManager
from ..connectors.documents.manager import DocumentManager, EmbeddingClient

logger = logging.getLogger(__name__)

class OblixBaseClient:
    """
    Base infrastructure class for Oblix SDK.
    
    The OblixBaseClient provides the foundational infrastructure for the Oblix SDK,
    including model management, agent registration, configuration persistence, 
    session management, and resource cleanup.
    
    This class is designed to be extended by more specific client implementations
    that provide higher-level, developer-friendly interfaces.
    
    Attributes:
        host (str): Server host address
        port (int): Server port number
        config_manager (ConfigManager): Configuration persistence manager
        session_manager (SessionManager): Chat session manager
        models (Dict[str, BaseModel]): Dictionary of registered models
        agents (Dict[str, BaseAgent]): Dictionary of registered agents
        current_session_id (Optional[str]): Currently active session ID
        is_connected (bool): Connection status
        
    Args:
        host (str): Server host address (default: "localhost")
        port (int): Server port number (default: 4321)
        config_path (Optional[str]): Path to configuration file
    """
    
    def __init__(self, 
                 host: str = "localhost", 
                 port: int = 4321,
                 config_path: Optional[str] = None):
        """
        Initialize Oblix Base Client with configuration.
        
        Args:
            host: Server host address
            port: Server port number
            config_path: Path to configuration file
        """
        try:
            self.host = host
            self.port = port
            
            # Ensure config path is set with a default
            if config_path is None:
                default_config_dir = os.path.join(os.path.expanduser("~"), ".oblix")
                os.makedirs(default_config_dir, exist_ok=True)
                config_path = os.path.join(default_config_dir, "config.yaml")
            
            # Initialize managers
            self.config_manager = ConfigManager(config_path)
            self.session_manager = SessionManager()
            
            # Initialize document manager
            documents_base_dir = os.path.join(os.path.expanduser("~"), ".oblix", "documents")
            self.document_manager = DocumentManager(base_dir=documents_base_dir)
            
            # Initialize model manager with config
            self.model_manager = ModelManager(self.config_manager)
            
            # Stores for models and agents
            self.models: Dict[str, BaseModel] = {}
            self.agents: Dict[str, BaseAgent] = {}
            
            # Initialize execution manager for orchestration
            self.execution_manager = ExecutionManager()
            
            # Track requirements
            self._has_local_model = False
            self._has_cloud_model = False
            self._has_resource_monitor = False
            self._has_connectivity_monitor = False
            
            # Session and connection management
            self.current_session_id: Optional[str] = None
            self.is_connected = False
            
            # Check for new versions
            self._check_for_updates()
            
        except Exception as e:
            logger.error(f"Error initializing Oblix client: {str(e)}")
            raise

    async def _validate_requirements(self):
        """
        Validate all required components are set up.
        
        Checks that required models and agents are hooked.
        
        Raises:
            RuntimeError: If any requirement is not satisfied
        """
        if not self._has_local_model:
            raise RuntimeError("Local model not hooked. Hook an Ollama model first")
            
        if not self._has_cloud_model:
            raise RuntimeError("Cloud model not hooked. Hook an OpenAI or Claude model first")
            
        # Check for at least one monitoring agent
        has_monitoring = self._has_resource_monitor or self._has_connectivity_monitor
        if not has_monitoring:
            raise RuntimeError("No monitoring agent attached. Hook either ResourceMonitor or ConnectivityAgent first")

    async def hook_model(self, 
                    model_type: ModelType, 
                    model_name: str, 
                    endpoint: Optional[str] = None,
                    api_key: Optional[str] = None,
                    **kwargs) -> bool:
        """
        Hook a new AI model to the client.
        
        Registers a model with the client, initializes it, and makes it
        available for execution. The model factory handles creation and
        validation of the model based on its type.
        
        Args:
            model_type: Type of model (Ollama, OpenAI, Claude, etc.)
            model_name: Name of the model
            endpoint: Optional API endpoint (for Ollama models)
            api_key: Optional API key for the model
            **kwargs: Additional model configuration parameters
            
        Returns:
            bool: True if model is successfully hooked
            
        Note:
            The model is stored with an ID in the format "{model_type}:{model_name}"
        """
        try:
            # Use the model manager to register and initialize the model
            success, error_message, model = await self.model_manager.register_model(
                model_type=model_type.value,
                model_name=model_name,
                endpoint=endpoint,
                api_key=api_key,
                auto_initialize=True,
                **kwargs
            )
            
            if not success or not model:
                if error_message:
                    logger.error(f"Failed to hook model: {error_message}")
                return False
            
            # Track local and cloud model presence
            if model_type == ModelType.OLLAMA:
                self._has_local_model = True
            elif model_type in [ModelType.OPENAI, ModelType.CLAUDE]:
                self._has_cloud_model = True
            
            # Store the model for backward compatibility
            model_id = f"{model_type.value}:{model_name}"
            self.models[model_id] = model
            
            # Register with execution manager for orchestration
            self.execution_manager.register_model(model)
            
            logger.debug(f"Successfully hooked model: {model_id}")
            return True
        
        except Exception as e:
            logger.error(f"Error hooking model {model_name}: {e}")
            return False

    def hook_agent(self, agent: BaseAgent) -> bool:
        """
        Hook an agent to the client.
        
        Registers an agent with the client, initializes it, and makes it
        available for execution checks and monitoring.
        
        Args:
            agent: Agent instance to hook
            
        Returns:
            bool: True if agent is successfully hooked, False otherwise
        """
        try:
            # Validate agent
            if not hasattr(agent, 'name') or not hasattr(agent, 'check'):
                logger.error("Invalid agent: Must have 'name' and 'check' methods")
                return False
            
            # Initialize the agent
            asyncio.create_task(agent.initialize())
            
            # Track specific agent types
            if isinstance(agent, ResourceMonitor):
                self._has_resource_monitor = True
            elif isinstance(agent, BaseConnectivityAgent):
                self._has_connectivity_monitor = True
            
            # Store the agent
            self.agents[agent.name] = agent
            
            # Register with execution manager for orchestration
            self.execution_manager.register_agent(agent)
            
            logger.debug(f"Successfully hooked agent: {agent.name}")
            return True
        
        except Exception as e:
            logger.error(f"Error hooking agent: {e}")
            return False

    async def get_connectivity_metrics(self) -> Optional[Dict[str, Any]]:
        """
        Get current connectivity metrics from the connectivity monitor.
        
        Retrieves detailed network metrics including latency, bandwidth,
        packet loss, and connection type from the registered connectivity agent.
        
        Returns:
            Optional[Dict[str, Any]]: Dictionary of connectivity metrics or None if unavailable
            
        Example metrics:
            {
                "connection_type": "wifi",
                "latency": 45.2,  # ms
                "packet_loss": 0.5,  # percentage
                "bandwidth": 25.8,  # Mbps
                "timestamp": 1646756732.45
            }
        """
        try:
            # Find the connectivity agent
            connectivity_agent = next(
                (agent for agent in self.agents.values() 
                 if isinstance(agent, BaseConnectivityAgent)), 
                None
            )
            
            if connectivity_agent:
                return await connectivity_agent.measure_connection_metrics()
            
            logger.warning("No connectivity agent found")
            return None
        
        except Exception as e:
            logger.error(f"Error getting connectivity metrics: {e}")
            return None

    async def create_embedding_client(self, 
                                    model_type: ModelType = ModelType.OPENAI, 
                                    model_name: str = "text-embedding-3-small",
                                    api_key: Optional[str] = None) -> EmbeddingClient:
        """
        Create a client for generating embeddings.
        
        Args:
            model_type (ModelType): Type of embedding model
            model_name (str): Name of embedding model
            api_key (Optional[str]): API key for the model
            
        Returns:
            EmbeddingClient: Client for generating embeddings
        """
        # If API key not provided, try to get from model details
        if not api_key:
            # Get model details from model manager
            model_details = self.model_manager.get_model_details(model_type.value, model_name)
            if model_details and 'api_key' in model_details:
                api_key = model_details['api_key']
                
            # If still not found, check config directly
            if not api_key and self.config_manager:
                model_config = self.config_manager.get_model(model_type.value, model_name)
                if model_config and model_config.api_key:
                    api_key = model_config.api_key
        
        return EmbeddingClient(model_type=model_type, model_name=model_name, api_key=api_key)
                
    async def shutdown(self):
        """
        Gracefully shut down all models and agents.
        
        Closes all connections, releases resources, and performs cleanup
        for all registered models and agents.
        
        This method should be called when the application is closing to
        ensure proper resource management.
        """
        # Clean up model manager
        await self.model_manager.cleanup()
        self.models.clear()
        
        # Shutdown agents
        for agent_name, agent in list(self.agents.items()):
            try:
                await agent.shutdown()
                del self.agents[agent_name]
                logger.info(f"Shutdown agent: {agent_name}")
            except Exception as e:
                logger.error(f"Error shutting down agent {agent_name}: {e}")
            
    def _check_for_updates(self):
        """
        Check for newer versions of Oblix package.
        
        This is a non-blocking operation that runs on client initialization
        to notify users if a newer version of the SDK is available.
        """
        try:
            # Import here to avoid circular imports
            from .. import check_for_updates
            
            # Run version check in a separate thread to avoid blocking
            import threading
            threading.Thread(target=check_for_updates, daemon=True).start()
        except Exception as e:
            # Silently handle any errors to prevent initialization issues
            pass