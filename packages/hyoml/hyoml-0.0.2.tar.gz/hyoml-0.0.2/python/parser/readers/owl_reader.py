"""
OwlReader - Parses OWL ontologies (RDF/XML or Turtle).
"""

from python.parser.readers.base_reader import BaseReader

class OwlReader(BaseReader):
    """
    Reader for OWL ontologies (RDF/XML, Turtle).
    Supports strict parsing and relaxed tolerant parsing.
    """

    def can_parse(self, input_text: str) -> bool:
        """
        Detect if the input looks like OWL RDF/XML or Turtle.

        Args:
            input_text (str): Text to inspect.

        Returns:
            bool: True if it looks like OWL format.
        """
        stripped = input_text.strip().lower()
        return ("owl:" in stripped or "rdf:" in stripped) and ("ontology" in stripped)

    def parse(self, input_text: str):
        """
        Parse the input OWL text.

        Args:
            input_text (str): OWL content (RDF/XML or Turtle).

        Returns:
            list: Parsed ontology triples.
        """
        try:
            return self._parse_owl(input_text)
        except Exception as e:
            print(f"Error: {e}")
            if self.strict_mode:
                raise ValueError(f"[OwlReader] Strict OWL parsing failed: {e}")
            else:
                relaxed_text = self._relax_owl(input_text)
                try:
                    return self._parse_owl(relaxed_text)
                except Exception as e2:
                    raise ValueError(f"[OwlReader] Relaxed OWL parsing failed after attempting fixes: {e2}")

    def _parse_owl(self, text):
        """
        Internal OWL parser using rdflib.
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
        Guess OWL format based on text hints.
        """
        if "<?xml" in text or "<rdf:" in text:
            return "xml"
        elif "@prefix" in text or "@base" in text:
            return "turtle"
        else:
            return "xml"  # Default fallback

    def _relax_owl(self, text):
        """
        Try to auto-fix relaxed OWL issues.

        Args:
            text (str): Raw OWL-like text.

        Returns:
            str: Modified text.
        """
        relaxed = text

        # (Optional future: Auto-close tags, normalize syntax)

        return relaxed
