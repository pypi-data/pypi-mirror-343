"""
RSS formatter for Hyoml framework.

Supports:
- Simple RSS 2.0 feed generation
- Static or dynamic fields from input
- Tuple restoration
"""

from python.formatters.base import BaseFormatter
from utils.formatter_utils import clean_output
from datetime import datetime

class RSS(BaseFormatter):
    """
    Converts dictionary data into a basic RSS feed structure.
    Suitable for testing or minimal XML serialization.
    """

    def __init__(self, **kwargs):
        """
        Initialize the formatter.

        Args:
            kwargs (dict): Formatter options
        """
        super().__init__(kwargs)

    def format(self, data, omit_keys=None, restore_tuple=None,
               title="Hyoml Feed", link="http://example.com", 
               description="Hyoml Export", items_key="items",
               item_title_key="title", item_link_key="link", item_desc_key="description",
               pub_date_key="pubDate", **kwargs):
        """
        Convert input into RSS XML format.

        Args:
            data (dict): Must contain an `items` list
            omit_keys (list): Keys to exclude
            restore_tuple (bool): Tuple restoration toggle
            title/link/description: Feed metadata
            items_key (str): Path to list of entries
            item_title_key/link_key/desc_key/pub_date_key: Field mapping

        Returns:
            str: RSS feed as XML string
        """
        try:
            if restore_tuple is not None:
                self.restore_tuple = restore_tuple

            data = clean_output(data, omit_keys)
            items = data.get(items_key, [])
            now = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')

            lines = [
                '<?xml version="1.0" encoding="UTF-8"?>',
                '<rss version="2.0">',
                '<channel>',
                f'<title>{title}</title>',
                f'<link>{link}</link>',
                f'<description>{description}</description>',
                f'<lastBuildDate>{now}</lastBuildDate>'
            ]

            for entry in items:
                entry = self._walk(entry)
                lines.append("<item>")
                lines.append(f"  <title>{entry.get(item_title_key, '')}</title>")
                lines.append(f"  <link>{entry.get(item_link_key, '')}</link>")
                lines.append(f"  <description>{entry.get(item_desc_key, '')}</description>")
                pub = entry.get(pub_date_key, now)
                lines.append(f"  <pubDate>{pub}</pubDate>")
                lines.append("</item>")

            lines.append("</channel>")
            lines.append("</rss>")
            return "\n".join(lines)
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[RSS.format] Failed to format: {e}")

    def validate(self, data):
        """
        Validate if data contains a valid items list.

        Args:
            data (Any): Parsed input

        Returns:
            bool: True if valid RSS structure
        """
        return isinstance(data, dict) and isinstance(data.get("items"), list)

    def _walk(self, value):
        """
        Restore tuples in item structure.

        Args:
            value (Any): Input node

        Returns:
            dict: Processed node
        """
        try:
            return {
                k: self._restore_tuple(v) if self.restore_tuple else v
                for k, v in value.items()
            } if isinstance(value, dict) else value
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[RSS._walk] Failed to walk item: {e}")