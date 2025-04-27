"""
JSON formatter for Hyoml framework.

Supports:
- Standard JSON serialization
- Optional restoration of Python tuples from {"@type": "tuple", "values": [...]}
- Validation of JSON-serializable structures
"""

import json
from python.formatters.base import BaseFormatter
from utils.formatter_utils import clean_output


class JSON(BaseFormatter):
    """
    JSON formatter with support for options like indent, quoting, tuple restoration,
    and strict mode enforcement.
    """

    def __init__(self, options=None):
        """
        Initialize the formatter with optional configuration.

        Args:
            options (dict): Formatter options, e.g., restore_tuple, quotes_required, etc.
        """
        super().__init__(options)

    def format(self, data, restore_tuple=False, **kwargs):
        """
        Format Hyoml-parsed data into a JSON string.

        Args:
            data (Any): Parsed data structure
            restore_tuple (bool): If True, converts {"@type": "tuple"} to tuple()
            **kwargs:
                space (int): Indentation level (default=2)
                ensure_ascii (bool): Escape non-ASCII (default=False)
                sort_keys (bool): Alphabetically sort keys (default=False)
                replacer (function or list): Modify or filter keys/values
                quotes_required (bool): Enforce double quotes for all strings
                omit_keys (list): Keys to omit from final output

        Returns:
            str: JSON-formatted string
        """
        try:
            self.restore_tuple = restore_tuple
            indent = kwargs.get("space", 2)
            ensure_ascii = kwargs.get("ensure_ascii", False)
            sort_keys = kwargs.get("sort_keys", False)
            replacer = kwargs.get("replacer", None)
            enforce_quotes = kwargs.get("quotes_required", False)

            # Apply replacer if specified
            if callable(replacer):
                data = {k: replacer(k, v) for k, v in data.items()}
            elif isinstance(replacer, list):
                data = {k: v for k, v in data.items() if k in replacer}

            # Omit keys if specified
            data = clean_output(data, kwargs.get("omit_keys"))

            # Define fallback serializer
            def default_serializer(o):
                return str(o)

            output = json.dumps(
                self._walk(data),
                indent=indent,
                ensure_ascii=ensure_ascii,
                sort_keys=sort_keys,
                default=default_serializer
            )

            if enforce_quotes:
                output = output.replace(":", ": ").replace("'", '"')  # simple normalization

            return output
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[JSON.format] Failed to format: {e}")

    def validate(self, data):
        """
        Validate whether data can be serialized as JSON.

        Args:
            data (Any): Hyoml-parsed structure

        Returns:
            bool: True if serializable, False otherwise
        """
        try:
            json.dumps(data)
            return True
        except Exception:
            return False
            return False

    def _walk(self, value):
        """
        Recursively traverse structure and optionally restore tuples.

        Args:
            value (Any): Node in the structure

        Returns:
            Any: Transformed value
        """
        try:
            value = self._restore_tuple(value) if self.restore_tuple else value

            if isinstance(value, dict):
                return {k: self._walk(v) for k, v in value.items()}
            if isinstance(value, list):
                return [self._walk(v) for v in value]
            return value
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[JSON._walk] Failed to process node: {e}")
