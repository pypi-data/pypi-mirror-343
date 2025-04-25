# oblix/agents/resource_monitor/linux/monitor.py
import psutil
import subprocess
import json
import re
import platform
from typing import Dict, Any, List, Optional
import logging
import asyncio
import os

from ..base import SystemMonitor

logger = logging.getLogger(__name__)

# Try to import pynvml for NVIDIA GPU monitoring
try:
    import pynvml
    PYNVML_AVAILABLE = True
except ImportError:
    PYNVML_AVAILABLE = False
    logger.debug("NVIDIA Management Library not available")

# Check if lm_sensors is installed for temperature monitoring
def is_lm_sensors_available():
    try:
        result = subprocess.run(['which', 'sensors'], capture_output=True, text=True)
        return result.returncode == 0
    except Exception:
        return False

LM_SENSORS_AVAILABLE = is_lm_sensors_available()

class LinuxGPUMonitor:
    """Linux GPU monitoring implementation with multiple backends"""
    
    def __init__(self):
        """Initialize GPU monitoring capabilities with fallbacks"""
        self.nvml_initialized = False
        self.subprocesses = []
        
        # Try to initialize NVML for NVIDIA GPU monitoring
        if PYNVML_AVAILABLE:
            try:
                pynvml.nvmlInit()
                self.nvml_initialized = True
                logger.debug("NVIDIA Management Library initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize NVIDIA Management Library: {e}")
                self.nvml_initialized = False
    
    def get_gpu_info(self) -> Dict[str, Any]:
        """Get basic GPU information"""
        # First try NVML for NVIDIA GPUs
        if self.nvml_initialized:
            try:
                device_count = pynvml.nvmlDeviceGetCount()
                if device_count > 0:
                    # Use the first GPU for now
                    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                    name = pynvml.nvmlDeviceGetName(handle)
                    memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
                    
                    return {
                        "available": True,
                        "name": name,
                        "type": "NVIDIA",
                        "memory_total_mb": memory_info.total / (1024 * 1024),
                        "device_count": device_count,
                        "source": "nvml"
                    }
            except Exception as e:
                logger.debug(f"Error getting NVIDIA GPU info: {e}")
                # Continue to next method
        
        # Try lspci as fallback
        try:
            process = subprocess.run(
                ["lspci", "-v"], 
                capture_output=True, 
                text=True
            )
            
            if process.returncode == 0:
                output = process.stdout
                
                # Find all VGA and 3D controller entries
                gpu_lines = []
                current_gpu = None
                
                for line in output.split('\n'):
                    if "VGA compatible controller" in line or "3D controller" in line:
                        current_gpu = line
                        gpu_lines.append(current_gpu)
                    elif current_gpu and line.startswith('\t'):
                        # Continuation of current GPU info
                        current_gpu = line
                
                if gpu_lines:
                    # Parse the first GPU entry
                    gpu_info = gpu_lines[0]
                    
                    # Determine GPU type and name
                    gpu_name = "Unknown GPU"
                    gpu_type = "Unknown"
                    
                    if "NVIDIA" in gpu_info:
                        gpu_type = "NVIDIA"
                        # Extract model
                        match = re.search(r"NVIDIA Corporation\s([^\[]*)", gpu_info)
                        if match:
                            gpu_name = match.group(1).strip()
                    elif "AMD" in gpu_info or "ATI" in gpu_info:
                        gpu_type = "AMD"
                        # Extract model
                        match = re.search(r"(AMD|ATI).*?([^\[]*)", gpu_info)
                        if match:
                            gpu_name = match.group(2).strip()
                    elif "Intel" in gpu_info:
                        gpu_type = "Intel"
                        # Extract model
                        match = re.search(r"Intel Corporation\s([^\[]*)", gpu_info)
                        if match:
                            gpu_name = match.group(1).strip()
                    
                    return {
                        "available": True,
                        "name": gpu_name,
                        "type": gpu_type,
                        "device_count": len(gpu_lines),
                        "source": "lspci"
                    }
            
        except Exception as e:
            logger.debug(f"Error getting lspci GPU info: {e}")
        
        # Try reading from sysfs for basic detection (works with Intel/AMD integrated GPUs too)
        try:
            # Check for GPUs in sysfs
            gpu_dirs = []
            dri_path = "/sys/class/drm"
            
            if os.path.exists(dri_path) and os.path.isdir(dri_path):
                for entry in os.listdir(dri_path):
                    card_path = os.path.join(dri_path, entry)
                    # Check if it's a card directory (not renderD*)
                    if os.path.isdir(card_path) and entry.startswith("card") and "renderD" not in entry:
                        gpu_dirs.append(card_path)
            
            if gpu_dirs:
                # Determine GPU name and type if possible
                gpu_name = "Linux GPU"
                gpu_type = "Integrated"  # Default assumption
                
                # Try to get more details
                try:
                    # Look for a device/vendor file that might exist
                    for card_path in gpu_dirs:
                        vendor_path = os.path.join(card_path, "device/vendor")
                        if os.path.exists(vendor_path):
                            with open(vendor_path, 'r') as f:
                                vendor_id = f.read().strip()
                                
                                if vendor_id == "0x10de":
                                    gpu_type = "NVIDIA"
                                elif vendor_id == "0x1002":
                                    gpu_type = "AMD"
                                elif vendor_id == "0x8086":
                                    gpu_type = "Intel"
                except Exception:
                    pass
                
                return {
                    "available": True,
                    "name": gpu_name,
                    "type": gpu_type,
                    "device_count": len(gpu_dirs),
                    "source": "sysfs"
                }
        except Exception as e:
            logger.debug(f"Error getting sysfs GPU info: {e}")
        
        # If all else fails, return basic info
        return {
            "available": True,  # Assume some GPU is available
            "name": "Unknown GPU",
            "type": "Unknown",
            "source": "fallback"
        }
    
    def get_gpu_utilization(self) -> Dict[str, Any]:
        """Get GPU utilization metrics"""
        # First try NVML for NVIDIA GPUs
        if self.nvml_initialized:
            try:
                device_count = pynvml.nvmlDeviceGetCount()
                if device_count > 0:
                    # Use the first GPU for now
                    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                    
                    # Get utilization
                    utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
                    memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
                    
                    # Calculate memory utilization percentage
                    memory_utilization = memory_info.used / memory_info.total
                    
                    return {
                        "available": True,
                        "utilization": utilization.gpu / 100.0,  # Convert to 0-1 scale
                        "memory_utilization": memory_utilization,
                        "temperature_c": pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU),
                        "source": "nvml"
                    }
            except Exception as e:
                logger.debug(f"Error getting NVIDIA GPU utilization: {e}")
                # Continue to next method
        
        # Try to get data from /proc and /sys/class/drm
        try:
            gpu_load = None
            
            # Try with Intel GPU through i915_gpu_busy
            i915_busy_path = "/sys/class/drm/card0/device/gpu_busy_percent"
            if os.path.exists(i915_busy_path):
                with open(i915_busy_path, 'r') as f:
                    gpu_load = int(f.read().strip()) / 100.0  # Convert to 0-1 scale
            
            # If we got a value, return it
            if gpu_load is not None:
                return {
                    "available": True,
                    "utilization": gpu_load,
                    "memory_utilization": None,  # Not available with this method
                    "source": "i915_sysfs"
                }
        except Exception as e:
            logger.debug(f"Error getting i915 GPU utilization: {e}")
        
        # For AMD GPUs, we can try with amdgpu sysfs entries
        try:
            # Try AMD GPU sysfs interface
            amdgpu_busy_path = "/sys/class/drm/card0/device/gpu_busy_percent"
            if os.path.exists(amdgpu_busy_path):
                with open(amdgpu_busy_path, 'r') as f:
                    gpu_load = int(f.read().strip()) / 100.0  # Convert to 0-1 scale
                
                # If we got a value, return it
                if gpu_load is not None:
                    return {
                        "available": True,
                        "utilization": gpu_load,
                        "memory_utilization": None,  # Not always available
                        "source": "amdgpu_sysfs"
                    }
        except Exception as e:
            logger.debug(f"Error getting amdgpu utilization: {e}")
        
        # Last fallback: estimate GPU performance based on available info
        try:
            # Run lspci to make an educated guess
            process = subprocess.run(
                ["lspci", "-v"], 
                capture_output=True, 
                text=True
            )
            
            if process.returncode == 0:
                gpu_info = process.stdout
                
                # Make an educated guess based on GPU name
                performance_score = 0.5  # Default score
                
                if "NVIDIA" in gpu_info:
                    if "RTX" in gpu_info or "GTX" in gpu_info:
                        # NVIDIA gaming cards - likely high performance
                        performance_score = 0.8
                    elif "Quadro" in gpu_info:
                        # NVIDIA workstation cards - likely high performance
                        performance_score = 0.7
                    elif "GT " in gpu_info or "MX" in gpu_info:
                        # Lower-end NVIDIA cards
                        performance_score = 0.5
                elif "AMD" in gpu_info or "ATI" in gpu_info:
                    if "RX" in gpu_info or "Vega" in gpu_info:
                        # AMD gaming cards - likely high performance
                        performance_score = 0.7
                    elif "Radeon" in gpu_info:
                        performance_score = 0.6
                elif "Intel" in gpu_info:
                    if "Arc" in gpu_info:
                        # Intel Arc - better performance
                        performance_score = 0.6
                    elif "Iris" in gpu_info:
                        # Intel Iris - medium performance
                        performance_score = 0.4
                    else:
                        # Intel integrated - lower performance
                        performance_score = 0.3
                
                return {
                    "available": True,
                    "utilization": 0.5,  # Default placeholder value
                    "memory_utilization": 0.5,  # Default placeholder value
                    "performance_score": performance_score,
                    "source": "estimation"
                }
        except Exception as e:
            logger.debug(f"Error estimating GPU performance: {e}")
        
        # If all else fails, return placeholders
        return {
            "available": True,
            "utilization": 0.5,  # Default placeholder
            "memory_utilization": 0.5,  # Default placeholder
            "source": "fallback"
        }
        
    def cleanup(self):
        """Clean up resources"""
        if self.nvml_initialized:
            try:
                pynvml.nvmlShutdown()
            except Exception:
                pass
        
        # Clean up any subprocesses we might have started
        for proc in self.subprocesses:
            if proc.poll() is None:  # Only terminate if still running
                try:
                    proc.terminate()
                except Exception:
                    pass

