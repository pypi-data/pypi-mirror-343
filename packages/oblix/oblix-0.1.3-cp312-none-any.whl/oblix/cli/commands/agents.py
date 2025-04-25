# oblix/cli/commands/agents.py
import click
import colorama
from colorama import Fore, Style

from oblix.cli.utils import (
    print_header, print_success, print_info, print_model_item, print_warning
)

# Initialize colorama
colorama.init()

@click.command(name='agents')
def agents_group():
    """Show the monitoring agents that help Oblix make smart decisions"""
    import platform
    
    print_header("Supported Agents")
    print_info("Oblix supports the following agents for system monitoring and task management:")
    
    print_success("\nResource Monitor")
    print_model_item("Monitors system resources like CPU, memory, and GPU")
    print_model_item("Helps make intelligent routing decisions based on resource availability")
    
    print_success("\nConnectivity Agent")
    print_model_item("Monitors network connectivity and latency")
    print_model_item("Routes requests to local models when connectivity is limited")
    
    print()