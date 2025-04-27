"""
S3Loader - Strategy to load resources from AWS S3 (s3://bucket/key).
"""

from python.loader.strategies.base_strategy import BaseLoaderStrategy

class S3Loader(BaseLoaderStrategy):
    """
    Strategy for loading from Amazon S3 storage.
    """

    def can_load(self, resource: str) -> bool:
        return resource.startswith("s3://")

    def load(self, resource: str, resource_agent=None, stream_mode="memory", **opts) -> str:
        """
        Load S3 resource.

        Args:
            resource (str): s3://bucket/key URI
            resource_agent: Boto3 S3 client
            stream_mode (str): "memory" (default, full content)
            **opts: Extra options

        Returns:
            str: Content as text
        """
        if resource_agent is None:
            raise ValueError("[S3Loader] Missing boto3 S3 client in resource_agent.")

        bucket, key = self._extract_bucket_key(resource)
        try:
            obj = resource_agent.get_object(Bucket=bucket, Key=key)
            if stream_mode == "streaming":
                return obj["Body"]  # Streaming file-like
            else:
                return obj["Body"].read().decode("utf-8")
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[S3Loader] Failed to load {resource}: {e}")

    @staticmethod
    def _extract_bucket_key(uri: str):
        no_scheme = uri.split("s3://", 1)[1]
        parts = no_scheme.split("/", 1)
        bucket = parts[0]
        key = parts[1] if len(parts) > 1 else ""
        return bucket, key
