from python.formatters.json import JSON
from python.formatters.yaml import YAML
from python.formatters.env import ENV
from python.formatters.ini import INI
from python.formatters.toml import TOML
from python.formatters.csv import CSV
from python.formatters.xml import XML
from python.formatters.markdown import Markdown
from python.formatters.html import HTML
from python.formatters.strictyml import StrictYML
from python.formatters.java_properties import JavaProperties
from python.formatters.sql import SQL
from python.formatters.shell_script import ShellScript
from python.formatters.rss import RSS
from python.formatters.atom import Atom
from python.formatters.jsonld import JSONLD
from python.formatters.rdf import RDF
from python.formatters.microdata import Microdata
from python.formatters.turtle_ttl import TurtleTTL
from python.formatters.ntriples import NTriples
from python.formatters.notation3 import Notation3
from python.formatters.owl import OWL
from python.formatters.sparql import SPARQL
class Validator:
    """
    Centralized validator for all supported Hyoml output formats.
    """

    #JSON
    @staticmethod
    def isValidJSON(data):
        return JSON.validate(data)

    #YAML
    @staticmethod
    def isValidYAML(data):
        return YAML.validate(data)

    #ENV
    @staticmethod
    def isValidENV(data):
        return ENV.validate(data)

    #INI
    @staticmethod
    def isValidINI(data):
        return INI.validate(data)

    #TOML
    @staticmethod
    def isValidTOML(data):
        return TOML.validate(data)

    #CSV
    @staticmethod
    def isValidCSV(data):
        return CSV.validate(data)

    #XML
    @staticmethod
    def isValidXML(data):
        return XML.validate(data)

    #Markdown
    @staticmethod
    def isValidMarkdown(data):
        return Markdown.validate(data)

    #HTML
    @staticmethod
    def isValidHTML(data):
        return HTML.validate(data)

    #StrictYML
    @staticmethod
    def isValidStrictYML(data):
        return StrictYML.validate(data)
    
    # Java Properties
    @staticmethod
    def isValidJavaProperties(data):
        return JavaProperties.validate(data)

    # SQL
    @staticmethod
    def isValidSQL(data):
        return SQL.validate(data)

    # Shell Script
    @staticmethod
    def isValidShellScript(data):
        return ShellScript.validate(data)

    # RSS
    @staticmethod
    def isValidRSS(data):
        return RSS.validate(data)

    # Atom
    @staticmethod
    def isValidAtom(data):
        return Atom.validate(data)

    # JSON-LD
    @staticmethod
    def isValidJSONLD(data):
        return JSONLD.validate(data)

    # RDF
    @staticmethod
    def isValidRDF(data):
        return RDF.validate(data)

    # Microdata
    @staticmethod
    def isValidMicrodata(data):
        return Microdata.validate(data)

    # Turtle TTL
    @staticmethod
    def isValidTurtleTTL(data):
        return TurtleTTL.validate(data)

    # NTriples
    @staticmethod
    def isValidNTriples(data):
        return NTriples.validate(data)

    # Notation3 (N3)
    @staticmethod
    def isValidNotation3(data):
        return Notation3.validate(data)

    # OWL
    @staticmethod
    def isValidOWL(data):
        return OWL.validate(data)

    # SPARQL
    @staticmethod
    def isValidSPARQL(data):
        return SPARQL.validate(data)

# ✅ Tuple/dict-compatible handling already covered by native checks.