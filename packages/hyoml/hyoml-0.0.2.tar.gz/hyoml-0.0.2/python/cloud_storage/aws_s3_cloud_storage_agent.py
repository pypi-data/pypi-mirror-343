from python.cloud_storage.cloud_storage_agent import CloudStorageAgent

class S3CloudStorageAgent(CloudStorageAgent):
    def __init__(self, s3_client, bucket_name: str):
        """
        Initialize the S3 cloud storage agent with the user's `s3_client` and `bucket_name`.
        
        Args:
            s3_client (boto3.client): The boto3 S3 client passed by the user.
            bucket_name (str): The name of the S3 bucket.
        """
        self.s3_client = s3_client
        self.bucket_name = bucket_name

    def upload(self, data: str, path: str):
        """
        Upload data to AWS S3 using the provided s3_client.
        
        Args:
            data (str): The content to upload.
            path (str): The S3 path (bucket_name/file).
        """
        self.s3_client.put_object(Body=data, Bucket=self.bucket_name, Key=path)
