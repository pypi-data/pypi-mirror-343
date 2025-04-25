# oblix/agents/connectivity/policies.py
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class ConnectivityState(Enum):
    """Represents the current connectivity state"""
    OPTIMAL = "optimal"
    DEGRADED = "degraded"
    DISCONNECTED = "disconnected"

class ConnectionTarget(Enum):
    """Recommended connection targets"""
    LOCAL = "local"
    CLOUD = "cloud"
    HYBRID = "hybrid"

@dataclass
class ConnectivityPolicyResult:
    """
    Result of connectivity policy evaluation
    
    Contains:
    - state: Overall connectivity state
    - target: Recommended execution target
    - reason: Explanation for the policy decision
    - metrics: Detailed connection metrics
    """
    state: ConnectivityState
    target: ConnectionTarget
    reason: str
    metrics: Dict[str, Any]

class ConnectivityPolicy:
    """
    Defines connectivity monitoring policies and thresholds
    """
    
    def __init__(
        self,
        latency_threshold: float = 500.0,  # ms - increased from 200ms to 500ms
        packet_loss_threshold: float = 10.0,  # percentage
        bandwidth_threshold: float = 5.0,  # Mbps
        **kwargs
    ):
        """
        Initialize connectivity policy with configurable thresholds
        
        :param latency_threshold: Maximum acceptable latency in milliseconds
        :param packet_loss_threshold: Maximum acceptable packet loss percentage
        :param bandwidth_threshold: Minimum acceptable bandwidth in Mbps
        """
        self.thresholds = {
            "latency": latency_threshold,
            "packet_loss": packet_loss_threshold,
            "bandwidth": bandwidth_threshold
        }
    
    def evaluate(self, metrics: Dict[str, Any]) -> ConnectivityPolicyResult:
        """
        Evaluate connection metrics against defined thresholds
        
        :param metrics: Connection metrics dictionary
        :return: Policy result with state and recommended action
        """
        try:
            # Validate metrics
            if not metrics or not isinstance(metrics, dict):
                return ConnectivityPolicyResult(
                    state=ConnectivityState.DISCONNECTED,
                    target=ConnectionTarget.CLOUD,
                    reason="No connection metrics available",
                    metrics=metrics or {}
                )
            
            # Extract key metrics with safe defaults
            latency = metrics.get('latency', float('inf'))
            packet_loss = metrics.get('packet_loss', 100.0)
            bandwidth = metrics.get('bandwidth', 0.0)
            connection_type = metrics.get('connection_type', 'unknown')
            
            # Connectivity state is critical
            if (latency == float('inf') or 
                packet_loss >= 100.0 or 
                bandwidth <= 0.0):
                return ConnectivityPolicyResult(
                    state=ConnectivityState.DISCONNECTED,
                    target=ConnectionTarget.LOCAL,  # When disconnected, always use LOCAL as cloud is unreachable
                    reason="Network completely unavailable - forcing local execution",
                    metrics=metrics
                )
            
            # Check for degraded connection
            if (latency > self.thresholds['latency'] or
                packet_loss > self.thresholds['packet_loss'] or
                bandwidth < self.thresholds['bandwidth']):
                
                # Detailed degradation reasons with more informative messages
                degradation_reasons = []
                if latency > self.thresholds['latency']:
                    degradation_reasons.append(f"High network response time: {latency}ms (affects cloud API responsiveness)")
                if packet_loss > self.thresholds['packet_loss']:
                    degradation_reasons.append(f"Network reliability issues: {packet_loss}% packet loss")
                if bandwidth < self.thresholds['bandwidth']:
                    degradation_reasons.append(f"Limited connection speed: {bandwidth}Mbps")
                
                return ConnectivityPolicyResult(
                    state=ConnectivityState.DEGRADED,
                    target=ConnectionTarget.HYBRID,
                    reason=f"Degraded connection: {'; '.join(degradation_reasons)}",
                    metrics=metrics
                )
            
            # Optimal connection state
            return ConnectivityPolicyResult(
                state=ConnectivityState.OPTIMAL,
                target=ConnectionTarget.LOCAL,
                reason=f"Optimal {connection_type} connection",
                metrics=metrics
            )
            
        except Exception as e:
            logger.error(f"Error evaluating connectivity policy: {e}")
            return ConnectivityPolicyResult(
                state=ConnectivityState.DISCONNECTED,
                target=ConnectionTarget.LOCAL,  # When disconnected, always use LOCAL as cloud is unreachable
                reason=f"Policy evaluation error: {str(e)} - defaulting to local execution",
                metrics=metrics or {}
            )
