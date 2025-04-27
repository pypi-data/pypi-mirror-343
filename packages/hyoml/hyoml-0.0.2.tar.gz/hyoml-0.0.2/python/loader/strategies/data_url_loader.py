"""
DataURLLoader - Strategy to load base64-encoded data URLs (data:text/plain;base64,...).
"""

import base64
from urllib.parse import unquote_to_bytes
from python.loader.strategies.base_strategy import BaseLoaderStrategy

class DataURLLoader(BaseLoaderStrategy):
    """
    Strategy for loading from base64 data URLs.
    """

    def can_load(self, resource: str) -> bool:
        return resource.startswith("data:")

    def load(self, resource: str, resource_agent=None, stream_mode="memory", **opts) -> str:
        """
        Load from a data URL.

        Args:
            resource (str): Data URL string
            resource_agent: (not used for data URLs)
            stream_mode (str): "memory" only supported
            **opts: Extra options

        Returns:
            str: Decoded content as text
        """
        try:
            header, encoded = resource.split(",", 1)
            if ";base64" in header:
                return base64.b64decode(encoded).decode("utf-8")
            else:
                return unquote_to_bytes(encoded).decode("utf-8")
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[DataURLLoader] Failed to decode {resource}: {e}")