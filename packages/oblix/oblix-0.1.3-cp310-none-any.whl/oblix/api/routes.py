# app/api/routes.py
from fastapi import APIRouter, Depends, HTTPException, Response
from typing import Dict, Any, Optional, List
import time
import uuid
import json
import logging

# Configure logging
logger = logging.getLogger(__name__)

try:
    # First try relative import
    from .schemas import (
        ModelHookRequest, 
        ExecuteRequest, 
        ExecuteResponse, 
        SessionResponse,
        ResourceMonitorConfig,
        ConnectivityMonitorConfig,
        ConnectivityMetricsResponse,
        # OpenAI-compatible schemas
        ChatCompletionRequest,
        ChatCompletionResponse,
        ChatCompletionChoice,
        ChatCompletionUsage,
        ChatMessage,
        ChatRole,
        ChatCompletionChunk,
        ChatCompletionChunkChoice,
        ChatCompletionChunkDelta
    )
except ImportError:
    try:
        # Then try absolute import
        from oblix.api.schemas import (
            ModelHookRequest, 
            ExecuteRequest, 
            ExecuteResponse, 
            SessionResponse,
            ResourceMonitorConfig,
            ConnectivityMonitorConfig,
            ConnectivityMetricsResponse,
            # OpenAI-compatible schemas
            ChatCompletionRequest,
            ChatCompletionResponse,
            ChatCompletionChoice,
            ChatCompletionUsage,
            ChatMessage,
            ChatRole,
            ChatCompletionChunk,
            ChatCompletionChunkChoice,
            ChatCompletionChunkDelta
        )
    except ImportError:
        # Last resort try legacy app import
        from app.api.schemas import (
            ModelHookRequest, 
            ExecuteRequest, 
            ExecuteResponse, 
            SessionResponse,
            ResourceMonitorConfig,
            ConnectivityMonitorConfig,
            ConnectivityMetricsResponse,
            # OpenAI-compatible schemas
            ChatCompletionRequest,
            ChatCompletionResponse,
            ChatCompletionChoice,
            ChatCompletionUsage,
            ChatMessage,
            ChatRole,
            ChatCompletionChunk,
            ChatCompletionChunkChoice,
            ChatCompletionChunkDelta
        )
from oblix.client import OblixClient
from oblix.models.base import ModelType
from oblix.agents.resource_monitor import ResourceMonitor
from oblix.agents.connectivity import BaseConnectivityAgent
from fastapi.responses import StreamingResponse

router = APIRouter()

class OblixAPIManager:
    """
    Manages the global Oblix client instance for API routes
    """
    _instance = None
    
    @classmethod
    def get_client(cls):
        """
        Singleton method to get or create OblixClient instance
        """
        if not cls._instance:
            cls._instance = OblixClient()
        return cls._instance

def get_oblix_client():
    """
    Dependency injection for Oblix client
    """
    return OblixAPIManager.get_client()

# Note: Health check endpoint is now provided by ServerManager in main.py
# This is kept here for backward compatibility
@router.get("/health")
async def health_check():
    """Health check endpoint (legacy version)"""
    # Import here to avoid circular imports
    from oblix import __version__
    return {"status": "healthy", "version": __version__}

