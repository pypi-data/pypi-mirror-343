"""
BaseLoaderStrategy - Abstract base class for all loader strategies.
"""

from abc import ABC, abstractmethod

class BaseLoaderStrategy(ABC):
    """
    Abstract base class for all loader strategies.
    Each loader must implement `can_load` and `load` methods.
    """

    @abstractmethod
    def can_load(self, resource: str) -> bool:
        """
        Check if this strategy can handle the given resource.

        Args:
            resource (str): The path, URI, or identifier.

        Returns:
            bool: True if this loader can handle the resource.
        """
        pass

    @abstractmethod
    def load(self, resource: str, resource_agent=None, stream_mode="memory", **opts) -> str:
        """
        Load the content of the resource.

        Args:
            resource (str): The path, URI, or identifier.
            resource_agent (optional): Cloud agent/client if needed.
            stream_mode (str): "memory" or "streaming"
            **opts: Additional options.

        Returns:
            str: Loaded content (or a stream if stream_mode="streaming")
        """
        pass
