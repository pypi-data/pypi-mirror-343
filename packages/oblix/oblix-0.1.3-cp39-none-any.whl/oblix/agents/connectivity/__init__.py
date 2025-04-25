# oblix/agents/connectivity/__init__.py
import platform

from .base import BaseConnectivityAgent
from .agent import ConnectivityAgent

# Import platform-specific monitors conditionally to avoid import errors
if platform.system().lower() == "darwin":
    from .darwin.monitor import DarwinConnectivityMonitor
    __all__ = [
        'BaseConnectivityAgent',
        'ConnectivityAgent',
        'DarwinConnectivityMonitor'
    ]
elif platform.system().lower() == "windows":
    from .windows.monitor import WindowsConnectivityMonitor
    __all__ = [
        'BaseConnectivityAgent',
        'ConnectivityAgent',
        'WindowsConnectivityMonitor'
    ]
elif platform.system().lower() == "linux":
    from .linux.monitor import LinuxConnectivityMonitor
    __all__ = [
        'BaseConnectivityAgent',
        'ConnectivityAgent',
        'LinuxConnectivityMonitor'
    ]
else:
    __all__ = [
        'BaseConnectivityAgent',
        'ConnectivityAgent'
    ]