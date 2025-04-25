# oblix/models/ollama.py
import aiohttp
from typing import Dict, Any, Optional, List, AsyncGenerator
import logging
import json
import tiktoken
import time
from oblix.models.base import BaseModel, ModelType
from oblix.monitoring.metrics import (
    PerformanceMonitor,
    ModelMetricsCollector,
    PerformanceMetrics
)

logger = logging.getLogger(__name__)

class OllamaModel(BaseModel):
    """
    Ollama model implementation with performance monitoring
    """
    
    def __init__(self, model_name: str, endpoint: str = "http://localhost:11434"):
        """
        Initialize Ollama model
        
        Args:
            model_name: Name of the Ollama model
            endpoint: Ollama API endpoint URL
        """
        super().__init__(ModelType.OLLAMA, model_name)
        self.endpoint = endpoint.rstrip('/')
        self._session: Optional[aiohttp.ClientSession] = None
        self.metrics_collector = ModelMetricsCollector()
        
        # Initialize tokenizer for approximate token counting
        # Using cl100k_base as it's similar to many modern models
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        
    def count_tokens(self, text: str) -> int:
        """Count tokens in text using the tokenizer"""
        return len(self.tokenizer.encode(text))

    async def initialize(self) -> bool:
        """
        Initialize the model and verify Ollama server connection
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            # Create HTTP session
            self._session = aiohttp.ClientSession()
            
            # Test connection and check model availability
            async with self._session.get(f"{self.endpoint}/api/tags") as response:
                if response.status != 200:
                    logger.error(f"Failed to connect to Ollama server: {await response.text()}")
                    return False
                    
                # Parse available models
                data = await response.json()
                available_models = [model.get('name', '') for model in data.get('models', [])]
                
                if self.model_name not in available_models:
                    # Log at info level instead of warning to avoid cluttering the CLI output
                    logger.info(f"Attempting to pull model {self.model_name}")
                    
                    # Try to pull the model
                    pull_success = await self._pull_model()
                    if not pull_success:
                        return False
            
            self.is_ready = True
            logger.debug(f"Successfully initialized Ollama model: {self.model_name}")
            return True
            
        except aiohttp.ClientError as e:
            logger.error(f"Connection error initializing Ollama model: {e}")
            return False
        except Exception as e:
            logger.error(f"Error initializing Ollama model: {e}")
            return False

    async def _pull_model(self) -> bool:
        """Pull the model from Ollama server"""
        try:
            async with self._session.post(
                f"{self.endpoint}/api/pull",
                json={"name": self.model_name}
            ) as response:
                if response.status != 200:
                    logger.error(f"Failed to pull model {self.model_name}")
                    return False
                    
                logger.info(f"Successfully pulled model {self.model_name}")
                return True
                
        except Exception as e:
            logger.error(f"Error pulling model {self.model_name}: {e}")
            return False

    async def generate(
        self,
        prompt: str,
        request_id: Optional[str] = None,
        context: Optional[List[Dict[str, Any]]] = None,
        use_gpu: bool = False,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stop: Optional[list] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate a response using the Ollama model with performance metrics
        
        Args:
            prompt: Input prompt for generation
            request_id: Optional identifier for tracking metrics
            context: Optional conversation context (list of message objects)
            use_gpu: Whether to use GPU for inference
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            stop: List of strings that will stop generation if encountered
            **kwargs: Additional generation parameters
        
        Returns:
            Dict containing:
            - response: Generated text
            - metrics: Performance metrics
            
        Raises:
            RuntimeError: If model is not initialized
            Exception: If generation fails
        """
        if not self.is_ready:
            raise RuntimeError("Model not initialized. Call initialize() first.")

        monitor = PerformanceMonitor()
        
        try:
            # Prepare structured messages for the conversation
            messages = []
            
            # Add previous context messages if provided
            if context:
                for msg in context:
                    # Ensure the message has required fields
                    role = msg.get('role', 'user')
                    content = msg.get('content', '')
                    
                    # Only add non-empty messages
                    if content:
                        messages.append({
                            "role": role,
                            "content": content
                        })
            
            # Add the current prompt as a user message
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            # Count input tokens for metrics
            input_tokens = self.count_tokens(prompt)
            if context:
                # Add tokens from context for more accurate metrics
                for msg in context:
                    content = msg.get('content', '')
                    if content:
                        input_tokens += self.count_tokens(content)
            
            # Prepare generation parameters
            params = {
                "model": self.model_name,
                "messages": messages,
                "stream": False,
                "temperature": temperature,
                **kwargs
            }
            
            # Add optional parameters
            if max_tokens is not None:
                params["num_predict"] = max_tokens
            if stop:
                params["stop"] = stop
            if use_gpu:
                params["options"] = {"gpu": True, **(params.get("options", {}))}
            
            # Start monitoring
            monitor.start_monitoring()
            
            # Use the chat endpoint instead of generate for structured messages
            async with self._session.post(
                f"{self.endpoint}/api/chat",
                json=params
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Ollama API error: {error_text}")
                
                # Parse the response JSON
                response_data = await response.json()
                
                # Extract the assistant's message
                response_text = response_data.get('message', {}).get('content', '')
                if not response_text:
                    raise Exception("No valid response content received from Ollama")
                
                # Mark first token time BEFORE stopping monitoring
                # This ensures time_to_first_token is different from total_latency
                # For non-streaming, we approximate it as 30% of total time
                start_time = monitor._start_time or time.time()
                elapsed = time.time() - start_time
                monitor._first_token_time = start_time + (elapsed * 0.3)
                
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

        except aiohttp.ClientError as e:
            logger.error(f"Connection error during generation: {e}")
            raise
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise

    async def shutdown(self) -> None:
        """Clean up resources and close connections"""
        if self._session:
            await self._session.close()
        self.is_ready = False
        logger.info(f"Shut down Ollama model: {self.model_name}")
        
    async def generate_streaming(
    self,
    prompt: str,
    request_id: Optional[str] = None,
    context: Optional[List[Dict[str, Any]]] = None,
    use_gpu: bool = False,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    stop: Optional[list] = None,
    **kwargs
) -> AsyncGenerator[str, None]:
        """
        Generate a streaming response from the Ollama model
        
        Yields tokens as they are generated, rather than waiting for the complete response.
        
        Args:
            prompt: Input prompt for generation
            request_id: Optional identifier for tracking metrics
            context: Optional conversation context
            use_gpu: Whether to use GPU for inference
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            stop: List of strings that will stop generation if encountered
            **kwargs: Additional generation parameters
        
        Yields:
            Each token as it's generated
        """
        if not self.is_ready:
            raise RuntimeError("Model not initialized. Call initialize() first.")
        
        self.last_metrics = {}  # We'll store metrics here
        
        # Start performance monitoring
        monitor = PerformanceMonitor()
        monitor.start_monitoring()
        
        # Initialize token count
        input_tokens = self.count_tokens(prompt)
        
        # Count tokens from context messages if provided
        if context:
            for msg in context:
                content = msg.get('content', '')
                if content:
                    input_tokens += self.count_tokens(content)
        
        # Use a list to accumulate response pieces instead of string concatenation
        response_chunks = []
        first_token_received = False
                    
        try:
            # Prepare structured messages for the conversation
            messages = []
            
            # Add previous context messages if provided
            if context:
                for msg in context:
                    role = msg.get('role', 'user')
                    content = msg.get('content', '')
                    
                    if content:
                        messages.append({
                            "role": role,
                            "content": content
                        })
            
            # Add the current prompt as a user message
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            # Create a cleaned copy of kwargs by removing parameters that are not supported by Ollama's API
            generation_kwargs = kwargs.copy()
            
            # Remove parameters that shouldn't be passed to Ollama's stream method
            params_to_remove = [
                'request_id', 
                'model_type',
                'model_name',
                'context'  # We handle context separately
            ]
            
            for param in params_to_remove:
                generation_kwargs.pop(param, None)
            
            # Prepare generation parameters
            params = {
                "model": self.model_name,
                "messages": messages,
                "stream": True,  # Ensure streaming is enabled
                "temperature": temperature
            }
            
            # Add optional parameters
            if max_tokens is not None:
                params["num_predict"] = max_tokens
            if stop:
                params["stop"] = stop
            if use_gpu:
                params["options"] = {"gpu": True, **(params.get("options", {}))}
                
            # Add any remaining supported parameters
            for key, value in generation_kwargs.items():
                params[key] = value
            
            # Use the chat endpoint with streaming - using async with to ensure proper cleanup
            # Add timeout to prevent hanging connections (120s total timeout, 10s connection timeout)
            
            async with self._session.post(
                f"{self.endpoint}/api/chat",
                json=params,
                headers={"Accept": "application/json, application/x-ndjson"},
                timeout=aiohttp.ClientTimeout(total=120, connect=10)
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Ollama API error: {error_text}")
                
                # Use a more efficient buffer implementation with io.BytesIO
                from io import BytesIO
                buffer = BytesIO()
                line_buffer = []
                
                chunk_count = 0
                
                try:
                    async for chunk in response.content:
                        # Append chunk to buffer
                        chunk_count += 1
                            
                        buffer.write(chunk)
                        buffer_value = buffer.getvalue()
                        
                        if b"\n" in buffer_value:
                            # Split on newlines but keep incomplete lines
                            lines = buffer_value.split(b"\n")
                            
                            # Process all complete lines
                            for line in lines[:-1]:
                                if line.strip():
                                    try:
                                        # Parse JSON for complete lines
                                        data = json.loads(line)
                                        if "message" in data and "content" in data["message"]:
                                            token = data["message"]["content"]
                                            
                                            # Mark time for first token only once
                                            if not first_token_received:
                                                monitor.mark_first_token()
                                                self.first_token_received_at = time.time()
                                                first_token_received = True
                                            
                                            # Add to response chunks list instead of string concatenation
                                            response_chunks.append(token)
                                            # Yield token immediately without counting
                                            yield token
                                    except json.JSONDecodeError:
                                        pass
                            
                            # Reset buffer with the last incomplete line
                            buffer = BytesIO()
                            buffer.write(lines[-1])
                except Exception as e:
                    logger.error(f"Error processing streaming content: {e}")
                    raise
            
        except aiohttp.ClientError as e:
            logger.error(f"Connection error during streaming: {e}")
            yield f"\nError: Connection error occurred - {str(e)}"
            raise
        except Exception as e:
            logger.error(f"Error generating streaming response: {e}")
            yield f"\nError: {str(e)}"
            raise
        finally:
            # Stop monitoring in all cases
            monitor.stop_monitoring()
            
            # Join all response chunks into the full response ONLY at the end
            full_response = "".join(response_chunks)
            
            # Calculate metrics if we have output - only count tokens once at the end
            if full_response:
                # Ensure first token time is valid
                if not monitor._first_token_time:
                    logger.warning("First token time was not properly set during streaming")
                    # Estimate a reasonable value if missing
                    start_time = monitor._start_time or time.time()
                    elapsed = monitor._end_time - start_time
                    monitor._first_token_time = start_time + (elapsed * 0.15)  # Assume 15% of total time
                
                # Count total output tokens only once at the end
                output_tokens = self.count_tokens(full_response)
                
                metrics = monitor.calculate_metrics(
                    model_name=self.model_name,
                    model_type=self.model_type.value,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens
                )
                
                # Log the key metrics for debugging
                
                # Store metrics for retrieval later
                self.last_metrics = metrics.to_dict()
                
                # Store metrics if request_id is provided
                if request_id:
                    self.metrics_collector.add_metrics(request_id, metrics)