"""
HTTPLoader - Strategy to load resources over HTTP/HTTPS.
"""

import requests
from python.loader.strategies.base_strategy import BaseLoaderStrategy

class HTTPLoader(BaseLoaderStrategy):
    """
    Strategy for loading HTTP/HTTPS resources.
    """

    def can_load(self, resource: str) -> bool:
        return resource.startswith("http://") or resource.startswith("https://")

    def load(self, resource: str, resource_agent=None, stream_mode="memory", timeout=10, **opts) -> str:
        """
        Load HTTP/HTTPS resource.

        Args:
            resource (str): URL to load
            resource_agent: (not used for HTTP)
            stream_mode (str): "memory" (default) or "streaming"
            timeout (int): Request timeout seconds
            **opts: Extra options

        Returns:
            str: Content as text or streaming response object
        """
        try:
            if stream_mode == "streaming":
                response = requests.get(resource, timeout=timeout, stream=True)
                response.raise_for_status()
                return response.raw
            else:
                response = requests.get(resource, timeout=timeout)
                response.raise_for_status()
                return response.text
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[HTTPLoader] Failed to load {resource}: {e}")