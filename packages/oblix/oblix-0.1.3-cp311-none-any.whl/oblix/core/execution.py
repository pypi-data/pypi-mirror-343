# app/core/execution.py
from typing import Dict, Any, Optional, List
import logging
import uuid

from oblix.models.base import BaseModel, ModelType
from oblix.agents.base import BaseAgent
from oblix.agents.resource_monitor import ResourceMonitor
from oblix.agents.resource_monitor.policies import ResourceState, ExecutionTarget
from oblix.agents.connectivity import BaseConnectivityAgent
from oblix.agents.connectivity.policies import (
    ConnectivityPolicy, 
    ConnectivityPolicyResult, 
    ConnectionTarget, 
    ConnectivityState
)
from oblix.agents.connectivity.actions import ConnectivityAction

logger = logging.getLogger(__name__)

class ExecutionManager:
    def __init__(self):
        """
        Initialize Execution Manager with connectivity support
        
        Manages models, agents, and execution flow with resource and 
        connectivity-aware routing
        """
        self.models: Dict[ModelType, Dict[str, BaseModel]] = {
            ModelType.OLLAMA: {},
            ModelType.OPENAI: {},
            ModelType.CLAUDE: {},
            ModelType.CUSTOM: {}
        }
        self.agents: List[BaseAgent] = []
        self.resource_monitor: Optional[ResourceMonitor] = None
        
        # New connectivity-related attributes
        self.connectivity_monitor: Optional[BaseConnectivityAgent] = None
        self.connectivity_policy = ConnectivityPolicy()
        self.connectivity_action_handler = ConnectivityAction()
    
    def register_model(self, model: BaseModel):
        """
        Register a new model
        
        :param model: Model to register
        """
        model_type = model.model_type
        model_name = model.model_name
        
        if model_type not in self.models:
            raise ValueError(f"Invalid model type: {model_type}")
        
        self.models[model_type][model_name] = model
        logger.info(f"Registered model: {model_type}/{model_name}")
        
    def register_agent(self, agent: BaseAgent):
        """
        Register a new agent with special handling for specific agent types
        
        :param agent: Agent to register
        """
        # Existing agent registration logic
        if isinstance(agent, ResourceMonitor):
            self.resource_monitor = agent
            logger.info("Registered ResourceMonitor agent")
        
        # Add connectivity monitor registration
        if isinstance(agent, BaseConnectivityAgent):
            self.connectivity_monitor = agent
            logger.info("Registered ConnectivityMonitor agent")
        
        self.agents.append(agent)
        logger.info(f"Registered agent: {agent.name}")
    
    async def execute(
        self, 
        prompt: str, 
        model_type: Optional[ModelType] = None,
        model_name: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute a prompt with resource and connectivity-aware routing
        
        :param prompt: Input prompt
        :param model_type: Specific model type to use
        :param model_name: Specific model name to use
        :param parameters: Generation parameters specified by user
        :return: Execution result with response and metadata
        """
        request_id = str(uuid.uuid4())
        parameters = parameters or {}
        
        # Initialize response tracking
        execution_metadata = {
            'request_id': request_id,
            'agent_checks': [],
            'routing_decision': {
                'resource_routing': None,
                'connectivity_routing': None
            },
            'selected_model': None
        }
        
        try:
            # Using asyncio.gather to run checks concurrently and safely
            import asyncio
            
            # Prepare coroutines to run concurrently
            tasks = []
            resource_routing = None
            connectivity_routing = None
            connectivity_metrics = None
            
            # Add resource monitor task if available
            if self.resource_monitor:
                tasks.append(('resource_monitor', self.resource_monitor.check(prompt=prompt)))
            
            # Add connectivity monitor task if available
            if self.connectivity_monitor:
                tasks.append(('connectivity_monitor', self.connectivity_monitor.measure_connection_metrics()))
            
            # Run tasks concurrently and safely
            if tasks:
                results = {}
                for name, task in tasks:
                    try:
                        results[name] = await task
                    except Exception as e:
                        logger.warning(f"{name} check failed: {e}")
                        results[name] = None
                
                # Process resource monitor results
                if 'resource_monitor' in results and results['resource_monitor']:
                    resource_check = results['resource_monitor']
                    execution_metadata['agent_checks'].append({
                        'agent': 'resource_monitor',
                        'result': resource_check
                    })
                    # Store routing info from resource check - these are already string values
                    resource_routing = {
                        'target': resource_check.get('target'),
                        'state': resource_check.get('state'),
                        'reason': resource_check.get('reason')
                    }
                    execution_metadata['routing_decision']['resource_routing'] = resource_routing
                
                # Process connectivity monitor results
                if 'connectivity_monitor' in results and results['connectivity_monitor']:
                    try:
                        connectivity_metrics = results['connectivity_monitor']
                        
                        # Evaluate connectivity policy
                        connectivity_policy_result = self.connectivity_policy.evaluate(connectivity_metrics)
                        
                        # Execute connectivity actions
                        connectivity_action_result = await self.connectivity_action_handler.execute(
                            connectivity_policy_result
                        )
                        
                        execution_metadata['agent_checks'].append({
                            'agent': 'connectivity_monitor',
                            'result': connectivity_action_result
                        })
                        
                        connectivity_routing = {
                            'state': connectivity_policy_result.state.value,
                            'target': connectivity_policy_result.target.value,
                            'reason': connectivity_policy_result.reason
                        }
                        execution_metadata['routing_decision']['connectivity_routing'] = connectivity_routing
                    except Exception as e:
                        logger.warning(f"Connectivity policy evaluation failed: {e}")
            
            # Determine model type and target based purely on routing decisions
            # Ignore any input model_type and model_name parameters
            final_model_type = None
            final_model_name = None
            
            # Priority order for model selection:
            # 1. Connectivity routing recommendation (highest priority, especially for disconnected state)
            # 2. Resource routing recommendation
            # 3. Default fallback
            
            # Ensure string values for consistent dictionary comparisons
            disconnected_state = ConnectivityState.DISCONNECTED.value
            cloud_target = ExecutionTarget.CLOUD.value
            local_target = ConnectionTarget.LOCAL.value
            
            # Log the routing decisions for debugging - we'll format this better in the client
            logger.debug(f"Routing decisions - Resource: {resource_routing}, Connectivity: {connectivity_routing}")
            
            # Check if we're disconnected first
            if (connectivity_routing and 
                connectivity_routing.get('state') == disconnected_state):
                # Force local fallback when disconnected from internet
                # Always use local model when disconnected since cloud is unreachable
                final_model_type = ModelType.OLLAMA
                logger.info("Selecting local model due to connectivity state: DISCONNECTED")
            # Then check if resources are constrained
            elif (resource_routing and 
                  resource_routing.get('target') == cloud_target):
                # Determine which cloud models are available and prefer Claude if available
                claude_available = bool(self.models[ModelType.CLAUDE])
                openai_available = bool(self.models[ModelType.OPENAI])
                
                if claude_available:
                    final_model_type = ModelType.CLAUDE
                elif openai_available:
                    final_model_type = ModelType.OPENAI
                else:
                    final_model_type = ModelType.OLLAMA  # Fallback to local if no cloud models
                    
                logger.info(f"Selecting {final_model_type.value} model due to resource target: {cloud_target}")
            # Finally check connectivity preference for local
            elif (connectivity_routing and 
                  connectivity_routing.get('target') == local_target):
                final_model_type = ModelType.OLLAMA
                logger.info(f"Selecting local model due to connectivity target: {local_target}")
            else:
                # Default to first available model type
                final_model_type = next(iter(self.models.keys()))
                logger.info(f"Selecting default model type: {final_model_type}")
            
            # Select the model based on the determined type
            model = self._select_model(final_model_type, final_model_name)
                
            if not model:
                logger.error(f"No model found for type {final_model_type}")
                return {
                    **execution_metadata,
                    'error': 'No suitable model found'
                }
            
            execution_metadata['selected_model'] = f"{model.model_type.value}:{model.model_name}"
            
            # Check if streaming is requested
            is_streaming = parameters.get('stream', False)
            
            if is_streaming:
                # Handle streaming response with a more robust approach
                # Create a wrapper for the stream generator that preserves the event loop context
                async def robust_stream_generator():
                    try:
                        # Create the generator in this function's event loop context
                        stream_gen = model.generate_streaming(prompt, **parameters)
                        
                        # Stream each token using the same event loop context
                        async for token in stream_gen:
                            yield token
                            
                    except Exception as e:
                        logger.error(f"Streaming error in robust generator: {e}")
                        # Return an error token that the client can handle
                        yield f"\nError during streaming: {str(e)}"
                        
                # Return the wrapped generator that maintains event loop context
                return {
                    **execution_metadata,
                    'model_id': f"{model.model_type.value}:{model.model_name}",
                    'stream': robust_stream_generator(),  # Use our wrapped generator
                    'connectivity_metrics': connectivity_metrics,
                    'model_instance': model  # Pass the model instance for metrics retrieval after streaming
                }
            else:
                # Generate regular response
                response = await model.generate(prompt, **parameters)
                
                # Extract metrics from model response if available
                metrics = {}
                if hasattr(model, 'last_metrics') and model.last_metrics:
                    metrics = model.last_metrics
                
                # Add timing metrics if not already included
                if 'total_latency' not in metrics and hasattr(model, 'last_generation_time'):
                    metrics['total_latency'] = model.last_generation_time
                
                return {
                    **execution_metadata,
                    'model_id': f"{model.model_type.value}:{model.model_name}",
                    'response': response,
                    'metrics': metrics,
                    'connectivity_metrics': connectivity_metrics
                }
        
        except Exception as e:
            logger.error(f"Execution error: {e}")
            return {
                **execution_metadata,
                'error': str(e)
            }
    
    def _select_model(
        self, 
        model_type: Optional[ModelType] = None, 
        model_name: Optional[str] = None
    ) -> Optional[BaseModel]:
        """
        Select a model based on given criteria
        
        :param model_type: Specific model type to select from
        :param model_name: Specific model name to select
        :return: Selected model or None
        """
        # If specific model type and name provided
        if model_type and model_name:
            model = self.models.get(model_type, {}).get(model_name)
            if not model:
                logger.warning(f"Requested specific model {model_type.value}:{model_name} not found")
            return model
        
        # If only model type provided
        if model_type:
            # If looking for a cloud model type (Claude or OpenAI)
            if model_type in [ModelType.CLAUDE, ModelType.OPENAI]:
                # For CLAUDE type, first check if there are any Claude models
                if model_type == ModelType.CLAUDE and self.models[ModelType.CLAUDE]:
                    claude_models = self.models[ModelType.CLAUDE]
                    if claude_models:
                        model_name = next(iter(claude_models.keys()))
                        selected_model = claude_models[model_name]
                        return selected_model
                    
                # For OPENAI type or if no Claude models found, check for OpenAI models
                elif model_type == ModelType.OPENAI and self.models[ModelType.OPENAI]:
                    openai_models = self.models[ModelType.OPENAI]
                    if openai_models:
                        model_name = next(iter(openai_models.keys()))
                        selected_model = openai_models[model_name]
                        return selected_model
                        
                # If requested cloud model type has no models, try the other cloud type
                if model_type == ModelType.CLAUDE and self.models[ModelType.OPENAI]:
                    # Fall back to OpenAI if Claude was requested but not available
                    openai_models = self.models[ModelType.OPENAI]
                    if openai_models:
                        model_name = next(iter(openai_models.keys()))
                        selected_model = openai_models[model_name]
                        return selected_model
                        
                elif model_type == ModelType.OPENAI and self.models[ModelType.CLAUDE]:
                    # Fall back to Claude if OpenAI was requested but not available
                    claude_models = self.models[ModelType.CLAUDE]
                    if claude_models:
                        model_name = next(iter(claude_models.keys()))
                        selected_model = claude_models[model_name]
                        return selected_model
            else:
                # For non-cloud models (like Ollama), use standard selection
                models = self.models.get(model_type, {})
                if models:
                    selected = next(iter(models.values()))
                    return selected
            
            # If we get here, no models were found for the requested type
            logger.warning(f"No models available for type: {model_type.value}")
            return None
        
        # If no model type specified, try to find any available model
        # First try Claude, then OpenAI, then Ollama, then Custom
        for preferred_type in [ModelType.CLAUDE, ModelType.OPENAI, ModelType.OLLAMA, ModelType.CUSTOM]:
            models = self.models.get(preferred_type, {})
            if models:
                selected = next(iter(models.values()))
                return selected
        
        logger.warning("No models available at all")
        return None