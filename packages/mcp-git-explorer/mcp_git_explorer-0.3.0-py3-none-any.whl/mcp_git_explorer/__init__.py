"""MCP Git Explorer - Tool for exploring Git repositories via MCP."""
__version__ = "0.1.0"

from .core import GitExplorer
from .settings import GitExplorerSettings

__all__ = ["GitExplorer", "GitExplorerSettings"]
