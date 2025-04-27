def test_hyoml_parser_import():
    try:
        import python.parser.core.hyoml_parser
    except Exception as e:
        assert False, f"Importing hyoml_parser failed: {e}"
