import unittest
from utils.validator import (
    isValidJSON,
    isValidYAML,
    isValidINI,
    isValidXML,
    isValidHTML
)

class TestValidators(unittest.TestCase):
    """
    Tests for data format validators.
    """

    def test_valid_json(self):
        data = {"name": "Ahmed", "age": 30}
        self.assertTrue(isValidJSON(data))

    def test_invalid_json(self):
        self.assertFalse(isValidJSON("not a dict"))

    def test_valid_yaml(self):
        yaml_str = "name: Ahmed\nage: 30"
        self.assertTrue(isValidYAML(yaml_str))

    def test_invalid_yaml(self):
        self.assertFalse(isValidYAML("{invalid: yaml: format}"))

    def test_valid_ini(self):
        ini_data = {"section": {"key": "value"}}
        self.assertTrue(isValidINI(ini_data))

    def test_valid_xml(self):
        xml_data = {"user": "Ahmed"}
        self.assertTrue(isValidXML(xml_data))

    def test_valid_html(self):
        html_data = {"title": "Test"}
        self.assertTrue(isValidHTML(html_data))

if __name__ == "__main__":
    unittest.main()
