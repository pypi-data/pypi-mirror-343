from python.cloud_storage.cloud_storage_agent import CloudStorageAgent

class GCPCloudStorageAgent(CloudStorageAgent):
    def __init__(self, storage_client, bucket_name: str):
        """
        Initialize the GCP cloud storage agent with the user's `storage_client` and `bucket_name`.
        
        Args:
            storage_client (google.cloud.storage.Client): The GCP storage client passed by the user.
            bucket_name (str): The name of the GCP bucket.
        """
        self.storage_client = storage_client
        self.bucket = self.storage_client.bucket(bucket_name)

    def upload(self, data: str, path: str):
        """
        Upload data to Google Cloud Storage using the provided storage_client.
        
        Args:
            data (str): The content to upload.
            path (str): The GCP path (gs://bucket_name/file).
        """
        blob = self.bucket.blob(path)
        blob.upload_from_string(data)
