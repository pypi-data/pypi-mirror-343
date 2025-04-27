def test_cli_main_runs():
    try:
        import python.cli.main
    except Exception as e:
        assert False, f"Importing CLI main failed: {e}"
