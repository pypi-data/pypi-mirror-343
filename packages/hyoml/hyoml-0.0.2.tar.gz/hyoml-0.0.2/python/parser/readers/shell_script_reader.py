"""
ShellScriptReader - Parses bash-style environment variable assignments.
"""

from python.parser.readers.base_reader import BaseReader

class ShellScriptReader(BaseReader):
    """
    Reader for Shell Script ENV exports (VAR=value or export VAR=value).
    Supports strict parsing and relaxed tolerant parsing.
    """

    def can_parse(self, input_text: str) -> bool:
        """
        Detect if the input looks like a Shell Script export.

        Args:
            input_text (str): Text to inspect.

        Returns:
            bool: True if it looks like shell ENV exports.
        """
        stripped = input_text.strip()
        return ("=" in stripped and ("export" in stripped or not stripped.startswith("{")))

    def parse(self, input_text: str):
        """
        Parse the input Shell Script text.

        Args:
            input_text (str): Shell script text.

        Returns:
            dict: Parsed key-value pairs.
        """
        try:
            return self._parse_shell(input_text)
        except Exception as e:
            print(f"Error: {e}")
            if self.strict_mode:
                raise ValueError(f"[ShellScriptReader] Strict parsing failed: {e}")
            else:
                relaxed_text = self._relax_shell(input_text)
                try:
                    return self._parse_shell(relaxed_text)
                except Exception as e2:
                    raise ValueError(f"[ShellScriptReader] Relaxed parsing failed after attempting fixes: {e2}")

    def _parse_shell(self, text):
        """
        Internal parser for shell exports.
        """
        result = {}
        lines = text.strip().splitlines()

        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("export "):
                line = line[len("export "):]
            if "=" in line:
                key, value = line.split("=", 1)
                result[key.strip()] = value.strip().strip('"').strip("'")

        return result

    def _relax_shell(self, text):
        """
        Try to auto-fix relaxed Shell Script issues.

        Args:
            text (str): Raw Shell text.

        Returns:
            str: Modified text.
        """
        relaxed = text

        # (Optional future: normalize missing export keyword)

        return relaxed
