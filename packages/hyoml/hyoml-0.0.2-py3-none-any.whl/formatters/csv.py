"""
CSV formatter for Hyoml framework.

Supports:
- Flat dictionary serialization to CSV format
- Optional header row
- Optional field quoting
- Tuple restoration using shared _walk logic
"""

from python.formatters.base import BaseFormatter
from utils.formatter_utils import clean_output


class CSV(BaseFormatter):
    """
    Converts dictionary data into CSV row format with optional headers and quoting.
    """

    def __init__(self, options=None):
        """
        Initialize the formatter.

        Args:
            options (dict): Optional config (e.g., separator, quote_all, restore_tuple)
        """
        super().__init__(options)

    def format(self, data, omit_keys=None, headers=True, separator=',',
               quote_all=False, flatten_nested=True, restore_tuple=False, **kwargs):
        """
        Format dictionary data into a CSV-formatted string.

        Args:
            data (dict): Input dictionary
            omit_keys (list): Keys to exclude
            headers (bool): Whether to include a header row
            separator (str): Delimiter to use (default: comma)
            quote_all (bool): Quote all fields with double quotes
            flatten_nested (bool): Reserved for future use
            restore_tuple (bool): If True, converts {"@type": "tuple"} to tuple()
            **kwargs: Additional formatting parameters (e.g. quotes_required)

        Returns:
            str: CSV-formatted string
        """
        try:
            self.restore_tuple = restore_tuple
            quote_all = kwargs.get("quotes_required", quote_all)

            data = clean_output(data, omit_keys)
            keys = list(data.keys())

            quote = lambda x: f'"{x}"' if quote_all else x
            output = []

            if headers:
                output.append(separator.join(keys))

            row = [quote(str(self._walk(data[k]))) for k in keys]
            output.append(separator.join(row))

            return "\n".join(output)

        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[CSV.format] Failed to format: {e}")

    def validate(self, data):
        """
        Check if the input is a dictionary.

        Args:
            data (Any): Parsed data

        Returns:
            bool: True if valid dictionary, False otherwise
        """
        return isinstance(data, dict)

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
            raise ValueError(f"[CSV._walk] Failed to process value: {e}")
