"""
SQL formatter for Hyoml framework.

Supports:
- Dict or list of dicts as input
- Custom table name
- Tuple restoration
- Optional field quoting and NULL handling
- BaseFormatter integration
"""

from python.formatters.base import BaseFormatter
from utils.formatter_utils import clean_output

class SQL(BaseFormatter):
    """
    Converts data into SQL INSERT statements.
    Supports quoting, NULL replacement, and tuple restoration.
    """

    def __init__(self, **kwargs):
        """
        Initialize the formatter.

        Args:
            kwargs (dict): Optional config (e.g., restore_tuple, table)
        """
        super().__init__(kwargs)

    def format(self, data, omit_keys=None, table="my_table",
               quote_fields=True, null_as="NULL", restore_tuple=None,
               sort_keys=False, **kwargs):
        """
        Format dictionary data into SQL INSERT statements.

        Args:
            data (dict or list): Input data (single or list of records)
            omit_keys (list): Keys to exclude from output
            table (str): Target SQL table name
            quote_fields (bool): Whether to quote all values
            null_as (str): Value to use for null/None fields
            restore_tuple (bool): If True, restore tuple values
            sort_keys (bool): Sort keys alphabetically
            **kwargs: Additional options

        Returns:
            str: SQL insert statements
        """
        try:
            if restore_tuple is not None:
                self.restore_tuple = restore_tuple

            if isinstance(data, dict):
                data = [data]
            if not isinstance(data, list):
                raise TypeError("SQL formatter expects a dict or list of dicts")

            rows = []
            for record in data:
                clean = clean_output(record, omit_keys)
                flat = self._walk(clean)
                keys = sorted(flat.keys()) if sort_keys else list(flat.keys())

                def sql_quote(v):
                    if v is None:
                        return null_as
                    v = str(v)
                    return "'{}'".format(v.replace("'", "''")) if quote_fields else v

                cols = ", ".join(keys)
                vals = ", ".join(sql_quote(flat[k]) for k in keys)
                rows.append(f"INSERT INTO {table} ({cols}) VALUES ({vals});")

            return "\n".join(rows)
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[SQL.format] Failed to format: {e}")

    def validate(self, data):
        """
        Check if input is a dict or list of dicts.

        Args:
            data (Any): Input data

        Returns:
            bool: True if valid
        """
        return isinstance(data, (dict, list))

    def _walk(self, value):
        """
        Preprocess values (e.g., restore tuple types).

        Args:
            value (Any): Input

        Returns:
            dict: Processed data
        """
        try:
            return {
                k: self._restore_tuple(v) if self.restore_tuple else v
                for k, v in value.items()
            } if isinstance(value, dict) else value
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[SQL._walk] Failed to walk data: {e}")
