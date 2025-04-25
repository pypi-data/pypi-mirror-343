# oblix/agents/resource_monitor/actions.py
from typing import Dict, Any, Optional
from enum import Enum
import logging
from .policies import PolicyResult, ExecutionTarget, ResourceState

logger = logging.getLogger(__name__)

class ActionType(Enum):
    ROUTE = "route"
    NOTIFY = "notify"
    THROTTLE = "throttle"
    OPTIMIZE = "optimize"  # New action type for optimization

class ResourceAction:
    """Handles actions based on policy decisions"""
    
    def __init__(self):
        self.current_state: Optional[ResourceState] = None
        self.current_target: Optional[ExecutionTarget] = None
    
    async def execute(self, policy_result: PolicyResult) -> Dict[str, Any]:
        """
        Execute appropriate actions based on policy result
        
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
            
            # Handle critical state
            if policy_result.state == ResourceState.CRITICAL:
                actions.extend([
                    {
                        "type": ActionType.ROUTE.value,
                        "target": ExecutionTarget.CLOUD.value,
                        "priority": "high"
                    },
                    {
                        "type": ActionType.NOTIFY.value,
                        "message": "System resources critical - forcing cloud execution",
                        "level": "error"
                    },
                    {
                        "type": ActionType.OPTIMIZE.value,
                        "action": "terminate_intensive_tasks"
                    }
                ])
            
            # Handle constrained state
            elif policy_result.state == ResourceState.CONSTRAINED:
                # Ensure target is always set to a valid value
                target = ExecutionTarget.CLOUD.value
                if policy_result.target in ExecutionTarget:
                    target = policy_result.target.value
                    
                actions.extend([
                    {
                        "type": ActionType.ROUTE.value,
                        "target": target,
                        "priority": "medium"
                    },
                    {
                        "type": ActionType.THROTTLE.value,
                        "level": "moderate"
                    },
                    {
                        "type": ActionType.OPTIMIZE.value,
                        "action": "reduce_batch_size"
                    }
                ])
            
            # Handle available state with GPU
            elif (
                policy_result.state == ResourceState.AVAILABLE and 
                policy_result.target == ExecutionTarget.LOCAL_GPU
            ):
                actions.extend([
                    {
                        "type": ActionType.ROUTE.value,
                        "target": ExecutionTarget.LOCAL_GPU.value,
                        "priority": "normal"
                    },
                    {
                        "type": ActionType.OPTIMIZE.value,
                        "action": "enable_gpu_acceleration"
                    }
                ])
            
            # Handle available state with CPU
            else:
                # Ensure target is always set to a valid value
                target = ExecutionTarget.LOCAL_CPU.value  # Safe default
                if policy_result.target in ExecutionTarget:
                    target = policy_result.target.value
                    
                actions.append({
                    "type": ActionType.ROUTE.value,
                    "target": target,
                    "priority": "normal"
                })
            
            response = {
                "state": policy_result.state.value,
                "target": policy_result.target.value,
                "reason": policy_result.reason,
                "actions": actions,
                "state_changed": state_changed,
                "metrics": policy_result.metrics
            }
            
            # Add GPU-specific information if available
            gpu_metrics = policy_result.metrics.get("gpu", {})
            if gpu_metrics.get("available", False):
                gpu_info = {
                    "name": gpu_metrics.get("name", "Unknown"),
                    "type": gpu_metrics.get("type", "Unknown"),
                    "metal_support": gpu_metrics.get("metal_support", False)
                }
                
                # Add utilization metrics if available
                if gpu_metrics.get("utilization") is not None:
                    gpu_info["utilization"] = gpu_metrics.get("utilization")
                if gpu_metrics.get("memory_utilization") is not None:
                    gpu_info["memory_utilization"] = gpu_metrics.get("memory_utilization")
                    
                response["gpu_info"] = gpu_info
            
            return response
            
        except Exception as e:
            logger.error(f"Error executing resource action: {e}")
            return {
                "error": str(e),
                "state": ResourceState.CONSTRAINED.value,
                "target": ExecutionTarget.CLOUD.value,
                "reason": "Error in action execution - defaulting to cloud",
                "actions": [{
                    "type": ActionType.ROUTE.value,
                    "target": ExecutionTarget.CLOUD.value,
                    "priority": "high"
                }]
            }