# oblix/auth/auth.py
from datetime import datetime, timedelta, timezone
import hashlib
import httpx
from typing import Dict, Any, Optional
import logging
import os
import uuid
import json
import asyncio
from pathlib import Path

logger = logging.getLogger(__name__)

class APIKeyValidationError(Exception):
    """Raised when API key validation fails."""
    def __init__(self, message: str, error_type: str = "validation"):
        super().__init__(message)
        self.error_type = error_type

class RateLimitExceededError(APIKeyValidationError):
    """Raised when API key rate limit is exceeded."""
    def __init__(self, reset_time: Optional[datetime] = None):
        message = "Rate limit exceeded"
        if reset_time:
            message += f". Reset at {reset_time.isoformat()}"
        super().__init__(message, error_type="rate_limit")
        self.reset_time = reset_time

class OblixAuth:
    """Handles authentication and API key validation for Oblix API."""
    
    def __init__(self, api_key: str, validation_url: str = None):
        self.api_key = api_key
        # Use environment variable if available, otherwise default
        self.validation_url = validation_url or os.environ.get(
            "OBLIX_API_URL", 
            "https://api.oblixai.com"
        )
        self._http_client = httpx.AsyncClient(timeout=10.0)
        
        # Key validation cache
        self._key_validation_cache = {
            "key_hash": None,
            "validated_at": None,
            "expires_at": None,
            "metadata": None,
            "user_id": None,
            "validation_type": None  # 'server', 'local', 'fallback'
        }
        
        # Cache file path
        self._cache_dir = os.path.join(os.path.expanduser("~"), ".oblix")
        self._cache_file = os.path.join(self._cache_dir, "auth_cache.json")
        
        # Background refresh task
        self._background_task = None
    
    async def validate_key(self, force_revalidation: bool = False) -> Dict[str, Any]:
        """
        Validate API key with advanced caching and validation mechanisms.
        
        Args:
            force_revalidation (bool): Force revalidation even if cached.
        
        Returns:
            Dict of key metadata upon successful validation.
        
        Raises:
            APIKeyValidationError: For various validation failures.
        """
        if not self.api_key:
            raise APIKeyValidationError("API key not provided")
        
        # Generate key hash
        key_hash = hashlib.sha256(self.api_key.encode()).hexdigest()
        now = datetime.now(timezone.utc)
        
        # Check in-memory cache first (fastest)
        if (not force_revalidation and 
            self._key_validation_cache['key_hash'] == key_hash and 
            self._key_validation_cache['expires_at'] and
            now < self._key_validation_cache['expires_at']):
            logger.info("Using in-memory API key validation cache")
            
            # Start background refresh if needed and not already running
            self._maybe_start_background_refresh(key_hash)
            
            return self._key_validation_cache['metadata']
        
        # If not in memory cache, try file cache
        if not force_revalidation and self._load_cache_from_file(key_hash):
            logger.info("Using file-cached API key validation")
            
            # Start background refresh if needed
            self._maybe_start_background_refresh(key_hash)
            
            return self._key_validation_cache['metadata']
        
        # IMPORTANT: First-time validation is ALWAYS with server - no exceptions!
        # We'll track validated keys in a special file

        # Check if this key has been validated with server before
        validated_file = os.path.join(self._cache_dir, f"validated_{key_hash[:16]}")
        is_first_validation = not os.path.exists(validated_file)
        
        # First-time validation MUST be with server
        if is_first_validation:
            logger.info("First-time API key validation - checking with server")
            try:
                # Force validation with server endpoint
                validation_data = await self._perform_server_validation(key_hash)
                
                # Validation succeeded - mark key as validated
                try:
                    os.makedirs(self._cache_dir, exist_ok=True)
                    with open(validated_file, 'w') as f:
                        f.write(datetime.now(timezone.utc).isoformat())
                except Exception as e:
                    logger.warning(f"Failed to create validation marker: {e}")
                
                # Set expiration to 24 hours for server validation
                expires_at = now + timedelta(hours=24)
                
                # Update cache
                self._update_cache(key_hash, validation_data, now, expires_at, 'server')
                
                logger.info("New API key validated successfully via server")
                return validation_data
                
            except (httpx.TimeoutException, httpx.ConnectError) as e:
                # Connection error during first-time validation
                logger.error(f"Connection error during first-time validation: {e}")
                raise APIKeyValidationError(
                    "Unable to connect to validation server. Please check your internet connection and try again."
                )
                
            except APIKeyValidationError as e:
                # Authentication error - pass through
                logger.error(f"API key validation error: {e}")
                raise
                
            except Exception as e:
                # Any other error during first-time validation
                logger.error(f"First-time validation failed: {e}")
                raise APIKeyValidationError(
                    "API key validation failed. Please check your key or visit www.oblix.ai for a valid key. " +
                    f"Error: {str(e)}"
                )
        
        # For previously validated keys, check local validation setting
        use_local_validation = os.environ.get('OBLIX_LOCAL_VALIDATION', 'true').lower() == 'true'
        
        if use_local_validation:
            logger.info("Using local API key validation for previously validated key")
            # Create valid metadata locally
            metadata = self._create_local_metadata(key_hash)
            
            # Set fixed 7-day expiration for local validation
            expires_at = now + timedelta(days=7)
            
            # Update cache
            self._update_cache(key_hash, metadata, now, expires_at, 'local')
            return metadata
        
        # If local validation is disabled, proceed with server validation
        try:
            validation_data = await self._perform_server_validation(key_hash)
            
            # Set expiration to 24 hours for server validation
            expires_at = now + timedelta(hours=24)
            
            # Update cache
            self._update_cache(key_hash, validation_data, now, expires_at, 'server')
            
            logger.info("API key validated successfully via server")
            return validation_data
            
        except (httpx.TimeoutException, httpx.ConnectError) as e:
            logger.warning(f"Validation service unavailable: {str(e)} - falling back to local validation")
            # Fall back to local validation if server is unreachable
            metadata = self._create_local_metadata(key_hash)
            
            # Cache for 4 hours when connection fallback
            expires_at = now + timedelta(hours=4)
            
            # Update cache
            self._update_cache(key_hash, metadata, now, expires_at, 'fallback_connection')
            return metadata
            
        except httpx.HTTPError as e:
            logger.error(f"API key validation failed: {str(e)}")
            # In production, we might want to fail here
            # But for better user experience, we can fall back to local validation
            if os.environ.get('OBLIX_STRICT_VALIDATION', 'false').lower() == 'true':
                raise APIKeyValidationError(f"Validation service error: {str(e)}")
            else:
                logger.warning("Falling back to local validation after HTTP error")
                metadata = self._create_local_metadata(key_hash)
                
                # Cache for 1 hour when error fallback
                expires_at = now + timedelta(hours=1)
                
                # Update cache
                self._update_cache(key_hash, metadata, now, expires_at, 'fallback_error')
                return metadata
    
    async def _perform_server_validation(self, key_hash: str) -> Dict[str, Any]:
        """Perform server-side validation of the API key"""
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        # Create URL for validation endpoint - ensure correct path is used
        validation_endpoint = f"{self.validation_url}/api/validate"
        logger.debug(f"Validating key with endpoint: {validation_endpoint}")
        
        # Make request with debugging info
        logger.debug(f"Making API key validation request with key hash: {key_hash[:8]}...")
        response = await self._http_client.post(
            validation_endpoint,
            json={"key_hash": key_hash, "client_version": "improved_validation"},
            headers=headers,
            timeout=15.0  # Extended timeout for validation
        )
        
        # Handle standard error codes
        if response.status_code == 401:
            raise APIKeyValidationError("Invalid API key. Please get a new API key from www.oblix.ai")
        
        if response.status_code == 403:
            raise APIKeyValidationError("Your API key has insufficient permissions. Visit www.oblix.ai to upgrade your account")
        
        if response.status_code == 404:
            raise APIKeyValidationError("API key not found. Please get a new API key from www.oblix.ai")
        
        if response.status_code == 429:
            reset_time = None
            try:
                reset_timestamp = int(response.headers.get('X-RateLimit-Reset', 0))
                if reset_timestamp:
                    reset_time = datetime.fromtimestamp(reset_timestamp)
            except (ValueError, TypeError):
                pass
            raise RateLimitExceededError(reset_time)
        
        response.raise_for_status()
        validation_data = response.json()
        
        # Ensure we have user information
        if 'user_id' not in validation_data:
            logger.warning("API key validation succeeded but no user_id was returned")
            validation_data['user_id'] = f"user_{key_hash[:8]}"
            
        return validation_data
    
    def _update_cache(self, key_hash: str, metadata: Dict[str, Any], 
                      validated_at: datetime, expires_at: datetime,
                      validation_type: str):
        """Update both in-memory and file caches"""
        # Update in-memory cache
        self._key_validation_cache = {
            "key_hash": key_hash,
            "validated_at": validated_at,
            "expires_at": expires_at,
            "metadata": metadata,
            "user_id": metadata.get('user_id'),
            "validation_type": validation_type
        }
        
        # Update file cache
        self._save_cache_to_file()
    
    def _save_cache_to_file(self):
        """Save the current cache to file"""
        try:
            # Ensure cache directory exists
            os.makedirs(self._cache_dir, exist_ok=True)
            
            # Don't store actual API key, only hash and metadata
            cache_data = {
                "key_hash": self._key_validation_cache["key_hash"],
                "validated_at": self._key_validation_cache["validated_at"].isoformat() if self._key_validation_cache["validated_at"] else None,
                "expires_at": self._key_validation_cache["expires_at"].isoformat() if self._key_validation_cache["expires_at"] else None,
                "metadata": self._key_validation_cache["metadata"],
                "user_id": self._key_validation_cache["user_id"],
                "validation_type": self._key_validation_cache["validation_type"]
            }
            
            with open(self._cache_file, 'w') as f:
                json.dump(cache_data, f)
                
            logger.debug(f"Saved authentication cache to {self._cache_file}")
            
        except Exception as e:
            logger.warning(f"Failed to save auth cache: {e}")
    
    def _load_cache_from_file(self, key_hash: str) -> bool:
        """
        Load cache from file if valid
        
        Args:
            key_hash: Hash of the API key to validate against
            
        Returns:
            bool: True if valid cache loaded, False otherwise
        """
        try:
            if not os.path.exists(self._cache_file):
                return False
                
            with open(self._cache_file, 'r') as f:
                cache_data = json.load(f)
                
            # Verify the cache is for the same key
            if cache_data.get("key_hash") != key_hash:
                logger.debug("Cache file exists but for different API key")
                return False
                
            # Parse dates back to datetime objects
            expires_at = None
            validated_at = None
            
            if cache_data.get("expires_at"):
                try:
                    expires_at = datetime.fromisoformat(cache_data["expires_at"])
                except (ValueError, TypeError):
                    logger.warning("Invalid expires_at date format in cache")
                    return False
                    
            if cache_data.get("validated_at"):
                try:
                    validated_at = datetime.fromisoformat(cache_data["validated_at"])
                except (ValueError, TypeError):
                    validated_at = None
            
            # Check if cache is expired
            if not expires_at or datetime.now(timezone.utc) >= expires_at:
                logger.debug("Cache file exists but is expired")
                return False
            
            # Cache is valid, load it
            self._key_validation_cache = {
                "key_hash": cache_data["key_hash"],
                "validated_at": validated_at,
                "expires_at": expires_at,
                "metadata": cache_data["metadata"],
                "user_id": cache_data["user_id"],
                "validation_type": cache_data.get("validation_type", "unknown")
            }
            return True
            
        except Exception as e:
            logger.warning(f"Failed to load auth cache: {e}")
            return False
    
    def _create_local_metadata(self, key_hash: str) -> Dict[str, Any]:
        """Create metadata for local validation"""
        user_id = f"user_{key_hash[:8]}"
        return {
            "user_id": user_id,
            "tier": "standard",
            "rate_limit": 100,
            "features": ["local_models", "cloud_models", "agents"],
            "validated_locally": True,
            "key_hash": key_hash[:16]  # Store partial hash for reference
        }
    
    def _maybe_start_background_refresh(self, key_hash: str):
        """
        Start background refresh task if needed
        
        This will refresh server validation in the background when:
        1. The current validation is from fallback or is approaching expiration
        2. No background task is already running
        3. We're not in purely local development mode
        """
        if self._background_task and not self._background_task.done():
            return  # Task already running
            
        # Skip if key was recently validated by server
        if (self._key_validation_cache.get('validation_type') == 'server' and 
            self._key_validation_cache.get('validated_at') and
            (datetime.now(timezone.utc) - self._key_validation_cache['validated_at']).total_seconds() < 3600):
            return
            
        # Always attempt background refresh for non-server validations
        # This improves user experience by silently validating in background
        if self._key_validation_cache.get('validation_type') in ('local', 'fallback_connection', 'fallback_error', 'unknown'):
            self._background_task = asyncio.create_task(self._background_refresh(key_hash))
    
    async def _background_refresh(self, key_hash: str):
        """
        Try to refresh validation in the background without blocking
        """
        try:
            # Wait a bit to not impact current operation
            await asyncio.sleep(1.0)
            
            # Try to validate with server quietly
            logger.debug("Starting background validation refresh")
            validation_data = await self._perform_server_validation(key_hash)
            
            now = datetime.now(timezone.utc)
            expires_at = now + timedelta(hours=24)
            
            # Update cache with new server validation
            self._update_cache(key_hash, validation_data, now, expires_at, 'server')
            
            logger.debug("Background validation refresh completed successfully")
            
        except Exception as e:
            # Just log any errors, don't affect main operation
            logger.debug(f"Background validation refresh failed: {e}")
    
    async def get_user_id(self) -> Optional[str]:
        """
        Get the user ID associated with the API key.
        
        Returns:
            Optional[str]: User ID if available, None otherwise
        """
        if self._key_validation_cache.get('user_id'):
            return self._key_validation_cache['user_id']
        
        # Validate if not already done
        validation_data = await self.validate_key()
        return validation_data.get('user_id')
    
    async def cleanup(self):
        """Cleanup resources."""
        # Cancel any background task
        if self._background_task and not self._background_task.done():
            self._background_task.cancel()
            
        # Close HTTP client
        if self._http_client:
            await self._http_client.aclose()
