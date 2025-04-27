"""
JsonReader - Parses JSON blocks in strict or relaxed mode.
"""

import json
from python.parser.readers.base_reader import BaseReader

class JsonReader(BaseReader):
    """
    Reader for JSON blocks.
    Supports strict JSON parsing and relaxed fault-tolerant parsing.
    """

    def can_parse(self, input_text: str) -> bool:
        """
        Detect if the input looks like JSON.

        Args:
            input_text (str): Text to inspect.

        Returns:
            bool: True if it looks like JSON, else False.
        """
        stripped = input_text.strip()
        return stripped.startswith("{") or stripped.startswith("[")

    def parse(self, input_text: str):
        """
        Parse the input JSON text.

        Args:
            input_text (str): JSON text to parse.

        Returns:
            dict or list: Parsed JSON object.
        """
        try:
            return json.loads(input_text)
        except json.JSONDecodeError as e:
            if self.strict_mode:
                raise ValueError(f"[JsonReader] Strict JSON parsing failed: {e}")
            else:
                # Try relaxed parsing
                relaxed_text = self._relax_json(input_text)
                try:
                    return json.loads(relaxed_text)
                except Exception as e2:
                    raise ValueError(f"[JsonReader] Relaxed JSON parsing failed after attempting fixes: {e2}")
                
    def _relax_json(self, input_text: str) -> str:
        """
        Try to auto-fix common relaxed JSON issues.

        Args:
            input_text (str): Raw JSON-like text.

        Returns:
            str: Modified text that is more likely to parse.
        """
        relaxed = input_text

        # Simple fixes:
        # 1. Allow single quotes (replace with double quotes carefully)
        relaxed = relaxed.replace("'", '"')

        # 2. Remove trailing commas (only simple cases)
        import re
        relaxed = re.sub(r",\\s*(\\}|\\])", r"\1", relaxed)

        # (Optional: more fixes like missing quotes on keys)

        return relaxed
