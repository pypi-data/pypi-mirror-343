"""
Markdown formatter for Hyoml framework.

Supports:
- Converts flat key-value pairs into Markdown table
- Optional headers and alignment
- Tuple restoration support
"""

from python.formatters.base import BaseFormatter
from utils.formatter_utils import clean_output


class Markdown(BaseFormatter):
    """
    Markdown table formatter from flat key-value structure.
    """

    def __init__(self, options=None):
        """
        Initialize the formatter.

        Args:
            options (dict): Optional config
        """
        super().__init__(options)

    def format(self, data, omit_keys=None, headers=True, align="left",
               flatten=True, restore_tuple=False, **kwargs):
        """
        Format data into a Markdown table.

        Args:
            data (dict): Parsed flat dictionary
            omit_keys (list): Keys to skip
            headers (bool): Include header row
            align (str): Column alignment ("left", "center", "right")
            flatten (bool): Reserved for future expansion
            restore_tuple (bool): Restore {"@type": "tuple"} → tuple
            **kwargs: Additional options

        Returns:
            str: Markdown-formatted string
        """
        try:
            self.restore_tuple = restore_tuple
            data = clean_output(data, omit_keys)
            keys = list(data.keys())
            rows = []

            if headers:
                rows.append("| " + " | ".join(keys) + " |")
                align_map = { "left": ":--", "center": ":-:", "right": "--:" }
                rows.append("|" + "|".join([align_map.get(align, ":--") for _ in keys]) + "|")

            values = [str(self._walk(data[k])) for k in keys]
            rows.append("| " + " | ".join(values) + " |")

            return "\n".join(rows)

        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[Markdown.format] Failed to format: {e}")

    def validate(self, data):
        """
        Validate that the structure is a dictionary.

        Args:
            data (Any): Parsed structure

        Returns:
            bool: True if valid dictionary
        """
        return isinstance(data, dict)

    def _walk(self, value):
        """
        Restore special structures like tuples before output.

        Args:
            value (Any): Field value

        Returns:
            Any: Transformed output
        """
        try:
            return self._restore_tuple(value) if self.restore_tuple else value
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[Markdown._walk] Failed to process value: {e}")
