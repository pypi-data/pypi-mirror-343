# oblix/agents/resource_monitor/darwin/monitor.py
import psutil
import subprocess
import json
import re
import platform
from typing import Dict, Any
import logging
from ..base import SystemMonitor

logger = logging.getLogger(__name__)

# Try to import Macmon GPU monitor (preferred)
try:
    from .macmon_wrapper import MacmonGPUMonitor
    MACMON_AVAILABLE = True
except ImportError:
    MACMON_AVAILABLE = False
    logger.debug("Macmon wrapper not available, falling back to other methods")

# Try to import Metal monitor, fallback gracefully if not available
try:
    from .metal import MetalGPUMonitor
    METAL_AVAILABLE = True
except ImportError:
    METAL_AVAILABLE = False
    logger.debug("Metal framework not available, using basic GPU detection")

# Try to import our simplified GPU monitor
try:
    from .simple_gpu_monitor import SimpleGPUMonitor
    SIMPLE_GPU_AVAILABLE = True
except ImportError:
    SIMPLE_GPU_AVAILABLE = False
    logger.debug("Simple GPU monitor not available, using fallback detection")

class DarwinSystemMonitor(SystemMonitor):
    """macOS specific system monitoring implementation"""
    
    def __init__(self):
        """
        Initialize the system monitor with robust error handling
        for GPU monitoring capabilities
        """
        self.macmon_monitor = None
        self.metal_monitor = None
        self.simple_gpu_monitor = None
        self.subprocesses = []  # Track any subprocesses that need cleanup
        
        # Try to initialize macmon monitor first (highest priority)
        if MACMON_AVAILABLE:
            try:
                self.macmon_monitor = MacmonGPUMonitor()
                # Only consider macmon available if it found a binary
                if not self.macmon_monitor.macmon_path:
                    self.macmon_monitor = None
                    logger.info("Macmon binary not available, falling back to other methods")
                else:
                    logger.info("Macmon GPU monitoring initialized successfully")
            except Exception as e:
                self.macmon_monitor = None
                logger.warning(f"Failed to initialize Macmon GPU monitor: {e}")
        
        # Try to initialize simple GPU monitor as second option
        if SIMPLE_GPU_AVAILABLE and not self.macmon_monitor:
            try:
                self.simple_gpu_monitor = SimpleGPUMonitor()
                logger.info("Simple GPU monitoring initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize Simple GPU monitor: {e}")
        
        # Fall back to Metal monitor if needed
        if METAL_AVAILABLE and not self.macmon_monitor and not self.simple_gpu_monitor:
            try:
                self.metal_monitor = MetalGPUMonitor()
                logger.info("Metal GPU monitoring initialized successfully")
            except RuntimeError as e:
                logger.warning(f"Failed to initialize Metal GPU monitor: {e}")
            except Exception as e:
                logger.error(f"Unexpected error initializing Metal GPU monitor: {e}")
                # Continue without Metal GPU monitoring
    
    async def get_cpu_info(self) -> Dict[str, Any]:
        """Get CPU information and usage"""
        # Standard psutil implementation for CPU info
        
        # Standard psutil implementation when IOReport is not available
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            cpu_freq = psutil.cpu_freq() if hasattr(psutil, 'cpu_freq') else None
            cpu_count = psutil.cpu_count()
            cpu_count_physical = psutil.cpu_count(logical=False)
            
            load_avg = psutil.getloadavg()
            
            return {
                "usage_percent": cpu_percent,
                "frequency_mhz": cpu_freq.current if cpu_freq else None,
                "core_count": {
                    "physical": cpu_count_physical,
                    "logical": cpu_count
                },
                "load_average": {
                    "1min": load_avg[0],
                    "5min": load_avg[1],
                    "15min": load_avg[2]
                },
                "source": "psutil"
            }
        except Exception as e:
            logger.error(f"Error getting CPU info: {e}")
            return {"error": str(e)}
    
    async def get_memory_info(self) -> Dict[str, Any]:
        """Get memory information and usage"""
        # Standard psutil implementation for memory info
        
        # Standard psutil implementation
        try:
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
        """
        Get GPU information using prioritized monitors:
        1. Macmon (Rust implementation, most accurate)
        2. SimpleGPUMonitor (Python ioreg wrapper) 
        3. Metal (framework-based monitor)
        4. Fallback to basic detection
        
        Returns:
            Dict containing GPU information and utilization metrics
        """
        try:
            # OPTION 1: If macmon monitor is available, use it first (highest priority)
            if self.macmon_monitor:
                try:
                    # Get GPU info
                    gpu_info = self.macmon_monitor.get_gpu_info()
                    
                    # Get GPU utilization
                    utilization_data = self.macmon_monitor.get_gpu_utilization()
                    
                    if gpu_info.get("available", False) and utilization_data.get("available", False):
                        return {
                            "available": True,
                            "name": gpu_info.get("name", "Unknown GPU"),
                            "type": gpu_info.get("type", "Unknown"),
                            "utilization": utilization_data.get("utilization"),
                            "memory_utilization": utilization_data.get("memory_utilization"),
                            "source": utilization_data.get("source", "macmon")
                        }
                except Exception as e:
                    logger.warning(f"Error using MacmonGPUMonitor: {e}")
                    # Continue to next method
            
            # OPTION 2: If simple GPU monitor is available, use it as secondary option
            if self.simple_gpu_monitor:
                try:
                    # Get GPU info
                    gpu_info = self.simple_gpu_monitor.get_gpu_info()
                    
                    # Get GPU utilization
                    utilization_data = self.simple_gpu_monitor.get_gpu_utilization()
                    
                    if gpu_info.get("available", False) and utilization_data.get("available", False):
                        return {
                            "available": True,
                            "name": gpu_info.get("name", "Unknown GPU"),
                            "type": gpu_info.get("type", "Unknown"),
                            "utilization": utilization_data.get("utilization"),
                            "memory_utilization": utilization_data.get("memory_utilization"),
                            "source": utilization_data.get("source", "simple_gpu_monitor")
                        }
                except Exception as e:
                    logger.warning(f"Error using SimpleGPUMonitor: {e}")
                    # Continue to next method
            
            # OPTION 3: If Metal is available, use it as third fallback
            if self.metal_monitor:
                try:
                    is_available, metal_info = self.metal_monitor.get_gpu_info()
                    if is_available and metal_info:
                        performance_score = None
                        try:
                            performance_score = self.metal_monitor.estimate_performance_score()
                        except Exception as e:
                            logger.warning(f"Failed to estimate GPU performance: {e}")
                        
                        # Get real-time GPU utilization metrics
                        utilization_metrics = {}
                        try:
                            gpu_metrics = self.metal_monitor.get_gpu_utilization()
                            if gpu_metrics:
                                utilization_metrics = gpu_metrics
                        except Exception as e:
                            logger.warning(f"Failed to get GPU utilization metrics: {e}")
                            
                        return {
                            "available": True,
                            "name": metal_info.get("name", "Unknown GPU"),
                            "type": "Apple Silicon" if metal_info.get("has_unified_memory") 
                                   else "Intel/Discrete",
                            "metal_support": True,
                            "performance_score": performance_score,
                            "utilization": utilization_metrics.get("gpu_utilization") if utilization_metrics else None,
                            "memory_utilization": utilization_metrics.get("memory_utilization") if utilization_metrics else None,
                            "source": "metal"
                        }
                except Exception as e:
                    logger.warning(f"Error using Metal GPU monitor: {e}")
                    # Continue to fallback implementation
            
            # OPTION 4: Fallback to basic system_profiler detection
            result = subprocess.run(
                ["system_profiler", "SPDisplaysDataType", "-json"],
                capture_output=True,
                text=True,
                check=True
            )
            
            gpu_data = json.loads(result.stdout)
            graphics_cards = gpu_data.get("SPDisplaysDataType", [])
            
            if not graphics_cards:
                return {
                    "available": False,
                    "reason": "No GPU information found"
                }
            
            primary_gpu = graphics_cards[0]
            gpu_name = primary_gpu.get("sppci_model", "Unknown GPU")
            is_apple_silicon = "Apple" in gpu_name
            
            # Try one last attempt with ioreg for basic utilization
            try:
                result = subprocess.run(
                    ["ioreg", "-l", "-w", "0"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                
                # Search for any utilization-related metrics
                gpu_util = None
                if "GPUUtilization" in result.stdout:
                    util_match = re.search(r'GPUUtilization.*?=.*?(\d+)', result.stdout)
                    if util_match:
                        gpu_util = int(util_match.group(1)) / 100.0
                
                return {
                    "available": True,
                    "name": gpu_name,
                    "type": "Apple Silicon" if is_apple_silicon else "Intel/Discrete",
                    "metal_support": bool(primary_gpu.get("metal_support")),
                    "utilization": gpu_util,
                    "performance_score": 0.8 if is_apple_silicon else 0.5,
                    "source": "system_profiler+ioreg"
                }
            except Exception as e:
                logger.debug(f"Failed to get GPU utilization with ioreg: {e}")
                
                return {
                    "available": True,
                    "name": gpu_name,
                    "type": "Apple Silicon" if is_apple_silicon else "Intel/Discrete",
                    "metal_support": bool(primary_gpu.get("metal_support")),
                    "performance_score": 0.8 if is_apple_silicon else 0.5,
                    "source": "system_profiler"
                }
            
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
            # Clean up macmon monitor if it exists
            if self.macmon_monitor and hasattr(self.macmon_monitor, 'cleanup'):
                self.macmon_monitor.cleanup()
                
            # Clean up metal monitor if it exists
            if self.metal_monitor and hasattr(self.metal_monitor, 'cleanup'):
                self.metal_monitor.cleanup()
                
            # Clean up simple GPU monitor if it exists
            if self.simple_gpu_monitor and hasattr(self.simple_gpu_monitor, 'cleanup'):
                self.simple_gpu_monitor.cleanup()
                
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