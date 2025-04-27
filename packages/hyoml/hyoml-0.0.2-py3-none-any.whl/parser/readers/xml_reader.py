"""
XmlReader - Parses XML blocks in strict or relaxed mode.
"""

from python.parser.readers.base_reader import BaseReader

class XmlReader(BaseReader):
    """
    Reader for XML blocks.
    Supports strict XML parsing and relaxed fault-tolerant parsing.
    """

    def can_parse(self, input_text: str) -> bool:
        """
        Detect if the input looks like XML.

        Args:
            input_text (str): Text to inspect.

        Returns:
            bool: True if it looks like XML, else False.
        """
        stripped = input_text.strip()
        return stripped.startswith("<") and stripped.endswith(">")

    def parse(self, input_text: str):
        """
        Parse the input XML text.

        Args:
            input_text (str): XML text to parse.

        Returns:
            dict: Parsed XML object.
        """
        try:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(input_text)
            return self._etree_to_dict(root)
        except Exception as e:
            print(f"Error: {e}")
            if self.strict_mode:
                raise ValueError(f"[XmlReader] Strict XML parsing failed: {e}")
            else:
                relaxed_text = self._relax_xml(input_text)
                try:
                    root = ET.fromstring(relaxed_text)
                    return self._etree_to_dict(root)
                except Exception as e2:
                    raise ValueError(f"[XmlReader] Relaxed XML parsing failed after attempting fixes: {e2}")

    def _etree_to_dict(self, element):
        """
        Recursively convert an ElementTree element to a dictionary.
        """
        result = {element.tag: {} if element.attrib else None}

        # Process children
        children = list(element)
        if children:
            dd = {}
            for dc in map(self._etree_to_dict, children):
                for k, v in dc.items():
                    if k in dd:
                        if not isinstance(dd[k], list):
                            dd[k] = [dd[k]]
                        dd[k].append(v)
                    else:
                        dd[k] = v
            result[element.tag] = dd

        # Process attributes
        if element.attrib:
            result[element.tag].update(('@' + k, v) for k, v in element.attrib.items())

        # Process text
        text = element.text.strip() if element.text else ''
        if text:
            if children or element.attrib:
                result[element.tag]['#text'] = text
            else:
                result[element.tag] = text

        return result

    def _relax_xml(self, input_text: str) -> str:
        """
        Try to auto-fix common relaxed XML issues.

        Args:
            input_text (str): Raw XML-like text.

        Returns:
            str: Modified text that is more likely to parse.
        """
        relaxed = input_text

        # Simple relaxed handling could be added here (currently safe fallback)
        # (Example: auto-close missing end tags — tricky, better to raise)

        return relaxed
