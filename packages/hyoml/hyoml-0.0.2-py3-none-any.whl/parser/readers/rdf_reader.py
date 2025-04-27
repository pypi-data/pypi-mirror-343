"""
RdfReader - Parses RDF-based blocks (Turtle, N-Triples, Notation3) into structured data.
"""

from python.parser.readers.base_reader import BaseReader

class RdfReader(BaseReader):
    """
    Reader for RDF formats: Turtle (TTL), N-Triples (NT), Notation3 (N3).
    Supports strict parsing and relaxed tolerant parsing.
    """

    def can_parse(self, input_text: str) -> bool:
        """
        Detect if the input looks like RDF (Turtle/N-Triples/N3).

        Args:
            input_text (str): Text to inspect.

        Returns:
            bool: True if it looks like RDF, else False.
        """
        stripped = input_text.strip()
        return stripped.startswith("@prefix") or stripped.endswith(".")

    def parse(self, input_text: str):
        """
        Parse the input RDF text.

        Args:
            input_text (str): RDF text to parse.

        Returns:
            list of triples: Parsed RDF as list of (subject, predicate, object).
        """
        try:
            return self._parse_rdf(input_text)
        except Exception as e:
            print(f"Error: {e}")
            if self.strict_mode:
                raise ValueError(f"[RdfReader] Strict RDF parsing failed: {e}")
            else:
                relaxed_text = self._relax_rdf(input_text)
                try:
                    return self._parse_rdf(relaxed_text)
                except Exception as e2:
                    raise ValueError(f"[RdfReader] Relaxed RDF parsing failed after attempting fixes: {e2}")

    def _parse_rdf(self, text):
        """
        Internal RDF parser using rdflib.
        """
        import rdflib

        g = rdflib.Graph()
        format_guess = self._guess_format(text)
        g.parse(data=text, format=format_guess)

        triples = []
        for subj, pred, obj in g:
            triples.append((str(subj), str(pred), str(obj)))
        return triples

    def _guess_format(self, text):
        """
        Guess RDF format based on text hints.
        """
        if "@prefix" in text or "@base" in text:
            return "turtle"
        elif text.strip().endswith("."):
            return "nt"  # N-Triples
        else:
            return "n3"  # Fallback to Notation3

    def _relax_rdf(self, text):
        """
        Try to auto-fix common relaxed RDF issues.

        Args:
            text (str): Raw RDF-like text.

        Returns:
            str: Modified text that is more likely to parse.
        """
        relaxed = text

        # Simple fixes could be added here
        # Example: Ensure that triples end with a period

        return relaxed
