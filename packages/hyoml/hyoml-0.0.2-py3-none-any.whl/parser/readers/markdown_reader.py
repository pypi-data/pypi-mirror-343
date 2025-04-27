"""
MarkdownReader - Parses simple Markdown tables into structured data.
"""

from python.parser.readers.base_reader import BaseReader

class MarkdownReader(BaseReader):
    """
    Reader for Markdown tables.
    Supports strict parsing and relaxed tolerant parsing.
    """

    def can_parse(self, input_text: str) -> bool:
        """
        Detect if the input looks like a Markdown table.

        Args:
            input_text (str): Text to inspect.

        Returns:
            bool: True if it looks like a Markdown table, else False.
        """
        stripped = input_text.strip()
        return "|" in stripped and "---" in stripped

    def parse(self, input_text: str):
        """
        Parse the input Markdown table text.

        Args:
            input_text (str): Markdown text to parse.

        Returns:
            list of dict: Parsed table rows.
        """
        try:
            return self._parse_markdown(input_text)
        except Exception as e:
            print(f"Error: {e}")
            if self.strict_mode:
                raise ValueError(f"[MarkdownReader] Strict Markdown parsing failed: {e}")
            else:
                relaxed_text = self._relax_markdown(input_text)
                try:
                    return self._parse_markdown(relaxed_text)
                except Exception as e2:
                    raise ValueError(f"[MarkdownReader] Relaxed Markdown parsing failed after attempting fixes: {e2}")

    def _parse_markdown(self, text):
        """
        Internal parser for simple Markdown tables.
        """
        lines = text.strip().splitlines()
        if len(lines) < 2:
            raise ValueError("Markdown table must have at least a header and separator.")

        headers = [h.strip() for h in lines[0].strip('|').split('|')]
        separator = lines[1]

        rows = []
        for line in lines[2:]:
            if not line.strip():
                continue
            values = [v.strip() for v in line.strip('|').split('|')]
            if len(values) != len(headers):
                raise ValueError(f"Row length mismatch in Markdown table: {values}")
            rows.append(dict(zip(headers, values)))

        return rows

    def _relax_markdown(self, text):
        """
        Try to auto-fix common relaxed Markdown issues.

        Args:
            text (str): Raw Markdown-like text.

        Returns:
            str: Modified text that is more likely to parse.
        """
        relaxed = text

        # Simple fix: Normalize pipes
        relaxed = "\n".join(line.strip() for line in relaxed.splitlines())

        return relaxed
