# oblix/agents/connectivity/linux/monitor.py
import subprocess
import asyncio
import statistics
from typing import Optional, List, Tuple, Dict, Any
import re
import socket
import platform
import time
import httpx
import logging
import json
import os

from ..base import BaseConnectivityMonitor

logger = logging.getLogger(__name__)

class LinuxConnectivityMonitor(BaseConnectivityMonitor):
    """Linux-specific connectivity monitoring implementation for x86 architecture"""
    
    def __init__(
        self, 
        endpoints: Optional[List[str]] = None,
        check_interval: int = 30
    ):
        """
        Initialize connectivity monitor
        
        :param endpoints: List of URLs to check for connectivity
        :param check_interval: Time between connectivity checks
        """
        # Set reliable test endpoints
        self.endpoints = endpoints or [
            "https://www.google.com",  # Primary check
            "https://www.cloudflare.com"  # Backup check
        ]
        self.check_interval = check_interval
        
        # Connection state caching
        self._last_metrics = None
        self._last_metrics_time = 0
        self._primary_interface = self._get_primary_interface()
        
        logger.debug(f"Initialized Linux connectivity monitor with primary interface: {self._primary_interface}")

    def _get_primary_interface(self) -> Optional[str]:
        """Get the primary network interface name"""
        try:
            # First check the default route
            cmd = ["ip", "route", "show", "default"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and result.stdout:
                # Parse the default route to find the interface
                match = re.search(r'dev\s+(\w+)', result.stdout)
                if match:
                    return match.group(1)
            
            # If that fails, check for common interface names
            # Check for traditional interface names
            interfaces = ["eth0", "wlan0", "enp0s3", "ens33", "wlp2s0"]
            for interface in interfaces:
                # Check if the interface exists
                if os.path.exists(f"/sys/class/net/{interface}"):
                    # Check if the interface is up
                    with open(f"/sys/class/net/{interface}/operstate", "r") as f:
                        state = f.read().strip()
                        if state == "up":
                            return interface
            
            return None
        except Exception as e:
            logger.debug(f"Error getting primary interface: {e}")
            return None

    async def _check_endpoint(self, url: str, timeout: float = 2.0) -> Tuple[float, bool]:
        """Check a single endpoint and return latency"""
        try:
            async with httpx.AsyncClient() as client:
                start_time = time.time()
                response = await client.head(url, timeout=timeout, follow_redirects=True)
                latency = (time.time() - start_time) * 1000  # Convert to ms
                
                if response.status_code < 400:
                    return latency, True
                return float('inf'), False
                
        except Exception as e:
            logger.debug(f"Endpoint check failed for {url}: {str(e)}")
            return float('inf'), False

    async def get_connection_type(self) -> Optional[str]:
        """Get current connection type on Linux"""
        if not self._primary_interface:
            return None
            
        try:
            if self._primary_interface.startswith('wl'):
                return "wifi"
            elif self._primary_interface.startswith(('en', 'eth')):
                return "ethernet"
            return "other"
            
        except Exception as e:
            logger.debug(f"Error getting connection type: {e}")
            return None

    async def measure_bandwidth(self) -> Optional[float]:
        """Measure current bandwidth on Linux"""
        try:
            if not self._primary_interface:
                return None
                
            # First attempt: Try to get a more accurate measurement with a longer duration
            try:
                # Get current bytes in/out
                rx_path = f"/sys/class/net/{self._primary_interface}/statistics/rx_bytes"
                tx_path = f"/sys/class/net/{self._primary_interface}/statistics/tx_bytes"
                
                if os.path.exists(rx_path) and os.path.exists(tx_path):
                    with open(rx_path, "r") as f:
                        rx_before = int(f.read().strip())
                    with open(tx_path, "r") as f:
                        tx_before = int(f.read().strip())
                    
                    # Wait a longer period for a more accurate reading when network is idle
                    await asyncio.sleep(2)
                    
                    # Get updated bytes
                    with open(rx_path, "r") as f:
                        rx_after = int(f.read().strip())
                    with open(tx_path, "r") as f:
                        tx_after = int(f.read().strip())
                    
                    # Calculate bandwidth
                    bytes_per_sec = (rx_after - rx_before) + (tx_after - tx_before)
                    bytes_per_sec = bytes_per_sec / 2  # Adjusted for the 2-second interval
                    
                    mbps = (bytes_per_sec * 8) / (1024 * 1024)  # Convert to Mbps
                    
                    # If we detect a very low bandwidth when network is idle,
                    # return a reasonable minimum value for a connected interface
                    if mbps < 1.0 and self._quick_connection_check_sync():
                        logger.debug(f"Low bandwidth measured ({mbps} Mbps) but network is connected, returning minimum")
                        return 5.0  # Minimum assumed bandwidth for a connected interface
                    
                    return mbps
            except Exception as inner_e:
                logger.debug(f"Error in primary bandwidth measurement: {inner_e}")
                # Continue to fallback method
            
            # Fallback: If we can ping Google DNS but measured low bandwidth, assume minimum bandwidth
            try:
                if self._quick_connection_check_sync():
                    logger.debug("Network is connected but bandwidth measurement failed, using minimum value")
                    return 5.0  # Minimum assumed bandwidth for a connected interface
            except Exception:
                pass
                
            return None
            
        except Exception as e:
            logger.debug(f"Error measuring bandwidth: {e}")
            return None
            
    def _quick_connection_check_sync(self) -> bool:
        """Synchronous version of quick connection check for bandwidth estimation"""
        try:
            # Try DNS resolution
            socket.gethostbyname("www.google.com")
            return True
        except Exception:
            pass
            
        # Try ping to Google DNS
        try:
            result = subprocess.run(
                ["ping", "-c", "1", "-W", "1", "8.8.8.8"],
                capture_output=True,
                timeout=2
            )
            return result.returncode == 0
        except Exception:
            return False

    async def _quick_connection_check(self) -> bool:
        """Perform a quick connection check using multiple methods"""
        # Try DNS resolution first
        try:
            socket.gethostbyname("www.google.com")
            return True
        except Exception as e:
            logger.debug(f"DNS resolution check failed: {e}")
            # Continue with other checks

        # Try socket connection
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('8.8.8.8', 53))
            sock.close()
            if result == 0:
                return True
        except Exception as e:
            logger.debug(f"Socket connection check failed: {e}")
            # Continue with other checks

        # Try ping as last resort
        try:
            result = subprocess.run(
                ["ping", "-c", "1", "-W", "1", "8.8.8.8"],
                capture_output=True,
                timeout=2
            )
            return result.returncode == 0
        except Exception as e:
            logger.debug(f"Ping check failed: {e}")
            return False

    async def measure_connection_metrics(self) -> Dict[str, Any]:
        """
        Measure current connection metrics with optimized checks
        Caches results for the check interval to reduce unnecessary network calls
        
        Returns:
            Dictionary of connection metrics
        """
        current_time = time.time()
        
        # Return cached metrics if within check interval
        if (self._last_metrics and 
            current_time - self._last_metrics_time < self.check_interval):
            return self._last_metrics
        
        # Get connection type
        connection_type = await self.get_connection_type()
        
        # Quick connectivity check first
        if not await self._quick_connection_check():
            metrics = {
                "latency": float('inf'),
                "packet_loss": 100.0,
                "connection_type": connection_type,
                "bandwidth": 0.0,
                "timestamp": current_time
            }
            
            # Cache and return metrics
            self._last_metrics = metrics
            self._last_metrics_time = current_time
            return metrics
        
        # Test endpoints
        latencies = []
        successes = 0
        total_checks = 0
        
        for endpoint in self.endpoints:
            latency, success = await self._check_endpoint(endpoint)
            if latency != float('inf'):
                latencies.append(latency)
            total_checks += 1
            if success:
                successes += 1
        
        # Calculate metrics
        avg_latency = statistics.mean(latencies) if latencies else float('inf')
        packet_loss = ((total_checks - successes) / total_checks * 100) if total_checks > 0 else 100.0
        
        # Get bandwidth
        bandwidth = await self.measure_bandwidth() or 0.0
        
        # Prepare final metrics
        metrics = {
            "latency": round(avg_latency, 2),
            "packet_loss": round(packet_loss, 2),
            "connection_type": connection_type,
            "bandwidth": round(bandwidth, 2),
            "timestamp": current_time
        }
        
        # Cache metrics
        self._last_metrics = metrics
        self._last_metrics_time = current_time
        
        return metrics

    async def validate_internet_connection(self) -> bool:
        """
        Validate full internet connectivity
        
        Returns:
            bool: True if internet is fully accessible, False otherwise
        """
        try:
            metrics = await self.measure_connection_metrics()
            return (
                metrics['latency'] != float('inf') and
                metrics['packet_loss'] < 50.0 and
                metrics['bandwidth'] > 1.0  # At least 1 Mbps
            )
        except Exception as e:
            logger.error(f"Error validating internet connection: {e}")
            return False

    def get_network_interfaces(self) -> List[Dict[str, Any]]:
        """
        Get detailed information about network interfaces
        
        Returns:
            List of dictionaries with network interface details
        """
        try:
            # Use `ip addr` to get network interface details
            result = subprocess.run(
                ["ip", "addr"], 
                capture_output=True, 
                text=True
            )
            
            interfaces = []
            current_interface = {}
            
            for line in result.stdout.split('\n'):
                line = line.strip()
                
                # New interface
                if line.startswith(tuple(str(i) + ":" for i in range(10))):
                    if current_interface:
                        interfaces.append(current_interface)
                    
                    interface_data = line.split(":", 2)
                    if len(interface_data) > 1:
                        interface_name = interface_data[1].strip()
                        current_interface = {
                            "name": interface_name,
                            "status": "down",
                            "ip_address": None,
                            "mac_address": None
                        }
                
                # Interface status
                if "state UP" in line:
                    current_interface['status'] = "up"
                elif "state DOWN" in line:
                    current_interface['status'] = "down"
                
                # IP Address
                ip_match = re.search(r'inet\s+(\d+\.\d+\.\d+\.\d+)', line)
                if ip_match:
                    current_interface['ip_address'] = ip_match.group(1)
                
                # MAC Address
                mac_match = re.search(r'link/ether\s+([0-9a-f:]+)', line)
                if mac_match:
                    current_interface['mac_address'] = mac_match.group(1)
            
            # Add last interface
            if current_interface:
                interfaces.append(current_interface)
            
            return interfaces
        
        except Exception as e:
            logger.error(f"Error getting network interfaces: {e}")
            return []