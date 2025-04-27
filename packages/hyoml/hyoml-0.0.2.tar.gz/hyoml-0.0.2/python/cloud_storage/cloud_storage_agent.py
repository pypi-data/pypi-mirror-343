class CloudStorageAgent:
    """
    Abstract class for cloud storage interaction.
    All cloud agents must implement the `upload()` method.
    """

    def upload(self, data: str, path: str):
        """
        Upload data to cloud storage.

        Args:
            data (str): The content to upload.
            path (str): The cloud path (bucket/container/file).

        Raises:
            NotImplementedError: If not implemented by the subclass.
        """
        raise NotImplementedError("Upload method must be implemented by subclass.")
