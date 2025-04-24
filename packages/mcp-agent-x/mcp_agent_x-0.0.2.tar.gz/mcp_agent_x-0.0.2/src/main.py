"""
Main entry point for the MCP Agent X application.

This module contains the main functions for starting the REPL interface
and initializing the agent with the appropriate LLM provider.

Environment Variables:
    GOOGLE_API_KEY: Required if using Google/Gemini as the LLM provider (default)
    OPENAI_API_KEY: Required if using OpenAI as the LLM provider
    ANTHROPIC_API_KEY: Required if using Anthropic as the LLM provider

API Key Notes:
    - The application checks for the required API key based on the configured LLM provider
    - API keys can be set in a .env file in the project root or as environment variables
    - If the required API key is missing or invalid, the application will display an error
      message and exit
    - To change providers, edit the config.json file or use the appropriate configuration
      command in the REPL
"""

import asyncio
import os
import sys
import uuid
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.language_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

# Pick either mcp_use or mcp_api_client based on which is actually installed
try:
    from mcp_use import MCPClient
except ImportError:
    from mcp_api_client import MCPClient
from rich.console import Console

from mcpx.agent import ExtendedMCPAgent
from mcpx.config import (
    CONVERSATION_DIR,
    Config,
    load_system_prompt,
)
from mcpx.repl import AgentREPL

# Constants
console = Console()


def display_api_key_warning(missing_key: str) -> None:
    """Display an ASCII art warning when a required API key is missing."""
    warning = f"""
    ╔══════════════════════════════════════════════════════════╗
    ║                   ⚠️  WARNING  ⚠️                       ║
    ╟──────────────────────────────────────────────────────────╢
    ║  Missing required API key: {missing_key:<30} ║
    ║                                                          ║
    ║  Please set this environment variable before continuing. ║
    ║  You can add it to your .env file or export it directly. ║
    ║                                                          ║
    ║  Example:                                                ║
    ║    echo '{missing_key}=your_key_here' >> .env            ║
    ║    # or                                                  ║
    ║    export {missing_key}=your_key_here                    ║
    ╚══════════════════════════════════════════════════════════╝
    """
    print(warning)


def check_api_keys(config: Config) -> tuple[bool, str | None]:
    """Check if necessary API keys are set based on the configuration.

    Returns:
        Tuple[bool, Optional[str]]: A tuple containing (success, missing_key_name)
    """
    provider = config.llm_provider.lower()

    if provider == "openai":
        key = os.environ.get("OPENAI_API_KEY") or ""
        if not key.strip():
            return False, "OPENAI_API_KEY"
    elif provider == "anthropic":
        key = os.environ.get("ANTHROPIC_API_KEY") or ""
        if not key.strip():
            return False, "ANTHROPIC_API_KEY"
    elif provider == "gemini" or provider == "google":
        key = os.environ.get("GOOGLE_API_KEY") or ""
        if not key.strip():
            return False, "GOOGLE_API_KEY"
    elif provider in config.custom_providers:
        provider_config = config.get_provider_config(provider)
        if provider_config and (
            not provider_config.api_key or provider_config.api_key == "YOUR_API_KEY"
        ):
            return False, f"Custom API key for {provider}"

    return True, None


