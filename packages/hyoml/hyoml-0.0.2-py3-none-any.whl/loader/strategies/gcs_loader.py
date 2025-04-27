"""
GCSLoader - Strategy to load resources from Google Cloud Storage (gs://bucket/blob).
"""

from python.loader.strategies.base_strategy import BaseLoaderStrategy

class GCSLoader(BaseLoaderStrategy):
    """
    Strategy for loading from Google Cloud Storage.
    """

    def can_load(self, resource: str) -> bool:
        return resource.startswith("gs://")

    def load(self, resource: str, resource_agent=None, stream_mode="memory", **opts) -> str:
        """
        Load GCS resource.

        Args:
            resource (str): gs://bucket/blob URI
            resource_agent: GCS Client instance
            stream_mode (str): "memory" (default)
            **opts: Extra options

        Returns:
            str: Content as text
        """
        if resource_agent is None:
            raise ValueError("[GCSLoader] Missing GCS client in resource_agent.")

        bucket_name, blob_name = self._extract_bucket_blob(resource)
        try:
            bucket = resource_agent.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            if stream_mode == "streaming":
                return blob.open("r")  # Streaming file-like reader
            else:
                return blob.download_as_text()
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[GCSLoader] Failed to load {resource}: {e}")

    @staticmethod
    def _extract_bucket_blob(uri: str):
        no_scheme = uri.split("gs://", 1)[1]
        parts = no_scheme.split("/", 1)
        bucket = parts[0]
        blob = parts[1] if len(parts) > 1 else ""
        return bucket, blob