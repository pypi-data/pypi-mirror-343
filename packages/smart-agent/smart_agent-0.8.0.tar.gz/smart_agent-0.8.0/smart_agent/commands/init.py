"""
Init command implementation for the Smart Agent CLI.
"""

import os
import logging
from typing import Dict, Tuple

import click
from rich.console import Console

from ..tool_manager import ConfigManager

# Set up logging
logger = logging.getLogger(__name__)

# Initialize console for rich output
console = Console()


def initialize_config_files(
    config_manager: ConfigManager,
) -> str:
    """
    Initialize configuration files.

    Args:
        config_manager: Configuration manager instance

    Returns:
        Path to the config file
    """
    # Initialize configuration file
    config_file = config_manager.init_config()

    return config_file


@click.command()
@click.option(
    "--config",
    default=None,
    help="Path to configuration file",
)
def init(config):
    """
    Initialize configuration file.

    Args:
        config: Path to configuration file
    """
    # Create configuration manager
    config_manager = ConfigManager(config_path=config)

    # Check if config file already exists before initializing
    config_file = os.path.join(os.getcwd(), "config.yaml")
    file_existed = os.path.exists(config_file)
    
    if file_existed:
        console.print(f"[yellow]Configuration file already exists: {config_file}[/]")
    else:
        # Initialize configuration file
        config_file = initialize_config_files(config_manager)
        console.print(f"[green]Initialized configuration file: {config_file}[/]")
        console.print("\n[bold]Edit this file to configure the agent and tools.[/]")

        # Print next steps
        console.print("\n[bold]Next steps:[/]")
        console.print("1. Edit the configuration files to set your API key and other settings")
        console.print("2. Run 'smart-agent start' to start server for tool services")
        console.print("3. Run 'smart-agent chat' to start chat client in terminal or 'smart-agent chainlit' to start chainlit app")
