def test_hyoml_interface():
    try:
        from python.interface.hyoml import Hyoml
        h = Hyoml()
        assert h is not None
    except Exception as e:
        assert False, f"Hyoml interface basic test failed: {e}"
