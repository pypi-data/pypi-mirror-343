#!/usr/bin/env python3
"""Command-line interface for the MCP Git Explorer."""

import sys
import os
import argparse

from .core import GitExplorer
from .settings import GitExplorerSettings

def main():
    """Run the MCP Git Explorer CLI."""
    parser = argparse.ArgumentParser(description="MCP Git Explorer")
    parser.add_argument(
        "--transport", 
        choices=["stdio", "sse"], 
        default="stdio",
        help="Transport protocol to use (default: stdio)"
    )
    parser.add_argument(
        "--gitlab-token",
        help="GitLab personal access token (alternatively set GIT_EXPLORER_GITLAB_TOKEN env var)"
    )
    
    args = parser.parse_args()
    
    # Set up settings
    settings = GitExplorerSettings()
    if args.gitlab_token:
        settings.gitlab_token = args.gitlab_token
    
    # Create and run the explorer
    explorer = GitExplorer(settings=settings)
    explorer.run(transport=args.transport)

if __name__ == "__main__":
    sys.exit(main())
