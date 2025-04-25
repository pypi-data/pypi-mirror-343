# app/api/schemas.py
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List, Union, Literal
from enum import Enum
from oblix.models.base import ModelType

class ModelHookRequest(BaseModel):
    """Request to hook a new model"""
    type: ModelType
    name: str
    endpoint: Optional[str] = None
    api_key: Optional[str] = None

class ResourceMonitorConfig(BaseModel):
    """Configuration for resource monitoring thresholds"""
    cpu_threshold: Optional[float] = 80.0
    memory_threshold: Optional[float] = 85.0
    load_threshold: Optional[float] = 4.0
    gpu_threshold: Optional[float] = 85.0
    critical_cpu: Optional[float] = 90.0
    critical_memory: Optional[float] = 95.0
    critical_gpu: Optional[float] = 95.0

class ConnectivityMonitorConfig(BaseModel):
    """Configuration for connectivity monitoring"""
    latency_threshold: Optional[float] = 200.0
    packet_loss_threshold: Optional[float] = 10.0
    bandwidth_threshold: Optional[float] = 5.0
    check_interval: Optional[int] = 30
    endpoints: Optional[List[str]] = None

class SessionResponse(BaseModel):
    """Response for session creation"""
    session_id: str
    status: str

class ExecuteRequest(BaseModel):
    """Request to execute a prompt"""
    prompt: str
    model_type: Optional[ModelType] = None
    model_name: Optional[str] = None
    session_id: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)

class ExecuteResponse(BaseModel):
    """Response from execution"""
    request_id: str
    model_id: str
    response: str
    metrics: Optional[Dict[str, Any]] = None  # Performance metrics
    agents_check: Optional[Dict[str, Any]] = None  # Captures agent check results

class ConnectivityMetricsResponse(BaseModel):
    """Response schema for connectivity metrics"""
    connection_type: Optional[str] = None
    latency: Optional[float] = None
    packet_loss: Optional[float] = None
    bandwidth: Optional[float] = None
    timestamp: Optional[float] = None

# OpenAI-compatible API schemas
class ChatRole(str, Enum):
    """Chat message roles compatible with OpenAI API"""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"

class ChatMessage(BaseModel):
    """Message format compatible with OpenAI API"""
    role: ChatRole
    content: str
    name: Optional[str] = None

class ChatCompletionRequest(BaseModel):
    """Request format compatible with OpenAI API /v1/chat/completions endpoint"""
    model: str
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 1.0
    n: Optional[int] = 1
    stream: Optional[bool] = False
    max_tokens: Optional[int] = None
    presence_penalty: Optional[float] = 0.0
    frequency_penalty: Optional[float] = 0.0
    logit_bias: Optional[Dict[str, float]] = None
    user: Optional[str] = None

class ChatCompletionChoice(BaseModel):
    """Individual completion choice in OpenAI API format"""
    index: int
    message: ChatMessage
    finish_reason: Optional[str] = "stop"

class ChatCompletionUsage(BaseModel):
    """Token usage information in OpenAI API format"""
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class ChatCompletionResponse(BaseModel):
    """Response format compatible with OpenAI API /v1/chat/completions endpoint"""
    id: str
    object: str = "chat.completion"
    created: int  # Unix timestamp
    model: str
    choices: List[ChatCompletionChoice]
    usage: Optional[ChatCompletionUsage] = None

# Streaming response schemas
class ChatCompletionChunkDelta(BaseModel):
    """Delta content for streaming responses"""
    content: Optional[str] = None
    role: Optional[ChatRole] = None
    
class ChatCompletionChunkChoice(BaseModel):
    """Individual chunk choice in streaming mode"""
    index: int
    delta: ChatCompletionChunkDelta
    finish_reason: Optional[str] = None

class ChatCompletionChunk(BaseModel):
    """Chunk format for streaming responses"""
    id: str
    object: str = "chat.completion.chunk"
    created: int
    model: str
    choices: List[ChatCompletionChunkChoice]