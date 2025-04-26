import importlib.metadata

from .dbcode import DBCode
from .easyquery import get_tree, query_data

try:
    __version__ = importlib.metadata.version("cnstats-py")
except importlib.metadata.PackageNotFoundError:
    # Handle case where the package is not installed (e.g., during development)
    __version__ = "unknown"

# You can now use the __version__ variable
print(f"cnstats version: {__version__}")

__all__ = ["__version__", "DBCode", "get_tree", "query_data"]
