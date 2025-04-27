"""
JSONLD formatter for Hyoml framework.

Supports:
- Adding @context for JSON-LD serialization
- Tuple restoration
- Flexible context injection
"""

import json
from python.formatters.base import BaseFormatter
from utils.formatter_utils import clean_output

class JSONLD(BaseFormatter):
    """
    Converts dictionary data into JSON-LD format.
    Adds standard or custom @context.
    """

    def __init__(self, **kwargs):
        """
        Initialize formatter.

        Args:
            kwargs (dict): Formatter settings
        """
        super().__init__(kwargs)

    def format(self, data, omit_keys=None, restore_tuple=None,
               context="http://schema.org", indent=2,
               compact=True, **kwargs):
        """
        Convert input to JSON-LD string.

        Args:
            data (dict): Input dictionary
            omit_keys (list): Keys to exclude
            restore_tuple (bool): Tuple restoration toggle
            context (str or dict): @context value
            indent (int): JSON indentation
            compact (bool): If False, outputs expanded JSON-LD
            **kwargs: Extra JSON serialization args

        Returns:
            str: JSON-LD string
        """
        try:
            if restore_tuple is not None:
                self.restore_tuple = restore_tuple

            obj = clean_output(data, omit_keys)
            obj = self._walk(obj)

            if "@context" not in obj:
                obj = {"@context": context, **obj}

            if not compact:
                return json.dumps(obj, indent=indent, separators=(",", ": "), **kwargs)
            return json.dumps(obj, indent=indent, **kwargs)
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[JSONLD.format] Failed to format: {e}")

    def validate(self, data):
        """
        Validate if input is dictionary.

        Args:
            data (Any): Input

        Returns:
            bool: True if dict
        """
        return isinstance(data, dict)

    def _walk(self, value):
        """
        Apply tuple restoration recursively.

        Args:
            value (Any): Node

        Returns:
            Any: Processed output
        """
        try:
            if isinstance(value, dict):
                return {k: self._walk(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [self._walk(v) for v in value]
            else:
                return self._restore_tuple(value) if self.restore_tuple else value
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[JSONLD._walk] Failed to walk data: {e}")