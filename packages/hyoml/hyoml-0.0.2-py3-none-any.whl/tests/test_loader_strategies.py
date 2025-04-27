def test_loader_strategies_imports():
    try:
        import python.loader.strategies.azure_loader
        import python.loader.strategies.data_url_loader
        import python.loader.strategies.file_path_loader
        import python.loader.strategies.gcs_loader
        import python.loader.strategies.http_loader
        import python.loader.strategies.s3_loader
    except Exception as e:
        assert False, f"Importing loader strategies failed: {e}"
