"""
FilePathLoader - Strategy to load local filesystem files.
"""

from python.loader.strategies.base_strategy import BaseLoaderStrategy

class FilePathLoader(BaseLoaderStrategy):
    """
    Strategy for loading local file paths.
    """

    def can_load(self, resource: str) -> bool:
        # Assume it's a path if no known scheme (http://, s3://, etc.)
        return not any(resource.startswith(prefix) for prefix in ("http://", "https://", "s3://", "gs://", "azure://", "data:"))

    def load(self, resource: str, resource_agent=None, stream_mode="memory", **opts) -> str:
        """
        Load from local filesystem.

        Args:
            resource (str): Local file path
            resource_agent: (not used for file loading)
            stream_mode (str): "memory" (default)
            **opts: Extra options

        Returns:
            str: Content as text
        """
        try:
            if stream_mode == "streaming":
                return open(resource, "rb")
            else:
                with open(resource, "r", encoding="utf-8") as f:
                    return f.read()
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[FilePathLoader] Failed to load {resource}: {e}")
