import unittest
import subprocess
import os

class TestCLI(unittest.TestCase):
    """
    Tests for the Hyoml command-line interface.
    """

    def setUp(self):
        self.sample_input = "name: Ahmed\nage: 30"
        self.input_file = "test_input.hyoml"
        self.output_file = "test_output.json"
        with open(self.input_file, "w") as f:
            f.write(self.sample_input)

    def tearDown(self):
        if os.path.exists(self.input_file):
            os.remove(self.input_file)
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def test_cli_parse_and_format(self):
        result = subprocess.run(
            ["python", "python/interface/cli.py", "parse", self.input_file, "--format", "json", "--output", self.output_file],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertTrue(os.path.exists(self.output_file))

    def test_cli_missing_argument(self):
        result = subprocess.run(
            ["python", "python/interface/cli.py", "parse"],
            capture_output=True,
            text=True
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("error", result.stderr.lower())

if __name__ == "__main__":
    unittest.main()
