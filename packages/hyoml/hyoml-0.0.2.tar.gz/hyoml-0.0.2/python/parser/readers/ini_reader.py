"""
IniReader - Parses INI blocks in strict or relaxed mode.
"""

from python.parser.readers.base_reader import BaseReader

class IniReader(BaseReader):
    """
    Reader for INI blocks.
    Supports strict INI parsing and relaxed fault-tolerant parsing.
    """

    def can_parse(self, input_text: str) -> bool:
        """
        Detect if the input looks like INI.

        Args:
            input_text (str): Text to inspect.

        Returns:
            bool: True if it looks like INI, else False.
        """
        stripped = input_text.strip()
        return "=" in stripped and not stripped.startswith("{") and not stripped.startswith("<")

    def parse(self, input_text: str):
        """
        Parse the input INI text.

        Args:
            input_text (str): INI text to parse.

        Returns:
            dict: Parsed INI object.
        """
        import configparser
        from io import StringIO

        config = configparser.ConfigParser()

        try:
            config.read_file(StringIO(input_text))
            return self._config_to_dict(config)
        except Exception as e:
            print(f"Error: {e}")
            if self.strict_mode:
                raise ValueError(f"[IniReader] Strict INI parsing failed: {e}")
            else:
                relaxed_text = self._relax_ini(input_text)
                try:
                    config.read_file(StringIO(relaxed_text))
                    return self._config_to_dict(config)
                except Exception as e2:
                    raise ValueError(f"[IniReader] Relaxed INI parsing failed after attempting fixes: {e2}")

    def _config_to_dict(self, config):
        """
        Convert a ConfigParser object to a dictionary.
        """
        result = {}
        for section in config.sections():
            result[section] = dict(config.items(section))
        return result

    def _relax_ini(self, input_text: str) -> str:
        """
        Try to auto-fix common relaxed INI issues.

        Args:
            input_text (str): Raw INI-like text.

        Returns:
            str: Modified text that is more likely to parse.
        """
        relaxed = input_text

        # Simple fixes:
        # 1. If there is no section header, add a fake one
        if not "[" in relaxed:
            relaxed = "[DEFAULT]\n" + relaxed

        return relaxed
