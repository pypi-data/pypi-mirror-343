"""
FormatterFactory - creates formatter instances based on format name.
"""

from python.formatters.json import JSON
from python.formatters.yaml import YAML
from python.formatters.csv import CSV
from python.formatters.ini import INI
from python.formatters.env import ENV
from python.formatters.html import HTML
from python.formatters.xml import XML
from python.formatters.toml import TOML
from python.formatters.markdown import Markdown
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


class FormatterFactory:
    """
    Factory class to create formatter instances.
    """

    _formatters = {
        "json": JSON,
        "yaml": YAML,
        "csv": CSV,
        "ini": INI,
        "env": ENV,
        "html": HTML,
        "xml": XML,
        "toml": TOML,
        "markdown": Markdown,
        "strictyml": StrictYML,
        "java_properties": JavaProperties,
        "sql": SQL,
        "shell_script": ShellScript,
        "rss": RSS,
        "atom": Atom,
        "jsonld": JSONLD,
        "rdf": RDF,
        "microdata": Microdata,
        "turtle_ttl": TurtleTTL,
        "ntriples": NTriples,
        "notation3": Notation3,
        "owl": OWL,
        "sparql": SPARQL,
    }

    @classmethod
    def create(cls, fmt_name):
        fmt_class = cls._formatters.get(fmt_name.lower())
        if fmt_class:
            return fmt_class()
        raise ValueError("No formatter found for the given type.")
