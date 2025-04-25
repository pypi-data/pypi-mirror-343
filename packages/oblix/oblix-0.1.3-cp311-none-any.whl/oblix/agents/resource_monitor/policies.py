# oblix/agents/resource_monitor/policies.py
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class ResourceState(Enum):
    AVAILABLE = "available"
    CONSTRAINED = "constrained"
    CRITICAL = "critical"

class ExecutionTarget(Enum):
    LOCAL_CPU = "local_cpu"
    LOCAL_GPU = "local_gpu"
    CLOUD = "cloud"

@dataclass
class PolicyResult:
    state: ResourceState
    target: ExecutionTarget
    reason: str
    metrics: Dict[str, Any]

class ResourcePolicy:
    """Defines resource monitoring policies and thresholds"""
    
    def __init__(
        self,
        cpu_threshold: float = 80.0,
        memory_threshold: float = 85.0,
        load_threshold: float = 4.0,
        gpu_threshold: float = 85.0,  # New GPU threshold
        critical_cpu: float = 90.0,
        critical_memory: float = 95.0,
        critical_gpu: float = 95.0    # New critical GPU threshold
    ):
        self.thresholds = {
            "cpu_percent": cpu_threshold,
            "memory_percent": memory_threshold,
            "load_average_5min": load_threshold,
            "gpu_percent": gpu_threshold,     # New
            "critical_cpu": critical_cpu,
            "critical_memory": critical_memory,
            "critical_gpu": critical_gpu      # New
        }
    
    def evaluate(self, metrics: Dict[str, Any]) -> PolicyResult:
        """
        Evaluate system metrics against policy thresholds
        
        Returns:
            PolicyResult with resource state and recommended action
        """
        try:
            cpu_metrics = metrics.get("cpu", {})
            memory_metrics = metrics.get("memory", {})
            gpu_metrics = metrics.get("gpu", {})
            
            # Get GPU utilization (normalize percentage)
            gpu_utilization = None
            if gpu_metrics.get("available", False):
                # Check for direct utilization value (new path)
                if gpu_metrics.get("utilization") is not None:
                    # Convert from 0-1 to percentage if needed
                    util_value = gpu_metrics.get("utilization")
                    gpu_utilization = util_value * 100 if util_value <= 1.0 else util_value
                # Fallback to old performance.utilization path
                elif gpu_metrics.get("performance", {}).get("utilization") is not None:
                    util_value = gpu_metrics.get("performance", {}).get("utilization")
                    gpu_utilization = util_value * 100 if util_value <= 1.0 else util_value
            
            # Check for critical state first
            if (
                cpu_metrics.get("usage_percent", 0) > self.thresholds["critical_cpu"] or
                memory_metrics.get("ram", {}).get("usage_percent", 0) > 
                self.thresholds["critical_memory"] or
                (gpu_utilization is not None and gpu_utilization > 
                self.thresholds["critical_gpu"] and gpu_metrics.get("available", False))
            ):
                return PolicyResult(
                    state=ResourceState.CRITICAL,
                    target=ExecutionTarget.CLOUD,
                    reason="System resources critically low",
                    metrics=metrics
                )
            
            # Check for constrained state
            if (
                cpu_metrics.get("usage_percent", 0) > self.thresholds["cpu_percent"] or
                memory_metrics.get("ram", {}).get("usage_percent", 0) > 
                self.thresholds["memory_percent"] or
                cpu_metrics.get("load_average", {}).get("5min", 0) > 
                self.thresholds["load_average_5min"] or
                (gpu_utilization is not None and gpu_utilization > 
                self.thresholds["gpu_percent"] and gpu_metrics.get("available", False))
            ):
                return PolicyResult(
                    state=ResourceState.CONSTRAINED,
                    target=ExecutionTarget.CLOUD,
                    reason="System resources constrained",
                    metrics=metrics
                )
            
            # System resources available, determine best target
            if gpu_metrics.get("available", False):
                # Check if GPU is suitable for execution
                if gpu_utilization is None:
                    gpu_util_display = "unknown"
                else:
                    # Format as percentage with 1 decimal place
                    gpu_util_display = f"{gpu_utilization * 100:.1f}" if 0 <= gpu_utilization <= 1 else f"{gpu_utilization:.1f}"
                
                if gpu_utilization is None or gpu_utilization < self.thresholds["gpu_percent"]:
                    return PolicyResult(
                        state=ResourceState.AVAILABLE,
                        target=ExecutionTarget.LOCAL_GPU,
                        reason=(
                            f"GPU available with {gpu_metrics.get('name', 'Unknown GPU')} "
                            f"(utilization: {gpu_util_display}%)"
                        ),
                        metrics=metrics
                    )
            
            # Default to CPU execution
            return PolicyResult(
                state=ResourceState.AVAILABLE,
                target=ExecutionTarget.LOCAL_CPU,
                reason="Sufficient CPU resources available",
                metrics=metrics
            )
            
        except Exception as e:
            logger.error(f"Error evaluating resource policy: {e}")
            # Safe default to cloud execution
            return PolicyResult(
                state=ResourceState.CONSTRAINED,
                target=ExecutionTarget.CLOUD,
                reason=f"Error evaluating resources: {str(e)}",
                metrics=metrics
            )