def create_llm_from_config(config: Config) -> BaseChatModel:
    """Create an LLM based on the configuration.

    Args:
        config: Config object containing LLM settings

    Returns:
        A configured LLM instance

    Raises:
        ValueError: If the provider is not supported or API key issues
    """
    provider = config.llm_provider

    # Handle standard providers
    if provider == "google":
        # Check for google api key specifically
        api_key = os.environ.get("GOOGLE_API_KEY", "")
        if not api_key.strip():
            raise ValueError(
                "GOOGLE_API_KEY environment variable is not set or is empty"
            )

        try:
            # Explicitly test the API key by trying to create the model
            return ChatGoogleGenerativeAI(model=config.llm_model)
        except Exception as e:
            # Check for common Google API key error messages
            error_msg = str(e).lower()
            if "invalid api key" in error_msg or "error 400" in error_msg:
                raise ValueError(
                    f"Google API Key appears to be invalid. Error details: {str(e)}"
                ) from e
            elif "rate limit" in error_msg:
                raise ValueError(f"Google API rate limit exceeded: {str(e)}") from e
            elif "permission" in error_msg or "access" in error_msg:
                raise ValueError(
                    f"Google API Key lacks permissions for this model: {str(e)}"
                ) from e
            else:
                raise ValueError(
                    f"Error initializing Google Generative AI: {str(e)}"
                ) from e
    elif provider == "openai":
        # Get OpenAI provider config
        provider_config = config.get_provider_config("openai")
        if not provider_config:
            raise ValueError("OpenAI provider configuration not found")

        if not provider_config.api_key or provider_config.api_key == "YOUR_API_KEY":
            raise ValueError("OpenAI API key is not properly configured")

        # Create OpenAI chat model
        return ChatOpenAI(
            model=config.llm_model,
            openai_api_key=provider_config.api_key,
            openai_api_base=(
                provider_config.base_url if provider_config.base_url else None
            ),
        )
    elif provider == "anthropic":
        # We would need to add the anthropic package import
        raise ValueError("Anthropic provider not yet implemented")
    elif provider in config.custom_providers:
        # Handle custom providers - this would require a more generic approach
        # and potentially custom implementations
        raise ValueError(f"Custom provider '{provider}' not yet implemented")
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")


async def start_repl(session_id=None):
    """Start the REPL interface with the given session ID."""
    # Load environment variables
    load_dotenv()

    # Generate a session ID if not provided
    if session_id is None:
        session_id = str(uuid.uuid4())[:8]

    # Create the conversations directory if it doesn't exist
    conversation_dir = Path(CONVERSATION_DIR)
    conversation_dir.mkdir(exist_ok=True, parents=True)

    # Load configuration and system prompt
    config = Config.from_file()
    system_prompt = load_system_prompt()

    # Check for required API keys before proceeding
    has_keys, missing_key = check_api_keys(config)
    if not has_keys:
        display_api_key_warning(missing_key)
        print("Exiting due to missing API key.")
        sys.exit(1)

    try:
        # Create MCPClient from configuration dictionary
        client = MCPClient.from_dict({"mcpServers": config.mcp_servers})
        print(
            f"Initialized MCPClient with servers: {', '.join(config.mcp_servers.keys())}"
        )

        # Create LLM based on config
        try:
            llm = create_llm_from_config(config)
        except Exception as e:
            print(f"Error creating LLM from config: {e}")
            if "GOOGLE_API_KEY" in str(e) or "google" in config.llm_provider.lower():
                display_api_key_warning("GOOGLE_API_KEY")
                print("Please check your Google API key and ensure it's valid.")
            elif "OPENAI_API_KEY" in str(e) or "openai" in config.llm_provider.lower():
                display_api_key_warning("OPENAI_API_KEY")
                print("Please check your OpenAI API key and ensure it's valid.")
            elif (
                "ANTHROPIC_API_KEY" in str(e)
                or "anthropic" in config.llm_provider.lower()
            ):
                display_api_key_warning("ANTHROPIC_API_KEY")
                print("Please check your Anthropic API key and ensure it's valid.")
            sys.exit(1)

        # Create agent with the client and configured settings
        agent = ExtendedMCPAgent(
            llm=llm,
            client=client,
            memory_enabled=config.memory_enabled,
            system_prompt=system_prompt,
            max_steps=config.max_steps,
        )
        print(
            f"Agent configured with max_steps={config.max_steps}, memory_enabled={config.memory_enabled}"
        )

        # Create and start the REPL interface
        repl = AgentREPL(
            agent=agent,
            system_prompt=system_prompt,
            session_id=session_id,
            lazy_init=True,  # Always use lazy_init to avoid initialization issues
        )
        await repl.run()
    except ValueError as e:
        print(f"Error starting REPL: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback

        print(traceback.format_exc())
        sys.exit(1)


async def main():
    """Legacy main function for backward compatibility."""
    await start_repl()


if __name__ == "__main__":
    asyncio.run(main())
