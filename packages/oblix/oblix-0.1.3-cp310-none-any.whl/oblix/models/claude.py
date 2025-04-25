# oblix/models/claude.py
from typing import Dict, Any, Optional, AsyncGenerator, List
import logging
import anthropic
import time
import traceback
from anthropic import Anthropic, APIError, APIConnectionError, AuthenticationError
import tiktoken
import time
from oblix.models.base import BaseModel, ModelType
from oblix.monitoring.metrics import (
    PerformanceMonitor,
    ModelMetricsCollector,
    PerformanceMetrics
)

logger = logging.getLogger(__name__)

class ClaudeModel(BaseModel):
    """
    Claude (Anthropic) model implementation with performance monitoring
    """
    
    def __init__(self, model_name: str, api_key: str, max_tokens: Optional[int] = None):
        """
        Initialize Claude model
        
        Args:
            model_name (str): Name of the Claude model (e.g., "claude-3-opus-20240229")
            api_key (str): Anthropic API key
            max_tokens (Optional[int]): Maximum tokens for response generation
        """
        super().__init__(ModelType.CLAUDE, model_name)
        
        # Use the full model name as is - don't strip the date suffix
        self.api_model_name = model_name
        logger.debug(f"Using full model name: {self.api_model_name}")
            
        self.client = anthropic.Anthropic(api_key=api_key)
        self.max_tokens = max_tokens or 4096  # Default max tokens
        self.metrics_collector = ModelMetricsCollector()
        
        # Initialize tokenizer for token counting
        # Using cl100k_base as it's close to Claude's tokenizer
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        
        # Validate the model name to ensure it follows Claude naming conventions
        self._validate_model_name(model_name)
    
    def _validate_model_name(self, model_name: str) -> None:
        """Validate the provided model name against supported Claude models"""
        # Known supported model naming patterns
        if model_name.startswith("claude-"):
            # Accept all Claude models with the standard prefix
            # This allows new models to work without code changes
            return
        else:
            # If model doesn't follow Claude naming convention
            raise ValueError(
                f"Unsupported Claude model: {model_name}. "
                f"Model name should start with 'claude-'"
            )

    def count_tokens(self, text: str) -> int:
        """Count tokens in text using the tokenizer"""
        return len(self.tokenizer.encode(text))

    async def initialize(self) -> bool:
        """Initialize the Claude model and verify API access"""
        try:
            # Print available Claude models from the API
            logger.debug(f"Initializing Claude model: {self.model_name}")
            logger.debug(f"Using Claude API key: {self.client.api_key[:8]}...")
            
            # Print current client version
            logger.debug(f"Using Anthropic client version: {anthropic.__version__}")
            
            # Test API key with a minimal request
            try:
                # List available models
                logger.debug("Trying to list available models...")
                if hasattr(self.client, 'models') and hasattr(self.client.models, 'list'):
                    models = self.client.models.list()
                    logger.debug(f"Available Claude models: {[m.id for m in models.data]}")
            except Exception as e:
                logger.debug(f"Failed to list models: {e}")
            
            # Test API key with a minimal request
            logger.debug(f"Testing model with minimal request using API model name: {self.api_model_name}")
            test_response = self.client.messages.create(
                model=self.api_model_name,
                max_tokens=10,
                messages=[{
                    "role": "user",
                    "content": "Test message for initialization"
                }]
            )
            
            if test_response:
                self.is_ready = True
                logger.info(f"Successfully initialized Claude model: {self.model_name}")
                return True
                
        except Exception as e:
            logger.error(f"Error initializing Claude model: {e}")
            # More detailed error information
            import traceback
            logger.debug(f"Initialization error details: {traceback.format_exc()}")
            return False

    async def generate(self, 
                      prompt: str, 
                      request_id: Optional[str] = None,
                      context: Optional[List[Dict[str, Any]]] = None,
                      **kwargs) -> Dict[str, Any]:
        """
        Generate a response with performance metrics
        
        Args:
            prompt: Input prompt for generation
            request_id: Optional identifier for tracking metrics
            context: Optional conversation context (list of message objects)
            **kwargs: Additional generation parameters
        
        Returns:
            Dict containing:
            - response: Generated text
            - metrics: Performance metrics
        """
        if not self.is_ready:
            raise RuntimeError("Model not initialized. Call initialize() first.")

        monitor = PerformanceMonitor()
        
        try:
            # Count input tokens from prompt
            input_tokens = self.count_tokens(prompt)
            
            # Count tokens from context messages if provided
            if context:
                for msg in context:
                    content = msg.get('content', '')
                    if content:
                        input_tokens += self.count_tokens(content)
            
            # Start monitoring
            monitor.start_monitoring()
            
            # Extract the context parameter from kwargs if needed
            if context is None and 'context' in kwargs:
                context = kwargs.get('context')
            
            # Create a cleaned copy of kwargs by removing parameters that are not supported by Anthropic's API
            generation_kwargs = kwargs.copy()
            
            # Remove parameters that shouldn't be passed to Anthropic's create method
            params_to_remove = [
                'request_id', 
                'model_type',
                'model_name',
                'context'  # We handle context separately
            ]
            
            for param in params_to_remove:
                generation_kwargs.pop(param, None)
            
            # Prepare messages with context
            messages = []
            
            # Add previous context messages
            if context:
                # Carefully process context messages
                messages.extend([
                    {
                        "role": msg.get('role', 'user'),
                        "content": str(msg.get('content', ''))
                    } for msg in context 
                    if msg.get('content')
                ])
            
            # Add current prompt
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            # Prepare default parameters
            params = {
                "model": self.api_model_name,
                "messages": messages,
                "max_tokens": self.max_tokens,
                **generation_kwargs
            }
            
            # Generate response
            response = self.client.messages.create(**params)
            
            # Get response text
            response_text = response.content[0].text
            
            # Mark first token time BEFORE stopping monitoring
            # This ensures time_to_first_token is different from total_latency
            # For non-streaming, we approximate it as 25% of total time
            start_time = monitor._start_time or time.time()
            elapsed = time.time() - start_time
            monitor._first_token_time = start_time + (elapsed * 0.25)
            
            # Stop monitoring
            monitor.stop_monitoring()
            
            # Count output tokens
            output_tokens = self.count_tokens(response_text)
            
            # Calculate metrics
            metrics = monitor.calculate_metrics(
                model_name=self.model_name,
                model_type=self.model_type.value,
                input_tokens=input_tokens,
                output_tokens=output_tokens
            )
            
            # Store metrics if request_id is provided
            if request_id:
                self.metrics_collector.add_metrics(request_id, metrics)
            
            return {
                "response": response_text,
                "metrics": metrics.to_dict()
            }
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise

    async def generate_streaming(
        self,
        prompt: str,
        request_id: Optional[str] = None,
        context: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """
        Generate a streaming response with the Claude model
        
        Args:
            prompt: Input prompt for generation
            request_id: Optional identifier for tracking metrics
            context: Optional conversation context (list of message objects)
            **kwargs: Additional generation parameters
        
        Yields:
            Each token as it's generated
        """
        if not self.is_ready:
            raise RuntimeError("Model not initialized. Call initialize() first.")
        
        self.last_metrics = {}  # We'll store metrics here
        
        try:
            # Count input tokens from prompt
            input_tokens = self.count_tokens(prompt)
            
            # Count tokens from context messages if provided
            if context:
                for msg in context:
                    content = msg.get('content', '')
                    if content:
                        input_tokens += self.count_tokens(content)
            
            # Start performance monitoring
            monitor = PerformanceMonitor()
            monitor.start_monitoring()
            
            # Create a cleaned copy of kwargs by removing parameters that are not supported by Anthropic's API
            generation_kwargs = kwargs.copy()
            
            # Extract the context parameter from kwargs if needed
            if context is None and 'context' in kwargs:
                context = kwargs.get('context')
            
            # Remove parameters that shouldn't be passed to Anthropic's stream method
            params_to_remove = [
                'request_id', 
                'stream',
                'model_type',
                'model_name',
                'context'  # We handle context separately
            ]
            
            for param in params_to_remove:
                generation_kwargs.pop(param, None)
            
            # Prepare messages with context
            messages = []
            
            # Add previous context messages
            if context:
                for msg in context:
                    role = msg.get('role', 'user')
                    content = msg.get('content', '')
                    
                    if content:
                        messages.append({
                            "role": role,
                            "content": content
                        })
            
            # Add current prompt as user message
            messages.append({"role": "user", "content": prompt})
            
            # Prepare parameters accepted by Anthropic API
            params = {
                "model": self.api_model_name,
                "messages": messages,
                "max_tokens": self.max_tokens
            }
            
            # Add supported parameters from the cleaned kwargs
            # Be selective about which parameters we pass to avoid unexpected parameter errors
            supported_params = [
                "temperature", 
                "top_p", 
                "top_k",
                "stop",
                "system"
            ]
            
            for param in supported_params:
                if param in generation_kwargs:
                    params[param] = generation_kwargs[param]
            
            # Generate streaming response
            full_response = ""
            first_token_received = False
            
            # Create a streaming message - stream() already implies streaming mode
            with self.client.messages.stream(**params) as stream:
                for text in stream.text_stream:
                    # Mark first token time if this is the first token
                    if not first_token_received:
                        logger.info("Received first token in Claude streaming response")
                        monitor.mark_first_token()
                        first_token_received = True
                        # Store timestamp for debugging
                        self.first_token_received_at = time.time()
                        
                    full_response += text
                    yield text
            
            # Count tokens properly on the complete response - avoid using a simple increment counter
            output_tokens = self.count_tokens(full_response)
            
            # Stop monitoring
            monitor.stop_monitoring()
            
            # Ensure first token time is valid
            if not monitor._first_token_time:
                logger.warning("First token time was not properly set during Claude streaming")
                # Estimate a reasonable value if missing
                start_time = monitor._start_time or time.time()
                elapsed = monitor._end_time - start_time
                monitor._first_token_time = start_time + (elapsed * 0.15)  # Assume 15% of total time
            
            # Calculate metrics
            metrics = monitor.calculate_metrics(
                model_name=self.model_name,
                model_type=self.model_type.value,
                input_tokens=input_tokens,
                output_tokens=output_tokens
            )
            
            # Log the key metrics for debugging
            logger.info(f"Claude streaming metrics - TTFT: {metrics.time_to_first_token:.3f}s, " +
                     f"Total Latency: {metrics.total_latency:.3f}s")
            
            # Store metrics if request_id is provided
            if request_id:
                self.metrics_collector.add_metrics(request_id, metrics)
                
            # Store metrics for later retrieval
            self.last_metrics = metrics.to_dict()
                
        except Exception as e:
            logger.error(f"Error generating streaming response: {e}")
            yield f"\nError: {str(e)}"
            raise

    async def shutdown(self) -> None:
        """Clean up resources and shut down the model"""
        self.is_ready = False
        logger.info(f"Shut down Claude model: {self.model_name}")