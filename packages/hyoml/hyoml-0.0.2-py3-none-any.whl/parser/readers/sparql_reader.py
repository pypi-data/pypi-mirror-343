"""
SparqlReader - Parses simple SPARQL queries into structured format.
"""

from python.parser.readers.base_reader import BaseReader

class SparqlReader(BaseReader):
    """
    Reader for basic SPARQL queries.
    Supports strict parsing and relaxed tolerant parsing.
    """

    def can_parse(self, input_text: str) -> bool:
        """
        Detect if the input looks like a SPARQL query.

        Args:
            input_text (str): Text to inspect.

        Returns:
            bool: True if it looks like SPARQL.
        """
        stripped = input_text.strip().lower()
        return stripped.startswith("select") or stripped.startswith("ask") or \
               stripped.startswith("construct") or stripped.startswith("describe")

    def parse(self, input_text: str):
        """
        Parse the input SPARQL query text.

        Args:
            input_text (str): SPARQL query text.

        Returns:
            dict: Parsed SPARQL structure.
        """
        try:
            return self._parse_sparql(input_text)
        except Exception as e:
            print(f"Error: {e}")
            if self.strict_mode:
                raise ValueError(f"[SparqlReader] Strict SPARQL parsing failed: {e}")
            else:
                relaxed_text = self._relax_sparql(input_text)
                try:
                    return self._parse_sparql(relaxed_text)
                except Exception as e2:
                    raise ValueError(f"[SparqlReader] Relaxed SPARQL parsing failed after attempting fixes: {e2}")

    def _parse_sparql(self, text):
        """
        Very basic SPARQL query parser (for select and simple structure extraction).
        """
        lines = text.strip().splitlines()
        query_type = lines[0].split()[0].lower()

        result = {"query_type": query_type}

        if query_type == "select":
            vars_section = lines[0]
            variables = [var.strip() for var in vars_section.split() if var.startswith("?")]
            result["variables"] = variables

            where_block = "\n".join(lines[1:])
            result["where"] = where_block.strip()

        elif query_type in ("ask", "construct", "describe"):
            result["body"] = "\n".join(lines[1:]).strip()

        else:
            raise ValueError(f"[SparqlReader] Unsupported SPARQL query type: {query_type}")

        return result

    def _relax_sparql(self, text):
        """
        Try to auto-fix simple relaxed SPARQL issues.

        Args:
            text (str): Raw SPARQL text.

        Returns:
            str: Modified text.
        """
        relaxed = text

        # Future: Normalize case, remove extra newlines, etc.

        return relaxed
