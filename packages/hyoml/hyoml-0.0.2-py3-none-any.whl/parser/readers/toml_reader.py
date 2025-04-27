"""
TomlReader - Parses TOML blocks in strict or relaxed mode.
"""

from python.parser.readers.base_reader import BaseReader

class TomlReader(BaseReader):
    """
    Reader for TOML blocks.
    Supports strict TOML parsing and relaxed fault-tolerant parsing.
    """

    def can_parse(self, input_text: str) -> bool:
        """
        Detect if the input looks like TOML.

        Args:
            input_text (str): Text to inspect.

        Returns:
            bool: True if it looks like TOML, else False.
        """
        stripped = input_text.strip()
        return "=" in stripped and not (stripped.startswith("{") or stripped.startswith("<"))

    def parse(self, input_text: str):
        """
        Parse the input TOML text.

        Args:
            input_text (str): TOML text to parse.

        Returns:
            dict: Parsed TOML object.
        """
        try:
            import toml
            return toml.loads(input_text)
        except Exception as e:
            print(f"Error: {e}")
            if self.strict_mode:
                raise ValueError(f"[TomlReader] Strict TOML parsing failed: {e}")
            else:
                relaxed_text = self._relax_toml(input_text)
                try:
                    return toml.loads(relaxed_text)
                except Exception as e2:
                    raise ValueError(f"[TomlReader] Relaxed TOML parsing failed after attempting fixes: {e2}")

    def _relax_toml(self, input_text: str) -> str:
        """
        Try to auto-fix common relaxed TOML issues.

        Args:
            input_text (str): Raw TOML-like text.

        Returns:
            str: Modified text that is more likely to parse.
        """
        relaxed = input_text

        # Simple fixes:
        # 1. Replace single quotes with double quotes (for strings)
        relaxed = relaxed.replace("'", '"')

        # 2. Allow missing quotes around simple strings (very basic cases could be expanded)

        return relaxed
