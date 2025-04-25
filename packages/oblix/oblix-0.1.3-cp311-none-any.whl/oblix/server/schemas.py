# app/server/schemas.py
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from app.models.base import ModelType

class ModelHookRequest(BaseModel):
    """Request to hook a new model"""
    type: ModelType
    name: str
    endpoint: Optional[str] = None
    api_key: Optional[str] = None

class ModelConfig(BaseModel):
    """Model configuration response"""
    id: str
    type: ModelType
    name: str
    endpoint: Optional[str] = None

class ModelListResponse(BaseModel):
    """Response for listing models"""
    models: List[ModelConfig]

class ExecuteRequest(BaseModel):
    """Request to execute a prompt"""
    model_type: ModelType
    model_name: str
    prompt: str
    parameters: Dict[str, Any] = Field(default_factory=dict)

class ExecuteResponse(BaseModel):
    """Response from execution"""
    request_id: str
    model_id: str
    response: str
    agents_check: Optional[Dict[str, Any]] = None  # New field to include agent checks
