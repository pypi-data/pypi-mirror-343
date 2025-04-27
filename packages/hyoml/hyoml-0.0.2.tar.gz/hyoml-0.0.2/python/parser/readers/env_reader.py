"""
EnvReader - Parses .env style files (key=value) in strict or relaxed mode.
"""

from python.parser.readers.base_reader import BaseReader

class EnvReader(BaseReader):
    """
    Reader for ENV (.env) style key=value blocks.
    Supports strict ENV parsing and relaxed fault-tolerant parsing.
    """

    def can_parse(self, input_text: str) -> bool:
        """
        Detect if the input looks like .env style.

        Args:
            input_text (str): Text to inspect.

        Returns:
            bool: True if it looks like ENV format, else False.
        """
        stripped = input_text.strip()
        return "=" in stripped and not stripped.startswith("{") and not stripped.startswith("<")

    def parse(self, input_text: str):
        """
        Parse the input ENV text.

        Args:
            input_text (str): ENV text to parse.

        Returns:
            dict: Parsed ENV object.
        """
        try:
            return self._parse_env(input_text)
        except Exception as e:
            print(f"Error: {e}")
            if self.strict_mode:
                raise ValueError(f"[EnvReader] Strict ENV parsing failed: {e}")
            else:
                relaxed_text = self._relax_env(input_text)
                try:
                    return self._parse_env(relaxed_text)
                except Exception as e2:
                    raise ValueError(f"[EnvReader] Relaxed ENV parsing failed after attempting fixes: {e2}")

    def _parse_env(self, text):
        """
        Internal parser for .env format.
        """
        result = {}
        lines = text.splitlines()

        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue  # skip empty and comment lines
            if "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip("'\"")  # remove wrapping quotes
                result[key] = value

        return result

    def _relax_env(self, text):
        """
        Try to auto-fix common relaxed ENV issues.

        Args:
            text (str): Raw ENV-like text.

        Returns:
            str: Modified text that is more likely to parse.
        """
        relaxed = text

        # Simple fix: Remove empty lines and standardize separators if needed (none for now)

        return relaxed
