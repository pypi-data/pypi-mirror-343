def test_cloud_storage_imports():
    try:
        import python.cloud_storage.aws_s3_cloud_storage_agent
        import python.cloud_storage.azure_blob_storage_agent
        import python.cloud_storage.cloud_storage_agent
        import python.cloud_storage.gcp_cloud_storage_agent
    except Exception as e:
        assert False, f"Importing cloud storage agents failed: {e}"
