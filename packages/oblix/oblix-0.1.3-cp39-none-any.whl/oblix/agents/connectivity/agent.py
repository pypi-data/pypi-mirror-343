# oblix/agents/connectivity/agent.py
import asyncio
import logging
import platform
import re
import statistics
from typing import Dict, Any, Optional, Tuple

from .base import BaseConnectivityAgent
from .policies import ConnectivityPolicy
from .actions import ConnectivityAction

logger = logging.getLogger(__name__)

class ConnectivityAgent(BaseConnectivityAgent):
    """
    Concrete implementation of the Connectivity Agent
    
    Provides comprehensive connectivity monitoring and policy enforcement for the Oblix system.
    This agent monitors network quality, evaluates connectivity policies, and recommends
    appropriate execution targets (local, cloud, or hybrid) based on current connectivity.
    
    The agent continuously tracks network metrics such as latency, packet loss, and bandwidth,
    applying configurable thresholds to determine the optimal execution strategy.
    
    Attributes:
        name (str): Unique name for the agent
        is_active (bool): Whether the agent is currently active
        policy (ConnectivityPolicy): Policy evaluator for connectivity decisions
        action_handler (ConnectivityAction): Handler for connectivity-related actions
        check_interval (int): Seconds between connectivity checks
        _last_metrics (Dict): Cached metrics from last check
        _last_check_time (float): Timestamp of last check
    """
    
    def __init__(
        self, 
        name: str = "connectivity_monitor",
        latency_threshold: float = 500.0,  # Increased from 200ms to 500ms
        packet_loss_threshold: float = 10.0,
        bandwidth_threshold: float = 5.0,
        check_interval: int = 30
    ):
        """
        Initialize the Connectivity Agent
        
        Args:
            name: Unique name for the agent
            latency_threshold: Maximum acceptable latency in ms
            packet_loss_threshold: Maximum acceptable packet loss percentage
            bandwidth_threshold: Minimum acceptable bandwidth in Mbps
            check_interval: Interval between connectivity checks in seconds
        """
        # Call the parent class initializer with platform-specific monitor
        super().__init__(name)
        
        # Initialize policy with custom thresholds
        self.policy = ConnectivityPolicy(
            latency_threshold=latency_threshold,
            packet_loss_threshold=packet_loss_threshold,
            bandwidth_threshold=bandwidth_threshold
        )
        
        # Initialize action handler
        self.action_handler = ConnectivityAction()
        
        # Connectivity check configuration
        self.check_interval = check_interval
        
        # Additional monitoring state
        self._last_metrics = None
        self._last_check_time = 0
    
    async def get_connection_type(self) -> Optional[str]:
        """
        Get current connection type
        
        Identifies the active network interface type (e.g., WiFi, Ethernet, Cellular).
        
        Returns:
            Optional[str]: Connection type as a string (e.g., 'wifi', 'ethernet', 'cellular')
                           or None if unavailable
        """
        try:
            # Fallback implementation
            return "ethernet"  # Default assumption
        except Exception as e:
            logger.error(f"Error getting connection type: {e}")
            return None
    
    async def measure_bandwidth(self) -> Optional[float]:
        """
        Measure current bandwidth
        
        Attempts to estimate the current available bandwidth.
        
        Returns:
            Optional[float]: Bandwidth in Mbps or None if measurement fails
        """
        try:
            # Delegate to parent class which uses platform-specific monitor
            return await super().measure_bandwidth()
        except Exception as e:
            logger.error(f"Error measuring bandwidth: {e}")
            return None
            
    async def _measure_latency_and_packet_loss(self) -> Tuple[float, float]:
        """
        Measure latency and packet loss using ping
        
        Returns:
            Tuple[float, float]: (latency in ms, packet loss percentage)
        """
        endpoints = ["8.8.8.8", "1.1.1.1"]  # Google DNS and Cloudflare DNS
        latencies = []
        successes = 0
        total_attempts = 0
        
        for endpoint in endpoints:
            try:
                cmd = f"ping -c 3 -W 1 {endpoint}"
                process = await asyncio.create_subprocess_shell(
                    cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, _ = await process.communicate()
                output = stdout.decode()
                
                # Process ping output
                if "bytes from" in output:
                    # Extract round trip times
                    rtt_matches = re.findall(r"time=(\d+\.?\d*)", output)
                    if rtt_matches:
                        latencies.extend([float(rtt) for rtt in rtt_matches])
                        successes += len(rtt_matches)
                
                # Count total attempts
                total_attempts += 3  # We sent 3 pings
                
            except Exception as e:
                logger.debug(f"Error pinging {endpoint}: {e}")
        
        # Calculate metrics
        avg_latency = statistics.mean(latencies) if latencies else float('inf')
        packet_loss = ((total_attempts - successes) / total_attempts * 100) if total_attempts > 0 else 100.0
        
        return avg_latency, packet_loss
    
    async def measure_connection_metrics(self) -> Dict[str, Any]:
        """
        Measure current connection metrics
        
        Performs a comprehensive network quality assessment, measuring
        latency, packet loss, bandwidth, and identifying connection type.
        
        Returns:
            Dict[str, Any]: Dictionary of connection metrics including:
                - connection_type: Type of connection (wifi, ethernet, etc.)
                - latency: Round-trip time in milliseconds
                - packet_loss: Packet loss percentage
                - bandwidth: Available bandwidth in Mbps
                - timestamp: Measurement timestamp
        """
        try:
            # Delegate to platform-specific monitor
            metrics = {}
            if hasattr(self, '_monitor') and self._monitor:
                try:
                    metrics = await self._monitor.measure_connection_metrics()
                except Exception as monitor_err:
                    logger.warning(f"Platform monitor failed: {monitor_err}, using fallback")
                
            # If monitor failed or returned empty metrics, use fallback approach
            if not metrics:
                # Fallback if monitor not initialized or failed
                connection_type = await self.get_connection_type()
                bandwidth = await self.measure_bandwidth() or 0.0
                
                # Use ping to measure latency and packet loss
                latency, packet_loss = await self._measure_latency_and_packet_loss()
                
                metrics = {
                    "connection_type": connection_type or "unknown",
                    "latency": latency,
                    "packet_loss": packet_loss,
                    "bandwidth": bandwidth,
                    "timestamp": asyncio.get_running_loop().time()
                }
            
            # Ensure all required metrics are present with reasonable defaults
            if "latency" not in metrics:
                metrics["latency"] = float('inf')
            if "packet_loss" not in metrics:
                metrics["packet_loss"] = 100.0
            if "bandwidth" not in metrics:
                metrics["bandwidth"] = 0.0
            if "connection_type" not in metrics:
                metrics["connection_type"] = "unknown"
            if "timestamp" not in metrics:
                metrics["timestamp"] = asyncio.get_running_loop().time()
                
            return metrics
        except Exception as e:
            logger.error(f"Error collecting connectivity metrics: {e}")
            return {
                "connection_type": None,
                "latency": float('inf'),
                "packet_loss": 100.0,
                "bandwidth": 0.0,
                "timestamp": asyncio.get_running_loop().time()
            }
    
    async def initialize(self) -> bool:
        """
        Initialize the connectivity agent
        
        Sets up the agent, verifies that connectivity monitoring is possible,
        and performs an initial metrics collection.
        
        Returns:
            bool: True if initialization is successful, False otherwise
        """
        try:
            # Test initial metrics collection
            metrics = await self.measure_connection_metrics()
            
            if not metrics:
                logger.error("Failed to collect initial connectivity metrics")
                return False
            
            self.is_active = True
            logger.info(f"Connectivity monitor initialized successfully on {platform.system()}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize connectivity monitor: {e}")
            return False
    
    async def check(self, **kwargs) -> Dict[str, Any]:
        """
        Perform connectivity checks for the system
        
        This is the main entry point for the agent's functionality. It assesses
        current network conditions, evaluates connectivity policies, and determines
        the optimal execution strategy based on the connectivity state.
        
        Args:
            **kwargs: Flexible keyword arguments for context (ignored)
            
        Returns:
            Dict[str, Any]: Check results containing:
                - proceed: Always true as this is advisory only
                - state: Current connectivity state (optimal, degraded, disconnected)
                - target: Recommended execution target (local, cloud, hybrid)
                - actions: List of recommended actions
                - metrics: Current connectivity metrics
                - reason: Reason for the recommendation
        """
        if not self.is_active:
            await self.initialize()
        
        try:
            # Collect current metrics
            metrics = await self.measure_connection_metrics()
            
            if not metrics:
                raise Exception("Failed to collect connectivity metrics")
            
            # Evaluate policy
            policy_result = self.policy.evaluate(metrics)
            
            # Execute actions
            action_result = await self.action_handler.execute(policy_result)
            
            return {
                "proceed": True,  # Always true as this is informational
                **action_result
            }
            
        except Exception as e:
            logger.error(f"Error during connectivity check: {e}")
            # Always return a proceed=True with safe defaults, don't block execution
            # even on error, just recommend cloud fallback due to uncertain connectivity
            return {
                "proceed": True,
                "error": str(e),
                "state": "disconnected",
                "target": "local",  # Changed to local since cloud is unreachable when disconnected
                "reason": f"Error assessing connectivity: {str(e)} - defaulting to local",
                "actions": [{
                    "type": "fallback",
                    "target": "local",
                    "priority": "high"
                }]
            }
    
    async def shutdown(self) -> None:
        """
        Gracefully shut down the connectivity monitor
        
        Releases resources and stops any ongoing monitoring activities.
        """
        self.is_active = False
        logger.info("Connectivity monitor shut down")