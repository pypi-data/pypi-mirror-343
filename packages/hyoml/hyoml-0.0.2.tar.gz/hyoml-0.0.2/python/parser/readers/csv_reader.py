"""
CsvReader - Parses CSV blocks in strict or relaxed mode.
"""

import csv
from io import StringIO
from python.parser.readers.base_reader import BaseReader

class CsvReader(BaseReader):
    """
    Reader for CSV blocks.
    Supports strict CSV parsing and relaxed fault-tolerant parsing.
    """

    def can_parse(self, input_text: str) -> bool:
        """
        Detect if the input looks like CSV.

        Args:
            input_text (str): Text to inspect.

        Returns:
            bool: True if it looks like CSV, else False.
        """
        stripped = input_text.strip()
        return "," in stripped or ";" in stripped

    def parse(self, input_text: str):
        """
        Parse the input CSV text.

        Args:
            input_text (str): CSV text to parse.

        Returns:
            list of dict: Parsed CSV rows as list of dictionaries.
        """
        try:
            return self._parse_csv(input_text)
        except Exception as e:
            print(f"Error: {e}")
            if self.strict_mode:
                raise ValueError(f"[CsvReader] Strict CSV parsing failed: {e}")
            else:
                relaxed_text = self._relax_csv(input_text)
                try:
                    return self._parse_csv(relaxed_text)
                except Exception as e2:
                    raise ValueError(f"[CsvReader] Relaxed CSV parsing failed after attempting fixes: {e2}")

    def _parse_csv(self, text):
        """
        Internal CSV parser.

        Args:
            text (str): CSV text.

        Returns:
            list of dict: Parsed CSV data.
        """
        f = StringIO(text)
        reader = csv.DictReader(f)
        return [row for row in reader]

    def _relax_csv(self, text):
        """
        Try to auto-fix common relaxed CSV issues.

        Args:
            text (str): Raw CSV-like text.

        Returns:
            str: Modified text that is more likely to parse.
        """
        relaxed = text

        # Simple fixes:
        # 1. Normalize line endings
        relaxed = relaxed.replace("\r\n", "\n").replace("\r", "\n")

        # (Optional future: auto-infer headers if missing)

        return relaxed
