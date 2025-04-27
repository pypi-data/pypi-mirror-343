"""
HTML formatter for Hyoml framework.

Supports:
- Converts dictionaries to styled HTML table output
- Optional document title, theme, and interactivity
- Tuple restoration via base formatter
"""

from python.formatters.base import BaseFormatter
from utils.formatter_utils import clean_output


class HTML(BaseFormatter):
    """
    Generates an HTML table view of key-value data.
    """

    def __init__(self, options=None):
        """
        Initialize the formatter.

        Args:
            options (dict): Optional configuration dictionary
        """
        super().__init__(options)

    def format(self, data, omit_keys=None, theme='light', interactive=True,
               title='Hyoml Output', restore_tuple=False, **kwargs):
        """
        Format data into a simple HTML table structure.

        Args:
            data (dict): Parsed Hyoml structure
            omit_keys (list): Keys to exclude
            theme (str): Light or dark theme class (unused)
            interactive (bool): Reserved for future (e.g. toggle, copy)
            title (str): HTML document title
            restore_tuple (bool): Restore {"@type": "tuple"} to Python tuple
            **kwargs: Reserved

        Returns:
            str: HTML table string
        """
        try:
            self.restore_tuple = restore_tuple
            data = clean_output(data, omit_keys)

            html = [f"<html><head><title>{title}</title></head><body>"]
            html.append(f"<h2>{title}</h2>")
            html.append("<table border='1'>")

            for k, v in data.items():
                val = self._walk(v)
                html.append(f"<tr><td><b>{k}</b></td><td>{val}</td></tr>")

            html.append("</table></body></html>")
            return "\n".join(html)

        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[HTML.format] Failed to format: {e}")

    def validate(self, data):
        """
        Validate the input is a dictionary.

        Args:
            data (Any): Parsed Hyoml object

        Returns:
            bool: True if dict
        """
        return isinstance(data, dict)

    def _walk(self, value):
        """
        Process a single value, restoring special structures if needed.

        Args:
            value (Any): A field value

        Returns:
            Any: Transformed output
        """
        try:
            return self._restore_tuple(value) if self.restore_tuple else value
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[HTML._walk] Failed to process value: {e}")
