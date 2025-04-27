def test_utils_imports():
    try:
        import python.utils.file_utils
        import python.utils.validator
    except Exception as e:
        assert False, f"Importing utils modules failed: {e}"
