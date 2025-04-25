# oblix/server/manager.py
import asyncio
import logging
import socket
import sys
from typing import Dict, List, Optional, Tuple, Any, Callable
import uvicorn
import threading

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..client import OblixClient
from ..models.base import ModelType
from ..agents.resource_monitor import ResourceMonitor
from ..agents.connectivity import ConnectivityAgent

logger = logging.getLogger(__name__)

class ServerManager:
    """
    Centralized manager for Oblix server operations.
    
    Provides a unified interface for:
    - Server initialization and configuration
    - Health checks
    - Model and agent validation
    - Client instance management
    
    This manager acts as a bridge between the CLI and API components,
    ensuring consistent behavior and reducing code duplication.
    """
    
    def __init__(self, 
                app: Optional[FastAPI] = None,
                client: Optional[OblixClient] = None):
        """
        Initialize the server manager.
        
        Args:
            app: Optional FastAPI app instance
            client: Optional OblixClient instance
        """
        self.app = app
        self.client = client or OblixClient()
        self._server_thread = None
        self._server_running = False
        
    def is_port_available(self, host: str, port: int) -> bool:
        """
        Check if a port is available for the server to use.
        
        Args:
            host: Host address to check
            port: Port number to check
            
        Returns:
            True if the port is available, False otherwise
        """
        # If host is 0.0.0.0, check on localhost
        check_host = '127.0.0.1' if host == '0.0.0.0' else host
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)  # 2 second timeout
            result = sock.connect_ex((check_host, port))
            sock.close()
            
            return result != 0  # If result is 0, connection succeeded, so port is in use
        except socket.error:
            # In case of error, assume port is not available to be safe
            return False
            
    async def validate_models(self) -> Tuple[bool, str, Dict[str, List[str]]]:
        """
        Validate whether the client has the required models for orchestration.
        
        Returns:
            Tuple containing:
            - Success flag (True if all requirements are met)
            - Error message (if any)
            - Dictionary of configured models by type
        """
        models = self.client.list_models()
        
        # Check for local models (Ollama)
        has_local_model = False
        local_model_names = models.get('ollama', [])
        if local_model_names:
            has_local_model = True
            
        # Check for cloud models (OpenAI or Claude)
        has_cloud_model = False
        openai_models = models.get('openai', [])
        claude_models = models.get('claude', [])
        
        if openai_models or claude_models:
            has_cloud_model = True
        
        # Build error message if needed
        error_message = ""
        if not has_local_model or not has_cloud_model:
            error_message = "Oblix orchestration requires both a local and a cloud model!"
            
            if not has_local_model:
                error_message += "\nMissing: Local model (Ollama)"
            
            if not has_cloud_model:
                error_message += "\nMissing: Cloud model (OpenAI or Claude)"
                
        return has_local_model and has_cloud_model, error_message, models
    
    async def setup_default_agents(self) -> None:
        """
        Set up default monitoring agents if not already present.
        """
        # Add resource monitor if not already hooked
        if 'resource_monitor' not in self.client.agents:
            logger.info("Adding resource monitoring agent...")
            self.client.hook_agent(ResourceMonitor(name="resource_monitor"))
        
        # Add connectivity agent if not already hooked
        if 'connectivity' not in self.client.agents:
            logger.info("Adding connectivity monitoring agent...")
            self.client.hook_agent(ConnectivityAgent(name="connectivity"))
    
    def get_health_status(self) -> Dict[str, Any]:
        """
        Get the current health status of the server.
        
        Returns:
            Dictionary with health status information
        """
        # Import version at runtime to avoid circular imports
        from .. import __version__
        
        # Basic health information
        health_info = {
            "status": "healthy",
            "version": __version__,
            "uptime": "unknown"  # Could add actual uptime calculation
        }
        
        # Add model information if client is available
        if self.client:
            try:
                models = self.client.list_models()
                health_info["models"] = {
                    "count": sum(len(models.get(k, [])) for k in models),
                    "types": list(models.keys())
                }
                
                # Add agent information
                health_info["agents"] = {
                    "count": len(self.client.agents),
                    "types": list(self.client.agents.keys())
                }
            except Exception as e:
                logger.warning(f"Error getting model information for health check: {e}")
                health_info["models"] = {"error": str(e)}
        
        return health_info
    
    def setup_app(self, app: FastAPI) -> None:
        """
        Set up the FastAPI application with common middleware and configuration.
        
        Args:
            app: FastAPI application to configure
        """
        self.app = app
        
        # Add CORS middleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Register health check endpoint
        @app.get("/health")
        async def health_check():
            return self.get_health_status()
    
    def configure_router(self, app: FastAPI, router) -> None:
        """
        Configure the FastAPI application with the API router.
        
        Args:
            app: FastAPI application to configure
            router: API router to include
        """
        # Include router with standard OpenAI-compatible paths
        app.include_router(router)
        
        # For backward compatibility, also include with /api prefix
        app.include_router(router, prefix="/api")
    
    def start_server(self, host: str, port: int, app: Optional[FastAPI] = None) -> None:
        """
        Start the server in a separate thread.
        
        Args:
            host: Host to bind the server to
            port: Port to run the server on
            app: Optional FastAPI app to use
        """
        if app:
            self.app = app
            
        if not self.app:
            logger.error("No FastAPI app provided to start_server")
            return
            
        # Check if port is available
        if not self.is_port_available(host, port):
            logger.error(f"Port {port} is already in use")
            return
            
        # Start the server in a thread
        def run_server():
            try:
                self._server_running = True
                uvicorn.run(self.app, host=host, port=port)
            except Exception as e:
                logger.error(f"Server error: {e}")
            finally:
                self._server_running = False
                
        self._server_thread = threading.Thread(target=run_server)
        self._server_thread.daemon = True
        self._server_thread.start()
        
        logger.info(f"Server started on http://{host}:{port}")
    
    def stop_server(self) -> None:
        """
        Stop the running server.
        """
        # Server cleanup is handled by uvicorn when the thread terminates
        self._server_running = False
        logger.info("Server shutdown requested")
    
    def is_server_running(self) -> bool:
        """
        Check if the server is currently running.
        
        Returns:
            True if the server is running, False otherwise
        """
        return self._server_running and (self._server_thread and self._server_thread.is_alive())
        
    async def check_server_status(self, host: str, port: int) -> Tuple[bool, Dict[str, Any]]:
        """
        Check the status of a running server.
        
        Args:
            host: Host address of the server
            port: Port number of the server
            
        Returns:
            Tuple containing:
            - Success flag (True if server is running)
            - Status information dictionary
        """
        import aiohttp
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"http://{host}:{port}/health", timeout=5) as response:
                    if response.status == 200:
                        data = await response.json()
                        return True, data
                    else:
                        return False, {"error": f"Server responded with status code {response.status}"}
        except aiohttp.ClientError:
            return False, {"error": f"Could not connect to server at {host}:{port}"}
        except Exception as e:
            return False, {"error": f"Error checking server status: {str(e)}"}
    
    def generate_server_info(self, host: str, port: int) -> str:
        """
        Generate server information text for display.
        
        Args:
            host: Host address of the server
            port: Port number of the server
            
        Returns:
            Formatted server information text
        """
        # Import version
        from .. import __version__
        
        # Define ANSI color codes
        GREEN = "\033[92m"
        YELLOW = "\033[93m"
        CYAN = "\033[96m"
        MAGENTA = "\033[95m"
        RESET = "\033[0m"
        BOLD = "\033[1m"
        
        # Create an ASCII art header for the server
        header = f"""
{MAGENTA}{BOLD}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓{RESET}
{MAGENTA}{BOLD}┃                  OBLIX SERVER READY                    ┃{RESET}
{MAGENTA}{BOLD}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{RESET}

{CYAN}Version:{RESET} {__version__}
{CYAN}OpenAI-compatible endpoint:{RESET} {GREEN}http://{host}:{port}/v1/chat/completions{RESET}
{CYAN}Health check endpoint:{RESET}      {GREEN}http://{host}:{port}/health{RESET}

{YELLOW}Use with OpenAI client:{RESET}
  from openai import OpenAI
  client = OpenAI(base_url="{GREEN}http://{host}:{port}/v1{RESET}", api_key="oblix-dev")
  response = client.chat.completions.create(
    model="model-name",  # Use "ollama:llama2" or "openai:gpt-3.5-turbo"
    messages=[{{"role": "user", "content": "Hello, world!"}}]
  )

{YELLOW}Press Ctrl+C to stop the server.{RESET}
"""
        return header