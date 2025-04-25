# oblix/cli/commands/sessions.py
import click
import sys
import os
import colorama
from colorama import Fore, Style
from datetime import datetime

# Change relative import to absolute import
from oblix.cli.utils import (
    setup_client, handle_async_command, print_header, print_success,
    print_warning, print_error, print_info, print_table, print_panel
)

# Initialize colorama
colorama.init()

@click.group(name='sessions')
def sessions_group():
    """View and manage your chat history"""
    pass

@sessions_group.command('list')
@click.option('--limit', default=50, help='Limit number of sessions to display')
def list_sessions(limit):
    """List recent chat sessions"""
    async def run_list_sessions():
        try:
            client = await setup_client()
            sessions = client.list_sessions(limit)
            
            if not sessions:
                print_warning("No sessions found.")
                return
            
            rows = []
            for session in sessions:
                created_at = datetime.fromisoformat(session['created_at']).strftime("%Y-%m-%d %H:%M")
                rows.append([
                    session['id'], 
                    session['title'], 
                    created_at, 
                    str(session['message_count'])
                ])
            
            print_table("Recent Chat Sessions", ["Session ID", "Title", "Created", "Messages"], rows)
        except Exception as e:
            print_error(f"Error listing sessions: {e}")
    
    handle_async_command(run_list_sessions)

@sessions_group.command('view')
@click.argument('session_id')
def view_session(session_id):
    """View details of a specific session"""
    async def run_view_session():
        try:
            client = await setup_client()
            
            # Use enhanced session manager validation
            exists, session_data, error = client.session_manager.validate_session_existence(session_id)
            
            if not exists:
                print_warning(error or f"No session found with ID: {session_id}")
                return
            
            # Get a formatted summary instead of manually formatting
            summary = client.session_manager.get_session_summary(session_id)
            
            # Create session overview content
            overview_content = (
                f"Session ID: {summary['id']}\n"
                f"Title: {summary['title']}\n"
                f"Created: {summary['created_at']}\n"
                f"Last Updated: {summary['updated_at']}\n"
                f"Messages: {summary['message_count']}"
            )
            print_panel("Session Overview", overview_content)
            
            # Display messages
            print_header("Conversation:")
            for msg in session_data.get('messages', []):
                role = msg['role'].capitalize()
                timestamp = datetime.fromisoformat(msg['timestamp']).strftime("%Y-%m-%d %H:%M:%S")
                
                if role == 'User':
                    print(f"{Fore.GREEN}{role} ({timestamp}):{Style.RESET_ALL} {msg['content']}")
                else:
                    print(f"{Fore.BLUE}{role} ({timestamp}):{Style.RESET_ALL} {msg['content']}")
        
        except Exception as e:
            print_error(f"Error viewing session: {e}")
    
    handle_async_command(run_view_session)

@sessions_group.command('delete')
@click.argument('session_id')
@click.confirmation_option(prompt='Are you sure you want to delete this session?')
def delete_session(session_id):
    """Delete a specific chat session"""
    async def run_delete_session():
        try:
            client = await setup_client()
            success = await client.delete_session(session_id)
            
            if success:
                print_success(f"Session {session_id} deleted successfully.")
            else:
                print_warning(f"Could not delete session {session_id}.")
        
        except Exception as e:
            print_error(f"Error deleting session: {e}")
    
    handle_async_command(run_delete_session)

@sessions_group.command('create')
@click.option('--title', help='Title for the new session')
def create_session(title):
    """Create a new chat session"""
    async def run_create_session():
        try:
            client = await setup_client()
            session_id = await client.create_session(title=title)
            
            print_success(f"New session created: {session_id}")
            print_info(f"Title: {title or 'Untitled Session'}")
        
        except Exception as e:
            print_error(f"Error creating session: {e}")
    
    handle_async_command(run_create_session)