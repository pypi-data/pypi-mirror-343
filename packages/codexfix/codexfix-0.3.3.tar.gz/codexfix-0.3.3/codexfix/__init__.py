"""
CodexFix - A powerful type-aware linter runner and Codex orchestrator.

This package provides tools to automatically fix code issues using AI.
"""

__version__ = "0.3.3"

# Import and expose the main function for CLI use
from codexfix.main import cli_entry_point


# For backward compatibility with existing installations
def main() -> None:
    """Entry point for the application."""
    return cli_entry_point()
