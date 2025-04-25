# oblix/monitoring/metrics.py
from dataclasses import dataclass
from typing import Dict, Any, Optional
from enum import Enum
import time
import json
import asyncio
from datetime import datetime, timezone

class MetricType(Enum):
    LATENCY = "latency"
    THROUGHPUT = "throughput"
    RESOURCE = "resource"
    COST = "cost"

@dataclass
class PerformanceMetrics:
    """Container for performance metrics"""
    total_latency: float  # in seconds
    tokens_per_second: Optional[float]
    input_tokens: Optional[int]
    output_tokens: Optional[int]
    start_time: datetime
    end_time: Optional[datetime]
    model_name: str
    model_type: str
    time_to_first_token: Optional[float] = None  # in seconds
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary format"""
        return {
            "total_latency": round(self.total_latency, 3),
            "tokens_per_second": round(self.tokens_per_second, 2) if self.tokens_per_second else None,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "model_name": self.model_name,
            "model_type": self.model_type,
            "time_to_first_token": round(self.time_to_first_token, 3) if self.time_to_first_token else None,
        }

class PerformanceMonitor:
    """Monitors and collects performance metrics for model execution"""
    
    def __init__(self):
        self._start_time: Optional[float] = None
        self._end_time: Optional[float] = None
        self._first_token_time: Optional[float] = None
        self._metrics: Dict[str, Any] = {}
    
    def start_monitoring(self) -> None:
        """Start monitoring execution"""
        self._start_time = time.time()
        self._metrics["start_time"] = datetime.now(timezone.utc)
    
    def mark_first_token(self) -> None:
        """Mark when the first token is received"""
        if not self._first_token_time:
            self._first_token_time = time.time()
    
    def stop_monitoring(self) -> None:
        """Stop monitoring execution"""
        self._end_time = time.time()
        self._metrics["end_time"] = datetime.now(timezone.utc)
    
    def calculate_metrics(self,
                         model_name: str,
                         model_type: str,
                         input_tokens: Optional[int] = None,
                         output_tokens: Optional[int] = None) -> PerformanceMetrics:
        """Calculate performance metrics"""
        if not self._start_time or not self._end_time:
            raise ValueError("Monitoring must be started and stopped first")
        
        total_latency = self._end_time - self._start_time
        
        # Calculate time to first token if available
        time_to_first_token = None
        if self._first_token_time:
            time_to_first_token = self._first_token_time - self._start_time
        
        # Calculate tokens per second if token counts are available
        tokens_per_second = None
        if output_tokens:
            tokens_per_second = output_tokens / total_latency
        
        return PerformanceMetrics(
            total_latency=total_latency,
            tokens_per_second=tokens_per_second,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            start_time=self._metrics["start_time"],
            end_time=self._metrics["end_time"],
            model_name=model_name,
            model_type=model_type,
            time_to_first_token=time_to_first_token
        )

class ModelMetricsCollector:
    """Collects and manages metrics for model execution"""
    
    def __init__(self):
        self.metrics_history: Dict[str, list] = {}
    
    def add_metrics(self, request_id: str, metrics: PerformanceMetrics) -> None:
        """Add metrics for a specific request"""
        if request_id not in self.metrics_history:
            self.metrics_history[request_id] = []
        self.metrics_history[request_id].append(metrics)
    
    def get_metrics(self, request_id: str) -> Optional[list]:
        """Get metrics for a specific request"""
        return self.metrics_history.get(request_id)
    
    def get_average_metrics(self, model_name: str) -> Dict[str, float]:
        """Calculate average metrics for a specific model"""
        model_runs = [
            metrics
            for runs in self.metrics_history.values()
            for metrics in runs
            if metrics.model_name == model_name
        ]
        
        if not model_runs:
            return {}
        
        total_latency = sum(run.total_latency for run in model_runs)
        avg_latency = total_latency / len(model_runs)
        
        # Calculate average tokens per second, excluding None values
        tps_values = [run.tokens_per_second for run in model_runs if run.tokens_per_second]
        avg_tps = sum(tps_values) / len(tps_values) if tps_values else None
        
        return {
            "average_latency": round(avg_latency, 3),
            "average_tokens_per_second": round(avg_tps, 2) if avg_tps else None,
            "total_requests": len(model_runs)
        }

async def measure_execution_time(coroutine, *args, **kwargs) -> tuple:
    """Utility function to measure execution time of a coroutine"""
    monitor = PerformanceMonitor()
    monitor.start_monitoring()
    
    try:
        result = await coroutine(*args, **kwargs)
        monitor.stop_monitoring()
        return result, monitor
    except Exception as e:
        monitor.stop_monitoring()
        raise e