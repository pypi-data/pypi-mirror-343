"""
AtomReader - Parses basic Atom feed XML into structured data.
"""

from python.parser.readers.base_reader import BaseReader

class AtomReader(BaseReader):
    """
    Reader for Atom Feeds.
    Supports strict parsing and relaxed tolerant parsing.
    """

    def can_parse(self, input_text: str) -> bool:
        """
        Detect if the input looks like Atom XML.

        Args:
            input_text (str): Text to inspect.

        Returns:
            bool: True if it looks like Atom.
        """
        stripped = input_text.strip().lower()
        return "<feed" in stripped and "xmlns=" in stripped and "atom" in stripped

    def parse(self, input_text: str):
        """
        Parse the input Atom feed text.

        Args:
            input_text (str): Atom XML text.

        Returns:
            dict: Parsed Atom feed structure.
        """
        try:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(input_text)
            return self._parse_atom(root)
        except Exception as e:
            print(f"Error: {e}")
            
            if self.strict_mode:
                raise ValueError(f"[AtomReader] Strict Atom parsing failed: {e}")
            else:
                relaxed_text = self._relax_atom(input_text)
                try:
                    root = ET.fromstring(relaxed_text)
                    return self._parse_atom(root)
                except Exception as e2:
                    raise ValueError(f"[AtomReader] Relaxed Atom parsing failed after attempting fixes: {e2}")

    def _parse_atom(self, root):
        """
        Internal method to parse Atom XML ElementTree into dict.
        """
        ns = {'atom': 'http://www.w3.org/2005/Atom'}

        feed = {
            "title": root.findtext("atom:title", namespaces=ns),
            "link": root.findtext("atom:link", namespaces=ns),
            "subtitle": root.findtext("atom:subtitle", namespaces=ns),
            "entries": []
        }

        for entry in root.findall("atom:entry", namespaces=ns):
            item = {
                "title": entry.findtext("atom:title", namespaces=ns),
                "link": entry.findtext("atom:link", namespaces=ns),
                "summary": entry.findtext("atom:summary", namespaces=ns),
                "updated": entry.findtext("atom:updated", namespaces=ns),
                "id": entry.findtext("atom:id", namespaces=ns)
            }
            feed["entries"].append(item)

        return feed

    def _relax_atom(self, input_text: str) -> str:
        """
        Try to auto-fix common relaxed Atom issues.

        Args:
            input_text (str): Raw Atom-like text.

        Returns:
            str: Modified text that is more likely to parse.
        """
        relaxed = input_text

        # (Future: Auto-fix if needed, for now just passthrough)
        return relaxed
