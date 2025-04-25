# oblix/platforms/darwin/metal.py
import platform
import subprocess
import json
import re
from typing import Tuple, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class MetalGPUMonitor:
    """Basic GPU monitoring using system information"""
    
    def __init__(self):
        """
        Initialize the Metal GPU monitor with proper validation
        
        Raises:
            RuntimeError: If initialized on a non-macOS platform
        """
        self.is_mac = platform.system() == "Darwin"
        
        # Validate platform
        if not self.is_mac:
            logger.warning("MetalGPUMonitor initialized on non-macOS platform. Functionality will be limited.")
        
        # Verify system_profiler availability
        try:
            subprocess.run(
                ["which", "system_profiler"],
                capture_output=True,
                check=True
            )
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.error(f"system_profiler tool not available: {e}")
            raise RuntimeError("MetalGPUMonitor requires system_profiler which is not available")
    
    def get_gpu_info(self) -> Tuple[bool, Optional[dict]]:
        """
        Get GPU information
        Returns: (is_available, info_dict)
        """
        if not self.is_mac:
            return False, None
            
        try:
            result = subprocess.run(
                ["system_profiler", "SPDisplaysDataType", "-json"],
                capture_output=True,
                text=True,
                check=True
            )
            
            gpu_data = json.loads(result.stdout)
            graphics_cards = gpu_data.get("SPDisplaysDataType", [])
            
            if not graphics_cards:
                return False, None
            
            primary_gpu = graphics_cards[0]
            gpu_name = primary_gpu.get("sppci_model", "Unknown GPU")
            is_apple_silicon = "Apple" in gpu_name
            
            info = {
                "name": gpu_name,
                "has_unified_memory": is_apple_silicon,
                "is_low_power": not is_apple_silicon,
                "supports_metal": bool(primary_gpu.get("metal_support"))
            }
            
            return True, info
            
        except Exception as e:
            logger.debug(f"Error getting GPU info: {e}")
            return False, None
    
    def estimate_performance_score(self) -> Optional[float]:
        """
        Estimate relative performance score for ML workloads
        Returns a value between 0 and 1, or None if unavailable
        """
        is_available, info = self.get_gpu_info()
        
        if not is_available or not info:
            return None
            
        # Basic scoring based on GPU type
        if info.get("has_unified_memory"):  # Apple Silicon
            return 0.8
        elif info.get("supports_metal"):    # Metal-capable discrete/integrated
            return 0.5
        else:
            return 0.3
            
    def get_gpu_utilization(self) -> Optional[dict]:
        """
        Get real-time GPU utilization metrics using ioreg
        This method uses ioreg which is accessible without sudo permissions
        once the user has installed the application with admin privileges
        
        Returns:
            Dictionary with GPU utilization metrics, or None if unavailable
        """
        if not self.is_mac:
            return None
            
        try:
            # Use ioreg to get GPU utilization data for Apple Silicon
            result = subprocess.run(
                ["ioreg", "-r", "-d", "1", "-k", "IOGPUUtilization"],
                capture_output=True,
                text=True,
                check=True
            )
            
            if "IOGPUUtilization" in result.stdout:
                # Parse the output to extract GPU utilization
                metrics = {}
                
                # Extract GPU utilization percentage
                gpu_util_match = re.search(r'"GPU"=(\d+)', result.stdout)
                if gpu_util_match:
                    metrics["gpu_utilization"] = int(gpu_util_match.group(1)) / 100.0
                
                # Extract GPU memory utilization if available
                gpu_mem_match = re.search(r'"MemController"=(\d+)', result.stdout)
                if gpu_mem_match:
                    metrics["memory_utilization"] = int(gpu_mem_match.group(1)) / 100.0
                
                return metrics
            
            # For non-Apple Silicon, try using powermetrics (doesn't require sudo if installed by admin)
            # This is a lightweight sample to minimize overhead
            result = subprocess.run(
                ["powermetrics", "--samplers", "gpu_power", "-n", "1", "-i", "100", "--show-process-energy"],
                capture_output=True,
                text=True,
                timeout=0.5,  # Short timeout to avoid blocking
                check=False   # Don't fail if it returns non-zero
            )
            
            if result.returncode == 0 and "GPU" in result.stdout:
                metrics = {}
                
                # Parse the output for GPU power/utilization
                gpu_active_match = re.search(r'GPU active frequency: (\d+)', result.stdout)
                if gpu_active_match:
                    gpu_freq = int(gpu_active_match.group(1))
                    gpu_idle_match = re.search(r'GPU idle frequency: (\d+)', result.stdout)
                    gpu_idle = int(gpu_idle_match.group(1)) if gpu_idle_match else 0
                    gpu_max_match = re.search(r'GPU max frequency: (\d+)', result.stdout)
                    gpu_max = int(gpu_max_match.group(1)) if gpu_max_match else gpu_freq
                    
                    # Calculate utilization based on frequency scaling
                    if gpu_max > gpu_idle:
                        metrics["gpu_utilization"] = (gpu_freq - gpu_idle) / (gpu_max - gpu_idle)
                    else:
                        metrics["gpu_utilization"] = 0.0
                
                return metrics
            
            return None
        except (subprocess.SubprocessError, ValueError, IndexError) as e:
            logger.debug(f"Error getting GPU utilization: {e}")
            return None
