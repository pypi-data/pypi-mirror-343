# oblix/cli/utils.py
import asyncio
import sys
import logging
import json
import colorama
from colorama import Fore, Style
from typing import Callable, Awaitable, Any, List

from oblix.client import OblixClient

# Initialize colorama
colorama.init()

def print_header(text):
    """Print a header with formatting"""
    print(f"\n{Fore.BLUE}{Style.BRIGHT}{text}{Style.RESET_ALL}")

def print_success(text):
    """Print success message"""
    print(f"{Fore.GREEN}{text}{Style.RESET_ALL}")

def print_warning(text):
    """Print warning message"""
    print(f"{Fore.YELLOW}{text}{Style.RESET_ALL}")

def print_error(text):
    """Print error message"""
    print(f"{Fore.RED}{Style.BRIGHT}{text}{Style.RESET_ALL}")

def print_info(text):
    """Print information with cyan color"""
    print(f"{Fore.CYAN}{text}{Style.RESET_ALL}")

def print_model_item(name, description=""):
    """Print a model item with bullet point"""
    if description:
        print(f"  • {Style.BRIGHT}{name}{Style.RESET_ALL} - {description}")
    else:
        print(f"  • {Style.BRIGHT}{name}{Style.RESET_ALL}")

def print_table(title, headers, rows):
    """Print a simple table"""
    print(f"\n{Fore.BLUE}{Style.BRIGHT}{title}{Style.RESET_ALL}")
    
    # Calculate column widths
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Print headers
    header_row = " | ".join(f"{h:{w}s}" for h, w in zip(headers, col_widths))
    print(f"{Fore.CYAN}{header_row}{Style.RESET_ALL}")
    print("-" * (sum(col_widths) + 3 * (len(headers) - 1)))
    
    # Print rows
    for row in rows:
        row_str = " | ".join(f"{str(cell):{w}s}" for cell, w in zip(row, col_widths))
        print(row_str)

def print_json(data):
    """Print formatted JSON data"""
    print(json.dumps(data, indent=2))

def print_panel(title, content):
    """Print a simple panel with a title and content"""
    width = max(len(title) + 4, max(len(line) for line in content.split('\n')) + 4)
    
    print(f"\n{Fore.BLUE}{Style.BRIGHT}┌─{title}{'─' * (width - len(title) - 3)}┐{Style.RESET_ALL}")
    for line in content.split('\n'):
        print(f"{Fore.BLUE}{Style.BRIGHT}│{Style.RESET_ALL} {line}{' ' * (width - len(line) - 2)} {Fore.BLUE}{Style.BRIGHT}│{Style.RESET_ALL}")
    print(f"{Fore.BLUE}{Style.BRIGHT}└{'─' * (width - 2)}┘{Style.RESET_ALL}")

def handle_async_command(async_func: Callable[[], Awaitable[Any]]) -> Any:
    """
    Wrapper to handle async CLI commands
    
    Args:
        async_func: Async function to execute
        
    Returns:
        Any: The return value from the async function
    """
    loop = None
    try:
        # Get or create an event loop
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
        # Run the async function
        return loop.run_until_complete(async_func())
    except KeyboardInterrupt:
        print_warning("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        # The inner function should handle specific exceptions
        # This is just a generic handler for any unhandled exceptions
        print_error(f"Error: {e}")
        
        # Only show traceback in debug mode
        if logging.getLogger().level == logging.DEBUG:
            import traceback
            traceback.print_exc()
            
        return None
    finally:
        # Clean up pending tasks and close the event loop properly
        if loop is not None:
            try:
                # Cancel all pending tasks
                tasks = [task for task in asyncio.all_tasks(loop) 
                        if not task.done() and task is not asyncio.current_task()]
                if tasks:
                    for task in tasks:
                        task.cancel()
                    loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
                
                # Close the loop
                loop.close()
            except Exception:
                # Ignore cleanup errors
                pass

async def setup_client() -> OblixClient:
    """
    Set up an Oblix client
    
    Returns:
        Initialized OblixClient instance
    """
    try:
        # Create client instance
        client = OblixClient()
        
        return client
    
    except Exception as e:
        print_error(f"Client setup error: {e}")
        sys.exit(1)