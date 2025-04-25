# oblix/sessions/manager.py
import os
import json
import uuid
import shutil
from typing import Dict, List, Optional, Any, Union, Tuple
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

class SessionManager:
    """
    Manages persistent chat sessions with file-based storage
    
    Provides capabilities to:
    - Create new sessions
    - Save conversation context
    - Load existing sessions
    - List and manage sessions
    - Export and import sessions
    - Add custom metadata to sessions
    - Manage context with token-based windowing
    
    Session data is stored as JSON files in a configurable directory, with each
    session containing messages, metadata, and optional context information.
    This enables applications to maintain conversation history across restarts.
    
    Attributes:
        base_dir (str): Base directory for storing session files
    """
    
    def __init__(self, base_dir: Optional[str] = None):
        """
        Initialize SessionManager
        
        Args:
            base_dir: Base directory for storing session files. If not specified,
                     defaults to ~/.oblix/sessions
        """
        # Use a default directory if not specified
        if base_dir is None:
            base_dir = os.path.join(
                os.path.expanduser("~"), 
                ".oblix", 
                "sessions"
            )
        
        # Ensure session directory exists
        os.makedirs(base_dir, exist_ok=True)
        self.base_dir = base_dir
    
    def _get_session_path(self, session_id: str) -> str:
        """
        Get full path for a session file
        
        Args:
            session_id: Unique session identifier
            
        Returns:
            str: Full file path to the session JSON file
        """
        return os.path.join(self.base_dir, f"{session_id}.json")
    
    def create_session(
        self, 
        initial_context: Optional[Dict] = None, 
        title: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Create a new chat session
        
        Creates a new session with a unique ID and initializes it with
        optional context and title. The session is stored as a JSON file.
        
        Args:
            initial_context: Optional initial context for the session
            title: Optional title for the session
            metadata: Optional additional metadata for the session
            
        Returns:
            str: Unique session ID
            
        Raises:
            Exception: If there's an error creating the session file
        """
        # Generate unique session ID
        session_id = str(uuid.uuid4())
        
        # Prepare session metadata
        session_data = {
            "id": session_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "title": title or f"Chat Session {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "messages": [],
            "context": initial_context or {},
            "metadata": metadata or {}
        }
        
        # Save session file
        try:
            with open(self._get_session_path(session_id), 'w') as f:
                json.dump(session_data, f, indent=2)
            
            logger.info(f"Created new session: {session_id}")
            return session_id
        
        except Exception as e:
            logger.error(f"Error creating session: {e}")
            raise
    
    def create_and_use_session(
        self, 
        title: Optional[str] = None,
        initial_context: Optional[Dict] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Create a new chat session and return the session ID for immediate use
        
        This is a convenience method for applications that want to create
        a session and immediately start using it.
        
        Args:
            title: Optional title for the session
            initial_context: Optional initial context for the session
            metadata: Optional additional metadata for the session
            
        Returns:
            str: Unique session ID that can be assigned to client.current_session_id
        """
        return self.create_session(
            initial_context=initial_context,
            title=title,
            metadata=metadata
        )
    
    def save_message(
        self, 
        session_id: str, 
        message, 
        role: str = 'user'
    ) -> bool:
        """
        Save a message to an existing session
        
        Adds a new message to a session with the specified role and
        updates the session's last modified timestamp.
        
        Args:
            session_id: Session identifier
            message: Message content (string or dict)
            role: Message role ('user' or 'assistant')
            
        Returns:
            bool: True if message was saved successfully, False otherwise
        """
        try:
            # Load existing session
            session_path = self._get_session_path(session_id)
            with open(session_path, 'r') as f:
                session_data = json.load(f)
            
            # Handle different message types appropriately
            if isinstance(message, dict):
                # If it's a dict with 'content' key, extract that
                if 'content' in message:
                    message_content = message['content']
                # If it's the actual model response dict
                elif 'response' in message:
                    # If response is a dict, use it directly
                    if isinstance(message['response'], dict):
                        message_content = json.dumps(message['response'])
                    else:
                        message_content = message['response']
                # If it's a metrics or other response dict, convert to JSON string
                else:
                    message_content = json.dumps(message)
            else:
                # Already a string or other type, just convert to string
                message_content = str(message)
            
            # Prepare message with metadata
            full_message = {
                "id": str(uuid.uuid4()),
                "role": role,
                "content": message_content,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            # Add message to session
            session_data['messages'].append(full_message)
            session_data['updated_at'] = datetime.now(timezone.utc).isoformat()
            
            # Save updated session
            with open(session_path, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            return True
        
        except FileNotFoundError:
            logger.error(f"Session {session_id} not found")
            return False
        except Exception as e:
            logger.error(f"Error saving message: {e}")
            return False
    
    def load_session(self, session_id: str) -> Optional[Dict]:
        """
        Load a specific session by ID
        
        Retrieves the full session data including all messages and metadata.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Optional[Dict]: Session data if found, None otherwise
        """
        try:
            with open(self._get_session_path(session_id), 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Session {session_id} not found")
            return None
        except Exception as e:
            logger.error(f"Error loading session: {e}")
            return None
    
    def list_sessions(self, limit: int = 50, filter_metadata: Optional[Dict[str, Any]] = None) -> List[Dict]:
        """
        List recent sessions with optional metadata filtering
        
        Returns metadata for the most recently updated sessions, up to the
        specified limit. Optionally filter by metadata fields.
        
        Args:
            limit: Maximum number of sessions to return
            filter_metadata: Optional metadata filters to apply (key-value pairs)
            
        Returns:
            List[Dict]: List of session metadata including:
                - id: Session identifier
                - title: Session title
                - created_at: Creation timestamp
                - updated_at: Last update timestamp
                - message_count: Number of messages in the session
                - metadata: Additional session metadata
        """
        try:
            # Get all session files
            session_files = [
                f for f in os.listdir(self.base_dir) 
                if f.endswith('.json')
            ]
            
            # Load session metadata
            sessions = []
            for filename in session_files:
                try:
                    with open(os.path.join(self.base_dir, filename), 'r') as f:
                        session = json.load(f)
                        
                        # Apply metadata filter if provided
                        if filter_metadata:
                            # Check if session metadata contains all filter criteria
                            session_metadata = session.get('metadata', {})
                            if not all(session_metadata.get(k) == v for k, v in filter_metadata.items()):
                                continue
                        
                        sessions.append({
                            "id": session['id'],
                            "title": session['title'],
                            "created_at": session['created_at'],
                            "updated_at": session['updated_at'],
                            "message_count": len(session.get('messages', [])),
                            "metadata": session.get('metadata', {})
                        })
                except Exception as e:
                    logger.warning(f"Error reading session {filename}: {e}")
            
            # Sort by most recently updated
            sessions.sort(key=lambda x: x['updated_at'], reverse=True)
            return sessions[:limit]
        
        except Exception as e:
            logger.error(f"Error listing sessions: {e}")
            return []
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a specific session
        
        Permanently removes a session file from storage.
        
        Args:
            session_id: Session identifier
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        try:
            session_path = self._get_session_path(session_id)
            if os.path.exists(session_path):
                os.remove(session_path)
                logger.info(f"Deleted session: {session_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting session: {e}")
            return False
            
    def update_session_metadata(self, session_id: str, metadata: Dict[str, Any]) -> bool:
        """
        Update or add metadata to a session
        
        Updates existing session metadata or adds new metadata fields
        without affecting other session data.
        
        Args:
            session_id: Session identifier
            metadata: Dictionary of metadata to update or add
            
        Returns:
            bool: True if metadata was updated successfully, False otherwise
        """
        try:
            # Load existing session
            session_path = self._get_session_path(session_id)
            with open(session_path, 'r') as f:
                session_data = json.load(f)
            
            # Initialize metadata if it doesn't exist
            if 'metadata' not in session_data:
                session_data['metadata'] = {}
                
            # Update metadata fields
            session_data['metadata'].update(metadata)
            session_data['updated_at'] = datetime.now(timezone.utc).isoformat()
            
            # Save updated session
            with open(session_path, 'w') as f:
                json.dump(session_data, f, indent=2)
                
            logger.info(f"Updated metadata for session: {session_id}")
            return True
            
        except FileNotFoundError:
            logger.error(f"Session {session_id} not found")
            return False
        except Exception as e:
            logger.error(f"Error updating session metadata: {e}")
            return False
            
    def get_session_metadata(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get metadata for a specific session
        
        Retrieves the metadata associated with a session without loading
        the entire session content.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Optional[Dict[str, Any]]: Session metadata if found, None otherwise
        """
        try:
            session_data = self.load_session(session_id)
            if session_data:
                return session_data.get('metadata', {})
            return None
        except Exception as e:
            logger.error(f"Error retrieving session metadata: {e}")
            return None
            
    def export_session(self, session_id: str, export_path: str) -> bool:
        """
        Export a session to a file
        
        Exports a complete session to a JSON file that can be shared or backed up.
        
        Args:
            session_id: Session identifier
            export_path: Path to save the exported session
            
        Returns:
            bool: True if export was successful, False otherwise
        """
        try:
            session_data = self.load_session(session_id)
            if not session_data:
                logger.error(f"Cannot export session {session_id}: not found")
                return False
                
            # Ensure export directory exists
            export_dir = os.path.dirname(export_path)
            if export_dir and not os.path.exists(export_dir):
                os.makedirs(export_dir, exist_ok=True)
                
            # Write export file
            with open(export_path, 'w') as f:
                json.dump(session_data, f, indent=2)
                
            logger.info(f"Exported session {session_id} to {export_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting session {session_id}: {e}")
            return False
            
    def import_session(self, import_path: str, new_id: bool = True) -> Optional[str]:
        """
        Import a session from a file
        
        Imports a session from a JSON file, optionally assigning a new ID
        to avoid conflicts with existing sessions.
        
        Args:
            import_path: Path to the JSON file to import
            new_id: Whether to assign a new ID (True) or keep original ID (False)
            
        Returns:
            Optional[str]: Session ID of the imported session, or None if import failed
        """
        try:
            # Read and validate the import file
            with open(import_path, 'r') as f:
                session_data = json.load(f)
                
            # Validate required fields
            required_fields = ['id', 'messages', 'created_at', 'updated_at', 'title']
            if not all(field in session_data for field in required_fields):
                logger.error(f"Import file missing required session fields")
                return None
                
            # Assign new ID if requested
            if new_id:
                original_id = session_data['id']
                session_data['id'] = str(uuid.uuid4())
                logger.info(f"Assigned new ID to imported session: {original_id} -> {session_data['id']}")
                
            # Update timestamps
            session_data['imported_at'] = datetime.now(timezone.utc).isoformat()
            if not new_id:
                # Only update updated_at if keeping original ID (otherwise keep creation metadata)
                session_data['updated_at'] = datetime.now(timezone.utc).isoformat()
                
            # Ensure metadata field exists
            if 'metadata' not in session_data:
                session_data['metadata'] = {}
                
            # Add import information to metadata
            session_data['metadata']['imported'] = True
            session_data['metadata']['import_date'] = datetime.now(timezone.utc).isoformat()
            session_data['metadata']['import_source'] = os.path.basename(import_path)
                
            # Save imported session
            session_path = self._get_session_path(session_data['id'])
            with open(session_path, 'w') as f:
                json.dump(session_data, f, indent=2)
                
            logger.info(f"Imported session from {import_path} with ID {session_data['id']}")
            return session_data['id']
            
        except FileNotFoundError:
            logger.error(f"Import file not found: {import_path}")
            return None
        except json.JSONDecodeError:
            logger.error(f"Import file is not valid JSON: {import_path}")
            return None
        except Exception as e:
            logger.error(f"Error importing session: {e}")
            return None
            
    def merge_sessions(self, source_ids: List[str], title: Optional[str] = None) -> Optional[str]:
        """
        Merge multiple sessions into a new session
        
        Creates a new session containing all messages from the source sessions,
        properly ordered by timestamp.
        
        Args:
            source_ids: List of session IDs to merge
            title: Optional title for the merged session
            
        Returns:
            Optional[str]: ID of the newly created merged session, or None if merge failed
        """
        try:
            if not source_ids:
                logger.error("No source sessions provided for merge")
                return None
                
            # Load all source sessions
            source_sessions = []
            for session_id in source_ids:
                session_data = self.load_session(session_id)
                if session_data:
                    source_sessions.append(session_data)
                else:
                    logger.warning(f"Source session {session_id} not found for merge")
                    
            if not source_sessions:
                logger.error("No valid source sessions found for merge")
                return None
                
            # Create new session
            merged_session_id = str(uuid.uuid4())
            merged_title = title or f"Merged Session {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            
            # Prepare base session data
            merged_session = {
                "id": merged_session_id,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat(),
                "title": merged_title,
                "messages": [],
                "context": {},
                "metadata": {
                    "merged": True,
                    "source_sessions": source_ids,
                    "merge_date": datetime.now(timezone.utc).isoformat()
                }
            }
            
            # Collect all messages from source sessions
            all_messages = []
            for session in source_sessions:
                for message in session.get('messages', []):
                    # Add source session ID to message metadata
                    message_copy = message.copy()
                    message_copy['source_session_id'] = session['id']
                    all_messages.append(message_copy)
                    
            # Sort messages by timestamp
            all_messages.sort(key=lambda x: x.get('timestamp', ''))
            merged_session['messages'] = all_messages
            
            # Save merged session
            session_path = self._get_session_path(merged_session_id)
            with open(session_path, 'w') as f:
                json.dump(merged_session, f, indent=2)
                
            logger.info(f"Created merged session {merged_session_id} from {len(source_ids)} source sessions")
            return merged_session_id
            
        except Exception as e:
            logger.error(f"Error merging sessions: {e}")
            return None
            
    def calculate_context_token_budget(self, models=None) -> int:
        """
        Calculate token budget for context based on model constraints.
        
        Args:
            models: Optional dictionary of model instances to check context sizes
            
        Returns:
            int: Token budget for context window (70% of smallest model's context)
        """
        # Get the smallest context window size from available models
        # Default to a conservative value if no models are available
        default_budget = 4000
        context_fraction = 0.7  # Use 70% of available context for history
        
        if not models:
            return default_budget
            
        smallest_context = None
        for model_id, model in models.items():
            # Get model context size if available
            model_context_size = getattr(model, 'context_size', None)
            if model_context_size:
                if smallest_context is None or model_context_size < smallest_context:
                    smallest_context = model_context_size
        
        if smallest_context:
            return int(smallest_context * context_fraction)
        return default_budget
    
    def estimate_tokens(self, text: str) -> int:
        """
        Estimate token count for a text string.
        
        Args:
            text: Text to estimate tokens for
            
        Returns:
            int: Estimated token count
        """
        if not text:
            return 0
            
        # Simple heuristic: ~4 characters per token for English text
        # This is a rough approximation; actual tokenization varies by model
        return len(text) // 4 + 1
        
    def get_context_window(self, session_id: str, token_budget: int = None) -> List[Dict]:
        """
        Get context window from session using token-based windowing.
        
        Retrieves messages from a session that fit within the specified token budget,
        prioritizing newer messages.
        
        Args:
            session_id: Session identifier
            token_budget: Maximum token budget for context (defaults to 4000 if not specified)
            
        Returns:
            List[Dict]: Context messages that fit within token budget
        """
        try:
            session_data = self.load_session(session_id)
            if not session_data or 'messages' not in session_data:
                return []
                
            messages = session_data['messages']
            token_budget = token_budget or 4000
            token_count = 0
            context_messages = []
            
            # Iterate through messages in reverse order (newest first)
            for msg in reversed(messages):
                content = msg.get('content', '')
                msg_tokens = self.estimate_tokens(content)
                
                # Add message if it fits in token budget
                if token_count + msg_tokens <= token_budget:
                    context_messages.insert(0, msg)  # Insert at beginning to maintain order
                    token_count += msg_tokens
                else:
                    # Stop once we exceed budget
                    break
            
            return context_messages
            
        except Exception as e:
            logger.error(f"Error retrieving context window: {e}")
            return []
    
    # Enhanced methods for session workflow management
    
    def create_or_use_session(self, session_id: Optional[str] = None, title: Optional[str] = None) -> Tuple[str, bool, Optional[str]]:
        """
        Create a new session or use an existing one if provided.
        
        This high-level method centralizes the session creation/loading workflow
        that is currently duplicated across CLI and API components.
        
        Args:
            session_id: Optional existing session ID to use
            title: Optional title for a new session
            
        Returns:
            Tuple containing:
            - Session ID to use
            - Whether a new session was created (True) or existing used (False)
            - Error message if any (None if successful)
        """
        try:
            # If no session ID provided, create a new session
            if not session_id:
                new_session_id = self.create_session(title=title)
                return new_session_id, True, None
                
            # Otherwise try to load the existing session
            session_data = self.load_session(session_id)
            if not session_data:
                # Session not found, create a new one
                error_message = f"Session not found: {session_id}"
                new_session_id = self.create_session(title=title)
                return new_session_id, True, error_message
                
            # Session found, use it
            return session_id, False, None
        
        except Exception as e:
            # Handle any errors by creating a new session
            error_message = f"Error loading session: {str(e)}"
            try:
                new_session_id = self.create_session(title=title)
                return new_session_id, True, error_message
            except Exception as create_error:
                # If creation also fails, propagate the error
                raise Exception(f"Failed to load or create session: {str(create_error)}")
    
    def format_session_for_display(self, session_data: Dict[str, Any], include_messages: bool = False, 
                                  max_messages: int = 5) -> Dict[str, Any]:
        """
        Format session data for display in UI or CLI.
        
        Args:
            session_data: Raw session data dictionary
            include_messages: Whether to include message content
            max_messages: Maximum number of messages to include
            
        Returns:
            Dict with formatted session data
        """
        if not session_data:
            return {}
            
        # Format timestamps
        created_at = session_data.get('created_at', '')
        updated_at = session_data.get('updated_at', '')
        
        # Basic formatted session info
        formatted_session = {
            "id": session_data.get('id', ''),
            "title": session_data.get('title', 'Untitled Session'),
            "created_at": created_at,
            "updated_at": updated_at,
            "message_count": len(session_data.get('messages', [])),
            "metadata": session_data.get('metadata', {})
        }
        
        # Include messages if requested
        if include_messages and 'messages' in session_data:
            messages = session_data['messages']
            
            # Limit to the most recent messages if max_messages is set
            if max_messages > 0 and len(messages) > max_messages:
                messages = messages[-max_messages:]
                
            # Format messages
            formatted_messages = []
            for msg in messages:
                formatted_msg = {
                    "role": msg.get('role', ''),
                    "content": msg.get('content', ''),
                    "timestamp": msg.get('timestamp', '')
                }
                formatted_messages.append(formatted_msg)
                
            formatted_session["messages"] = formatted_messages
        
        return formatted_session
    
    def format_sessions_list(self, sessions: List[Dict[str, Any]], 
                            include_metadata: bool = True) -> List[Dict[str, Any]]:
        """
        Format a list of sessions for display.
        
        Args:
            sessions: List of raw session data dictionaries
            include_metadata: Whether to include metadata in the output
            
        Returns:
            List of formatted session data dictionaries
        """
        formatted_sessions = []
        
        for session in sessions:
            # Basic formatted session info
            formatted_session = {
                "id": session.get('id', ''),
                "title": session.get('title', 'Untitled Session'),
                "created_at": session.get('created_at', ''),
                "updated_at": session.get('updated_at', ''),
                "message_count": session.get('message_count', 0)
            }
            
            # Include metadata if requested
            if include_metadata and 'metadata' in session:
                formatted_session["metadata"] = session['metadata']
                
            formatted_sessions.append(formatted_session)
            
        return formatted_sessions
    
    def search_sessions(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Search for sessions by title or content.
        
        Args:
            query: Search query string
            limit: Maximum number of results to return
            
        Returns:
            List of matching session metadata dictionaries
        """
        # Convert to lowercase for case-insensitive search
        query = query.lower()
        matching_sessions = []
        
        try:
            # Get all session files
            session_files = [
                f for f in os.listdir(self.base_dir) 
                if f.endswith('.json')
            ]
            
            for filename in session_files:
                try:
                    with open(os.path.join(self.base_dir, filename), 'r') as f:
                        session = json.load(f)
                        
                        # Check title match
                        title = session.get('title', '').lower()
                        if query in title:
                            matching_sessions.append({
                                "id": session['id'],
                                "title": session['title'],
                                "created_at": session['created_at'],
                                "updated_at": session['updated_at'],
                                "message_count": len(session.get('messages', [])),
                                "match_type": "title"
                            })
                            continue
                            
                        # Check content match (in messages)
                        if 'messages' in session:
                            for message in session['messages']:
                                content = message.get('content', '').lower()
                                if query in content:
                                    matching_sessions.append({
                                        "id": session['id'],
                                        "title": session['title'],
                                        "created_at": session['created_at'],
                                        "updated_at": session['updated_at'],
                                        "message_count": len(session.get('messages', [])),
                                        "match_type": "content"
                                    })
                                    break
                                    
                except Exception as e:
                    logger.warning(f"Error reading session {filename}: {e}")
            
            # Sort by most recently updated
            matching_sessions.sort(key=lambda x: x['updated_at'], reverse=True)
            return matching_sessions[:limit]
        
        except Exception as e:
            logger.error(f"Error searching sessions: {e}")
            return []
    
    def validate_session_existence(self, session_id: str) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
        """
        Validate that a session exists and return its data.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Tuple containing:
            - Success flag (True if session exists)
            - Session data if found, None otherwise
            - Error message if session not found or error occurred
        """
        try:
            session_data = self.load_session(session_id)
            if not session_data:
                return False, None, f"Session not found: {session_id}"
            return True, session_data, None
        except FileNotFoundError:
            return False, None, f"Session file for {session_id} not found"
        except Exception as e:
            return False, None, f"Error loading session: {str(e)}"
            
    def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """
        Get a summary of a session for display.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Dictionary with summary information
        """
        exists, session_data, error = self.validate_session_existence(session_id)
        
        if not exists:
            return {"error": error or f"Session not found: {session_id}"}
            
        # Create summary
        return {
            "id": session_data['id'],
            "title": session_data['title'],
            "created_at": session_data['created_at'],
            "updated_at": session_data['updated_at'],
            "message_count": len(session_data.get('messages', [])),
            "first_message_time": session_data.get('messages', [{}])[0].get('timestamp') if session_data.get('messages') else None,
            "last_message_time": session_data.get('messages', [{}])[-1].get('timestamp') if session_data.get('messages') else None,
            "metadata": session_data.get('metadata', {})
        }
    
    def copy_session(self, session_id: str, new_title: Optional[str] = None) -> Optional[str]:
        """
        Create a copy of an existing session
        
        Creates a new session with the same content as an existing session
        but with a new ID.
        
        Args:
            session_id: Session identifier to copy
            new_title: Optional new title for the copied session
            
        Returns:
            Optional[str]: ID of the new copy, or None if copy failed
        """
        try:
            # Load source session
            source_session = self.load_session(session_id)
            if not source_session:
                logger.error(f"Source session {session_id} not found for copy")
                return None
                
            # Create a new ID and update metadata
            new_session_id = str(uuid.uuid4())
            new_session = source_session.copy()
            new_session['id'] = new_session_id
            new_session['created_at'] = datetime.now(timezone.utc).isoformat()
            new_session['updated_at'] = datetime.now(timezone.utc).isoformat()
            
            if new_title:
                new_session['title'] = new_title
            else:
                new_session['title'] = f"Copy of {source_session['title']}"
                
            # Ensure metadata exists
            if 'metadata' not in new_session:
                new_session['metadata'] = {}
                
            # Add copy information
            new_session['metadata']['copied_from'] = session_id
            new_session['metadata']['copy_date'] = datetime.now(timezone.utc).isoformat()
            
            # Save new session
            session_path = self._get_session_path(new_session_id)
            with open(session_path, 'w') as f:
                json.dump(new_session, f, indent=2)
                
            logger.info(f"Created copy of session {session_id} with new ID {new_session_id}")
            return new_session_id
            
        except Exception as e:
            logger.error(f"Error copying session: {e}")
            return None