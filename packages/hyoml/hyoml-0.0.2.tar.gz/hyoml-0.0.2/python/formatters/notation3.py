"""
Notation3 (N3) formatter for Hyoml framework.

Supports:
- N3 RDF serialization
- Tuple restoration
- Subject-predicate-object syntax
"""

from python.formatters.base import BaseFormatter
from utils.formatter_utils import clean_output

class Notation3(BaseFormatter):
    """
    Converts dictionary data into Notation3 (N3) format.
    """

    def __init__(self, **kwargs):
        """
        Initialize formatter.

        Args:
            kwargs (dict): Settings
        """
        super().__init__(kwargs)

    def format(self, data, omit_keys=None, restore_tuple=None,
               base_uri="http://example.org/", prefix="ex", sort_keys=False,
               **kwargs):
        """
        Format dictionary into N3 RDF syntax.

        Args:
            data (dict): Input data
            omit_keys (list): Keys to omit
            restore_tuple (bool): Control tuple restoration
            base_uri (str): Base URI for prefixes
            prefix (str): Prefix label
            sort_keys (bool): Sort triples
            **kwargs: Extra options

        Returns:
            str: N3-formatted string
        """
        try:
            if restore_tuple is not None:
                self.restore_tuple = restore_tuple

            data = clean_output(data, omit_keys)
            flat = self._walk(data)

            lines = [f"@prefix {prefix}: <{base_uri}> .\n"]
            items = sorted(flat.items()) if sort_keys else flat.items()

            for subj, pred_obj in items:
                lines.append(f"{prefix}:{subj} {{")
                if isinstance(pred_obj, dict):
                    for pred, obj in pred_obj.items():
                        lines.append(f"  {prefix}:{pred} \"{obj}\" .")
                else:
                    lines.append(f"  {prefix}:value \"{pred_obj}\" .")
                lines.append("}")

            return "\n".join(lines)
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[Notation3.format] Failed to format: {e}")

    def validate(self, data):
        """
        Validate input.

        Args:
            data (Any): Input

        Returns:
            bool: True if dictionary
        """
        return isinstance(data, dict)

    def _walk(self, value):
        """
        Recursively restore tuples if needed.

        Args:
            value (Any): Node

        Returns:
            Any: Processed node
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
            raise ValueError(f"[Notation3._walk] Failed to walk data: {e}")