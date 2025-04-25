# oblix/agents/connectivity/darwin/monitor.py
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

from ..base import BaseConnectivityMonitor

logger = logging.getLogger(__name__)

class DarwinConnectivityMonitor(BaseConnectivityMonitor):
    """macOS-specific connectivity monitoring implementation"""
    
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
        self._network_service = self._get_primary_network_service()
        
        logger.debug(f"Initialized Darwin connectivity monitor with network service: {self._network_service}")

    def _get_primary_network_service(self) -> Optional[str]:
        """Get the primary network service name"""
        try:
            cmd = ["networksetup", "-listnetworkserviceorder"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Look for primary interface (usually first in list)
                lines = result.stdout.split('\n')
                for line in lines:
                    if '(1)' in line and 'Wi-Fi' in line:
                        return 'Wi-Fi'
                    elif '(1)' in line and 'Ethernet' in line:
                        return 'Ethernet'
                        
                # If no primary, look for any active interface
                for line in lines:
                    if 'Wi-Fi' in line:
                        return 'Wi-Fi'
                    elif 'Ethernet' in line:
                        return 'Ethernet'
            return None
        except Exception as e:
            logger.debug(f"Error getting network service: {e}")
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
        """Get current connection type on macOS"""
        if not self._network_service:
            return None
            
        try:
            if self._network_service == 'Wi-Fi':
                return "wifi"
            elif self._network_service == 'Ethernet':
                return "ethernet"
            return None
            
        except Exception as e:
            logger.debug(f"Error getting connection type: {e}")
            return None

    async def measure_bandwidth(self) -> Optional[float]:
        """Measure current bandwidth on macOS"""
        try:
            cmd = "nettop -P -L 1 -J bytes_in,bytes_out"
            process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, _ = await process.communicate()
            
            if stdout:
                total_bytes = 0
                for line in stdout.decode().split('\n'):
                    if not line.strip():
                        continue
                    matches = re.findall(r'\d+', line)
                    if matches:
                        total_bytes += sum(int(m) for m in matches)
                
                bandwidth = (total_bytes * 8) / (1024 * 1024)  # Convert to Mbps
                return bandwidth
                
            return None
            
        except Exception as e:
            logger.debug(f"Error measuring bandwidth: {e}")
            return None

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
                ["ping", "-c", "1", "-t", "1", "8.8.8.8"],
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
            # Use `ifconfig` to get network interface details
            result = subprocess.run(
                ["ifconfig"], 
                capture_output=True, 
                text=True
            )
            
            interfaces = []
            current_interface = {}
            
            for line in result.stdout.split('\n'):
                line = line.strip()
                
                # New interface
                if ':' in line and not line.startswith('\t'):
                    if current_interface:
                        interfaces.append(current_interface)
                    
                    interface_name = line.split(':')[0]
                    current_interface = {
                        "name": interface_name,
                        "status": "down",
                        "ip_address": None,
                        "mac_address": None
                    }
                
                # Interface status
                if line.startswith('status:'):
                    current_interface['status'] = line.split(':')[1].strip()
                
                # IP Address
                if line.startswith('inet '):
                    current_interface['ip_address'] = line.split()[1]
                
                # MAC Address
                if line.startswith('ether '):
                    current_interface['mac_address'] = line.split()[1]
            
            # Add last interface
            if current_interface:
                interfaces.append(current_interface)
            
            return interfaces
        
        except Exception as e:
            logger.error(f"Error getting network interfaces: {e}")
            return []
