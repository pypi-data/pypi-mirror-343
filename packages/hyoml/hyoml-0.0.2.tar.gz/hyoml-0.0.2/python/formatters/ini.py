"""
INI formatter for Hyoml framework.

Supports:
- Basic INI-style key=value output
- Optional value quoting
- Tuple restoration from encoded forms
"""

from python.formatters.base import BaseFormatter
from utils.formatter_utils import clean_output


class INI(BaseFormatter):
    """
    Basic INI file formatter with optional value quoting and tuple restoration.
    """

    def __init__(self, options=None):
        """
        Initialize the formatter.

        Args:
            options (dict): Optional configuration
        """
        super().__init__(options)

    def format(self, data, omit_keys=None, restore_tuple=False, **kwargs):
        """
        Format data as INI-style key=value entries.

        Args:
            data (dict): Parsed key-value data
            omit_keys (list): Keys to omit from output
            restore_tuple (bool): If True, restores {"@type": "tuple"} → tuple
            **kwargs:
                quotes_required (bool): If True, wrap all strings in double quotes

        Returns:
            str: INI-formatted string
        """
        try:
            self.restore_tuple = restore_tuple
            enforce_quotes = kwargs.get("quotes_required", False)

            def quote(v):
                return f'"{v}"' if enforce_quotes and isinstance(v, str) else v

            data = clean_output(data, omit_keys)
            return "\n".join(f"{k} = {quote(self._walk(v))}" for k, v in data.items())

        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[INI.format] Failed to format: {e}")

    def validate(self, data):
        """
        Validate that the data is a dictionary.

        Args:
            data (Any): Parsed structure

        Returns:
            bool: True if valid
        """
        return isinstance(data, dict)

    def _walk(self, value):
        """
        Restore tuple or return original value.

        Args:
            value (Any): Raw value

        Returns:
            Any: Cleaned value
        """
        try:
            return self._restore_tuple(value) if self.restore_tuple else value
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[INI._walk] Failed to process value: {e}")
