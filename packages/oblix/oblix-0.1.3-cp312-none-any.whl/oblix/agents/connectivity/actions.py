# oblix/agents/connectivity/actions.py
from typing import Dict, Any, Optional, List
from enum import Enum
import logging
from .policies import ConnectivityPolicyResult, ConnectionTarget, ConnectivityState

logger = logging.getLogger(__name__)

class ConnectivityActionType(Enum):
    """Types of connectivity-related actions"""
    SWITCH_MODEL = "switch_model"
    RETRY = "retry"
    NOTIFY = "notify"
    FALLBACK = "fallback"
    OPTIMIZE = "optimize"

class ConnectivityAction:
    """
    Handles actions based on connectivity policy decisions
    """
    
    def __init__(self):
        """Initialize connectivity action handler"""
        self.current_state: Optional[ConnectivityState] = None
        self.current_target: Optional[ConnectionTarget] = None
    
    async def execute(self, policy_result: ConnectivityPolicyResult) -> Dict[str, Any]:
        """
        Execute appropriate actions based on connectivity policy result
        
        Args:
            policy_result: Connectivity policy evaluation result
        
        Returns:
            Dict containing action results and recommendations
        """
        try:
            # Track state changes
            state_changed = (
                self.current_state != policy_result.state or
                self.current_target != policy_result.target
            )
            
            self.current_state = policy_result.state
            self.current_target = policy_result.target
            
            actions = []
            
            # Handle disconnected state
            if policy_result.state == ConnectivityState.DISCONNECTED:
                actions.extend([
                    {
                        "type": ConnectivityActionType.FALLBACK.value,
                        "target": ConnectionTarget.LOCAL.value,  # Changed to LOCAL since cloud is unreachable
                        "priority": "high"
                    },
                    {
                        "type": ConnectivityActionType.NOTIFY.value,
                        "message": "Network connection lost - switching to local fallback",
                        "level": "error"
                    }
                ])
            
            # Handle degraded state
            elif policy_result.state == ConnectivityState.DEGRADED:
                actions.extend([
                    {
                        "type": ConnectivityActionType.SWITCH_MODEL.value,
                        "target": ConnectionTarget.HYBRID.value,
                        "priority": "medium"
                    },
                    {
                        "type": ConnectivityActionType.OPTIMIZE.value,
                        "action": "reduce_model_complexity"
                    },
                    {
                        "type": ConnectivityActionType.NOTIFY.value,
                        "message": f"Network performance may affect cloud operations: {policy_result.reason}",
                        "level": "warning"
                    }
                ])
            
            # Optimal state with local execution
            elif (policy_result.state == ConnectivityState.OPTIMAL and 
                  policy_result.target == ConnectionTarget.LOCAL):
                actions.append({
                    "type": ConnectivityActionType.SWITCH_MODEL.value,
                    "target": ConnectionTarget.LOCAL.value,
                    "priority": "normal"
                })
            
            # Prepare response
            response = {
                "state": policy_result.state.value,
                "target": policy_result.target.value,
                "reason": policy_result.reason,
                "actions": actions,
                "state_changed": state_changed,
                "metrics": policy_result.metrics
            }
            
            # Add connection-specific information
            if policy_result.metrics:
                response["connection_info"] = {
                    "type": policy_result.metrics.get("connection_type", "unknown"),
                    "latency": policy_result.metrics.get("latency"),
                    "bandwidth": policy_result.metrics.get("bandwidth"),
                    "packet_loss": policy_result.metrics.get("packet_loss")
                }
            
            return response
            
        except Exception as e:
            logger.error(f"Error executing connectivity action: {e}")
            return {
                "error": str(e),
                "state": ConnectivityState.DISCONNECTED.value,
                "target": ConnectionTarget.LOCAL.value,  # Changed to LOCAL since cloud is unreachable when disconnected
                "reason": "Error in action execution - defaulting to local fallback",
                "actions": [{
                    "type": ConnectivityActionType.FALLBACK.value,
                    "target": ConnectionTarget.LOCAL.value,
                    "priority": "high"
                }]
            }
