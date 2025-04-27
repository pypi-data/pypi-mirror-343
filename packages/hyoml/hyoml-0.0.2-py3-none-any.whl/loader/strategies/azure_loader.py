"""
AzureLoader - Strategy to load resources from Azure Blob Storage (azure://container/blob).
"""

from python.loader.strategies.base_strategy import BaseLoaderStrategy

class AzureLoader(BaseLoaderStrategy):
    """
    Strategy for loading from Azure Blob Storage.
    """

    def can_load(self, resource: str) -> bool:
        return resource.startswith("azure://")

    def load(self, resource: str, resource_agent=None, stream_mode="memory", **opts) -> str:
        """
        Load Azure Blob Storage resource.

        Args:
            resource (str): azure://container/blob URI
            resource_agent: Azure BlobServiceClient
            stream_mode (str): "memory" (default)
            **opts: Extra options

        Returns:
            str: Content as text
        """
        if resource_agent is None:
            raise ValueError("[AzureLoader] Missing Azure BlobServiceClient in resource_agent.")

        container_name, blob_name = self._extract_container_blob(resource)
        try:
            blob_client = resource_agent.get_blob_client(container=container_name, blob=blob_name)
            if stream_mode == "streaming":
                return blob_client.download_blob().readall()
            else:
                return blob_client.download_blob().readall().decode("utf-8")
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[AzureLoader] Failed to load {resource}: {e}")

    @staticmethod
    def _extract_container_blob(uri: str):
        no_scheme = uri.split("azure://", 1)[1]
        parts = no_scheme.split("/", 1)
        container = parts[0]
        blob = parts[1] if len(parts) > 1 else ""
        return container, blob