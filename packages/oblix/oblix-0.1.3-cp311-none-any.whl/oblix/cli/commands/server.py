# oblix/cli/commands/server.py
import click
import sys
import os
import asyncio
import colorama
from colorama import Fore, Style
import uvicorn
import logging
import threading
import time

from oblix.cli.utils import (
    setup_client, handle_async_command, print_header, 
    print_success, print_warning, print_error, print_info
)

# Initialize colorama
colorama.init()

logger = logging.getLogger("oblix.cli.server")


@click.group(name='server')
def server_group():
    """Start and manage the Oblix server"""
    pass

@server_group.command('start')
@click.option('--port', default=62549, help='Port to run the server on')
@click.option('--host', default='0.0.0.0', help='Host to bind the server to')
def start_server(port, host):
    """
    Start the Oblix server with OpenAI-compatible API
    
    Important: Before starting the server, you should hook at least one model
    
    Example workflow:
      oblix models hook         # Hook a model to use
      oblix server start        # Start the server
    """
    # ANSI escape codes for colored text
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    
    async def prepare_server():
        """Check if the configuration is valid before starting the server"""
        try:
            # Import the server manager
            from oblix.server import ServerManager
            from oblix.client import OblixClient
            from oblix.api.routes import OblixAPIManager
            from oblix.main import app
            
            # Create the client without authentication
            client = OblixClient()
            
            # Store the client in the API Manager
            OblixAPIManager._instance = client
            
            # Create a server manager instance
            server_manager = ServerManager(app=app, client=client)
            
            # Validate configured models
            is_valid, error_message, models = await server_manager.validate_models()
            
            # Show which models are configured
            print_info("\nConfigured models:")
            for model_type, model_names in models.items():
                if model_names:
                    print_info(f"  {model_type}: {', '.join(model_names)}")
                    
            # Require both local and cloud models for orchestration
            if not is_valid:
                print_error(f"\n⚠️ {error_message}")
                
                if "Missing: Local model" in error_message:
                    print_warning("Hook a local model with:")
                    print_warning("  oblix models hook --type ollama --name llama2 --endpoint http://localhost:11434")
                
                if "Missing: Cloud model" in error_message:
                    print_warning("Hook a cloud model with:")
                    print_warning("  oblix models hook --type openai --name gpt-3.5-turbo --api-key YOUR_OPENAI_KEY")
                
                sys.exit(1)
            
            # Set up default agents
            await server_manager.setup_default_agents()
            
            # Check if port is available
            if not server_manager.is_port_available(host, port):
                print_error(f"\nPort {port} is already in use!")
                print_warning("This could mean:")
                print_warning("1. Another Oblix server is already running")
                print_warning("2. Another application is using this port")
                print_warning("\nChoose a different port with: --port <number>")
                print_warning("Or check if an Oblix server is already running:")
                print_warning(f"  oblix server status --port {port}")
                sys.exit(1)
            
            # Display server information
            server_info = server_manager.generate_server_info(host, port)
            print(server_info)
            
            # Start the server
            server_manager.start_server(host, port)
            
            # Keep the main thread running to maintain client instance
            while True:
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            print_info("\nShutting down server...")
            print_success("Server stopped.")
            sys.exit(0)
        except Exception as e:
            print_error(f"Error preparing server: {e}")
            if logging.getLogger().level == logging.DEBUG:
                import traceback
                traceback.print_exc()
            sys.exit(1)
    
    # Run the async prepare function
    handle_async_command(prepare_server)

@server_group.command('status')
@click.option('--host', default='localhost', help='Server host')
@click.option('--port', default=62549, help='Server port')
def server_status(host, port):
    """Check the status of the Oblix server"""
    async def run_server_status():
        try:
            # Import the server manager
            from oblix.server import ServerManager
            
            # Create a server manager instance
            server_manager = ServerManager()
            
            # Check the server status
            is_running, status_data = await server_manager.check_server_status(host, port)
            
            if is_running:
                print_success(f"Server is running. Status: {status_data.get('status', 'unknown')}")
                print_info(f"Version: {status_data.get('version', 'unknown')}")
                
                # Show additional info if available
                if 'models' in status_data:
                    model_info = status_data['models']
                    if isinstance(model_info, dict) and 'count' in model_info:
                        print_info(f"Models: {model_info['count']} ({', '.join(model_info.get('types', []))})")
                
                if 'agents' in status_data:
                    agent_info = status_data['agents']
                    if isinstance(agent_info, dict) and 'count' in agent_info:
                        print_info(f"Agents: {agent_info['count']} ({', '.join(agent_info.get('types', []))})")
            else:
                error_msg = status_data.get('error', 'Unknown error')
                print_error(f"Could not connect to server at {host}:{port}")
                print_error(f"Error: {error_msg}")
                print_info("Make sure the server is running with: oblix server start")
                
        except Exception as e:
            print_error(f"Error checking server status: {e}")
    
    # Run the async function
    handle_async_command(run_server_status)