# oblix/agents/resource_monitor/darwin/simple_gpu_monitor.py
import subprocess
import re
import platform
import json
import logging
from typing import Dict, Any, Optional, Tuple

logger = logging.getLogger(__name__)

class SimpleGPUMonitor:
    """
    Simplified GPU monitoring using ioreg to get GPU utilization without sudo.
    Based on the core technique used in macmon.
    """
    
    def __init__(self):
        """Initialize the GPU monitor"""
        self.is_mac = platform.system() == "Darwin"
        
        if not self.is_mac:
            raise RuntimeError("SimpleGPUMonitor only supports macOS")
            
        # Get basic system info once during initialization
        self.system_info = self._get_basic_system_info()
        
    def _get_basic_system_info(self) -> Dict[str, Any]:
        """Get basic system information"""
        try:
            # Run system_profiler to get hardware details
            result = subprocess.run(
                ["system_profiler", "SPHardwareDataType", "SPDisplaysDataType", "-json"],
                capture_output=True,
                text=True,
                check=True
            )
            
            data = json.loads(result.stdout)
            hardware = data.get("SPHardwareDataType", [{}])[0]
            displays = data.get("SPDisplaysDataType", [{}])[0]
            
            # Extract relevant information
            chip_name = hardware.get("chip_type", "Unknown")
            mac_model = hardware.get("machine_model", "Unknown model")
            
            # Extract memory
            mem_str = hardware.get("physical_memory", "0 GB")
            mem_gb = int(mem_str.split()[0]) if "GB" in mem_str else 0
            
            # Extract GPU info
            gpu_name = displays.get("sppci_model", chip_name)
            is_apple_silicon = "Apple" in chip_name or "Apple" in gpu_name
            
            return {
                "chip_name": chip_name,
                "mac_model": mac_model,
                "memory_gb": mem_gb,
                "gpu_name": gpu_name,
                "is_apple_silicon": is_apple_silicon
            }
        except Exception as e:
            logger.warning(f"Failed to get system info: {e}")
            return {
                "chip_name": "Unknown",
                "mac_model": "Unknown",
                "memory_gb": 0,
                "gpu_name": "Unknown GPU",
                "is_apple_silicon": False
            }
            
    def get_gpu_info(self) -> Dict[str, Any]:
        """Get basic GPU information"""
        try:
            return {
                "available": True,
                "name": self.system_info.get("gpu_name", "Unknown GPU"),
                "type": "Apple Silicon" if self.system_info.get("is_apple_silicon") else "Intel/Discrete"
            }
        except Exception as e:
            logger.error(f"Error getting GPU info: {e}")
            return {"available": False, "error": str(e)}
    
    def get_gpu_utilization(self) -> Dict[str, Any]:
        """
        Get GPU utilization metrics using ioreg
        This works without sudo and is based on the technique used in macmon
        
        Returns:
            Dictionary with GPU utilization data
        """
        try:
            # Run ioreg command to get GPU utilization data
            result = subprocess.run(
                ["ioreg", "-r", "-c", "IOService", "-k", "IOGPUUtilization"],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Look for IOGPUUtilization in the output
            if "IOGPUUtilization" in result.stdout:
                # Parse the output to extract GPU utilization
                gpu_util_match = re.search(r'"GPU"=(\d+)', result.stdout)
                gpu_util = None
                memory_util = None
                
                if gpu_util_match:
                    gpu_util = int(gpu_util_match.group(1)) / 100.0
                
                # Extract GPU memory utilization if available
                gpu_mem_match = re.search(r'"MemController"=(\d+)', result.stdout)
                if gpu_mem_match:
                    memory_util = int(gpu_mem_match.group(1)) / 100.0
                
                return {
                    "available": True,
                    "utilization": gpu_util,
                    "memory_utilization": memory_util,
                    "source": "ioreg"
                }
            
            # If we can't find IOGPUUtilization, try a broader search
            logger.debug("Using broader search for GPU utilization in ioreg")
            result = subprocess.run(
                ["ioreg", "-l", "-w", "0"],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Search for any utilization-related metrics
            if "GPUUtilization" in result.stdout:
                # Extract any utilization metrics found
                util_match = re.search(r'GPUUtilization.*?=.*?(\d+)', result.stdout)
                if util_match:
                    gpu_util = int(util_match.group(1)) / 100.0
                    return {
                        "available": True,
                        "utilization": gpu_util,
                        "source": "ioreg_broader"
                    }
            
            # Fallback to using top command to check GPU process activity
            # This is a simple heuristic, not precise measurement
            logger.debug("Using top to check GPU process activity")
            top_result = subprocess.run(
                ["top", "-l", "1", "-stats", "cpu"],
                capture_output=True,
                text=True,
                check=True
            )
            
            gpu_processes = 0
            for line in top_result.stdout.splitlines():
                if "WindowServer" in line or "com.apple.WebKit" in line:
                    gpu_processes += 1
            
            if gpu_processes > 0:
                # Rough estimate based on process activity
                return {
                    "available": True,
                    "utilization": 0.1 * gpu_processes,  # Very rough estimate
                    "source": "process_heuristic"
                }
            
            # If we still can't get data, try using a simpler ioreg approach
            result = subprocess.run(
                ["ioreg", "-n", "AGXAccelerator", "-r", "-d", "1"],
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode == 0 and "AGXAccelerator" in result.stdout:
                # Simply report the GPU is active but we can't measure utilization
                return {
                    "available": True,
                    "utilization": None,
                    "source": "agx_detection",
                    "note": "GPU is active but utilization cannot be measured"
                }
            
            # If all methods fail, return not available
            return {
                "available": False,
                "reason": "Could not obtain GPU utilization with available methods"
            }
                
        except Exception as e:
            logger.error(f"Error getting GPU utilization: {e}")
            return {
                "available": False,
                "error": str(e)
            }