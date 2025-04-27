"""
JavaPropertiesReader - Parses .properties key=value files.
"""

from python.parser.readers.base_reader import BaseReader

class JavaPropertiesReader(BaseReader):
    """
    Reader for Java .properties files.
    Supports strict parsing and relaxed tolerant parsing.
    """

    def can_parse(self, input_text: str) -> bool:
        """
        Detect if the input looks like a Java Properties file.

        Args:
            input_text (str): Text to inspect.

        Returns:
            bool: True if it looks like Java Properties format.
        """
        stripped = input_text.strip()
        return "=" in stripped and not stripped.startswith("{") and not stripped.startswith("<")

    def parse(self, input_text: str):
        """
        Parse the input Java Properties text.

        Args:
            input_text (str): Java Properties text.

        Returns:
            dict: Parsed key-value pairs.
        """
        try:
            return self._parse_properties(input_text)
        except Exception as e:
            print(f"Error: {e}")
            if self.strict_mode:
                raise ValueError(f"[JavaPropertiesReader] Strict parsing failed: {e}")
            else:
                relaxed_text = self._relax_properties(input_text)
                try:
                    return self._parse_properties(relaxed_text)
                except Exception as e2:
                    raise ValueError(f"[JavaPropertiesReader] Relaxed parsing failed after attempting fixes: {e2}")

    def _parse_properties(self, text):
        """
        Internal parser for .properties format.
        """
        result = {}
        lines = text.strip().splitlines()

        for line in lines:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("!"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                result[key.strip()] = value.strip()

        return result

    def _relax_properties(self, text):
        """
        Try to auto-fix relaxed issues in .properties.

        Args:
            text (str): Raw Properties text.

        Returns:
            str: Modified text.
        """
        relaxed = text

        # (Optional future: normalize spaces)

        return relaxed
