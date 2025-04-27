"""
SPARQL formatter for Hyoml framework.

Supports:
- Simple SPARQL SELECT query generation
- Tuple restoration
- Configurable query clauses
"""

from python.formatters.base import BaseFormatter
from utils.formatter_utils import clean_output

class SPARQL(BaseFormatter):
    """
    Converts dictionary data into a SPARQL SELECT query.
    """

    def __init__(self, **kwargs):
        """
        Initialize formatter.

        Args:
            kwargs (dict): Settings
        """
        super().__init__(kwargs)

    def format(self, data, omit_keys=None, restore_tuple=None,
               query_type="SELECT", where_clause=None, prefix_map=None,
               sort_keys=False, **kwargs):
        """
        Generate SPARQL query from dictionary input.

        Args:
            data (dict): Input dictionary
            omit_keys (list): Keys to omit
            restore_tuple (bool): Tuple restoration toggle
            query_type (str): SPARQL query type (e.g., SELECT, ASK)
            where_clause (str): Custom WHERE clause body
            prefix_map (dict): Prefix declarations
            sort_keys (bool): Sort fields alphabetically
            **kwargs: Extra options

        Returns:
            str: SPARQL query string
        """
        try:
            if restore_tuple is not None:
                self.restore_tuple = restore_tuple

            lines = []

            if prefix_map:
                for prefix, uri in prefix_map.items():
                    lines.append(f"PREFIX {prefix}: <{uri}>")

            data = clean_output(data, omit_keys)
            fields = self._walk(data)
            vars = sorted(fields.keys()) if sort_keys else fields.keys()
            var_list = " ".join(f"?{v}" for v in vars)

            lines.append(f"{query_type} {var_list} WHERE {{")
            if where_clause:
                lines.append(where_clause)
            else:
                lines.append("  ?s ?p ?o .")
            lines.append("}")

            return "\n".join(lines)
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[SPARQL.format] Failed to format: {e}")

    def validate(self, data):
        """
        Validate input for SPARQL generation.

        Args:
            data (Any): Input

        Returns:
            bool: True if dictionary
        """
        return isinstance(data, dict)

    def _walk(self, value):
        """
        Apply tuple restoration recursively.

        Args:
            value (Any): Node

        Returns:
            Any: Processed data
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
            raise ValueError(f"[SPARQL._walk] Failed to walk data: {e}")
