"""
YAML formatter for Hyoml framework.

Supports:
- YAML-like string serialization
- Optional restoration of Python tuples from {"@type": "tuple", "values": [...]}
- Validation of key-value structures
"""

from python.formatters.base import BaseFormatter
from utils.formatter_utils import clean_output


class YAML(BaseFormatter):
    """YAML-like formatter with indentation, tuple restoration, and value quoting options."""

    def __init__(self, options=None):
        """
        Initialize the formatter with optional configuration.

        Args:
            options (dict): Optional dictionary of config parameters
        """
        super().__init__(options)

    def format(self, data, omit_keys=None, indent=2, restore_tuple=False, key_order=None, **kwargs):
        """
        Format Hyoml-parsed data into a YAML-style string.

        Args:
            data (Any): Parsed data structure
            omit_keys (list): List of keys to exclude from output
            indent (int): Number of spaces for indentation (default=2)
            restore_tuple (bool): If True, converts {"@type": "tuple"} to tuple()
            key_order (list): Optional key sort order
            **kwargs:
                quotes_required (bool): If True, force double quotes for string values

        Returns:
            str: YAML-like formatted string
        """
        try:
            self.restore_tuple = restore_tuple
            enforce_quotes = kwargs.get("quotes_required", False)
            pad = ' ' * indent
            lines = []
            data = clean_output(data, omit_keys)
            keys = key_order if key_order else data.keys()

            def quote(v):
                return f'"{v}"' if enforce_quotes and isinstance(v, str) else v

            for k in keys:
                v = data[k]
                if isinstance(v, dict):
                    lines.append(f"{k}:")
                    for sk, sv in v.items():
                        lines.append(f"{pad}{sk}: {quote(sv)}")
                else:
                    lines.append(f"{k}: {quote(v)}")

            return self._walk("\n".join(lines))
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[YAML.format] Failed to format: {e}")

    def validate(self, data):
        """
        Validate whether the structure can be serialized as YAML.

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

    def _walk(self, value, indent=0):
        """
        Recursively convert structure to YAML-like format.

        Args:
            value (Any): Current node
            indent (int): Current indentation level

        Returns:
            str: YAML representation
        """
        try:
            value = self._restore_tuple(value) if self.restore_tuple else value
            pad = "  " * indent

            if isinstance(value, dict):
                output = ""
                for k, v in value.items():
                    if isinstance(v, (dict, list)):
                        output += f"{pad}{k}:\n{self._walk(v, indent + 1)}"
                    else:
                        output += f"{pad}{k}: {v}\n"
                return output
            elif isinstance(value, list) or isinstance(value, tuple):
                return ''.join(f"{pad}- {self._walk(v, indent + 1).strip()}\n" for v in value)
            else:
                return f"{pad}{value}\n"
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[YAML._walk] Failed at indent={indent}: {e}")