@router.post("/models/hook")
async def hook_model(
    request: ModelHookRequest, 
    client: OblixClient = Depends(get_oblix_client)
):
    """
    Hook a new AI model to the Oblix client
    """
    try:
        success = await client.hook_model(
            request.type, 
            request.name, 
            endpoint=request.endpoint,
            api_key=request.api_key
        )
        
        if not success:
            raise HTTPException(status_code=400, detail="Failed to hook model")
        
        return {
            "status": "success", 
            "message": f"Model {request.name} hooked successfully"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/agents/resource-monitor")
async def attach_resource_monitor(
    config: Optional[ResourceMonitorConfig] = None,
    client: OblixClient = Depends(get_oblix_client)
):
    """
    Attach a resource monitor with optional custom thresholds
    """
    try:
        thresholds = config.dict() if config else None
        monitor = ResourceMonitor(
            name="api_resource_monitor", 
            custom_thresholds=thresholds
        )
        
        success = client.hook_agent(monitor)
        
        if not success:
            raise HTTPException(status_code=400, detail="Failed to attach resource monitor")
        
        return {
            "status": "success", 
            "message": "Resource monitor attached successfully"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/agents/connectivity-monitor")
async def attach_connectivity_monitor(
    config: Optional[ConnectivityMonitorConfig] = None,
    client: OblixClient = Depends(get_oblix_client)
):
    """
    Attach a connectivity monitor with optional custom configuration
    """
    try:
        # Import the connectivity agent dynamically to avoid circular imports
        from oblix.agents.connectivity import ConnectivityAgent
        
        # Prepare configuration
        monitor_kwargs = {}
        if config:
            # Convert Pydantic model to dictionary, filtering out None values
            monitor_kwargs = {
                k: v for k, v in config.dict().items() 
                if v is not None
            }
        
        # Create and initialize connectivity monitor
        monitor = ConnectivityAgent(
            name="api_connectivity_monitor", 
            **monitor_kwargs
        )
        
        success = client.hook_agent(monitor)
        
        if not success:
            raise HTTPException(status_code=400, detail="Failed to attach connectivity monitor")
        
        return {
            "status": "success", 
            "message": "Connectivity monitor attached successfully"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/connectivity/metrics")
async def get_connectivity_metrics(
    client: OblixClient = Depends(get_oblix_client)
):
    """
    Retrieve current connectivity metrics
    """
    try:
        metrics = await client.get_connectivity_metrics()
        
        if metrics:
            return ConnectivityMetricsResponse(
                connection_type=metrics.get('connection_type'),
                latency=metrics.get('latency'),
                packet_loss=metrics.get('packet_loss'),
                bandwidth=metrics.get('bandwidth'),
                timestamp=metrics.get('timestamp')
            )
        else:
            raise HTTPException(status_code=404, detail="No connectivity metrics available")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sessions/start")
async def start_chat_session(
    initial_context: Optional[Dict[str, Any]] = None,
    title: Optional[str] = None,
    client: OblixClient = Depends(get_oblix_client)
):
    """
    Start a new chat session
    """
    try:
        # Use the centralized session creation logic
        session_id = client.session_manager.create_session(
            title=title,
            initial_context=initial_context
        )
        
        return SessionResponse(
            session_id=session_id,
            status="active"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions")
async def list_sessions(
    limit: int = 50,
    include_metadata: bool = True,
    client: OblixClient = Depends(get_oblix_client)
):
    """
    List recent chat sessions
    """
    try:
        # Get sessions with the centralized method
        sessions = client.session_manager.list_sessions(limit)
        
        # Format sessions for the response
        formatted_sessions = client.session_manager.format_sessions_list(
            sessions,
            include_metadata=include_metadata
        )
        
        return {"sessions": formatted_sessions}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions/{session_id}")
async def get_session(
    session_id: str,
    include_messages: bool = False,
    client: OblixClient = Depends(get_oblix_client)
):
    """
    Get details of a specific session
    """
    try:
        # Validate session existence
        exists, session_data, error = client.session_manager.validate_session_existence(session_id)
        
        if not exists:
            raise HTTPException(status_code=404, detail=error or f"Session not found: {session_id}")
        
        # Format session for display
        formatted_session = client.session_manager.format_session_for_display(
            session_data,
            include_messages=include_messages
        )
        
        return formatted_session
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sessions/{session_id}/messages")
async def add_message_to_session(
    session_id: str,
    message: Dict[str, Any],
    client: OblixClient = Depends(get_oblix_client)
):
    """
    Add a message to an existing session
    """
    try:
        # Validate required fields
        if 'content' not in message:
            raise HTTPException(status_code=400, detail="Message content is required")
            
        role = message.get('role', 'user')
        content = message['content']
        
        # Save message to session
        success = client.session_manager.save_message(
            session_id,
            content,
            role=role
        )
        
        if not success:
            raise HTTPException(status_code=404, detail=f"Session not found: {session_id}")
            
        return {"status": "success"} 
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/execute")
async def execute_prompt(
    request: ExecuteRequest,
    client: OblixClient = Depends(get_oblix_client)
):
    """
    Execute an AI prompt with flexible routing
    """
    try:
        response = await client.execute(
            request.prompt, 
            model_type=request.model_type,
            model_name=request.model_name,
            session_id=request.session_id,
            parameters=request.parameters
        )
        
        return ExecuteResponse(
            request_id=response.get('request_id', ''),
            model_id=response.get('model_id', ''),
            response=response.get('response', ''),
            metrics=response.get('metrics', {}),
            agents_check=response.get('agents_check')
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/v1/chat/completions")
async def chat_completions(
    request: ChatCompletionRequest,
    client: OblixClient = Depends(get_oblix_client)
):
    """
    OpenAI-compatible chat completions API endpoint
    
    This endpoint allows applications to use the Oblix orchestration layer through
    the same interface as OpenAI's API, enabling drop-in compatibility with
    existing OpenAI-based applications.
    """
    # Handle streaming response if requested
    if request.stream:
        return StreamingResponse(
            chat_completions_stream(request, client),
            media_type="text/event-stream"
        )
    
    try:
        # Validate model name
        if request.model != "auto" and not request.model.startswith("gpt-") and not request.model.startswith("claude-") and not request.model.startswith("llama"):
            raise HTTPException(
                status_code=400,
                detail=f"Model '{request.model}' is not supported. Use 'auto' for Oblix orchestration."
            )
        
        # Validate messages
        if not request.messages:
            raise HTTPException(
                status_code=400,
                detail="'messages' array must not be empty"
            )
        
        # Always use orchestration - don't parse model parameter
        # Regardless of what model name is provided, use orchestration
        model_type = None  # Let Oblix orchestration decide
        model_name = None  # No specific model
        
        # Prepare context format that Oblix expects
        context = []
        combined_prompt = ""
        
        # Convert OpenAI-style messages to context array for Oblix
        for msg in request.messages:
            context.append({
                "role": msg.role,
                "content": msg.content
            })
            # For system and user messages, also add to the combined prompt
            if msg.role in [ChatRole.SYSTEM, ChatRole.USER]:
                prefix = f"{msg.role.value.capitalize()}: " if msg.role != ChatRole.SYSTEM else ""
                combined_prompt += f"{prefix}{msg.content}\n"
        
        # Extract the last user message as the primary prompt
        last_user_msg = next((msg for msg in reversed(request.messages) 
                             if msg.role == ChatRole.USER), None)
        
        if last_user_msg:
            primary_prompt = last_user_msg.content
        else:
            # Fallback if no user message is found
            primary_prompt = combined_prompt or "Hello"
        
        # Prepare parameters
        parameters = {
            "context": context,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
        }
        
        # Add additional parameters if provided
        if request.top_p is not None:
            parameters["top_p"] = request.top_p
        if request.presence_penalty is not None:
            parameters["presence_penalty"] = request.presence_penalty
        if request.frequency_penalty is not None:
            parameters["frequency_penalty"] = request.frequency_penalty
        
        # Create response in OpenAI format
        completion_id = str(uuid.uuid4())
        
        # Determine number of completions to generate (n parameter)
        n_value = min(request.n or 1, 5)  # Limit to 5 max choices for practical reasons
        
        if n_value > 1:
            # Handle multiple completions case
            response_list = []
            choices = []
            total_input_tokens = 0
            total_output_tokens = 0
            
            try:
                # Generate multiple responses
                for i in range(n_value):
                    # Adjust temperature slightly for variation
                    temp_param = parameters.copy()
                    if 'temperature' in temp_param and temp_param['temperature'] > 0:
                        temp_param['temperature'] = min(temp_param['temperature'] * (1 + i * 0.1), 2.0)
                    
                    # Generate additional responses
                    additional_response = await client.execute(
                        primary_prompt,
                        model_type=model_type,
                        model_name=model_name,
                        **temp_param
                    )
                    
                    # Check for error in response
                    if 'error' in additional_response:
                        logger.error(f"Execution error in completion {i}: {additional_response['error']}")
                        continue
                    
                    response_list.append(additional_response)
                    
                    # Accumulate token counts for usage
                    metrics = additional_response.get('metrics', {})
                    total_input_tokens += metrics.get('input_tokens', 0)
                    total_output_tokens += metrics.get('output_tokens', 0)
                
                # Create choices from responses
                for i, resp in enumerate(response_list):
                    # Determine finish reason
                    finish_reason = "stop"
                    
                    # Check if response was truncated due to max_tokens
                    if request.max_tokens is not None:
                        metrics = resp.get('metrics', {})
                        # If we directly passed max_tokens to the model, look for signs of truncation
                        if resp.get('response', '').endswith('...') or resp.get('response', '').endswith('…'):
                            finish_reason = "length"
                        # If the output tokens are close to max_tokens (within 10%)
                        elif metrics.get('output_tokens', 0) >= (request.max_tokens * 0.9):
                            finish_reason = "length"
                    
                    choices.append(
                        ChatCompletionChoice(
                            index=i,
                            message=ChatMessage(
                                role=ChatRole.ASSISTANT,
                                content=str(resp.get('response', ''))
                            ),
                            finish_reason=finish_reason
                        )
                    )
                
                # Create usage information if token counts are available
                usage = None
                if total_input_tokens and total_output_tokens:
                    usage = ChatCompletionUsage(
                        prompt_tokens=total_input_tokens,
                        completion_tokens=total_output_tokens,
                        total_tokens=total_input_tokens + total_output_tokens
                    )
                
                # Create the response object with multiple choices
                chat_completion = ChatCompletionResponse(
                    id=completion_id,
                    created=int(time.time()),
                    model=request.model,
                    choices=choices,
                    usage=usage
                )
                
                return chat_completion
                
            except Exception as e:
                logger.error(f"Error processing multiple completions: {e}")
                raise HTTPException(status_code=500, detail=f"Error processing multiple completions: {str(e)}")
        else:
            # Handle single completion case (original behavior)
            try:
                # Execute the request using Oblix orchestration with proper error handling
                response = await client.execute(
                    primary_prompt,
                    model_type=model_type,
                    model_name=model_name,
                    **parameters
                )
                
                # Check for error in response
                if 'error' in response:
                    logger.error(f"Execution error: {response['error']}")
                    raise HTTPException(
                        status_code=500, 
                        detail=f"Execution error: {response['error']}"
                    )
                
                # Get metrics if available
                metrics = response.get('metrics', {})
                input_tokens = metrics.get('input_tokens', 0)
                output_tokens = metrics.get('output_tokens', 0)
                
                # Create usage information if token counts are available
                usage = None
                if input_tokens and output_tokens:
                    usage = ChatCompletionUsage(
                        prompt_tokens=input_tokens,
                        completion_tokens=output_tokens,
                        total_tokens=input_tokens + output_tokens
                    )
                
                # Determine finish reason
                finish_reason = "stop"
                
                # Check if response was truncated due to max_tokens
                # Use a different approach to determine if max_tokens was reached
                if request.max_tokens is not None:
                    # If we directly passed max_tokens to the model, look for signs of truncation
                    if len(str(response.get('response', ''))) > 0 and 'metrics' in response:
                        if response['response'].endswith('...') or response['response'].endswith('…'):
                            finish_reason = "length"
                        # If the output tokens are close to max_tokens (within 10%)
                        elif output_tokens >= (request.max_tokens * 0.9):
                            finish_reason = "length"
                
                # Create the response object
                chat_completion = ChatCompletionResponse(
                    id=completion_id,
                    created=int(time.time()),
                    model=request.model,
                    choices=[
                        ChatCompletionChoice(
                            index=0,
                            message=ChatMessage(
                                role=ChatRole.ASSISTANT,
                                content=str(response.get('response', ''))  # Ensure response is a string
                            ),
                            finish_reason=finish_reason
                        )
                    ],
                    usage=usage
                )
                
                return chat_completion
            except Exception as e:
                logger.error(f"Error processing request: {e}")
                raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")
    except HTTPException:
        # Re-raise HTTP exceptions without modification
        raise
    except Exception as e:
        logger.error(f"Unexpected error in chat_completions: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

async def chat_completions_stream(request: ChatCompletionRequest, client: OblixClient):
    """
    Stream chat completions in OpenAI-compatible format
    """
    # Define a variable to hold the state we need to clean up at the end
    execution_result = None
    
    try:
        # Validate model name
        if request.model != "auto" and not request.model.startswith("gpt-") and not request.model.startswith("claude-") and not request.model.startswith("llama"):
            error_chunk = {
                "error": {
                    "message": f"Model '{request.model}' is not supported. Use 'auto' for Oblix orchestration.",
                    "type": "invalid_request_error",
                    "code": 400
                }
            }
            yield f"data: {json.dumps(error_chunk)}\n\n"
            yield "data: [DONE]\n\n"
            return
        
        # Validate messages
        if not request.messages:
            error_chunk = {
                "error": {
                    "message": "'messages' array must not be empty",
                    "type": "invalid_request_error",
                    "code": 400
                }
            }
            yield f"data: {json.dumps(error_chunk)}\n\n"
            yield "data: [DONE]\n\n"
            return
        
        # Always use orchestration - don't parse model parameter
        # Regardless of what model name is provided, use orchestration
        model_type = None  # Let Oblix orchestration decide
        model_name = None  # No specific model
        
        # Prepare context format that Oblix expects
        context = []
        combined_prompt = ""
        
        # Convert OpenAI-style messages to context array for Oblix
        for msg in request.messages:
            context.append({
                "role": msg.role,
                "content": msg.content
            })
            # For system and user messages, also add to the combined prompt
            if msg.role in [ChatRole.SYSTEM, ChatRole.USER]:
                prefix = f"{msg.role.value.capitalize()}: " if msg.role != ChatRole.SYSTEM else ""
                combined_prompt += f"{prefix}{msg.content}\n"
        
        # Extract the last user message as the primary prompt
        last_user_msg = next((msg for msg in reversed(request.messages) 
                             if msg.role == ChatRole.USER), None)
        
        if last_user_msg:
            primary_prompt = last_user_msg.content
        else:
            # Fallback if no user message is found
            primary_prompt = combined_prompt or "Hello"
        
        # Prepare parameters
        parameters = {
            "context": context,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
            "stream": True  # Ensure streaming is enabled
        }
        
        # Add additional parameters if provided
        if request.top_p is not None:
            parameters["top_p"] = request.top_p
        if request.presence_penalty is not None:
            parameters["presence_penalty"] = request.presence_penalty
        if request.frequency_penalty is not None:
            parameters["frequency_penalty"] = request.frequency_penalty
        
        # Get a unique ID for this streaming session
        completion_id = str(uuid.uuid4())
        
        # Create the first chunk with role
        first_chunk = ChatCompletionChunk(
            id=completion_id,
            created=int(time.time()),
            model=request.model,
            choices=[
                ChatCompletionChunkChoice(
                    index=0,
                    delta=ChatCompletionChunkDelta(
                        role=ChatRole.ASSISTANT
                    ),
                    finish_reason=None
                )
            ]
        )
        
        # Yield the first chunk
        yield f"data: {first_chunk.json()}\n\n"
        
        # Log that we're starting execution
        logger.info(f"Starting streaming execution with ID: {completion_id}")
        
        # Execute the request using Oblix streaming
        execution_result = await client.execution_manager.execute(
            primary_prompt,
            model_type=model_type,
            model_name=model_name,
            parameters=parameters
        )
        
        # Check for error in the execution result
        if 'error' in execution_result:
            error_message = execution_result.get('error', 'Unknown error')
            logger.error(f"Execution error in streaming: {error_message}")
            
            # Create an error chunk
            error_chunk = {
                "error": {
                    "message": error_message,
                    "type": "server_error",
                    "code": 500
                }
            }
            
            yield f"data: {json.dumps(error_chunk)}\n\n"
            yield "data: [DONE]\n\n"
            return
        
        # Extract streaming content if available
        if 'stream' not in execution_result:
            logger.error("No stream content in execution result")
            yield f"data: {json.dumps({'error': 'No stream content available'})}\n\n"
            yield "data: [DONE]\n\n"
            return
            
        # Define a robust streaming iterator
        async def safe_stream_iterator():
            stream = execution_result['stream']
            try:
                # Use a more robust approach - handle chunks in batches to avoid closing event loop
                async for token in stream:
                    # Yield each token with proper error handling
                    yield token
            except Exception as e:
                logger.error(f"Error in stream iterator: {e}")
                # Return an error indicator that we can detect
                yield f"\nERROR: {str(e)}"
            
        # Use our safe stream iterator
        try:
            async for token in safe_stream_iterator():
                # Check if token is an error message
                if isinstance(token, str) and token.startswith("\nERROR:"):
                    logger.error(f"Error token received: {token}")
                    # Create an error chunk
                    error_chunk = ChatCompletionChunk(
                        id=completion_id,
                        created=int(time.time()),
                        model=request.model,
                        choices=[
                            ChatCompletionChunkChoice(
                                index=0,
                                delta=ChatCompletionChunkDelta(
                                    content=f"Error during streaming: {token}"
                                ),
                                finish_reason="error"
                            )
                        ]
                    )
                    yield f"data: {error_chunk.json()}\n\n"
                    continue
                
                # Create a normal chunk for the token
                chunk = ChatCompletionChunk(
                    id=completion_id,
                    created=int(time.time()),
                    model=request.model,
                    choices=[
                        ChatCompletionChunkChoice(
                            index=0,
                            delta=ChatCompletionChunkDelta(
                                content=token
                            ),
                            finish_reason=None
                        )
                    ]
                )
                
                # Yield the chunk
                yield f"data: {chunk.json()}\n\n"
        except Exception as e:
            # Log the error
            logger.error(f"Error during token streaming: {e}")
        
        # Send the final chunk with finish_reason
        final_chunk = ChatCompletionChunk(
            id=completion_id,
            created=int(time.time()),
            model=request.model,
            choices=[
                ChatCompletionChunkChoice(
                    index=0,
                    delta=ChatCompletionChunkDelta(),
                    finish_reason="stop"
                )
            ]
        )
        
        yield f"data: {final_chunk.json()}\n\n"
        
        # Send the [DONE] message to indicate end of stream
        yield "data: [DONE]\n\n"
        
    except Exception as e:
        # Log the detailed error
        logger.error(f"Unhandled exception in streaming: {e}", exc_info=True)
        
        # Create an error chunk with detailed information
        error_chunk = {
            "error": {
                "message": f"Streaming error: {str(e)}",
                "type": "server_error",
                "code": 500
            }
        }
        
        yield f"data: {json.dumps(error_chunk)}\n\n"
        yield "data: [DONE]\n\n"
    finally:
        # Clean up resources if needed
        # This is important to prevent resource leaks and event loop issues
        if execution_result and 'model_instance' in execution_result:
            model_instance = execution_result.get('model_instance')
            if hasattr(model_instance, '_session') and model_instance._session:
                try:
                    if not model_instance._session.closed:
                        logger.info(f"Cleaning up session for model {model_instance.model_name}")
                        # Use asyncio.create_task to avoid blocking
                        import asyncio
                        asyncio.create_task(model_instance._session.close())
                except Exception as cleanup_error:
                    logger.warning(f"Error cleaning up session: {cleanup_error}")