# Defines the package version. Will be updated by build script if needed.
__version__ = "0.0.0"  # Placeholder, consider injecting actual version during build

# Makes the client class available directly from the package import
from .client import CarapisClient

__all__ = ['CarapisClient', '__version__']
