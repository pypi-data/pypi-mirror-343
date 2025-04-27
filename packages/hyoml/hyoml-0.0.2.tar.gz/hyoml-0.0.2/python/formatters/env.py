"""
ENV formatter for Hyoml framework.

Supports:
- Environment-style export strings (e.g. VAR="value")
- Optional export keyword
- Optional strict mode (omit nested values)
- Tuple restoration via formatter base
"""

from python.formatters.base import BaseFormatter
from utils.formatter_utils import clean_output


class ENV(BaseFormatter):
    """
    .env-style key=value formatter for environment variable files.
    """

    def __init__(self, options=None):
        """
        Initialize the formatter.

        Args:
            options (dict): Optional dictionary of config parameters
        """
        super().__init__(options)

    def format(self, data, omit_keys=None, export=True, prefix='', strict=False,
               restore_tuple=False, **kwargs):
        """
        Format data into environment variable lines.

        Args:
            data (dict): Parsed data structure
            omit_keys (list): Keys to exclude
            export (bool): Include 'export' prefix
            prefix (str): Optional string before each variable name
            strict (bool): Skip lists/dicts if strict is enabled
            restore_tuple (bool): If True, restores {"@type": "tuple"} → tuple
            **kwargs: Additional options (e.g. quotes_required)

        Returns:
            str: .env file formatted content
        """
        try:
            self.restore_tuple = restore_tuple
            enforce_quotes = kwargs.get("quotes_required", True)

            data = clean_output(data, omit_keys)
            lines = []

            for k, v in data.items():
                v = self._walk(v)
                if isinstance(v, (dict, list, tuple)) and strict:
                    continue
                value = f'"{v}"' if enforce_quotes else v
                line = f"{prefix}{k}={value}"
                if export:
                    line = f"export {line}"
                lines.append(line)

            return "\n".join(lines)

        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[ENV.format] Failed to format: {e}")

    def validate(self, data):
        """
        Ensure all keys/values can be converted to env-style strings.

        Args:
            data (dict): Parsed data

        Returns:
            bool: True if valid
        """
        try:
            return all(isinstance(k, str) and isinstance(v, (str, int, float, bool, type(None)))
                       for k, v in data.items())
        except Exception:
            return False
            return False

    def _walk(self, value):
        """
        Preprocess values (e.g., restore tuple types) before output.

        Args:
            value (Any): Field value

        Returns:
            Any: Transformed field value
        """
        try:
            return self._restore_tuple(value) if self.restore_tuple else value
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[ENV._walk] Failed to process value: {e}")
