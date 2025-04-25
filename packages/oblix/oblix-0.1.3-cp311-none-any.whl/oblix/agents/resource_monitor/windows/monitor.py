# oblix/agents/resource_monitor/windows/monitor.py
import psutil
import subprocess
import json
import re
import platform
import ctypes
from typing import Dict, Any, List, Optional
import logging
import asyncio

from ..base import SystemMonitor

logger = logging.getLogger(__name__)

# Try to import wmi, a Windows-specific package for hardware monitoring
try:
    import wmi
    WMI_AVAILABLE = True
except ImportError:
    WMI_AVAILABLE = False
    logger.debug("WMI package not available, some GPU monitoring features will be limited")

# Check if we can import win32api for better Windows integration
try:
    import win32api
    WIN32API_AVAILABLE = True
except ImportError:
    WIN32API_AVAILABLE = False
    logger.debug("win32api not available, using fallback methods")

# Try to import pynvml for NVIDIA GPU monitoring
try:
    import pynvml
    PYNVML_AVAILABLE = True
except ImportError:
    PYNVML_AVAILABLE = False
    logger.debug("NVIDIA Management Library not available")

class WindowsGPUMonitor:
    """Windows GPU monitoring implementation with multiple backends"""
    
    def __init__(self):
        """Initialize GPU monitoring capabilities with fallbacks"""
        self.wmi_client = None
        self.nvml_initialized = False
        
        # Try to initialize WMI for basic GPU detection
        if WMI_AVAILABLE:
            try:
                self.wmi_client = wmi.WMI()
                logger.debug("WMI client initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize WMI: {e}")
                self.wmi_client = None
        
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
        
        # Fall back to WMI
        if self.wmi_client:
            try:
                gpus = self.wmi_client.Win32_VideoController()
                if gpus:
                    # Use the first GPU
                    gpu = gpus[0]
                    
                    # Determine GPU type based on name
                    gpu_type = "Integrated"
                    if "NVIDIA" in gpu.Name:
                        gpu_type = "NVIDIA"
                    elif "AMD" in gpu.Name or "Radeon" in gpu.Name:
                        gpu_type = "AMD"
                    elif "Intel" in gpu.Name:
                        gpu_type = "Intel"
                    
                    return {
                        "available": True,
                        "name": gpu.Name,
                        "type": gpu_type,
                        "adapter_ram_mb": int(getattr(gpu, "AdapterRAM", 0) or 0) / (1024 * 1024),
                        "driver_version": getattr(gpu, "DriverVersion", "Unknown"),
                        "device_count": len(gpus),
                        "source": "wmi"
                    }
            except Exception as e:
                logger.debug(f"Error getting WMI GPU info: {e}")
                # Continue to fallback method
        
        # Last resort: use dxdiag
        try:
            # Run dxdiag and capture output
            process = subprocess.Popen(
                ["dxdiag", "/t", "temp_dxdiag.txt"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True
            )
            process.wait(timeout=10)
            
            # Read the output file
            with open("temp_dxdiag.txt", "r") as f:
                dxdiag_output = f.read()
            
            # Clean up
            subprocess.run(["del", "temp_dxdiag.txt"], shell=True)
            
            # Extract GPU info
            gpu_name = None
            gpu_memory = None
            
            for line in dxdiag_output.split("\n"):
                if "Card name:" in line:
                    gpu_name = line.split("Card name:")[1].strip()
                if "Dedicated Memory:" in line:
                    memory_match = re.search(r"(\d+) MB", line)
                    if memory_match:
                        gpu_memory = int(memory_match.group(1))
            
            if gpu_name:
                # Determine GPU type based on name
                gpu_type = "Integrated"
                if "NVIDIA" in gpu_name:
                    gpu_type = "NVIDIA"
                elif "AMD" in gpu_name or "Radeon" in gpu_name:
                    gpu_type = "AMD"
                elif "Intel" in gpu_name:
                    gpu_type = "Intel"
                
                return {
                    "available": True,
                    "name": gpu_name,
                    "type": gpu_type,
                    "memory_mb": gpu_memory,
                    "source": "dxdiag"
                }
        except Exception as e:
            logger.debug(f"Error getting dxdiag GPU info: {e}")
            
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
        
        # WMI doesn't provide reliable GPU utilization metrics, so use typeperf as fallback
        try:
            # Use typeperf to get GPU metrics
            process = subprocess.Popen(
                ["typeperf", "-sc", "1", "\\GPU Engine(*engtype_3D)\\Utilization Percentage"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate(timeout=5)
            
            # Parse the output
            lines = stdout.strip().split('\n')
            if len(lines) >= 2:
                # Last line should have the values
                values = lines[1].strip('"').split(',')
                if len(values) >= 2:
                    # The GPU utilization value
                    try:
                        utilization = float(values[1]) / 100.0  # Convert to 0-1 scale
                        return {
                            "available": True,
                            "utilization": utilization,
                            "memory_utilization": None,  # Not available with this method
                            "source": "typeperf"
                        }
                    except (ValueError, IndexError):
                        pass
        except Exception as e:
            logger.debug(f"Error getting typeperf GPU utilization: {e}")
        
        # Last fallback: estimate GPU performance based on available info
        try:
            if self.wmi_client:
                gpus = self.wmi_client.Win32_VideoController()
                if gpus:
                    gpu = gpus[0]
                    
                    # Make an educated guess based on GPU name
                    performance_score = 0.5  # Default score
                    
                    if "RTX" in gpu.Name or "GTX" in gpu.Name:
                        # NVIDIA gaming cards - likely high performance
                        performance_score = 0.8
                    elif "Quadro" in gpu.Name:
                        # NVIDIA workstation cards - likely high performance
                        performance_score = 0.7
                    elif "Radeon" in gpu.Name and ("RX" in gpu.Name or "Vega" in gpu.Name):
                        # AMD gaming cards - likely high performance
                        performance_score = 0.7
                    elif "Intel" in gpu.Name and "Iris" in gpu.Name:
                        # Intel Iris - medium performance
                        performance_score = 0.4
                    elif "Intel" in gpu.Name:
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

class WindowsSystemMonitor(SystemMonitor):
    """Windows specific system monitoring implementation"""
    
    def __init__(self):
        """Initialize the system monitor"""
        self.gpu_monitor = WindowsGPUMonitor()
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
            
            # Get load average (not directly available on Windows)
            # We'll use a custom calculation based on CPU usage
            # Load average on Windows can be approximated
            load_1min = cpu_percent / 100.0 * cpu_count
            
            # Get CPU model information
            cpu_model = "Unknown CPU"
            if WIN32API_AVAILABLE:
                try:
                    cpu_model = win32api.GetSystemInfo()[4]
                except Exception:
                    pass
            
            # Fallback to registry if win32api failed
            if cpu_model == "Unknown CPU":
                try:
                    result = subprocess.run(
                        ["wmic", "cpu", "get", "name"],
                        capture_output=True,
                        text=True
                    )
                    # Parse output - skip the header line
                    lines = result.stdout.strip().split('\n')
                    if len(lines) > 1:
                        cpu_model = lines[1].strip()
                except Exception as e:
                    logger.debug(f"Failed to get CPU model: {e}")
            
            return {
                "usage_percent": cpu_percent,
                "frequency_mhz": cpu_freq.current if cpu_freq else None,
                "core_count": {
                    "physical": cpu_count_physical,
                    "logical": cpu_count
                },
                "model": cpu_model,
                "load_average": {
                    "1min": load_1min,
                    "5min": load_1min,  # Same value as 1min since Windows doesn't track this
                    "15min": load_1min  # Same value as 1min since Windows doesn't track this
                },
                "source": "psutil+wmic"
            }
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