class LinuxSystemMonitor(SystemMonitor):
    """Linux specific system monitoring implementation for x86 architecture"""
    
    def __init__(self):
        """Initialize the system monitor"""
        self.gpu_monitor = LinuxGPUMonitor()
        self.subprocesses = []  # Track any subprocesses that need cleanup
    
    async def get_cpu_info(self) -> Dict[str, Any]:
        """Get CPU information and usage"""
        try:
            # Get CPU percentage - wait a bit for accurate reading
            cpu_percent = psutil.cpu_percent(interval=0.1)
            
            # Get CPU frequency
            cpu_freq = psutil.cpu_freq()
            
            # Get logical and physical cores
            cpu_count = psutil.cpu_count()
            cpu_count_physical = psutil.cpu_count(logical=False)
            
            # Get load average
            load_avg = psutil.getloadavg()
            
            # Get CPU model information
            cpu_model = "Unknown CPU"
            
            # Attempt to get CPU model from /proc/cpuinfo
            try:
                with open('/proc/cpuinfo', 'r') as f:
                    for line in f:
                        if "model name" in line:
                            cpu_model = line.split(':', 1)[1].strip()
                            break
            except Exception as e:
                logger.debug(f"Failed to get CPU model from /proc/cpuinfo: {e}")
                
                # Fallback to lscpu
                try:
                    result = subprocess.run(['lscpu'], capture_output=True, text=True)
                    if result.returncode == 0:
                        for line in result.stdout.splitlines():
                            if "Model name:" in line:
                                cpu_model = line.split(':', 1)[1].strip()
                                break
                except Exception as e:
                    logger.debug(f"Failed to get CPU model from lscpu: {e}")
            
            # Try to get temperature if available
            cpu_temp = None
            if LM_SENSORS_AVAILABLE:
                try:
                    # Run sensors command to get temperature data
                    result = subprocess.run(['sensors'], capture_output=True, text=True)
                    if result.returncode == 0:
                        # Look for temperature readings
                        for line in result.stdout.splitlines():
                            if "Core" in line and "°C" in line:
                                # Extract temperature value
                                temp_match = re.search(r'(\+|\-)?([0-9]+\.[0-9]+)°C', line)
                                if temp_match:
                                    # If we find multiple cores, use the first one
                                    # (or implement average if needed)
                                    if cpu_temp is None:
                                        temp_value = float(temp_match.group(2))
                                        cpu_temp = temp_value
                except Exception as e:
                    logger.debug(f"Failed to get CPU temperature: {e}")
            
            result = {
                "usage_percent": cpu_percent,
                "frequency_mhz": cpu_freq.current if cpu_freq else None,
                "core_count": {
                    "physical": cpu_count_physical,
                    "logical": cpu_count
                },
                "model": cpu_model,
                "load_average": {
                    "1min": load_avg[0],
                    "5min": load_avg[1],
                    "15min": load_avg[2]
                },
                "source": "psutil+procfs"
            }
            
            # Add temperature if available
            if cpu_temp is not None:
                result["temperature_c"] = cpu_temp
                
            return result
        except Exception as e:
            logger.error(f"Error getting CPU info: {e}")
            return {"error": str(e)}
    
    async def get_memory_info(self) -> Dict[str, Any]:
        """Get memory information and usage"""
        try:
            # Standard psutil implementation
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            return {
                "ram": {
                    "total_gb": memory.total / (1024 ** 3),
                    "available_gb": memory.available / (1024 ** 3),
                    "used_gb": memory.used / (1024 ** 3),
                    "usage_percent": memory.percent
                },
                "swap": {
                    "total_gb": swap.total / (1024 ** 3),
                    "used_gb": swap.used / (1024 ** 3),
                    "usage_percent": swap.percent
                },
                "source": "psutil"
            }
        except Exception as e:
            logger.error(f"Error getting memory info: {e}")
            return {"error": str(e)}
    
    async def get_gpu_info(self) -> Dict[str, Any]:
        """Get GPU information and utilization"""
        try:
            # Get basic GPU info
            gpu_info = self.gpu_monitor.get_gpu_info()
            
            # Get GPU utilization
            utilization_data = self.gpu_monitor.get_gpu_utilization()
            
            # Combine the data
            combined_data = {
                **gpu_info,
                "utilization": utilization_data.get("utilization"),
                "memory_utilization": utilization_data.get("memory_utilization"),
                "utilization_source": utilization_data.get("source")
            }
            
            return combined_data
            
        except Exception as e:
            logger.error(f"Error in get_gpu_info: {e}")
            return {
                "available": False,
                "error": str(e),
                "reason": "Error getting GPU information"
            }
    
    async def cleanup(self):
        """Clean up any resources used by the monitor"""
        try:
            # Clean up GPU monitor
            if hasattr(self.gpu_monitor, 'cleanup'):
                self.gpu_monitor.cleanup()
                
            # Terminate any tracked subprocesses
            for proc in self.subprocesses:
                if proc.poll() is None:  # Only terminate if still running
                    try:
                        proc.terminate()
                    except Exception:
                        pass
        except Exception:
            # Silently ignore any errors during cleanup
            pass