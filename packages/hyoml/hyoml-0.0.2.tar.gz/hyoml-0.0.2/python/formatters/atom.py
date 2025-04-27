"""
Atom formatter for Hyoml framework.

Supports:
- Atom 1.0 feed structure generation
- Tuple restoration
- Configurable field mapping for entries
"""

from python.formatters.base import BaseFormatter
from utils.formatter_utils import clean_output
from datetime import datetime

class Atom(BaseFormatter):
    """
    Converts dictionary data into Atom 1.0 XML feed format.
    """

    def __init__(self, **kwargs):
        """
        Initialize the formatter with optional config.

        Args:
            kwargs (dict): Formatter options
        """
        super().__init__(kwargs)

    def format(self, data, omit_keys=None, restore_tuple=None,
               title="Hyoml Atom Feed", feed_id="urn:uuid:hyoml-feed",
               link="http://example.com", updated=None,
               entries_key="items", entry_title_key="title",
               entry_id_key="id", entry_updated_key="updated",
               entry_content_key="content", **kwargs):
        """
        Convert input dictionary to Atom feed XML string.

        Args:
            data (dict): Input dictionary containing entries
            omit_keys (list): Keys to skip
            restore_tuple (bool): Tuple restoration toggle
            title/feed_id/link: Feed metadata
            updated (str): Optional override for updated time
            entries_key: Key holding list of entries
            entry_*_key: Mappings for each entry field

        Returns:
            str: Atom feed XML string
        """
        try:
            if restore_tuple is not None:
                self.restore_tuple = restore_tuple

            data = clean_output(data, omit_keys)
            entries = data.get(entries_key, [])
            updated_time = updated or datetime.utcnow().isoformat() + "Z"

            lines = [
                '<?xml version="1.0" encoding="utf-8"?>',
                '<feed xmlns="http://www.w3.org/2005/Atom">',
                f'  <title>{title}</title>',
                f'  <id>{feed_id}</id>',
                f'  <link href="{link}"/>',
                f'  <updated>{updated_time}</updated>'
            ]

            for entry in entries:
                entry = self._walk(entry)
                lines.append("  <entry>")
                lines.append(f"    <title>{entry.get(entry_title_key, '')}</title>")
                lines.append(f"    <id>{entry.get(entry_id_key, '')}</id>")
                lines.append(f"    <updated>{entry.get(entry_updated_key, updated_time)}</updated>")
                lines.append(f"    <content type=\"text\">{entry.get(entry_content_key, '')}</content>")
                lines.append("  </entry>")

            lines.append("</feed>")
            return "\n".join(lines)
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[Atom.format] Failed to format: {e}")

    def validate(self, data):
        """
        Validate if input has entries.

        Args:
            data (Any): Input

        Returns:
            bool: True if valid Atom input
        """
        return isinstance(data, dict) and isinstance(data.get("items"), list)

    def _walk(self, value):
        """
        Restore tuple values in each entry if applicable.

        Args:
            value (Any): Entry

        Returns:
            dict: Processed entry
        """
        try:
            return {
                k: self._restore_tuple(v) if self.restore_tuple else v
                for k, v in value.items()
            } if isinstance(value, dict) else value
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[Atom._walk] Failed to walk item: {e}")
