from python.cloud_storage.cloud_storage_agent import CloudStorageAgent

class AzureBlobStorageAgent(CloudStorageAgent):
    def __init__(self, blob_service_client, container_name: str):
        """
        Initialize the Azure Blob storage agent with the user's `blob_service_client` and `container_name`.
        
        Args:
            blob_service_client (azure.storage.blob.BlobServiceClient): The Azure Blob service client passed by the user.
            container_name (str): The name of the Azure Blob container.
        """
        self.blob_service_client = blob_service_client
        self.container_client = self.blob_service_client.get_container_client(container_name)

    def upload(self, data: str, path: str):
        """
        Upload data to Azure Blob Storage using the provided blob_service_client.
        
        Args:
            data (str): The content to upload.
            path (str): The Azure Blob path (azure://container_name/file).
        """
        blob_client = self.container_client.get_blob_client(path)
        blob_client.upload_blob(data)
