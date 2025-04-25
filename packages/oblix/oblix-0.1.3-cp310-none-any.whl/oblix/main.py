# app/main.py
# Copyright 2025 Oblix.ai
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from fastapi import FastAPI
import logging
import os

# Fix relative import issue - if running outside of module structure
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Fix imports using relative paths
try:
    from .api.routes import router  # First try relative import
    from .server import ServerManager  # First try relative import
except ImportError:
    try:
        from oblix.api.routes import router  # Then try absolute import
        from oblix.server import ServerManager  # Then try absolute import
    except ImportError:
        try:
            from api.routes import router  # Then try relative path from current directory
            from server import ServerManager  # Then try relative path from current directory
        except ImportError:
            # Last resort for direct script execution
            import sys
            import os
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            if parent_dir not in sys.path:
                sys.path.append(parent_dir)
            try:
                from oblix.api.routes import router
                from oblix.server import ServerManager
            except ImportError:
                raise ImportError("Could not import required modules from any path")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Oblix Server",
    description="AI Orchestration Server with Model Hooks and Execution Agents",
    version="0.1.0"
)

# Initialize the server manager
server_manager = ServerManager(app=app)

# Set up the FastAPI application
server_manager.setup_app(app)

# Configure the router
server_manager.configure_router(app, router)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting Oblix Server...")
    logger.info("OpenAI-compatible endpoint available at /v1/chat/completions")
    
    # Set up default agents
    await server_manager.setup_default_agents()

# No shutdown event handler - completely silent exit
