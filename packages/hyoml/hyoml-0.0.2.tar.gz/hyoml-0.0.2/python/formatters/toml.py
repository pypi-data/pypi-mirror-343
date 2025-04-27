"""
TOML formatter for Hyoml framework.

Supports:
- Flattening Hyoml structures to TOML-style key=value
- Optional restoration of Python tuples from {"@type": "tuple", "values": [...]}
- Validation of TOML-compatible structures
"""

from python.formatters.base import BaseFormatter
from utils.formatter_utils import clean_output


class TOML(BaseFormatter):
    """
    Basic TOML formatter with section support and optional inline tables.
    """

    def __init__(self, options=None):
        """
        Initialize the formatter with optional configuration.

        Args:
            options (dict): Optional dictionary of config parameters
        """
        super().__init__(options)

    def format(self, data, restore_tuple=False, omit_keys=None, sectioned=True, **kwargs):
        """
        Format Hyoml-parsed data into TOML-style flat key=value lines.

        Args:
            data (Any): Parsed data structure
            restore_tuple (bool): If True, converts {"@type": "tuple"} to tuple()
            omit_keys (list): Keys to skip during serialization
            sectioned (bool): If True, adds TOML [sections] for nested objects
            **kwargs:
                quotes_required (bool): Quote all strings with double quotes

        Returns:
            str: TOML-formatted string
        """
        try:
            lines = []
            self.restore_tuple = restore_tuple
            enforce_quotes = kwargs.get("quotes_required", False)
            data = clean_output(data, omit_keys)
            flat = self._walk(data)

            def quote(v):
                return f'"{v}"' if enforce_quotes and isinstance(v, str) else v

            for k, v in flat.items():
                if isinstance(v, dict) and sectioned:
                    lines.append(f"[{k}]")
                    for sk, sv in v.items():
                        lines.append(f"{sk} = {quote(sv)}")
                else:
                    lines.append(f"{k} = {quote(v)}")

            return "\n".join(lines)
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[TOML.format] Failed to format: {e}")

    def validate(self, data):
        """
        Validate whether the structure can be flattened into TOML.

        Args:
            data (Any): Parsed Hyoml structure

        Returns:
            bool: True if valid, False otherwise
        """
        try:
            return isinstance(data, (dict, list))
        except Exception:
            return False
            return False

    def _walk(self, value, prefix=""):
        """
        Recursively flatten structure to dot-separated keys.

        Args:
            value (Any): Current node
            prefix (str): Key path prefix

        Returns:
            dict: Flattened structure
        """
        try:
            value = self._restore_tuple(value) if self.restore_tuple else value
            result = {}

            if isinstance(value, dict):
                for k, v in value.items():
                    new_prefix = f"{prefix}.{k}" if prefix else k
                    result.update(self._walk(v, new_prefix))
            elif isinstance(value, (list, tuple)):
                for i, item in enumerate(value):
                    result.update(self._walk(item, f"{prefix}[{i}]"))
            else:
                result[prefix] = value

            return result
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[TOML._walk] Flattening failed at '{prefix}': {e}")
