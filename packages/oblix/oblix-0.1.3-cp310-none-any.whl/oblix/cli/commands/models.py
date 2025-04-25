# oblix/cli/commands/models.py
import click
import colorama
from colorama import Fore, Style
import httpx
import asyncio
import sys
import json

from oblix.cli.utils import (
    print_header, print_success, print_warning, print_error, 
    print_info, print_model_item
)

# Initialize colorama
colorama.init()

from oblix.models.manager import ModelManager

# Create a model manager instance
model_manager = ModelManager()

@click.command(name='models')
@click.option('--refresh', is_flag=True, help='Force refresh of model list')
def models_group(refresh):
    """Show available AI models for use with Oblix"""
    # We need to use asyncio.run since this is a synchronous Click command
    # but we need to make async API calls
    asyncio.run(async_models_group(refresh))

async def async_models_group(refresh):
    print_header("Supported Model Providers")
    print_info("Oblix supports the following AI model providers and models:")
    
    # Get all available models from the model manager
    available_models = await model_manager.list_available_models()
    
    # Show Ollama models
    print_header("Ollama")
    print_info("Local models served through Ollama")
    
    ollama_models = available_models.get("ollama", [])
    
    if ollama_models:
        print_success("\nInstalled Ollama models:")
        for model in ollama_models:
            print_model_item(model)
    else:
        print_warning("\nCould not connect to Ollama server or no models found.")
        print_info("To use local models, please:")
        print_info("1. Install Ollama from https://ollama.com")
        print_info("2. Start the Ollama service")
        print_info("3. Run 'ollama pull <model_name>' to download models")
    
    # Show OpenAI models
    print_header("OpenAI")
    print_info("GPT models via OpenAI API")
    print_success("\nRecommended OpenAI models:")
    
    openai_models = model_manager.get_openai_models()
    for model in openai_models:
        description = f"{model['description']} - {model.get('features', '')}"
        context = model.get('context_window', '')
        if context:
            description += f" (Context: {context})"
        print_model_item(model["name"], description)
    
    # Show Claude models
    print_header("Claude")
    print_info("Claude models via Anthropic API")
    print_success("\nRecommended Claude models:")
    
    claude_models = model_manager.get_claude_models()
    for model in claude_models:
        description = f"{model['description']} - {model.get('features', '')}"
        context = model.get('context_window', '')
        if context:
            description += f" (Context: {context})"
        print_model_item(model["name"], description)
    
    print() # Add a blank line at the end