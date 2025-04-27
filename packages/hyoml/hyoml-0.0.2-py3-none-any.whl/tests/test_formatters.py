import unittest
from python.formatters.json_formatter import format as format_json
from python.formatters.yml_formatter import format as format_yml
from python.formatters.toml_formatter import format as format_toml
from python.formatters.xml_formatter import format as format_xml

class TestFormatters(unittest.TestCase):
    """
    Unit tests for various Hyoml formatters.
    """

    def setUp(self):
        self.sample_data = {
            "name": "Ahmed",
            "age": 30,
            "active": True
        }

    def test_json_formatter(self):
        output = format_json(self.sample_data, indent=2)
        self.assertIn('"name": "Ahmed"', output)
        self.assertIn('"age": 30', output)

    def test_yaml_formatter(self):
        output = format_yml(self.sample_data)
        self.assertIn('name: Ahmed', output)

    def test_toml_formatter(self):
        output = format_toml(self.sample_data)
        self.assertIn('name = "Ahmed"', output)

    def test_xml_formatter(self):
        output = format_xml(self.sample_data)
        self.assertIn('<name>Ahmed</name>', output)

if __name__ == "__main__":
    unittest.main()
