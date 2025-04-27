"""
ShellScript formatter for Hyoml framework.

Supports:
- Conversion to export-based shell script
- Tuple restoration and formatting controls
- Flattening nested keys into SH-compatible names
"""

from python.formatters.base import BaseFormatter
from utils.formatter_utils import clean_output

class ShellScript(BaseFormatter):
    """
    Converts dictionary data into shell script with export statements.
    Suitable for .sh files and Unix environments.
    """

    def __init__(self, **kwargs):
        """
        Initialize the formatter.

        Args:
            kwargs (dict): Formatter configuration (e.g., restore_tuple)
        """
        super().__init__(kwargs)

    def format(self, data, omit_keys=None, restore_tuple=None,
               header=True, flatten_nested=True, uppercase_keys=False,
               prefix=None, sort_keys=False, **kwargs):
        """
        Format dictionary into export-based shell script.

        Args:
            data (dict): Input data
            omit_keys (list): Keys to exclude
            restore_tuple (bool): Override global restore_tuple flag
            header (bool): Include #!/bin/bash header
            flatten_nested (bool): Flatten nested keys (default True)
            uppercase_keys (bool): Convert keys to uppercase
            prefix (str): Optional prefix for env vars (e.g., APP_)
            sort_keys (bool): Alphabetical ordering
            **kwargs: Extra

        Returns:
            str: Shell-compatible script
        """
        try:
            if restore_tuple is not None:
                self.restore_tuple = restore_tuple
            data = clean_output(data, omit_keys)
            flat = self._walk(data)

            lines = ["#!/bin/bash"] if header else []
            items = sorted(flat.items()) if sort_keys else flat.items()

            for k, v in items:
                key = k.upper() if uppercase_keys else k
                if prefix:
                    key = f"{prefix}{key}"
                lines.append(f"export {key}='{v}'")

            return "\n".join(lines)
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[ShellScript.format] Failed to format: {e}")

    def validate(self, data):
        """
        Check if input is a dictionary.

        Args:
            data (Any): Input value

        Returns:
            bool: True if valid dict
        """
        return isinstance(data, dict)

    def _walk(self, value, prefix=""):
        """
        Flatten nested dicts and lists into shell-safe key names.

        Args:
            value (Any): Input
            prefix (str): Key prefix for recursion

        Returns:
            dict: Flattened output
        """
        flat = {}
        try:
            if isinstance(value, dict):
                for k, v in value.items():
                    full_key = f"{prefix}_{k}" if prefix else k
                    flat.update(self._walk(v, full_key))
            elif isinstance(value, list):
                for idx, v in enumerate(value):
                    full_key = f"{prefix}_{idx}" if prefix else str(idx)
                    flat.update(self._walk(v, full_key))
            else:
                flat[prefix] = self._restore_tuple(value) if self.restore_tuple else value
            return flat
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[ShellScript._walk] Failed to walk data: {e}")
