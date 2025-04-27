"""
NTriples formatter for Hyoml framework.

Supports:
- Basic N-Triples RDF output
- Tuple restoration
- Subject-predicate-object serialization
"""

from python.formatters.base import BaseFormatter
from utils.formatter_utils import clean_output

class NTriples(BaseFormatter):
    """
    Converts dictionary data into N-Triples format.
    Each line represents a subject-predicate-object triple.
    """

    def __init__(self, **kwargs):
        """
        Initialize formatter.

        Args:
            kwargs (dict): Formatter settings
        """
        super().__init__(kwargs)

    def format(self, data, omit_keys=None, restore_tuple=None,
               base_uri="http://example.org/", sort_keys=False, **kwargs):
        """
        Format input as N-Triples.

        Args:
            data (dict): Input dictionary
            omit_keys (list): Keys to exclude
            restore_tuple (bool): Enable tuple restoration
            base_uri (str): Base URI for subjects
            sort_keys (bool): Sort triples alphabetically
            **kwargs: Extra options

        Returns:
            str: N-Triples formatted string
        """
        try:
            if restore_tuple is not None:
                self.restore_tuple = restore_tuple

            data = clean_output(data, omit_keys)
            flat = self._walk(data)

            lines = []
            items = sorted(flat.items()) if sort_keys else flat.items()

            for subj, pred_obj in items:
                subject_uri = f"<{base_uri}{subj}>"
                if isinstance(pred_obj, dict):
                    for pred, obj in pred_obj.items():
                        lines.append(f"{subject_uri} <{base_uri}{pred}> \"{obj}\" .")
                else:
                    lines.append(f"{subject_uri} <{base_uri}value> \"{pred_obj}\" .")

            return "\n".join(lines)
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[NTriples.format] Failed to format: {e}")

    def validate(self, data):
        """
        Validate input for N-Triples output.

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
            value (Any): Input node

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
            raise ValueError(f"[NTriples._walk] Failed to walk data: {e}")