import unittest
from utils.formatter_utils import clean_output
from utils.file_utils import load_file, save_file
import os

class TestUtils(unittest.TestCase):
    """
    Tests for Hyoml utility functions.
    """

    def setUp(self):
        self.test_data = {
            "name": "Ahmed",
            "temp": "remove_this",
            "nested": {"keep": True, "temp": "delete_me"}
        }
        self.omit_keys = ["temp"]
        self.file_path = "temp_test_file.txt"
        self.content = "test content"

    def tearDown(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_clean_output(self):
        cleaned = clean_output(self.test_data, omit_keys=self.omit_keys)
        self.assertNotIn("temp", cleaned)
        self.assertNotIn("temp", cleaned["nested"])
        self.assertIn("name", cleaned)

    def test_file_save_and_load(self):
        save_file(self.file_path, self.content)
        loaded = load_file(self.file_path)
        self.assertEqual(self.content, loaded)

if __name__ == "__main__":
    unittest.main()
