"""
OWL (Web Ontology Language) formatter for Hyoml framework.

Supports:
- Basic OWL/RDF XML serialization
- Tuple restoration
- Configurable ontology URI
"""

from python.formatters.base import BaseFormatter
from utils.formatter_utils import clean_output

class OWL(BaseFormatter):
    """
    Converts dictionary data into OWL (RDF/XML) format.
    """

    def __init__(self, **kwargs):
        """
        Initialize formatter.

        Args:
            kwargs (dict): Settings
        """
        super().__init__(kwargs)

    def format(self, data, omit_keys=None, restore_tuple=None,
               ontology_uri="http://example.org/ontology#", 
               rdf_prefix="rdf", owl_prefix="owl", sort_keys=False,
               **kwargs):
        """
        Format input into OWL RDF/XML.

        Args:
            data (dict): Input data
            omit_keys (list): Keys to exclude
            restore_tuple (bool): Tuple restoration toggle
            ontology_uri (str): Ontology base URI
            rdf_prefix (str): RDF prefix
            owl_prefix (str): OWL prefix
            sort_keys (bool): Sort elements
            **kwargs: Extra

        Returns:
            str: OWL RDF/XML formatted string
        """
        try:
            if restore_tuple is not None:
                self.restore_tuple = restore_tuple

            data = clean_output(data, omit_keys)
            flat = self._walk(data)

            lines = [
                '<?xml version="1.0"?>',
                f'<{rdf_prefix}:RDF xmlns:{rdf_prefix}="http://www.w3.org/1999/02/22-rdf-syntax-ns#"',
                f'    xmlns:{owl_prefix}="http://www.w3.org/2002/07/owl#"',
                f'    xmlns="{ontology_uri}">',
                f'  <{owl_prefix}:Ontology {rdf_prefix}:about="{ontology_uri}" />'
            ]

            items = sorted(flat.items()) if sort_keys else flat.items()

            for entity, properties in items:
                lines.append(f'  <{owl_prefix}:Class {rdf_prefix}:about="{ontology_uri}{entity}">')
                if isinstance(properties, dict):
                    for prop, val in properties.items():
                        lines.append(f'    <{prop}>{val}</{prop}>')
                else:
                    lines.append(f'    <{rdf_prefix}:value>{properties}</{rdf_prefix}:value>')
                lines.append(f'  </{owl_prefix}:Class>')

            lines.append(f'</{rdf_prefix}:RDF>')
            return "\n".join(lines)
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[OWL.format] Failed to format: {e}")

    def validate(self, data):
        """
        Validate input for OWL formatting.

        Args:
            data (Any): Input

        Returns:
            bool: True if dictionary
        """
        return isinstance(data, dict)

    def _walk(self, value):
        """
        Recursively restore tuples.

        Args:
            value (Any): Node

        Returns:
            Any: Processed
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
            raise ValueError(f"[OWL._walk] Failed to walk data: {e}")