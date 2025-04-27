"""
StrictYML formatter for Hyoml framework.

Supports:
- Quoted string keys and values
- Indentation configuration
- Tuple restoration via base formatter
"""

from python.formatters.base import BaseFormatter
from utils.formatter_utils import clean_output


class StrictYML(BaseFormatter):
    """
    Enforces strict YAML-style formatting with quoted strings and spacing control.
    """

    def __init__(self, options=None):
        """
        Initialize the formatter.

        Args:
            options (dict): Optional config
        """
        super().__init__(options)

    def format(self, data, omit_keys=None, indent=2, enforce_quotes=True,
               restore_tuple=False, **kwargs):
        """
        Format the parsed Hyoml data as strict YML with enforced syntax.

        Args:
            data (dict): Parsed data
            omit_keys (list): Keys to exclude
            indent (int): Indentation width (default=2)
            enforce_quotes (bool): Quote all strings (default=True)
            restore_tuple (bool): If True, converts {"@type": "tuple"} → tuple
            **kwargs: Additional formatting options

        Returns:
            str: StrictYML-formatted output
        """
        try:
            self.restore_tuple = restore_tuple
            data = clean_output(data, omit_keys)
            pad = ' ' * indent
            lines = []

            def quote(v):
                return f'"{v}"' if enforce_quotes and isinstance(v, str) else v

            for k, v in data.items():
                v = self._walk(v)
                lines.append(f"{k}:{pad}{quote(v)}")

            return "\n".join(lines)

        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[StrictYML.format] Failed to format: {e}")

    def validate(self, data):
        """
        Validate input is a dictionary.

        Args:
            data (Any): Parsed structure

        Returns:
            bool: True if valid
        """
        return isinstance(data, dict)

    def _walk(self, value):
        """
        Recursively prepare values (restore tuple support).

        Args:
            value (Any): Node

        Returns:
            Any: Processed value
        """
        try:
            return self._restore_tuple(value) if self.restore_tuple else value
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[StrictYML._walk] Failed to process value: {e}")
