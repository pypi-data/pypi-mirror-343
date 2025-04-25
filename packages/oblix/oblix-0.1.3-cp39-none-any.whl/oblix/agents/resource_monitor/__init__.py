# oblix/agents/resource_monitor/__init__.py
import platform
import logging
import sys
from typing import Dict, Any, Optional

from oblix.agents.base import BaseAgent
from .base import SystemMonitor
from .policies import ResourcePolicy
from .actions import ResourceAction

# Import platform-specific monitors at module level to avoid slow imports during runtime
from .darwin.monitor import DarwinSystemMonitor

# Conditionally import Windows monitor only if on Windows 
# This prevents import errors on other platforms
if platform.system().lower() == "windows":
    from .windows.monitor import WindowsSystemMonitor
elif platform.system().lower() == "linux":
    from .linux.monitor import LinuxSystemMonitor

logger = logging.getLogger(__name__)

class ResourceMonitor(BaseAgent):
    """
    Resource monitoring agent that provides system metrics and execution recommendations
    based on resource availability
    """
    
    def __init__(
        self,
        name: str = "resource_monitor",
        custom_thresholds: Optional[Dict[str, float]] = None
    ):
        super().__init__(name)
        
        # Initialize platform-specific monitor
        self.platform = platform.system().lower()
        self.system_monitor = self._get_platform_monitor()
        
        # Initialize policy and action handlers
        self.policy = ResourcePolicy(**(custom_thresholds or {}))
        self.action_handler = ResourceAction()
    
    def _get_platform_monitor(self) -> SystemMonitor:
        """Get platform-specific system monitor implementation"""
        if self.platform == "darwin":
            return DarwinSystemMonitor()
        elif self.platform == "windows":
            from .windows.monitor import WindowsSystemMonitor
            return WindowsSystemMonitor()
        elif self.platform == "linux":
            from .linux.monitor import LinuxSystemMonitor
            return LinuxSystemMonitor()
        # Add other platforms here
        raise NotImplementedError(f"Platform {self.platform} not supported yet")
    
    async def initialize(self) -> bool:
        """Initialize the resource monitor"""
        try:
            # Test metrics collection
            metrics = await self._collect_metrics()
            if metrics.get("error"):
                raise Exception(metrics["error"])
            
            self.is_active = True
            logger.info(
                f"Resource monitor initialized successfully on platform: {self.platform}"
            )
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize resource monitor: {e}")
            return False
    
    async def _collect_metrics(self) -> Dict[str, Any]:
        """Collect all system metrics in parallel"""
        import asyncio
        
        try:
            # Run all metric collection concurrently for faster results
            cpu_task = asyncio.create_task(self.system_monitor.get_cpu_info())
            memory_task = asyncio.create_task(self.system_monitor.get_memory_info())
            gpu_task = asyncio.create_task(self.system_monitor.get_gpu_info())
            
            # Wait for all tasks to complete
            cpu_info, memory_info, gpu_info = await asyncio.gather(
                cpu_task, memory_task, gpu_task, 
                return_exceptions=True
            )
            
            # Handle any exceptions
            cpu_result = cpu_info if not isinstance(cpu_info, Exception) else {"error": str(cpu_info)}
            memory_result = memory_info if not isinstance(memory_info, Exception) else {"error": str(memory_info)}
            gpu_result = gpu_info if not isinstance(gpu_info, Exception) else {"error": str(gpu_info)}
            
            return {
                "cpu": cpu_result,
                "memory": memory_result,
                "gpu": gpu_result
            }
        except Exception as e:
            logger.error(f"Error collecting metrics: {e}")
            return {"error": str(e)}
    
    async def check(self, **kwargs) -> Dict[str, Any]:
        """
        Check system resources and provide execution recommendations
        
        Returns:
            Dict containing:
            - proceed (bool): Whether execution can proceed
            - state (str): Current resource state
            - target (str): Recommended execution target
            - actions (list): Recommended actions
            - metrics (dict): Current system metrics
        """
        if not self.is_active:
            await self.initialize()
        
        try:
            # Collect current metrics
            metrics = await self._collect_metrics()
            if "error" in metrics:
                raise Exception(metrics["error"])
            
            # Evaluate policy
            policy_result = self.policy.evaluate(metrics)
            
            # Execute actions
            action_result = await self.action_handler.execute(policy_result)
            
            return {
                "proceed": True,  # Always true as this is informational
                **action_result
            }
            
        except Exception as e:
            logger.error(f"Error during resource check: {e}")
            # Always return proceed=True with safe defaults to prevent blocking execution
            return {
                "proceed": True,
                "error": str(e),
                "state": "constrained",  # Default to constrained state on error
                "target": "cloud",       # Default to cloud target on error
                "reason": f"Error assessing resources: {str(e)} - defaulting to cloud",
                "actions": [{
                    "type": "route",
                    "target": "cloud",
                    "priority": "high"
                }]
            }
    
    async def shutdown(self) -> None:
        """Shutdown the resource monitor silently"""
        try:
            # Gracefully shutdown any running processes
            if hasattr(self, 'system_monitor') and hasattr(self.system_monitor, 'cleanup'):
                await self.system_monitor.cleanup()
            self.is_active = False
        except Exception:
            # Suppress all exceptions during shutdown
            pass
