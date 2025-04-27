import unittest
from python.parser.core.middleware.autofixer import AutoFixer

class TestAutoFixer(unittest.TestCase):
    """
    Tests for the Hyoml AutoFixer component.
    """

    def setUp(self):
        self.fixer = AutoFixer()

    def test_fix_missing_comma(self):
        broken_json = '{name: "Ahmed" age: 30}'  # missing comma
        fixed = self.fixer.fix(broken_json)
        self.assertIn("name", fixed)
        self.assertIn("age", fixed)

    def test_fix_unquoted_keys(self):
        broken_json = '{name: Ahmed, age: 30}'
        fixed = self.fixer.fix(broken_json)
        self.assertIn("name", fixed)

    def test_pass_through_valid_input(self):
        valid = '{"name": "Ahmed", "age": 30}'
        fixed = self.fixer.fix(valid)
        self.assertEqual(fixed, valid)

    def test_handle_empty_string(self):
        with self.assertRaises(ValueError):
            self.fixer.fix("")

if __name__ == "__main__":
    unittest.main()
