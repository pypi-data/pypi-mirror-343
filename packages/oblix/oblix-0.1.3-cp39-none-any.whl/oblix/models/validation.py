# oblix/models/validation.py
from typing import Dict, Any, Optional, List
from enum import Enum
import logging
import re
import aiohttp
from dataclasses import dataclass
from .base import ModelType
from .supported_models import is_model_supported, get_supported_models

logger = logging.getLogger(__name__)

class ValidationErrorType(Enum):
    """Types of validation errors"""
    INVALID_CONFIG = "invalid_config"
    CONNECTION_ERROR = "connection_error"
    MODEL_UNSUPPORTED = "model_unsupported"
    AUTHENTICATION_ERROR = "authentication_error"
    RESOURCE_ERROR = "resource_error"

@dataclass
class ValidationError:
    """Represents a validation error"""
    error_type: ValidationErrorType
    message: str
    details: Optional[Dict[str, Any]] = None

@dataclass
class ValidationResult:
    """Result of model validation"""
    is_valid: bool
    model_type: ModelType
    model_name: str
    errors: List[ValidationError]
    warnings: List[str]
    metadata: Dict[str, Any]

class ModelValidator:
    """
    Validates model configurations and checks compatibility
    """
    
    def __init__(self):
        self._http_session: Optional[aiohttp.ClientSession] = None
    
    async def _get_http_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session"""
        if not self._http_session:
            self._http_session = aiohttp.ClientSession()
        return self._http_session

    def _validate_api_key_format(self, api_key: str, model_type: ModelType) -> Optional[ValidationError]:
        """Validate API key format"""
        if not api_key:
            return ValidationError(
                ValidationErrorType.AUTHENTICATION_ERROR,
                "API key is required"
            )

        # OpenAI API key format: sk-...
        if model_type == ModelType.OPENAI and not api_key.startswith('sk-'):
            return ValidationError(
                ValidationErrorType.AUTHENTICATION_ERROR,
                "Invalid OpenAI API key format"
            )

        # Claude API key format: sk-ant-...
        if model_type == ModelType.CLAUDE and not api_key.startswith('sk-ant-'):
            return ValidationError(
                ValidationErrorType.AUTHENTICATION_ERROR,
                "Invalid Claude API key format"
            )

        return None

    def _validate_endpoint_url(self, endpoint: str) -> Optional[ValidationError]:
        """Validate endpoint URL format"""
        if not endpoint:
            return ValidationError(
                ValidationErrorType.INVALID_CONFIG,
                "Endpoint URL is required"
            )

        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        if not url_pattern.match(endpoint):
            return ValidationError(
                ValidationErrorType.INVALID_CONFIG,
                f"Invalid endpoint URL format: {endpoint}"
            )

        return None

    async def _validate_ollama_endpoint(self, endpoint: str) -> List[ValidationError]:
        """Validate Ollama endpoint connectivity"""
        errors = []
        
        # Validate URL format
        url_error = self._validate_endpoint_url(endpoint)
        if url_error:
            errors.append(url_error)
            return errors

        try:
            session = await self._get_http_session()
            async with session.get(f"{endpoint}/api/tags") as response:
                if response.status != 200:
                    errors.append(ValidationError(
                        ValidationErrorType.CONNECTION_ERROR,
                        f"Ollama server returned status {response.status}",
                        {"status_code": response.status}
                    ))
                    return errors

                # Check response format
                data = await response.json()
                if not isinstance(data, dict) or 'models' not in data:
                    errors.append(ValidationError(
                        ValidationErrorType.CONNECTION_ERROR,
                        "Invalid response format from Ollama server"
                    ))

        except aiohttp.ClientError as e:
            errors.append(ValidationError(
                ValidationErrorType.CONNECTION_ERROR,
                f"Failed to connect to Ollama server: {str(e)}"
            ))
        except Exception as e:
            errors.append(ValidationError(
                ValidationErrorType.CONNECTION_ERROR,
                f"Unexpected error validating Ollama endpoint: {str(e)}"
            ))

        return errors

    async def validate_model_config(self, config: Dict[str, Any]) -> ValidationResult:
        """
        Validate model configuration
        
        Args:
            config: Model configuration dictionary
        
        Returns:
            ValidationResult containing validation status and details
        """
        errors: List[ValidationError] = []
        warnings: List[str] = []
        metadata: Dict[str, Any] = {}

        try:
            # Extract basic config
            model_type = ModelType(config.get('type', ''))
            model_name = config.get('name')
            
            # Debug the incoming config
            logger.debug(f"Validating model config: {config}")

            # Validate required fields
            if not model_name:
                errors.append(ValidationError(
                    ValidationErrorType.INVALID_CONFIG,
                    "Model name is required"
                ))
                return ValidationResult(
                    is_valid=False,
                    model_type=model_type,
                    model_name=model_name,
                    errors=errors,
                    warnings=warnings,
                    metadata=metadata
                )

            # Validate model support for all providers
            if model_type == ModelType.OPENAI:
                logger.debug(f"Validating OpenAI model: {model_name}")
                if not is_model_supported(model_type.value, model_name):
                    supported_models = get_supported_models(model_type.value)
                    errors.append(ValidationError(
                        ValidationErrorType.MODEL_UNSUPPORTED,
                        f"Unsupported {model_type.value} model: {model_name}",
                        {"supported_models": supported_models}
                    ))
            elif model_type == ModelType.CLAUDE:
                logger.debug(f"Validating Claude model: {model_name}")
                if not is_model_supported(model_type.value, model_name):
                    supported_models = get_supported_models(model_type.value)
                    errors.append(ValidationError(
                        ValidationErrorType.MODEL_UNSUPPORTED,
                        f"Unsupported {model_type.value} model: {model_name}",
                        {"supported_models": supported_models}
                    ))

            # Type-specific validation
            if model_type == ModelType.OLLAMA:
                # Validate Ollama endpoint
                endpoint = config.get('endpoint') or "http://localhost:11434"
                ollama_errors = await self._validate_ollama_endpoint(endpoint)
                errors.extend(ollama_errors)

                # We don't warn about default endpoint as it's the expected default
                # The user can modify it if needed via configuration

            elif model_type in [ModelType.OPENAI, ModelType.CLAUDE]:
                # Validate API key
                api_key = config.get('api_key')
                api_key_error = self._validate_api_key_format(api_key, model_type)
                if api_key_error:
                    errors.append(api_key_error)

            # Add model type metadata
            metadata["model_type"] = model_type.value
            metadata["supports_streaming"] = model_type in [ModelType.OPENAI, ModelType.CLAUDE]
            
            # Determine validation result
            is_valid = len(errors) == 0

            return ValidationResult(
                is_valid=is_valid,
                model_type=model_type,
                model_name=model_name,
                errors=errors,
                warnings=warnings,
                metadata=metadata
            )

        except ValueError as e:
            errors.append(ValidationError(
                ValidationErrorType.INVALID_CONFIG,
                f"Invalid model type: {str(e)}"
            ))
            return ValidationResult(
                is_valid=False,
                model_type=ModelType.CUSTOM,  # Fallback type
                model_name=model_name,
                errors=errors,
                warnings=warnings,
                metadata=metadata
            )

        except Exception as e:
            errors.append(ValidationError(
                ValidationErrorType.INVALID_CONFIG,
                f"Unexpected error during validation: {str(e)}"
            ))
            return ValidationResult(
                is_valid=False,
                model_type=ModelType.CUSTOM,  # Fallback type
                model_name=model_name,
                errors=errors,
                warnings=warnings,
                metadata=metadata
            )

    async def cleanup(self):
        """Clean up resources"""
        if self._http_session:
            await self._http_session.close()
            self._http_session = None
