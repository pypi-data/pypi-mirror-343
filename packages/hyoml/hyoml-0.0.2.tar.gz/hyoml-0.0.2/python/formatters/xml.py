"""
XML formatter for Hyoml framework.

Supports:
- Basic XML tag generation for key-value pairs
- String escaping for special XML characters
- Tuple restoration via base formatter
"""

from python.formatters.base import BaseFormatter
from utils.formatter_utils import clean_output


class XML(BaseFormatter):
    """
    Converts dictionary data into basic XML representation with optional tuple restoration.
    """

    def __init__(self, options=None):
        """
        Initialize the formatter.

        Args:
            options (dict): Optional configuration dictionary
        """
        super().__init__(options)

    def format(self, data, omit_keys=None, root='root', restore_tuple=False, **kwargs):
        """
        Format dictionary into a simple XML representation.

        Args:
            data (dict): Parsed Hyoml structure
            omit_keys (list): Keys to skip
            root (str): Root tag name
            restore_tuple (bool): If True, converts {"@type": "tuple"} → tuple
            **kwargs: Additional options

        Returns:
            str: XML-formatted string
        """
        try:
            self.restore_tuple = restore_tuple
            data = clean_output(data, omit_keys)

            def escape(s):
                return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

            xml = [f"<{root}>"]
            for k, v in data.items():
                v = self._walk(v)
                xml.append(f"  <{k}>{escape(v)}</{k}>")
            xml.append(f"</{root}>")

            return "\n".join(xml)

        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[XML.format] Failed to format: {e}")

    def validate(self, data):
        """
        Validate that the structure is a dictionary.

        Args:
            data (Any): Input data

        Returns:
            bool: True if valid
        """
        return isinstance(data, dict)

    def _walk(self, value):
        """
        Preprocess value, restoring special structures if needed.

        Args:
            value (Any): Field value

        Returns:
            Any: Transformed value
        """
        try:
            return self._restore_tuple(value) if self.restore_tuple else value
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[XML._walk] Failed to process value: {e}")
