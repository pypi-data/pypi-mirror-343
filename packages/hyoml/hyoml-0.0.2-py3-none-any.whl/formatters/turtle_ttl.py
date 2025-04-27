"""
TurtleTTL formatter for Hyoml framework.

Supports:
- Basic Turtle (TTL) RDF triples
- Tuple restoration
- Namespace control
"""

from python.formatters.base import BaseFormatter
from utils.formatter_utils import clean_output

class TurtleTTL(BaseFormatter):
    """
    Converts dictionary data into Turtle (TTL) RDF triple format.
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
        Format input as TTL triples.

        Args:
            data (dict): Input data
            omit_keys (list): Keys to exclude
            restore_tuple (bool): Control tuple restoration
            base_uri (str): Default namespace
            prefix (str): Prefix for compact URIs
            sort_keys (bool): Sort triples alphabetically
            **kwargs: Extra options

        Returns:
            str: Turtle TTL string
        """
        try:
            if restore_tuple is not None:
                self.restore_tuple = restore_tuple

            data = clean_output(data, omit_keys)
            flat = self._walk(data)

            lines = [f"@prefix {prefix}: <{base_uri}> .\n"]

            items = sorted(flat.items()) if sort_keys else flat.items()
            for subj, pred_obj in items:
                if isinstance(pred_obj, dict):
                    for pred, obj in pred_obj.items():
                        lines.append(f"{prefix}:{subj} {prefix}:{pred} \"{obj}\" .")
                else:
                    lines.append(f"{prefix}:{subj} {prefix}:value \"{pred_obj}\" .")

            return "\n".join(lines)
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[TurtleTTL.format] Failed to format: {e}")

    def validate(self, data):
        """
        Validate input.

        Args:
            data (Any): Input

        Returns:
            bool: True if dict
        """
        return isinstance(data, dict)

    def _walk(self, value):
        """
        Recursive tuple restoration.

        Args:
            value (Any): Node

        Returns:
            Any: Processed value
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
            raise ValueError(f"[TurtleTTL._walk] Failed to walk data: {e}")
