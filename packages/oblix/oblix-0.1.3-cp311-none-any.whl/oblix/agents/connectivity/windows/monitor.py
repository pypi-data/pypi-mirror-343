# oblix/agents/connectivity/windows/monitor.py
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

class WindowsConnectivityMonitor(BaseConnectivityMonitor):
    """Windows-specific connectivity monitoring implementation"""
    
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
        self._network_adapter = self._get_primary_network_adapter()
        
        logger.debug(f"Initialized Windows connectivity monitor with network adapter: {self._network_adapter}")

    def _get_primary_network_adapter(self) -> Optional[str]:
        """Get the primary network adapter name"""
        try:
            # Run netsh to get interface information (works on all Windows versions)
            cmd = ["netsh", "interface", "show", "interface"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                # Look for "Connected" interfaces
                for line in lines:
                    if 'Connected' in line:
                        # Extract the adapter name, typically at the end of the line
                        parts = line.strip().split()
                        if len(parts) >= 4:
                            return parts[-1]  # Last part should be the name
                
                # If no "Connected" interface found, look for any interface
                for line in lines:
                    if line.strip() and not 'Admin State' in line and not '---' in line:
                        parts = line.strip().split()
                        if len(parts) >= 4:
                            return parts[-1]  # Last part should be the name
                            
            return None
        except Exception as e:
            logger.debug(f"Error getting network adapter: {e}")
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
        """Get current connection type on Windows"""
        if not self._network_adapter:
            return None
            
        try:
            # Use ipconfig to get connection details
            cmd = ["ipconfig", "/all"]
            process = await asyncio.create_subprocess_shell(
                " ".join(cmd),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, _ = await process.communicate()
            
            output = stdout.decode(errors='ignore')
            
            # Check for WiFi indicators
            if "Wireless" in output or "Wi-Fi" in output or "802.11" in output:
                return "wifi"
            # Check for Ethernet indicators
            elif "Ethernet" in output:
                return "ethernet"
            # If we have an adapter but can't determine type
            return "unknown"
                
        except Exception as e:
            logger.debug(f"Error getting connection type: {e}")
            return None

    async def measure_bandwidth(self) -> Optional[float]:
        """Estimate current bandwidth on Windows"""
        try:
            # Use netstat to get connection statistics
            cmd = "netstat -e"
            process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, _ = await process.communicate()
            
            # Parse the output to get bytes in/out
            if stdout:
                lines = stdout.decode().split('\n')
                for i, line in enumerate(lines):
                    if "Bytes" in line:
                        # Next line should contain the numbers
                        if i + 1 < len(lines):
                            numbers = re.findall(r'\d+', lines[i + 1])
                            if len(numbers) >= 2:
                                # Very rough bandwidth estimate - assume 1 second of data
                                bytes_received = int(numbers[0])
                                bytes_sent = int(numbers[1])
                                total_bytes = bytes_received + bytes_sent
                                
                                # Convert to Mbps (rough estimate)
                                bandwidth = (total_bytes * 8) / (1024 * 1024)
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
                ["ping", "-n", "1", "-w", "1000", "8.8.8.8"],
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
            # Use ipconfig to get interface details
            result = subprocess.run(
                ["ipconfig", "/all"], 
                capture_output=True, 
                text=True
            )
            
            interfaces = []
            current_interface = {}
            current_name = None
            
            for line in result.stdout.split('\n'):
                line = line.strip()
                
                # New interface section
                if line.endswith(':'):
                    if current_interface and current_name:
                        interfaces.append(current_interface)
                    
                    current_name = line[:-1].strip()
                    current_interface = {
                        "name": current_name,
                        "status": "down",
                        "ip_address": None,
                        "mac_address": None
                    }
                
                # IP Address
                if "IPv4 Address" in line and ":" in line:
                    current_interface['ip_address'] = line.split(':')[1].strip()
                    current_interface['status'] = "up"  # If it has an IP, it's up
                
                # MAC Address
                if "Physical Address" in line and ":" in line:
                    current_interface['mac_address'] = line.split(':')[1].strip()
            
            # Add last interface
            if current_interface and current_name:
                interfaces.append(current_interface)
            
            return interfaces
        
        except Exception as e:
            logger.error(f"Error getting network interfaces: {e}")
            return []