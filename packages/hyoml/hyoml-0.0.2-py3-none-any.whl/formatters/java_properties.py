"""
JavaProperties formatter for .properties output.
Inherits BaseFormatter and supports recursive data via _walk.
"""

from python.formatters.base import BaseFormatter
from utils.formatter_utils import clean_output

class JavaProperties(BaseFormatter):
    """
    Converts dictionary data into Java-style .properties key-value format.
    Nested structures are flattened using dotted keys.
    Tuple restoration is supported.
    """

    def __init__(self, **kwargs):
        """
        Initialize the formatter.

        Args:
            kwargs (dict): Optional config (e.g., restore_tuple)
        """
        super().__init__(kwargs)

    def format(self, data, omit_keys=None, flatten_nested=True, restore_tuple=None,
               separator='=', escape_unicode=False, sort_keys=False, **kwargs):
        """
        Format dictionary data into .properties format.

        Args:
            data (dict): Input dictionary
            omit_keys (list): Keys to exclude
            flatten_nested (bool): Flatten nested keys (default: True)
            restore_tuple (bool): Restore tuple values if True (overrides global)
            separator (str): Character to use between key and value (default '=')
            escape_unicode (bool): Escape non-ASCII characters
            sort_keys (bool): Sort keys alphabetically
            **kwargs: Additional formatting options

        Returns:
            str: Formatted .properties string
        """
        try:
            if restore_tuple is not None:
                self.restore_tuple = restore_tuple
            data = clean_output(data, omit_keys)
            flat = self._walk(data)
            items = flat.items()
            if sort_keys:
                items = sorted(items)

            def escape(val):
                if escape_unicode:
                    return val.encode('unicode_escape').decode('utf-8')
                return val

            lines = [f"{k}{separator}{escape(str(v))}" for k, v in items if not omit_keys or k not in omit_keys]
            return "\n".join(lines)
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[JavaProperties.format] Failed to format: {e}")

    def validate(self, data):
        """
        Check if the input is a dictionary.

        Args:
            data (Any): Parsed data

        Returns:
            bool: True if valid dictionary, False otherwise
        """
        return isinstance(data, dict)

    def _walk(self, value, prefix=""):
        """
        Flatten nested dicts and lists into dotted keys.

        Args:
            value (Any): Input value
            prefix (str): Key prefix for recursion

        Returns:
            dict: Flattened key-value structure
        """
        flat = {}
        try:
            if isinstance(value, dict):
                for k, v in value.items():
                    full_key = f"{prefix}.{k}" if prefix else k
                    flat.update(self._walk(v, full_key))
            elif isinstance(value, list):
                for idx, v in enumerate(value):
                    full_key = f"{prefix}[{idx}]"
                    flat.update(self._walk(v, full_key))
            else:
                flat[prefix] = self._restore_tuple(value) if self.restore_tuple else value
            return flat
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[JavaProperties._walk] Failed to walk data: {e}")
