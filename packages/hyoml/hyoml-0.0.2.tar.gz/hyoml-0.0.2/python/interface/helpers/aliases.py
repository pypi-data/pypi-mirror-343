"""
AliasHelper - provides simple alias mappings for Hyoml outputs.
"""

class AliasHelper:
    def __init__(self, hyoml_instance):
        self.hyoml = hyoml_instance

        # String output aliases
        self.asString = self.toString = self.hyoml.toTXT

        # JSON family
        self.asJSN = self.hyoml.asJSON
        self.toJSONLD = self.hyoml.asJSONLD

        # YAML family
        self.asYML = self.hyoml.asYAML

        # HTML/XML family
        self.toHTM = self.hyoml.asHTML
        self.toXML = self.hyoml.asXML

        # Markdown
        self.toMD = self.hyoml.asMarkdown

        # ENV/INI
        self.toENV = self.hyoml.asENV
        self.toINI = self.hyoml.asINI

        # Shell Script
        self.asSH = self.hyoml.asShellScript

        # SQL
        self.toSQL = self.hyoml.asSQL

        # RDF family
        self.asTTL = self.hyoml.asTurtleTTL
        self.asN3 = self.hyoml.asNotation3
        self.asNT = self.hyoml.asNTriples
        self.toRDF = self.hyoml.asRDF

        # Microdata/RSS/Atom
        self.toMicrodata = self.hyoml.asMicrodata
        self.toRSS = self.hyoml.asRSS
        self.toAtom = self.hyoml.asAtom

        # OWL
        self.toOWL = self.hyoml.asOWL

        # SPARQL
        self.toSPARQL = self.hyoml.asSPARQL
