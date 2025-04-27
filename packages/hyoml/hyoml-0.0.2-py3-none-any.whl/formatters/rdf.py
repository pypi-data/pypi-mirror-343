"""
RDF/XML formatter for Hyoml framework.

Supports:
- Minimal RDF serialization
- Tuple restoration
- Placeholder for real RDF triples
"""

from python.formatters.base import BaseFormatter
from utils.formatter_utils import clean_output

class RDF(BaseFormatter):
    """
    Converts dictionary data into minimal RDF/XML structure.
    (Placeholder version — triples assumed simple.)
    """

    def __init__(self, **kwargs):
        """
        Initialize formatter with options.

        Args:
            kwargs (dict): Formatter settings
        """
        super().__init__(kwargs)

    def format(self, data, omit_keys=None, restore_tuple=None,
               root_namespace="http://example.org/", rdf_prefix="rdf", **kwargs):
        """
        Format dictionary into RDF/XML.

        Args:
            data (dict): Input data
            omit_keys (list): Keys to exclude
            restore_tuple (bool): Tuple restoration toggle
            root_namespace (str): Namespace URI
            rdf_prefix (str): RDF prefix (default rdf)
            **kwargs: Extra options

        Returns:
            str: RDF/XML string
        """
        try:
            if restore_tuple is not None:
                self.restore_tuple = restore_tuple

            data = clean_output(data, omit_keys)
            flat = self._walk(data)

            lines = [
                '<?xml version="1.0"?>',
                f'<{rdf_prefix}:RDF xmlns:{rdf_prefix}="{root_namespace}">' 
            ]

            for subject, predicate_object in flat.items():
                lines.append(f"  <{rdf_prefix}:Description {rdf_prefix}:about=\"{subject}\">")
                if isinstance(predicate_object, dict):
                    for pred, obj in predicate_object.items():
                        lines.append(f"    <{pred}>{obj}</{pred}>")
                else:
                    lines.append(f"    <{rdf_prefix}:value>{predicate_object}</{rdf_prefix}:value>")
                lines.append(f"  </{rdf_prefix}:Description>")

            lines.append(f'</{rdf_prefix}:RDF>')
            return "\n".join(lines)
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[RDF.format] Failed to format: {e}")

    def validate(self, data):
        """
        Validate input for RDF serialization.

        Args:
            data (Any): Input

        Returns:
            bool: True if dict
        """
        return isinstance(data, dict)

    def _walk(self, value):
        """
        Restore tuples if present.

        Args:
            value (Any): Data node

        Returns:
            Any: Transformed node
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
            raise ValueError(f"[RDF._walk] Failed to walk data: {e}")
