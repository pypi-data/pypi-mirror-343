# oblix/core/websocket.py
from typing import Dict, Any, Optional, Set, List, Generator
from fastapi import WebSocket, WebSocketDisconnect, Depends
from enum import Enum
import asyncio
import json
from datetime import datetime, timezone
import logging
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class WebSocketMessageType(Enum):
    """Message types for WebSocket communication."""
    METRICS = "metrics"
    MODEL_STATUS = "model_status"
    EXECUTION_PROGRESS = "execution_progress"
    SYSTEM_RESOURCES = "system_resources"
    ERROR = "error"

class WebSocketMessage(BaseModel):
    """Message format for WebSocket communication."""
    type: WebSocketMessageType
    data: Dict[str, Any]
    timestamp: datetime = datetime.now(timezone.utc)

class ModelResponse(BaseModel):
    """Model response schema."""
    id: str
    name: str
    type: str
    config: dict = {}

class WebSocketManager:
    """WebSocket manager for dashboard communication."""
    
    def __init__(self):
        """Initialize WebSocket manager."""
        self.active_connections: Dict[str, WebSocket] = {}
        self.subscriptions: Dict[str, Set[str]] = {
            WebSocketMessageType.METRICS.value: set(),
            WebSocketMessageType.MODEL_STATUS.value: set(),
            WebSocketMessageType.EXECUTION_PROGRESS.value: set(),
            WebSocketMessageType.SYSTEM_RESOURCES.value: set(),
        }
        
    async def connect(self, websocket: WebSocket, client_id: str):
        """
        Connect a new client.
        
        Args:
            websocket: WebSocket connection
            client_id: Unique client identifier
        """
        await websocket.accept()
        self.active_connections[client_id] = websocket
        logger.info(f"Client {client_id} connected")
        
    def disconnect(self, client_id: str):
        """
        Disconnect a client.
        
        Args:
            client_id: Client identifier to disconnect
        """
        if client_id in self.active_connections:
            # Remove from all subscriptions
            for subscribers in self.subscriptions.values():
                subscribers.discard(client_id)
            del self.active_connections[client_id]
            logger.info(f"Client {client_id} disconnected")
            
    async def subscribe(self, client_id: str, message_type: WebSocketMessageType):
        """
        Subscribe client to specific message type.
        
        Args:
            client_id: Client identifier
            message_type: Type of messages to subscribe to
        """
        if client_id in self.active_connections:
            self.subscriptions[message_type.value].add(client_id)
            logger.info(f"Client {client_id} subscribed to {message_type.value}")
            
    async def unsubscribe(self, client_id: str, message_type: WebSocketMessageType):
        """
        Unsubscribe client from specific message type.
        
        Args:
            client_id: Client identifier
            message_type: Type of messages to unsubscribe from
        """
        if client_id in self.active_connections:
            self.subscriptions[message_type.value].discard(client_id)
            
    async def broadcast_message(self, message: WebSocketMessage):
        """
        Broadcast message to subscribed clients.
        
        Args:
            message: Message to broadcast
        """
        subscribers = self.subscriptions[message.type.value]
        
        if not subscribers:
            return
            
        for client_id in subscribers:
            if client_id in self.active_connections:
                try:
                    await self.active_connections[client_id].send_json(
                        message.dict()
                    )
                except Exception as e:
                    logger.error(f"Error sending message to client {client_id}: {e}")
                    await self.disconnect(client_id)
                    
    async def broadcast_metrics(self, metrics: Dict[str, Any]):
        """
        Broadcast system metrics.
        
        Args:
            metrics: Metrics data to broadcast
        """
        await self.broadcast_message(
            WebSocketMessage(
                type=WebSocketMessageType.METRICS,
                data=metrics
            )
        )
        
    async def broadcast_model_status(self, model_id: str, status: Dict[str, Any]):
        """
        Broadcast model status updates.
        
        Args:
            model_id: Model identifier
            status: Status data to broadcast
        """
        await self.broadcast_message(
            WebSocketMessage(
                type=WebSocketMessageType.MODEL_STATUS,
                data={"model_id": model_id, **status}
            )
        )
        
    async def broadcast_execution_progress(
        self, 
        execution_id: str, 
        progress: Dict[str, Any]
    ):
        """
        Broadcast execution progress.
        
        Args:
            execution_id: Execution identifier
            progress: Progress data to broadcast
        """
        await self.broadcast_message(
            WebSocketMessage(
                type=WebSocketMessageType.EXECUTION_PROGRESS,
                data={"execution_id": execution_id, **progress}
            )
        )
        
    async def broadcast_error(self, error: str, details: Optional[Dict] = None):
        """
        Broadcast error message.
        
        Args:
            error: Error message
            details: Additional error details
        """
        await self.broadcast_message(
            WebSocketMessage(
                type=WebSocketMessageType.ERROR,
                data={"error": error, "details": details or {}}
            )
        )

# WebSocket route handlers
async def handle_websocket_connection(
    websocket: WebSocket,
    client_id: str,
    manager: WebSocketManager
):
    """
    Handle WebSocket connection lifecycle.
    
    Args:
        websocket: WebSocket connection
        client_id: Client identifier
        manager: WebSocket manager instance
    """
    await manager.connect(websocket, client_id)
    
    try:
        while True:
            data = await websocket.receive_json()
            
            # Handle subscription messages
            if data.get("action") == "subscribe":
                message_type = WebSocketMessageType(data.get("type"))
                await manager.subscribe(client_id, message_type)
            elif data.get("action") == "unsubscribe":
                message_type = WebSocketMessageType(data.get("type"))
                await manager.unsubscribe(client_id, message_type)
            
    except WebSocketDisconnect:
        manager.disconnect(client_id)
    except Exception as e:
        logger.error(f"WebSocket error for client {client_id}: {e}")
        manager.disconnect(client_id)