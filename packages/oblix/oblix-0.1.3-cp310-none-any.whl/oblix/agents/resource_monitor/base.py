# oblix/agents/resource_monitor/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class SystemMonitor(ABC):
    """Abstract base class for platform-specific system monitoring"""
    
    @abstractmethod
    async def get_cpu_info(self) -> Dict[str, Any]:
        """Get CPU information and usage"""
        pass
    
    @abstractmethod
    async def get_memory_info(self) -> Dict[str, Any]:
        """Get memory information and usage"""
        pass
    
    @abstractmethod
    async def get_gpu_info(self) -> Dict[str, Any]:
        """Get GPU information and usage"""
        pass
        
    async def cleanup(self):
        """
        Clean up any resources used by the monitor.
        This method should be overridden by implementations that need cleanup.
        """
        pass
