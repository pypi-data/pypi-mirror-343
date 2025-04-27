"""
Microdata formatter for Hyoml framework.

Supports:
- HTML5 Microdata embedding
- Tuple restoration
- Simple itemprop/itemtype mapping
"""

from python.formatters.base import BaseFormatter
from utils.formatter_utils import clean_output

class Microdata(BaseFormatter):
    """
    Converts dictionary data into HTML with Microdata attributes.
    """

    def __init__(self, **kwargs):
        """
        Initialize formatter with options.

        Args:
            kwargs (dict): Formatter settings
        """
        super().__init__(kwargs)

    def format(self, data, omit_keys=None, restore_tuple=None,
               itemtype="http://schema.org/Thing", root_tag="div",
               flatten_nested=True, sort_keys=False, **kwargs):
        """
        Convert input into Microdata embedded HTML.

        Args:
            data (dict): Input
            omit_keys (list): Keys to exclude
            restore_tuple (bool): Tuple restoration toggle
            itemtype (str): Schema.org type URL
            root_tag (str): Root HTML tag
            flatten_nested (bool): Flatten nested dicts (simple mode)
            sort_keys (bool): Sort attributes
            **kwargs: Extra options

        Returns:
            str: HTML string
        """
        try:
            if restore_tuple is not None:
                self.restore_tuple = restore_tuple

            data = clean_output(data, omit_keys)
            flat = self._walk(data)
            items = sorted(flat.items()) if sort_keys else flat.items()

            lines = [f"<{root_tag} itemscope itemtype=\"{itemtype}\">"]
            for k, v in items:
                lines.append(f"  <span itemprop=\"{k}\">{v}</span>")
            lines.append(f"</{root_tag}>")
            return "\n".join(lines)
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[Microdata.format] Failed to format: {e}")

    def validate(self, data):
        """
        Validate input for Microdata formatting.

        Args:
            data (Any): Input

        Returns:
            bool: True if dict
        """
        return isinstance(data, dict)

    def _walk(self, value):
        """
        Apply tuple restoration.

        Args:
            value (Any): Node

        Returns:
            dict: Processed data
        """
        try:
            if isinstance(value, dict):
                return {k: self._walk(v) for k, v in value.items()}
            elif isinstance(value, list):
                return {str(i): self._walk(v) for i, v in enumerate(value)}
            else:
                return self._restore_tuple(value) if self.restore_tuple else value
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[Microdata._walk] Failed to walk data: {e}")
