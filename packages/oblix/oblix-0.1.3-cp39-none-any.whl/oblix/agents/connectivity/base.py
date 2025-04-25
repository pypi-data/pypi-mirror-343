# oblix/agents/connectivity/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from enum import Enum
import logging
import platform

logger = logging.getLogger(__name__)

class ConnectivityState(Enum):
    """Represents the current connectivity state"""
    OPTIMAL = "optimal"
    DEGRADED = "degraded"
    DISCONNECTED = "disconnected"

class BaseConnectivityMonitor(ABC):
    """
    Abstract base class for platform-specific connectivity monitoring
    """
    
    @abstractmethod
    async def get_connection_type(self) -> Optional[str]:
        """Get current connection type"""
        pass
    
    @abstractmethod
    async def measure_bandwidth(self) -> Optional[float]:
        """Measure current bandwidth"""
        pass
    
    @abstractmethod
    async def measure_connection_metrics(self) -> Dict[str, Any]:
        """Measure detailed connection metrics"""
        pass

class BaseConnectivityAgent(BaseConnectivityMonitor):
    """
    Base connectivity agent that provides system-specific connectivity monitoring
    """
    
    def __init__(self, name: str = "connectivity_monitor"):
        """
        Initialize the connectivity agent
        
        :param name: Unique name for the agent
        """
        self.name = name
        self.is_active = False
        self._monitor = self._get_platform_monitor()
    
    def _get_platform_monitor(self) -> BaseConnectivityMonitor:
        """
        Get platform-specific connectivity monitor
        
        :return: Platform-specific connectivity monitor
        """
        platform_name = platform.system().lower()
        
        if platform_name == "darwin":
            from .darwin.monitor import DarwinConnectivityMonitor
            return DarwinConnectivityMonitor()
        elif platform_name == "windows":
            from .windows.monitor import WindowsConnectivityMonitor
            return WindowsConnectivityMonitor()
        elif platform_name == "linux":
            from .linux.monitor import LinuxConnectivityMonitor
            return LinuxConnectivityMonitor()
        
        # Add other platforms here
        raise NotImplementedError(f"Platform {platform_name} not supported yet")
    
    async def get_connection_type(self) -> Optional[str]:
        """Delegate connection type retrieval to platform monitor"""
        return await self._monitor.get_connection_type()
    
    async def measure_bandwidth(self) -> Optional[float]:
        """Delegate bandwidth measurement to platform monitor"""
        return await self._monitor.measure_bandwidth()
        
    async def measure_connection_metrics(self) -> Dict[str, Any]:
        """Delegate connection metrics measurement to platform monitor"""
        return await self._monitor.measure_connection_metrics()
