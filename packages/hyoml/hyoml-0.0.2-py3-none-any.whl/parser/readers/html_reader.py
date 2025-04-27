"""
HtmlReader - Parses full HTML documents into structured Python tree.
"""

from python.parser.readers.base_reader import BaseReader

class HtmlReader(BaseReader):
    """
    Reader for raw HTML documents.
    Supports strict parsing and relaxed tolerant parsing.
    """

    def can_parse(self, input_text: str) -> bool:
        """
        Detect if the input looks like HTML.

        Args:
            input_text (str): Text to inspect.

        Returns:
            bool: True if it looks like HTML.
        """
        stripped = input_text.strip().lower()
        return "<html" in stripped or "<!doctype html" in stripped

    def parse(self, input_text: str):
        """
        Parse the input HTML text.

        Args:
            input_text (str): HTML content.

        Returns:
            dict: Parsed HTML tree structure.
        """
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(input_text, "html.parser")
            return self._element_to_dict(soup)
        except Exception as e:
            print(f"Error: {e}")
            if self.strict_mode:
                raise ValueError(f"[HtmlReader] Strict HTML parsing failed: {e}")
            else:
                relaxed_text = self._relax_html(input_text)
                try:
                    soup = BeautifulSoup(relaxed_text, "html.parser")
                    return self._element_to_dict(soup)
                except Exception as e2:
                    raise ValueError(f"[HtmlReader] Relaxed HTML parsing failed after attempting fixes: {e2}")
                
    def _element_to_dict(self, element):
        """
        Recursively convert a BeautifulSoup element to a dictionary.
        """
        if isinstance(element, str):
            return element.strip()

        if not hasattr(element, 'name') or element.name is None:
            return element.string.strip() if element.string else ''

        obj = {
            "tag": element.name,
            "attrs": dict(element.attrs),
            "children": []
        }

        for child in element.children:
            child_dict = self._element_to_dict(child)
            if child_dict:
                obj["children"].append(child_dict)

        if not obj["children"] and element.string:
            obj["text"] = element.string.strip()

        return obj

    def _relax_html(self, input_text: str) -> str:
        """
        Try to auto-fix common relaxed HTML issues.

        Args:
            input_text (str): Raw HTML-like text.

        Returns:
            str: Modified text.
        """
        relaxed = input_text

        # Future: minor normalization (e.g., ensure tags closed)

        return relaxed
