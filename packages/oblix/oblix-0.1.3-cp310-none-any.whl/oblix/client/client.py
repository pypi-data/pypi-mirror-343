# oblix/client/client.py
from typing import Dict, Any, Optional, List, Union
import logging
import os
import asyncio
import uuid
import json
from datetime import datetime
import sys
import gc

from .base_client import OblixBaseClient
from ..models.base import ModelType
from ..agents.base import BaseAgent
from ..agents.resource_monitor import ResourceMonitor
from ..agents.connectivity import ConnectivityAgent
from ..agents.connectivity.policies import ConnectivityState, ConnectionTarget
from ..connectors.documents.manager import EmbeddingClient

logger = logging.getLogger(__name__)

# Helper function for user-friendly error printing
def print_error(message):
    """Print error message in red if available, otherwise standard print"""
    try:
        # Try to use colorama if available
        from colorama import Fore, Style
        print(f"{Fore.RED}{Style.BRIGHT}{message}{Style.RESET_ALL}")
    except ImportError:
        # Fallback to standard print
        print(f"ERROR: {message}")

class OblixClient(OblixBaseClient):
    """
    Main client class for Oblix AI Orchestration SDK.
    
    OblixClient provides a high-level, developer-friendly interface for working with
    multiple AI models, managing sessions, and utilizing intelligent routing
    based on system resources and connectivity.
    
    This client extends OblixBaseClient with convenient methods for execution,
    chat management, and common operations while abstracting away the complexity
    of model routing, resource monitoring, and connectivity management.
    
    Attributes:
        models (Dict): Dictionary of registered models
        agents (Dict): Dictionary of registered agents
        current_session_id (Optional[str]): ID of the active chat session
        default_embedding_config (Dict): Default configuration for embedding models
    
    Examples:
        # Initialize client
        client = OblixClient()
        
        # Hook models
        await client.hook_model(ModelType.OLLAMA, "llama2")
        await client.hook_model(ModelType.OPENAI, "gpt-3.5-turbo", api_key="sk-...")
        
        # Configure embedding model
        embedding_config = await client.configure_embedding_model("openai", "text-embedding-3-small", api_key="sk-...")
        client.set_default_embedding_model(embedding_config)
        
        # Add monitoring
        client.hook_agent(ResourceMonitor())
        
        # Execute prompt
        response = await client.execute("Explain quantum computing")
        print(response["response"])
        
        # Manage sessions
        session_id = await client.create_session("My Chat")
        sessions = client.list_sessions()
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_embedding_config = None
    
    def set_default_embedding_model(self, config: Dict[str, Any]) -> None:
        """
        Set the default embedding model configuration for all document operations.
        
        Args:
            config (Dict[str, Any]): Configuration dictionary for the embedding model
                Can be created using the configure_embedding_model method
        """
        self.default_embedding_config = config
            
    async def execute(self, 
                   prompt: str, 
                   temperature: Optional[float] = None,
                   max_tokens: Optional[int] = None,
                   request_id: Optional[str] = None,
                   display_metrics: bool = True,
                   session_id: Optional[str] = None,
                   stream: bool = True,
                   chat: bool = False,
                   **kwargs) -> Optional[Dict[str, Any]]:
        """
        Execute a prompt using available models and agents with intelligent routing.
        
        This method handles the execution flow including:
        1. Using the ExecutionManager to determine the best model based on resource/connectivity
        2. Retrieving conversation context (if in an active session)
        3. Generating the response (streaming or non-streaming)
        4. Saving the interaction to the session (if active)
        
        Args:
            prompt (str): User prompt to process
            temperature (Optional[float]): Sampling temperature for text generation
            max_tokens (Optional[int]): Maximum tokens to generate
            request_id (Optional[str]): Custom request identifier for tracking
            display_metrics (bool): Whether to display performance metrics
            session_id (Optional[str]): Session ID to use for this interaction
                If provided, will use this session instead of current_session_id
            stream (bool): When True (default), streams the response token-by-token to the terminal
                When False, returns the complete response at once
            chat (bool): When True, starts an interactive chat loop after processing 
                the initial prompt. Will create a session if session_id not provided.
            **kwargs: Additional model-specific generation parameters
        
        Returns:
            Optional[Dict[str, Any]]: Response containing:
                - response: Generated text
                - metrics: Performance metrics
                - agent_checks: Results from agent checks
                - error: Error message (if execution failed)
            If chat=True, returns the session_id after the chat ends
        
        Raises:
            RuntimeError: If requirements validation fails
        """
        # Generate request ID if not provided
        if not request_id:
            request_id = str(uuid.uuid4())
            
        try:
            # Validate all requirements are met
            await self._validate_requirements()
        except Exception as e:
            # Handle validation errors
            logger.error(f"Validation error in execute: {e}")
            return {
                "request_id": request_id,
                "error": str(e)
            }
        
        try:
            # Get conversation context if session exists
            context = []
            # Use session_id parameter if provided, otherwise use current_session_id
            current_session = session_id if session_id is not None else self.current_session_id
            
            if current_session:
                try:
                    # Use token-based windowing from session manager
                    token_budget = self.session_manager.calculate_context_token_budget(self.models)
                    context = self.session_manager.get_context_window(current_session, token_budget)
                except Exception as e:
                    logger.warning(f"Error retrieving session context: {e}")
            
            # Check if we need to enhance the prompt with connector data
            enhanced_prompt = prompt
            
            # Only enhance if we have registered connectors
            if hasattr(self, 'connectors') and self.connectors:
                # Initialize document manager if needed 
                if not hasattr(self, 'document_manager'):
                    from ..connectors.documents.manager import DocumentManager
                    self.document_manager = DocumentManager()
                
                # Collect search results from all connectors
                connector_results = {}
                
                # Get results from each active connector
                for connector_id, connector in self.connectors.items():
                    try:
                        # Only search if we have a workspace and embedding client
                        if connector.get('workspace_id') and connector.get('embedding_client'):
                            # Search for relevant content
                            results = await self.document_manager.create_vector_search(
                                query=prompt,
                                workspace_id=connector['workspace_id'],
                                embedding_client=connector['embedding_client'],
                                top_k=5  # Default to 5 results per connector
                            )
                            
                            if results:
                                connector_results[connector.get('alias', 'Document')] = results
                    except Exception as e:
                        logger.warning(f"Error searching connector {connector_id}: {e}")
                
                # Format search results into context
                if connector_results:
                    context_parts = ["### Document Context:"]
                    
                    # Process each connector's results
                    for alias, results in connector_results.items():
                        # Add connector header
                        context_parts.append(f"\nFrom source: {alias}")
                        
                        # Track which files we've already seen to add headers only once per file
                        seen_files = set()
                        
                        for result in results:
                            file_name = result.get('document', 'Unknown Document')
                            
                            # Add file header if this is the first chunk from this file
                            if file_name not in seen_files:
                                context_parts.append(f"\nDocument: {file_name}")
                                seen_files.add(file_name)
                                
                            # Add text with relevance score
                            context_parts.append(f"Section (relevance: {result['score']:.2f}):\n{result['text']}")
                    
                    # Add the formatted context to the prompt
                    document_context = "\n".join(context_parts)
                    enhanced_prompt = f"{document_context}\n\n### Question:\n{prompt}\n\n### Answer:"
                    
                    logger.info(f"Enhanced prompt with context from {len(connector_results)} connectors")
            
            # Prepare parameters for execution
            parameters = {
                'request_id': request_id,
                'context': context,
                'stream': stream  # Use streaming if requested
            }
            
            # Add optional parameters if provided
            if temperature is not None:
                parameters['temperature'] = temperature
            if max_tokens is not None:
                parameters['max_tokens'] = max_tokens
                
            # Add any additional kwargs
            parameters.update(kwargs)
            
            # No model selection or redundant connectivity checks here - relying entirely on the ExecutionManager's orchestration
            # which will check connectivity and resource policies automatically
            model_type = None
            model_name = None
            
            if stream:
                logger.info("Executing streaming with pure policy-based orchestration")
            else:
                logger.info("Executing with pure policy-based orchestration")
                        
            # Use ExecutionManager for orchestration with enhanced prompt
            execution_result = await self.execution_manager.execute(
                enhanced_prompt,
                model_type=model_type,
                model_name=model_name,
                parameters=parameters
            )
            
            # Handle execution errors
            if 'error' in execution_result:
                logger.error(f"Execution error: {execution_result['error']}")
                return execution_result
                
            # Get the model that was selected
            model_identifier = execution_result.get('model_id', 'Unknown model')
            
            # Get the response text from execution result (may already be complete for non-streaming models)
            if 'response' in execution_result:
                # Extract clean response without metrics
                response_value = execution_result['response']
                
                # Handle different response formats
                if isinstance(response_value, dict) and 'response' in response_value:
                    # Extract the nested response if it's a dictionary
                    clean_response = response_value['response']
                else:
                    # Otherwise use it directly
                    clean_response = response_value
                    
                print(f"\nA: {clean_response}")
                full_response = clean_response
                
                # Display metrics in non-chat mode if requested
                if display_metrics:
                    # Get current metrics
                    current_metrics = execution_result.get('metrics', {})
                    if not current_metrics and 'model_instance' in execution_result:
                        model_instance = execution_result.get('model_instance')
                        if hasattr(model_instance, 'last_metrics') and model_instance.last_metrics:
                            current_metrics = model_instance.last_metrics
                    
                    # Only try to display if we actually have metrics
                    if current_metrics:
                        # Format metrics for display
                        import json
                        enhanced_metrics = self.format_metrics(current_metrics)
                        
                        # Extract model info
                        response_json = {
                            "model_name": model_identifier.split(':')[1] if ':' in model_identifier else model_identifier,
                            "model_type": model_identifier.split(':')[0] if ':' in model_identifier else "",
                            "time_to_first_token": enhanced_metrics.get("time_to_first_token"),
                            "tokens_per_second": enhanced_metrics.get("tokens_per_second"),
                            "latency": enhanced_metrics.get("total_latency"),
                            "input_tokens": enhanced_metrics.get("input_tokens"),
                            "output_tokens": enhanced_metrics.get("output_tokens")
                        }
                        
                        # Remove null values
                        response_json = {k: v for k, v in response_json.items() if v is not None}
                        
                        # Display metrics
                        print(f"\nPerformance Metrics:\n{json.dumps(response_json, indent=2)}")
                        
                        # Display routing decisions if available
                        if execution_result.get('routing_decision'):
                            resource_routing = execution_result['routing_decision'].get('resource_routing')
                            connectivity_routing = execution_result['routing_decision'].get('connectivity_routing')
                            
                            print("\nRouting decisions:")
                            if resource_routing:
                                print(f"Resource: {{\n  'target': '{resource_routing.get('target')}',\n  'state': '{resource_routing.get('state')}',\n  'reason': '{resource_routing.get('reason')}'\n}}")
                            if connectivity_routing:
                                print(f"Connectivity: {{\n  'state': '{connectivity_routing.get('state')}',\n  'target': '{connectivity_routing.get('target')}',\n  'reason': '{connectivity_routing.get('reason')}'\n}}")
            else:
                # Otherwise we expect streaming data from the execution
                print("\nA: ", end="", flush=True)
                full_response = ""
                
                # Extract streaming content if available
                if 'stream' in execution_result:
                    try:
                        async for token in execution_result['stream']:
                            print(token, end="", flush=True)
                            full_response += token
                        print()  # Add newline at the end
                    except Exception as e:
                        logger.error(f"Error streaming response: {e}")
                        print(f"\nError: {str(e)}")
                else:
                    print("\nError: No streaming response available")
                    full_response = "Streaming response not available"
                
                # Calculate metrics regardless of whether we display them
                import json
                
                # Retrieve metrics from model instance after streaming is complete
                metrics = {}
                
                # For streaming responses, metrics are stored in the model's last_metrics property
                if 'model_instance' in execution_result:
                    model_instance = execution_result.get('model_instance')
                    if hasattr(model_instance, 'last_metrics') and model_instance.last_metrics:
                        metrics = model_instance.last_metrics
                else:
                    # Fallback to any metrics directly in the execution result
                    metrics = execution_result.get("metrics", {})
                
                # Format metrics using helper function
                enhanced_metrics = self.format_metrics(metrics)
                
                # Extract model type and name from model_id
                model_type = model_identifier.split(":")[0] if ":" in model_identifier else ""
                model_name = model_identifier.split(":")[1] if ":" in model_identifier else model_identifier
                
                # Create a response object with metrics only (no response text as it's already streamed)
                response_json = {
                    "model_name": model_name,
                    "model_type": model_type,
                    "time_to_first_token": enhanced_metrics.get("time_to_first_token"),
                    "tokens_per_second": enhanced_metrics.get("tokens_per_second"),
                    "latency": enhanced_metrics.get("total_latency"),
                    "input_tokens": enhanced_metrics.get("input_tokens"),
                    "output_tokens": enhanced_metrics.get("output_tokens")
                }
                
                # Remove null values
                response_json = {k: v for k, v in response_json.items() if v is not None}
                
                # Display metrics if requested
                if display_metrics:
                    print(f"\nPerformance Metrics:\n{json.dumps(response_json, indent=2)}")
                    
                    # Display routing decisions after the JSON
                    if execution_result.get('routing_decision'):
                        resource_routing = execution_result['routing_decision'].get('resource_routing')
                        connectivity_routing = execution_result['routing_decision'].get('connectivity_routing')
                        
                        print("\nRouting decisions:")
                        if resource_routing:
                            print(f"Resource: {{\n  'target': '{resource_routing.get('target')}',\n  'state': '{resource_routing.get('state')}',\n  'reason': '{resource_routing.get('reason')}'\n}}")
                        if connectivity_routing:
                            print(f"Connectivity: {{\n  'state': '{connectivity_routing.get('state')}',\n  'target': '{connectivity_routing.get('target')}',\n  'reason': '{connectivity_routing.get('reason')}'\n}}")
            
            # Save to session if active
            current_session = session_id if session_id is not None else self.current_session_id
            if current_session:
                try:
                    # Save user message
                    self.session_manager.save_message(
                        current_session,
                        prompt,
                        role='user'
                    )
                    
                    # Save assistant message - ensure it's properly formatted
                    if isinstance(full_response, str):
                        message_to_save = full_response
                    elif isinstance(full_response, dict):
                        # Don't wrap an existing dict in another dict
                        message_to_save = full_response
                    else:
                        # For other types, convert to string
                        message_to_save = str(full_response)
                        
                    self.session_manager.save_message(
                        current_session,
                        message_to_save,
                        role='assistant'
                    )
                except Exception as e:
                    logger.warning(f"Error saving session messages: {e}")
            
            # Ensure metrics are also included in the return value
            # Use the same metrics retrieval logic as above
            metrics = {}
            if 'model_instance' in execution_result:
                model_instance = execution_result.get('model_instance')
                if hasattr(model_instance, 'last_metrics') and model_instance.last_metrics:
                    metrics = model_instance.last_metrics
            else:
                metrics = execution_result.get('metrics', {})
                
            # Check if chat mode was requested
            if chat:
                # NOTE: We're skipping metrics display here because they are already displayed above
                # in the non-streaming and streaming response sections.
                # This removes the duplicate metrics display in Method 5
                
                # Create or use provided session
                chat_session_id = session_id
                if not chat_session_id:
                    chat_session_id = await self.create_session(f"Chat Session {datetime.now().strftime('%Y-%m-%d %H:%M')}")
                    logger.info(f"Created new chat session: {chat_session_id}")
                
                # Make sure the first response is already processed before starting the loop
                # Save the initial message to the session if needed
                if session_id is None:
                    # First message was already processed above, just ensure it's in the session
                    current_session = chat_session_id if chat_session_id is not None else self.current_session_id
                    
                # Now start the interactive chat loop with the same streaming settings as the initial call
                print(f"\nInteractive Chat Started (Session ID: {chat_session_id})")
                print("Type 'exit' to quit\n")
                
                # Interactive chat loop for subsequent messages
                while True:
                    try:
                        user_input = input("\nYou: ").strip()
                        
                        if user_input.lower() == 'exit':
                            print("Chat session ended")
                            # Perform cleanup before exiting
                            await self.cleanup()
                            break
                            
                        # Reuse the same method but without chat mode
                        # Use the original stream setting from the first call
                        await self.execute(
                            prompt=user_input, 
                            temperature=temperature,
                            max_tokens=max_tokens,
                            display_metrics=display_metrics,
                            session_id=chat_session_id,
                            stream=stream,  # Use the original stream setting
                            chat=False,    # Prevent infinite recursion
                            **kwargs
                        )
                        
                    except KeyboardInterrupt:
                        print("\nChat session ended")
                        # Perform cleanup before exiting
                        await self.cleanup()
                        break
                    except Exception as e:
                        print(f"\nAn error occurred: {str(e)}")
                        logger.error(f"Chat error: {e}")
                
                # Return the session ID after chat ends
                return {"session_id": chat_session_id}
            
            # Normal mode - return response with execution metadata
            return {
                "request_id": request_id,
                "model_id": model_identifier,
                "response": full_response,
                "metrics": metrics,
                "agent_checks": execution_result.get('agent_checks', []),
                "routing_decision": execution_result.get('routing_decision', {})
            }
            
        except Exception as e:
            logger.error(f"Execution error: {e}")
            return {
                "request_id": request_id,
                "error": str(e)
            }
            
    
    # The _select_model_from_agent_checks method has been removed
    # All model selection logic is now handled exclusively in the ExecutionManager

    async def create_session(self, 
                           title: Optional[str] = None, 
                           initial_context: Optional[Dict] = None,
                           metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Create a new chat session with optional title and initial context.
        
        Args:
            title (Optional[str]): Optional session title
            initial_context (Optional[Dict]): Optional initial context dictionary
            metadata (Optional[Dict[str, Any]]): Optional additional metadata
        
        Returns:
            str: New session ID
        """
        session_id = self.session_manager.create_session(
            title=title,
            initial_context=initial_context,
            metadata=metadata
        )
        return session_id
        
    async def create_and_use_session(self, 
                           title: Optional[str] = None, 
                           initial_context: Optional[Dict] = None,
                           metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Create a new chat session and automatically set it as the current session.
        
        This convenience method creates a new session and sets it as the
        current session, making it immediately available for conversation.
        
        Args:
            title (Optional[str]): Optional session title
            initial_context (Optional[Dict]): Optional initial context dictionary
            metadata (Optional[Dict[str, Any]]): Optional additional metadata
        
        Returns:
            str: New session ID (already set as current_session_id)
        """
        session_id = await self.create_session(
            title=title,
            initial_context=initial_context,
            metadata=metadata
        )
        self.current_session_id = session_id
        logger.info(f"Created and activated session: {session_id}")
        return session_id

    def use_session(self, session_id: str) -> bool:
        """
        Set an existing session as the current active session.
        
        Validates that the session exists and sets it as the active session
        for future conversation interactions.
        
        Args:
            session_id (str): Session identifier to activate
            
        Returns:
            bool: True if session was successfully activated, False if not found
        """
        session_data = self.session_manager.load_session(session_id)
        if not session_data:
            logger.warning(f"Cannot activate session {session_id}: not found")
            return False
            
        self.current_session_id = session_id
        logger.info(f"Activated session: {session_id}")
        return True

    def list_sessions(self, limit: int = 50, filter_metadata: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        List recent chat sessions with metadata and optional filtering.
        
        Args:
            limit (int): Maximum number of sessions to return
            filter_metadata (Optional[Dict[str, Any]]): Optional metadata filters
                to only return sessions matching specific criteria
        
        Returns:
            List[Dict[str, Any]]: List of session metadata dictionaries containing:
                - id: Unique session identifier
                - title: Session title
                - created_at: Creation timestamp
                - updated_at: Last update timestamp
                - message_count: Number of messages in the session
                - metadata: Additional session metadata
        """
        return self.session_manager.list_sessions(limit, filter_metadata)

    def load_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Load a specific chat session by ID.
        
        Args:
            session_id (str): Session identifier
        
        Returns:
            Optional[Dict[str, Any]]: Session data if found, None otherwise
        """
        return self.session_manager.load_session(session_id)

    def delete_session(self, session_id: str) -> bool:
        """
        Delete a chat session permanently.
        
        Args:
            session_id (str): Session identifier
        
        Returns:
            bool: True if session was deleted successfully
        """
        return self.session_manager.delete_session(session_id)
        
    def update_session_metadata(self, session_id: str, metadata: Dict[str, Any]) -> bool:
        """
        Update or add metadata to a session.
        
        Updates existing metadata fields or adds new fields without
        affecting other session data.
        
        Args:
            session_id (str): Session identifier
            metadata (Dict[str, Any]): Metadata fields to update or add
            
        Returns:
            bool: True if metadata was updated successfully
        """
        return self.session_manager.update_session_metadata(session_id, metadata)
        
    def get_session_metadata(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get metadata for a specific session.
        
        Retrieves just the metadata fields for a session without
        loading the entire conversation.
        
        Args:
            session_id (str): Session identifier
            
        Returns:
            Optional[Dict[str, Any]]: Session metadata if found
        """
        return self.session_manager.get_session_metadata(session_id)
        
    async def export_session(self, session_id: str, export_path: str) -> bool:
        """
        Export a session to a file.
        
        Exports a complete session to a JSON file that can be shared
        or backed up.
        
        Args:
            session_id (str): Session identifier
            export_path (str): Path to save the exported session
            
        Returns:
            bool: True if export was successful
        """
        return self.session_manager.export_session(session_id, export_path)
        
    async def import_session(self, import_path: str, new_id: bool = True, use_immediately: bool = False) -> Optional[str]:
        """
        Import a session from a file.
        
        Imports a session from a JSON file, optionally assigning a new ID
        to avoid conflicts with existing sessions.
        
        Args:
            import_path (str): Path to the JSON file to import
            new_id (bool): Whether to assign a new ID (True) or keep original ID (False)
            use_immediately (bool): Whether to set the imported session as the current session
            
        Returns:
            Optional[str]: Session ID of the imported session, or None if import failed
        """
        session_id = self.session_manager.import_session(import_path, new_id)
        if session_id and use_immediately:
            self.current_session_id = session_id
            logger.info(f"Imported and activated session: {session_id}")
        return session_id
        
    async def merge_sessions(self, source_ids: List[str], title: Optional[str] = None, use_immediately: bool = False) -> Optional[str]:
        """
        Merge multiple sessions into a new session.
        
        Creates a new session containing all messages from the source sessions,
        properly ordered by timestamp.
        
        Args:
            source_ids (List[str]): List of session IDs to merge
            title (Optional[str]): Optional title for the merged session
            use_immediately (bool): Whether to set the merged session as the current session
            
        Returns:
            Optional[str]: ID of the newly created merged session, or None if merge failed
        """
        session_id = self.session_manager.merge_sessions(source_ids, title)
        if session_id and use_immediately:
            self.current_session_id = session_id
            logger.info(f"Created and activated merged session: {session_id}")
        return session_id
        
    async def copy_session(self, session_id: str, new_title: Optional[str] = None, use_immediately: bool = False) -> Optional[str]:
        """
        Create a copy of an existing session.
        
        Creates a new session with the same content as an existing session
        but with a new ID.
        
        Args:
            session_id (str): Session identifier to copy
            new_title (Optional[str]): Optional new title for the copied session
            use_immediately (bool): Whether to set the copied session as the current session
            
        Returns:
            Optional[str]: ID of the new copy, or None if copy failed
        """
        new_session_id = self.session_manager.copy_session(session_id, new_title)
        if new_session_id and use_immediately:
            self.current_session_id = new_session_id
            logger.info(f"Copied and activated session: {new_session_id}")
        return new_session_id


    def list_models(self) -> Dict[str, List[str]]:
        """
        List all available models grouped by type.
        
        Returns:
            Dict[str, List[str]]: Dictionary mapping model types to lists of model names
        """
        return self.config_manager.list_models()
    
    def format_response(self, result: Dict[str, Any]) -> str:
        """
        Format response as pretty-printed JSON.
        
        Args:
            result (Dict[str, Any]): Raw result from execute() method
            
        Returns:
            str: Formatted response text
        """
        # Get the response content
        response_data = result.get("response", "")
        
        # Handle nested response objects
        if isinstance(response_data, dict) and "response" in response_data:
            # Extract the actual response from the nested structure
            response_text = response_data["response"]
        else:
            response_text = response_data
            
        # No longer displaying routing decisions here, moved to the calling functions
        
        return response_text
        
    def format_metrics(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format metrics dictionary to ensure consistent output across streaming and non-streaming modes.
        
        Args:
            metrics (Dict[str, Any]): Raw metrics dictionary
            
        Returns:
            Dict[str, Any]: Enhanced metrics dictionary with all required fields
        """
        # Check if essential metrics are present
        has_metrics = (metrics and 
                      metrics.get("total_latency") is not None)
        
        if not has_metrics:
            # Return metrics with all fields set to None if no metrics are available yet
            return {
                "total_latency": None,
                "tokens_per_second": None,
                "start_time": None,
                "end_time": None,
                "input_tokens": None,
                "output_tokens": None,
                "model_name": None,
                "model_type": None,
                "time_to_first_token": None
            }
            
        # Create enhanced metrics dictionary with all requested fields
        enhanced_metrics = {
            "total_latency": metrics.get("total_latency"),
            "tokens_per_second": metrics.get("tokens_per_second"),
            "start_time": metrics.get("start_time"),
            "end_time": metrics.get("end_time"),
            "input_tokens": metrics.get("input_tokens"),
            "output_tokens": metrics.get("output_tokens"),
            "model_name": metrics.get("model_name"),
            "model_type": metrics.get("model_type"),
            "time_to_first_token": metrics.get("time_to_first_token")
        }
        
        return enhanced_metrics
    
    async def get_resource_metrics(self) -> Dict[str, Any]:
        """
        Get current resource metrics from the resource monitor agent.
        
        Returns:
            Dict[str, Any]: Dictionary of resource metrics or None if unavailable
        """
        try:
            # Find the resource monitor agent
            resource_agent = next(
                (agent for agent in self.agents.values() 
                if isinstance(agent, ResourceMonitor)), 
                None
            )
            
            if resource_agent:
                metrics = await resource_agent.check()
                return metrics
            
            logger.warning("No resource monitoring agent found")
            return None
        
        except Exception as e:
            logger.error(f"Error getting resource metrics: {e}")
            return None

    def get_model(self, model_type: str, model_name: str) -> Optional[Dict[str, Any]]:
        """
        Get configuration for a specific model.
        
        Args:
            model_type (str): Type of model (e.g., 'ollama', 'openai', 'claude')
            model_name (str): Name of model
        
        Returns:
            Optional[Dict[str, Any]]: Model configuration if found
        """
        return self.config_manager.get_model(model_type, model_name)
    
    
    
        
    async def configure_embedding_model(self, type_name: str, model_name: str, **kwargs) -> Dict[str, Any]:
        """
        Configure a custom embedding model for use in the client.
        
        Args:
            type_name (str): Type of embedding model (openai, claude, ollama, huggingface)
            model_name (str): Name of the model
            **kwargs: Additional configuration parameters
                - api_key: API key for cloud providers (OpenAI, Claude, HuggingFace API)
                - endpoint: Endpoint URL for Ollama
                - local: Whether to use local model for HuggingFace (True) or API (False)
                - embedding_dim: Override the default embedding dimension if needed
                
        Returns:
            Dict[str, Any]: Configuration dictionary for the embedding model
        """
        from ..models.base import EmbeddingModelType
        
        # Convert string type to enum
        try:
            model_type = EmbeddingModelType(type_name.lower())
        except ValueError:
            raise ValueError(f"Unsupported embedding model type: {type_name}")
        
        # Create base configuration
        config = {
            "type": model_type,
            "name": model_name
        }
        
        # Add additional configuration parameters
        for key, value in kwargs.items():
            config[key] = value
        
        # Return the configuration
        return config
    
    async def create_embedding_client(self, embedding_model_type=None, 
                                 model_name=None, 
                                 api_key=None,
                                 config=None) -> EmbeddingClient:
        """
        Create a properly configured embedding client using the new embedding models framework.
        
        Args:
            embedding_model_type: Type of embedding model to use (defaults to auto-detect)
            model_name (str): Name of embedding model (defaults to appropriate default for model type)
            api_key (str): API key for the model (defaults to one from configured models)
            config (Dict): Complete configuration dictionary for the embedding model
            
        Returns:
            EmbeddingClient: Configured embedding client
        """
        # Import required components
        from ..models.base import EmbeddingModelType
        from ..models.embedding_factory import EmbeddingModelFactory
        
        # Use provided config parameter first
        if config:
            try:
                # Create the embedding model with the factory
                factory = EmbeddingModelFactory()
                embedding_model = await factory.create_embedding_model(config)
                return EmbeddingClient(embedding_model)
            except Exception as e:
                logger.error(f"Error creating embedding model from config: {e}")
                # Fall back to default config or auto-detection
        
        # Use default embedding config if available
        if self.default_embedding_config:
            try:
                # Create the embedding model with the factory
                factory = EmbeddingModelFactory()
                embedding_model = await factory.create_embedding_model(self.default_embedding_config)
                return EmbeddingClient(embedding_model)
            except Exception as e:
                logger.error(f"Error creating embedding model from default config: {e}")
                # Fall back to auto-detection
        
        # Auto-detect from configured models
        # Default to OpenAI embedding model if available, otherwise use best available model
        openai_models = [m for m in self.models.keys() if m.startswith("openai:")]
        
        # Convert ModelType to EmbeddingModelType if needed
        if embedding_model_type is None:
            # Auto-detect model type
            if openai_models:
                embedding_model_type = EmbeddingModelType.OPENAI
            elif any(m.startswith("claude:") for m in self.models.keys()):
                embedding_model_type = EmbeddingModelType.CLAUDE
            elif any(m.startswith("ollama:") for m in self.models.keys()):
                embedding_model_type = EmbeddingModelType.OLLAMA
            else:
                # Fallback
                embedding_model_type = EmbeddingModelType.OPENAI
        # Handle case where ModelType is passed instead of EmbeddingModelType
        elif hasattr(embedding_model_type, "value"):
            # Convert from ModelType to EmbeddingModelType if the value exists in EmbeddingModelType
            try:
                embedding_model_type = EmbeddingModelType(embedding_model_type.value)
            except ValueError:
                # Fallback to OpenAI if conversion fails
                embedding_model_type = EmbeddingModelType.OPENAI
        
        # Create the embedding model factory
        factory = EmbeddingModelFactory()
        
        # Get default model name if not provided
        if not model_name:
            model_name = factory.get_default_model_name(embedding_model_type)
        
        # Look up API key if not provided
        if not api_key:
            if embedding_model_type == EmbeddingModelType.OPENAI and openai_models:
                # Try to get API key from OpenAI configuration
                for model_id in openai_models:
                    model = self.get_model("openai", model_id.split(":")[1])
                    if model and "api_key" in model:
                        api_key = model["api_key"]
                        break
            elif embedding_model_type == EmbeddingModelType.CLAUDE:
                # Try to get API key from Claude configuration
                for model_id in [m for m in self.models.keys() if m.startswith("claude:")]:
                    model = self.get_model("claude", model_id.split(":")[1])
                    if model and "api_key" in model:
                        api_key = model["api_key"]
                        break
        
        # Build the embedding model config
        model_config = {
            "type": embedding_model_type,
            "name": model_name
        }
        
        # Add API key if available
        if api_key:
            model_config["api_key"] = api_key
            
        # Add endpoint for Ollama if needed
        if embedding_model_type == EmbeddingModelType.OLLAMA:
            # Try to get endpoint from Ollama configuration
            for model_id in [m for m in self.models.keys() if m.startswith("ollama:")]:
                model = self.get_model("ollama", model_id.split(":")[1])
                if model and "endpoint" in model:
                    model_config["endpoint"] = model["endpoint"]
                    break
            # Default to localhost if not found
            if "endpoint" not in model_config:
                model_config["endpoint"] = "http://localhost:11434"
        
        try:
            # Create the embedding model with the factory
            logger.info(f"Creating embedding model with config: {model_config}")
            embedding_model = await factory.create_embedding_model(model_config)
            logger.info(f"Successfully created embedding model: {embedding_model}")
            return EmbeddingClient(embedding_model)
        except Exception as e:
            logger.error(f"Error creating embedding model: {e}")
            # Return a client with no model - operations will fail until a model is provided
            return EmbeddingClient(None)
        
    async def upload_document(self, file_path: str, name: Optional[str] = None, 
                              workspace_id: Optional[str] = None, embed: bool = False,
                              metadata: Optional[Dict[str, Any]] = None,
                              embedding_model_type: str = None) -> Union[str, Dict[str, Any]]:
        """
        Upload and process a document.
        
        Args:
            file_path (str): Path to the document file
            name (Optional[str]): Document name (defaults to filename)
            workspace_id (Optional[str]): Workspace ID to add the document to
            embed (bool): Whether to embed the document for vector search
            metadata (Optional[Dict[str, Any]]): Additional metadata
            embedding_model_type (str): Type of embedding model to use (openai or ollama)
            
        Returns:
            Union[str, Dict[str, Any]]: Document ID if simple upload, or result dict if workspace/embedding specified
        """
        # If no workspace or embedding is requested, just do a simple upload
        if not workspace_id and not embed:
            return self.document_manager.upload_document(file_path, name, metadata)
        
        # Otherwise, use the full workflow method
        embedding_client = None
        if embed:
            # Configure embedding client with specified type if provided
            if embedding_model_type:
                from ..models.base import EmbeddingModelType
                try:
                    # Convert string to enum
                    model_type = EmbeddingModelType(embedding_model_type.lower())
                    embedding_client = await self.create_embedding_client(embedding_model_type=model_type)
                except ValueError:
                    # Fallback to default if invalid type
                    embedding_client = await self.create_embedding_client()
            else:
                # Use default configuration
                embedding_client = await self.create_embedding_client()
        
        return await self.document_manager.upload_process_and_embed_document(
            file_path=file_path,
            workspace_id=workspace_id,
            name=name,
            embedding_client=embedding_client,
            metadata=metadata
        )
        
    async def upload_directory(self, directory_path: str, workspace_id: Optional[str] = None,
                             embedding_model_type: str = "openai", recursive: bool = True,
                             metadata: Optional[Dict[str, Any]] = None,
                             batch_size: int = 100) -> Dict[str, Any]:
        """
        Upload and process a directory of documents.
        
        Args:
            directory_path (str): Path to directory containing documents
            workspace_id (Optional[str]): Workspace ID to add documents to
            embedding_model_type (str): Type of embedding model to use (openai or ollama)
            recursive (bool): Whether to process subdirectories
            metadata (Optional[Dict[str, Any]]): Additional metadata to add to documents
            batch_size (int): Number of chunks to embed at once
            
        Returns:
            Dict[str, Any]: Results dictionary with statistics
        """
        # Set up document manager if needed
        if not hasattr(self, 'document_manager'):
            from ..connectors.documents.manager import DocumentManager
            self.document_manager = DocumentManager()
        
        # Configure embedding client with specified type
        from ..models.base import EmbeddingModelType
        try:
            # Convert string to enum
            model_type = EmbeddingModelType(embedding_model_type.lower())
            embedding_client = await self.create_embedding_client(embedding_model_type=model_type)
        except ValueError:
            # Fallback to OpenAI embeddings if invalid type
            embedding_client = await self.create_embedding_client(
                embedding_model_type=EmbeddingModelType.OPENAI
            )
        
        # Use the document manager's directory processing functionality
        return await self.document_manager.process_directory(
            directory_path=directory_path,
            workspace_id=workspace_id,
            embedding_client=embedding_client,
            recursive=recursive,
            metadata=metadata,
            batch_size=batch_size
        )
        
    async def register_connector(self, 
                             connector_type: str, 
                             path: str,
                             embedding_model: str = None,
                             embedding_api_key: str = None,
                             alias: str = None,
                             exclude_patterns: List[str] = None,
                             **kwargs) -> Dict[str, Any]:
        """
        Register a connector to an external data source.
        
        This unified API allows attaching various data connectors to the client.
        Currently supported connector types:
        - 'document': Connect to a single document
        - 'directory': Connect to a directory of documents
        
        Future connector types might include:
        - 'database': Connect to a database
        - 'api': Connect to an API endpoint
        - 'website': Connect to a website
        
        Args:
            connector_type (str): Type of connector ('document', 'directory', etc.)
            path (str): Path to the resource (file path, directory path, URL, etc.)
            embedding_model (str, optional): Name of embedding model to use (defaults to client default)
            embedding_api_key (str, optional): API key for the embedding model
            alias (str, optional): Friendly name for this connector (defaults to basename of path)
            **kwargs: Additional connector-specific options
                - recursive (bool): For directory connector, whether to process subdirectories 
                - workspace_id (str): Existing workspace ID to use (will create new one if not provided)
                - batch_size (int): Number of documents to process at once (for directory connector)
                - exclude_patterns (List[str]): File/directory patterns to exclude (e.g., ["*.egg-info", ".git"])
        
        Returns:
            Dict[str, Any]: Connector information including:
                - connector_id: Unique ID for this connector
                - workspace_id: ID of workspace where data is stored
                - success: Whether registration was successful
                - alias: The alias name for this connector
                - stats: Connector-specific statistics
        """
        # Validate connector type
        supported_types = ["document", "directory"]
        if connector_type not in supported_types:
            raise ValueError(f"Unsupported connector type: {connector_type}. "
                           f"Supported types: {', '.join(supported_types)}")
            
        # Validate path exists
        if not os.path.exists(path):
            raise ValueError(f"Path does not exist: {path}")
            
        # Create default alias if not provided
        if not alias:
            alias = os.path.basename(path)
            
        # Configure embedding model if specified
        embedding_type = None
        if embedding_model:
            # Determine embedding type based on model name
            if embedding_model.startswith(("text-embedding", "ada")):
                embedding_type = "openai"
            elif embedding_model in ["nomic-embed-text", "all-minilm", "mxbai-embed-large"]:
                embedding_type = "ollama"
            else:
                # Default to OpenAI
                embedding_type = "openai"
        else:
            # Try to use a default embedding model from an existing model
            for model_key in self.models:
                if model_key.startswith("openai:"):
                    embedding_type = "openai"
                    embedding_model = "text-embedding-3-small"
                    embedding_api_key = self.models[model_key].get("api_key")
                    break
                elif model_key.startswith("claude:"):
                    embedding_type = "openai"  # Still use OpenAI for embeddings as a default
                    embedding_model = "text-embedding-3-small"
                    embedding_api_key = embedding_api_key or self.models[model_key].get("api_key")
                    break
            
            if not embedding_type:
                # No suitable model found
                raise ValueError("No embedding model specified and no suitable default found")
        
        # Create embedding config
        embedding_config = await self.configure_embedding_model(
            type_name=embedding_type,
            model_name=embedding_model,
            api_key=embedding_api_key
        )
        
        # Create embedding client
        embedding_client = await self.create_embedding_client(config=embedding_config)
        
        # Initialize document manager if needed
        if not hasattr(self, 'document_manager'):
            from ..connectors.documents.manager import DocumentManager
            self.document_manager = DocumentManager()
            
        # Generate a unique connector ID
        import uuid
        connector_id = str(uuid.uuid4())
        
        # Initialize connector registry if it doesn't exist
        if not hasattr(self, 'connectors'):
            self.connectors = {}
            
        result = {}
            
        # Handle document connector
        if connector_type == "document":
            # Create workspace if needed
            workspace_id = kwargs.get('workspace_id')
            if not workspace_id:
                workspace_id = await self.create_workspace(
                    name=f"Document - {alias}",
                    description=f"Workspace for document {path}"
                )
                
            # Process document
            doc_result = await self.document_manager.upload_process_and_embed_document(
                file_path=path,
                workspace_id=workspace_id,
                embedding_client=embedding_client
            )
            
            # Create result
            result = {
                "connector_id": connector_id,
                "workspace_id": workspace_id,
                "success": doc_result.get("success", False),
                "alias": alias,
                "type": "document",
                "path": path,
                "error": doc_result.get("error")
            }
            
        # Handle directory connector
        elif connector_type == "directory":
            # Get directory options
            recursive = kwargs.get('recursive', True)
            batch_size = kwargs.get('batch_size', 100)
            
            # Use any explicitly provided exclude patterns, or pass None to use defaults
            exclude_patterns_to_use = exclude_patterns
            
            # Process directory
            dir_result = await self.document_manager.process_directory(
                directory_path=path,
                workspace_id=kwargs.get('workspace_id'),
                embedding_client=embedding_client,
                recursive=recursive,
                batch_size=batch_size,
                exclude_patterns=exclude_patterns_to_use
            )
            
            # Create result
            result = {
                "connector_id": connector_id,
                "workspace_id": dir_result.get("workspace_id"),
                "success": dir_result.get("success", False),
                "alias": alias,
                "type": "directory",
                "path": path,
                "stats": {
                    "total_files": dir_result.get("total_files", 0),
                    "processed_files": dir_result.get("processed_files", 0)
                },
                "error": dir_result.get("error")
            }
        
        # Store successful connector in registry
        if result.get("success", False):
            self.connectors[connector_id] = {
                "id": connector_id,
                "type": connector_type,
                "workspace_id": result.get("workspace_id"),
                "alias": alias,
                "path": path,
                "embedding_client": embedding_client
            }
            
            # Store the connector for future use
            # This will modify execute behavior to use document context
            if not hasattr(self, '_document_connectors'):
                self._document_connectors = []
                
            self._document_connectors.append({
                "id": connector_id,
                "workspace_id": result.get("workspace_id"),
                "embedding_client": embedding_client
            })
        
        return result
        
    async def vector_search(self, query: str, workspace_id: str, 
                          embedding_model_type: str = None, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for relevant documents using vector similarity.
        
        Args:
            query (str): The search query
            workspace_id (str): Workspace ID to search in
            embedding_model_type (str): Type of embedding model to use (openai or ollama)
            top_k (int): Number of results to return
            
        Returns:
            List[Dict[str, Any]]: Search results with document context
        """
        # Set up document manager if needed
        if not hasattr(self, 'document_manager'):
            from ..connectors.documents.manager import DocumentManager
            self.document_manager = DocumentManager()
        
        # Configure embedding client with specified type
        embedding_client = None
        if embedding_model_type:
            from ..models.base import EmbeddingModelType
            try:
                # Convert string to enum
                model_type = EmbeddingModelType(embedding_model_type.lower())
                embedding_client = await self.create_embedding_client(embedding_model_type=model_type)
            except ValueError:
                # Fallback to default
                embedding_client = await self.create_embedding_client()
        else:
            # Use default configuration
            embedding_client = await self.create_embedding_client()
        
        # Use the document manager's vector search functionality
        return await self.document_manager.create_vector_search(
            query=query,
            workspace_id=workspace_id,
            embedding_client=embedding_client,
            top_k=top_k
        )
        
    async def create_workspace(self, name: str, description: str = "", metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Create a new document workspace.
        
        Args:
            name (str): Workspace name
            description (str): Workspace description
            metadata (Optional[Dict[str, Any]]): Additional metadata
            
        Returns:
            str: Workspace ID
        """
        return self.document_manager.create_workspace(name, description, metadata)
        
    async def add_document_to_workspace(self, doc_id: str, workspace_id: str) -> bool:
        """
        Add a document to a workspace.
        
        Args:
            doc_id (str): Document ID
            workspace_id (str): Workspace ID
            
        Returns:
            bool: True if document was added
        """
        return self.document_manager.add_document_to_workspace(doc_id, workspace_id)
        
    async def embed_document(self, doc_id: str, workspace_id: str) -> bool:
        """
        Embed document chunks and add to vector store.
        
        Args:
            doc_id (str): Document ID
            workspace_id (str): Workspace ID
            
        Returns:
            bool: True if embedding was successful
        """
        # Create an embedding client
        embedding_client = await self.create_embedding_client()
        
        # Embed the document
        return await self.document_manager.embed_document(doc_id, workspace_id, embedding_client)
        
    async def list_workspaces(self) -> List[Dict[str, Any]]:
        """
        List all document workspaces.
        
        Returns:
            List[Dict[str, Any]]: List of workspace metadata
        """
        return self.document_manager.list_workspaces()
        
    async def get_documents_in_workspace(self, workspace_id: str) -> List[Dict[str, Any]]:
        """
        Get all documents in a workspace.
        
        Args:
            workspace_id (str): Workspace ID
            
        Returns:
            List[Dict[str, Any]]: List of document metadata
        """
        return await self.document_manager.get_documents_in_workspace(workspace_id)
        
    async def search_workspace(self, workspace_id: str, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """
        Search for relevant document chunks in a workspace.
        
        Args:
            workspace_id (str): Workspace ID
            query (str): Search query
            top_k (int): Number of results to return (default increased to 10 for better coverage)
            
        Returns:
            List[Dict[str, Any]]: List of relevant document chunks
        """
        # Create an embedding client
        embedding_client = await self.create_embedding_client()
        
        # Search the workspace
        return await self.document_manager.search_workspace(workspace_id, query, embedding_client, top_k)
        
    async def update_workspace_embeddings(self, workspace_id: str, 
                                    embedding_config: Optional[Dict[str, Any]] = None) -> bool:
        """
        Re-embed all documents in a workspace with a new embedding model.
        
        This is useful when switching to a different embedding model with a different dimension.
        
        Args:
            workspace_id (str): Workspace ID
            embedding_config (Optional[Dict[str, Any]]): Configuration for the embedding model
                                                         If None, uses the default embedding model
            
        Returns:
            bool: True if all documents were re-embedded successfully
        """
        # Create embedding client with the provided config or default
        embedding_client = await self.create_embedding_client(config=embedding_config)
        
        # Update embeddings in the workspace
        return await self.document_manager.update_workspace_embeddings(workspace_id, embedding_client)
        
    async def cleanup(self):
        """
        Clean up all resources used by the client.
        
        This method ensures proper cleanup of all async resources, 
        including HTTP sessions, connections, and any pending tasks.
        
        Call this method when shutting down the client to prevent 
        resource leaks and event loop warnings.
        """
        logger.info("Cleaning up client resources...")
        
        try:
            # Close all model connections if available
            for model_key, model in self.models.items():
                try:
                    if hasattr(model, 'close') and callable(model.close):
                        await model.close()
                    elif hasattr(model, 'cleanup') and callable(model.cleanup):
                        await model.cleanup()
                    logger.info(f"Closed model: {model_key}")
                except Exception as e:
                    logger.error(f"Error closing model {model_key}: {e}")
            
            # Close execution manager if available
            if hasattr(self, 'execution_manager'):
                try:
                    if hasattr(self.execution_manager, 'close') and callable(self.execution_manager.close):
                        await self.execution_manager.close()
                    logger.info("Closed execution manager")
                except Exception as e:
                    logger.error(f"Error closing execution manager: {e}")
            
            # Close embedding clients and their models if available
            if hasattr(self, 'connectors'):
                for connector_id, connector in self.connectors.items():
                    if 'embedding_client' in connector:
                        embedding_client = connector['embedding_client']
                        try:
                            if hasattr(embedding_client, 'embedding_model'):
                                model = embedding_client.embedding_model
                                if hasattr(model, 'shutdown') and callable(model.shutdown):
                                    await model.shutdown()
                                    logger.info(f"Closed embedding model for connector: {connector_id}")
                        except Exception as e:
                            logger.error(f"Error closing embedding model for connector {connector_id}: {e}")
            
            # Find and close any other aiohttp sessions with improved detection
            try:
                import inspect
                import aiohttp
                
                # First, check for aiohttp.ClientSession objects directly
                for obj in gc.get_objects():
                    try:
                        # Use safer isinstance() check first to detect direct instances
                        if isinstance(obj, aiohttp.ClientSession):
                            if not obj.closed:
                                try:
                                    await obj.close()
                                    logger.info(f"Closed aiohttp ClientSession: {obj}")
                                except Exception as e:
                                    logger.error(f"Error closing aiohttp session: {e}")
                                    
                        # Fallback to class name check to catch proxy objects or other variations
                        elif (not inspect.isclass(obj) and 
                              hasattr(obj, '__class__') and 
                              obj.__class__.__name__ == 'ClientSession'):
                            if hasattr(obj, 'closed') and not obj.closed:
                                try:
                                    await obj.close()
                                    logger.info(f"Closed lingering ClientSession: {obj}")
                                except Exception as e:
                                    logger.error(f"Error closing session: {e}")
                        
                        # Also check for aiohttp.TCPConnector objects
                        elif isinstance(obj, aiohttp.TCPConnector):
                            if not obj.closed:
                                try:
                                    await obj.close()
                                    logger.info(f"Closed TCPConnector: {obj}")
                                except Exception as e:
                                    logger.error(f"Error closing connector: {e}")
                        
                        # Also check for OllamaEmbeddingModel objects and close their sessions
                        elif (not inspect.isclass(obj) and 
                              hasattr(obj, '__class__') and
                              obj.__class__.__name__ == 'OllamaEmbeddingModel'):
                            
                            # Check if it has a session attribute that's not closed
                            if hasattr(obj, 'session') and obj.session and hasattr(obj.session, 'closed') and not obj.session.closed:
                                try:
                                    # Try to close it
                                    await obj.session.close()
                                    logger.info(f"Closed OllamaEmbeddingModel session: {obj.session}")
                                except Exception as e:
                                    logger.error(f"Error closing OllamaEmbeddingModel session: {e}")
                                    
                        # Check for EmbeddingClient objects and close their model sessions
                        elif (not inspect.isclass(obj) and 
                              hasattr(obj, '__class__') and
                              obj.__class__.__name__ == 'EmbeddingClient'):
                            
                            # Check if it has an embedding_model attribute that has a session
                            if (hasattr(obj, 'embedding_model') and obj.embedding_model and
                                hasattr(obj.embedding_model, 'shutdown') and callable(obj.embedding_model.shutdown)):
                                try:
                                    # Try to shutdown the model
                                    await obj.embedding_model.shutdown()
                                    logger.info(f"Closed EmbeddingClient model")
                                except Exception as e:
                                    logger.error(f"Error closing EmbeddingClient model: {e}")
                                    
                    except ReferenceError:
                        # Skip objects that were garbage collected during iteration
                        continue
                    except Exception as e:
                        logger.debug(f"Error checking object during cleanup: {e}")
                        continue
                        
            except Exception as e:
                # Log the error but continue with cleanup
                logger.error(f"Error during session cleanup: {e}")
            
            # Cancel any pending tasks
            tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
            if tasks:
                for task in tasks:
                    task.cancel()
                
                # Wait for tasks to be cancelled
                await asyncio.gather(*tasks, return_exceptions=True)
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
            
    async def shutdown(self):
        """Alias for cleanup() - ensures compatibility with other frameworks"""
        await self.cleanup()