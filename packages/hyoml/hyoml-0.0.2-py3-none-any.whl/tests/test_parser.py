import unittest
from python.parser.core.hyoml_parser import HyomlParser

class TestHyomlParser(unittest.TestCase):
    """
    Unit tests for the HyomlParser.
    """

    def setUp(self):
        self.parser = HyomlParser()

    def test_parse_valid_json(self):
        data = '{name: Ahmed, age: 30}'
        result = self.parser.parse(data)
        self.assertEqual(result.get('name'), 'Ahmed')
        self.assertEqual(result.get('age'), 30)

    def test_parse_valid_yaml(self):
        data = 'name: Ahmed\nage: 30'
        result = self.parser.parse(data)
        self.assertIn('name', result)
        self.assertIn('age', result)

    def test_parse_invalid_input(self):
        with self.assertRaises(ValueError):
            self.parser.parse('{name: "Ahmed"')  # missing closing brace

if __name__ == "__main__":
    unittest.main()
