"""
RssReader - Parses basic RSS feed XML into structured data.
"""

from python.parser.readers.base_reader import BaseReader

class RssReader(BaseReader):
    """
    Reader for RSS Feeds.
    Supports strict parsing and relaxed tolerant parsing.
    """

    def can_parse(self, input_text: str) -> bool:
        """
        Detect if the input looks like RSS XML.

        Args:
            input_text (str): Text to inspect.

        Returns:
            bool: True if it looks like RSS.
        """
        stripped = input_text.strip().lower()
        return "<rss" in stripped or "<channel>" in stripped

    def parse(self, input_text: str):
        """
        Parse the input RSS feed text.

        Args:
            input_text (str): RSS XML text.

        Returns:
            dict: Parsed RSS feed structure.
        """
        try:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(input_text)
            return self._parse_rss(root)
        except Exception as e:
            print(f"Error: {e}")
            if self.strict_mode:
                raise ValueError(f"[RssReader] Strict RSS parsing failed: {e}")
            else:
                relaxed_text = self._relax_rss(input_text)
                try:
                    root = ET.fromstring(relaxed_text)
                    return self._parse_rss(root)
                except Exception as e2:
                    raise ValueError(f"[RssReader] Relaxed RSS parsing failed after attempting fixes: {e2}")

    def _parse_rss(self, root):
        """
        Internal method to parse RSS XML ElementTree into dict.
        """
        channel = root.find("channel")
        if channel is None:
            raise ValueError("[RssReader] No <channel> found in RSS.")

        feed = {
            "title": channel.findtext("title"),
            "link": channel.findtext("link"),
            "description": channel.findtext("description"),
            "items": []
        }

        for item in channel.findall("item"):
            entry = {
                "title": item.findtext("title"),
                "link": item.findtext("link"),
                "description": item.findtext("description"),
                "pubDate": item.findtext("pubDate"),
                "guid": item.findtext("guid")
            }
            feed["items"].append(entry)

        return feed

    def _relax_rss(self, input_text: str) -> str:
        """
        Try to auto-fix common relaxed RSS issues.

        Args:
            input_text (str): Raw RSS-like text.

        Returns:
            str: Modified text that is more likely to parse.
        """
        relaxed = input_text

        # (Future: basic fixes could be added if needed, for now just a passthrough)
        return relaxed
