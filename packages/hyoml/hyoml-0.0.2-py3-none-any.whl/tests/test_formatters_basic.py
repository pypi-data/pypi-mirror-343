def test_formatters_imports():
    try:
        import python.formatters.json
        import python.formatters.yaml
        import python.formatters.csv
        import python.formatters.xml
    except Exception as e:
        assert False, f"Importing formatters failed: {e}"
