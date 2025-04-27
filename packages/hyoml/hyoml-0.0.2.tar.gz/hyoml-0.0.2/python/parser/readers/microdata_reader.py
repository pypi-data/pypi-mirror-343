"""
MicrodataReader - Parses Microdata embedded inside simple HTML.
"""

from python.parser.readers.base_reader import BaseReader

class MicrodataReader(BaseReader):
    """
    Reader for extracting Microdata from HTML content.
    Supports strict parsing and relaxed tolerant parsing.
    """

    def can_parse(self, input_text: str) -> bool:
        """
        Detect if the input looks like HTML with Microdata.

        Args:
            input_text (str): Text to inspect.

        Returns:
            bool: True if it looks like Microdata HTML, else False.
        """
        stripped = input_text.strip().lower()
        return "<html" in stripped or "<!doctype html" in stripped or "itemscope" in stripped

    def parse(self, input_text: str):
        """
        Parse Microdata from the HTML text.

        Args:
            input_text (str): HTML content.

        Returns:
            dict: Extracted Microdata.
        """
        try:
            from bs4 import BeautifulSoup

            soup = BeautifulSoup(input_text, "html.parser")
            data = {}

            for item in soup.find_all(attrs={"itemscope": True}):
                item_data = {}
                for prop in item.find_all(attrs={"itemprop": True}):
                    key = prop.attrs.get("itemprop")
                    value = prop.get("content") or prop.text.strip()
                    item_data[key] = value
                if item.attrs.get("itemtype"):
                    typename = item.attrs.get("itemtype").split("/")[-1]
                    data[typename] = item_data
                else:
                    data.update(item_data)

            return data

        except Exception as e:
            print(f"Error: {e}")
            if self.strict_mode:
                raise ValueError(f"[MicrodataReader] Strict parsing failed: {e}")
            else:
                try:
                    return {"error": str(e)}
                except Exception as e:
                    print(f"Unknown Error: {e}")
                    raise ValueError(f"[MicrodataReader] Unknown Error: {e}")
