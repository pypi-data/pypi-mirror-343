# oblix/agents/resource_monitor/darwin/macmon_wrapper.py
import subprocess
import os
import json
import logging
import platform
from typing import Dict, Any, Optional, Tuple

logger = logging.getLogger(__name__)

class MacmonGPUMonitor:
    """
    Python wrapper for the macmon Rust monitoring tool
    Provides GPU utilization and other metrics from macmon
    """
    
    def __init__(self):
        """
        Initialize the macmon GPU monitor
        
        Raises:
            RuntimeError: If not on macOS or macmon binary is not available
        """
        self.is_mac = platform.system() == "Darwin"
        
        if not self.is_mac:
            raise RuntimeError("MacmonGPUMonitor only supports macOS")
        
        # Determine the path to the macmon binary
        self.macmon_path = self._find_macmon_binary()
        
        if not self.macmon_path:
            logger.warning("macmon binary not found. Advanced GPU monitoring unavailable.")
            # Don't raise exception - the monitor.py will fall back to other methods
        else:
            logger.info(f"MacmonGPUMonitor initialized with binary: {self.macmon_path}")
        
    def _find_macmon_binary(self) -> Optional[str]:
        """Find the macmon binary path"""
        # Check in the same directory as this file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        macmon_dir = os.path.join(script_dir, "macmon")
        
        # Potential locations for the binary - prioritize the pre-built binary in bin directory
        potential_paths = [
            os.path.join(macmon_dir, "bin", "macmon"),  # Pre-packaged binary
            os.path.join(macmon_dir, "macmon"),  # Direct in macmon directory
            os.path.join(macmon_dir, "target", "release", "macmon"),
            os.path.join(macmon_dir, "target", "debug", "macmon")
        ]
        
        for path in potential_paths:
            if os.path.isfile(path) and os.access(path, os.X_OK):
                return path
        
        # We no longer auto-build at runtime, just log that the binary wasn't found
        logger.warning("Pre-built macmon binary not found. Advanced GPU monitoring will not be available.")
        
        return None
    
    def get_gpu_info(self) -> Dict[str, Any]:
        """Get basic GPU information"""
        # If binary not found, report unavailable immediately
        if not self.macmon_path:
            return {"available": False, "reason": "macmon binary not available"}
            
        try:
            # Use a single sample with minimal interval for fastest hardware info
            metrics = self._run_macmon_command(samples=1, interval=100)
            
            if not metrics:
                return {"available": False, "reason": "Failed to collect GPU info from macmon"}
            
            # Look for GPU info in the metrics
            gpu_available = "gpu_usage" in metrics
            gpu_type = "Apple Silicon" if gpu_available else "Unknown"
            
            # Try to extract GPU name
            gpu_name = None
            
            return {
                "available": gpu_available,
                "name": gpu_name or ("Apple Silicon GPU" if gpu_available else "Unknown GPU"),
                "type": gpu_type
            }
        except Exception as e:
            logger.error(f"Error getting GPU info from macmon: {e}")
            return {"available": False, "error": str(e)}
    
    def get_gpu_utilization(self) -> Dict[str, Any]:
        """
        Get GPU utilization metrics using macmon
        
        Returns:
            Dictionary with GPU utilization data
        """
        # If binary not found, report unavailable immediately
        if not self.macmon_path:
            return {"available": False, "reason": "macmon binary not available"}
            
        try:
            # Run macmon with 1 sample and minimal interval for fastest responses
            metrics = self._run_macmon_command(samples=1, interval=100)
            
            if not metrics or "gpu_usage" not in metrics:
                return {"available": False, "reason": "GPU metrics not available from macmon"}
            
            # Extract GPU utilization - macmon provides as (frequency, percent_from_max)
            gpu_usage = metrics.get("gpu_usage", (0, 0))
            if isinstance(gpu_usage, list) and len(gpu_usage) >= 2:
                gpu_util = gpu_usage[1]  # percent_from_max is the utilization
            else:
                gpu_util = gpu_usage[1] if isinstance(gpu_usage, tuple) else 0
            
            # Extract memory utilization if available
            memory_utilization = None
            memory_data = metrics.get("memory", {})
            if memory_data and "ram_total" in memory_data and "ram_usage" in memory_data:
                ram_total = memory_data.get("ram_total", 1)
                ram_usage = memory_data.get("ram_usage", 0)
                if ram_total > 0:
                    memory_utilization = ram_usage / ram_total
            
            return {
                "available": True,
                "utilization": gpu_util,
                "memory_utilization": memory_utilization,
                "source": "macmon"
            }
                
        except Exception as e:
            logger.error(f"Error getting GPU utilization from macmon: {e}")
            return {
                "available": False,
                "error": str(e)
            }
    
    def _run_macmon_command(self, samples=1, interval=100) -> Optional[Dict[str, Any]]:
        """
        Run macmon and parse its output
        
        Args:
            samples: Number of samples to collect (default 1)
            interval: Sampling interval in milliseconds (default 100ms - minimized for faster response)
        """
        try:
            if not self.macmon_path:
                return None
            
            # Run macmon in pipe mode to get JSON output
            # Use start_new_session=True to prevent macmon from being killed by SIGINT to the parent process
            result = subprocess.run(
                [self.macmon_path, "pipe", "--samples", str(samples), "--interval", str(interval)],
                capture_output=True,
                text=True,
                check=True,
                timeout=3,  # Balanced timeout for reliability and responsiveness
                start_new_session=True  # Isolate subprocess from parent signals
            )
            
            # Parse the JSON output
            try:
                # Macmon outputs one JSON object per line for each sample
                last_line = result.stdout.strip().split('\n')[-1]
                metrics = json.loads(last_line)
                return metrics
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse macmon output: {e}")
                logger.debug(f"macmon raw output: {result.stdout}")
                return None
                
        except subprocess.SubprocessError as e:
            logger.error(f"Error running macmon: {e}")
            return None
            
    def cleanup(self):
        """Cleanup any resources used by the monitor"""
        # Nothing to do here as we don't keep subprocesses running
        pass