"""
ReaderFactory - Selects appropriate Reader based on input text.
"""

from python.parser.readers.json_reader import JsonReader
from python.parser.readers.toml_reader import TomlReader
from python.parser.readers.ini_reader import IniReader
from python.parser.readers.env_reader import EnvReader
from python.parser.readers.xml_reader import XmlReader
from python.parser.readers.csv_reader import CsvReader
from python.parser.readers.markdown_reader import MarkdownReader
from python.parser.readers.rdf_reader import RdfReader
from python.parser.readers.microdata_reader import MicrodataReader
from python.parser.readers.rss_reader import RssReader
from python.parser.readers.atom_reader import AtomReader
from python.parser.readers.sql_reader import SqlReader
from python.parser.readers.sparql_reader import SparqlReader
from python.parser.readers.html_reader import HtmlReader
from python.parser.readers.java_properties_reader import JavaPropertiesReader
from python.parser.readers.shell_script_reader import ShellScriptReader
from python.parser.readers.owl_reader import OwlReader

class ReaderFactory:
    """
    Factory that detects and delegates parsing to the correct Reader.
    """

    def __init__(self, strict_mode=True):
        self.strict_mode = strict_mode
        self.readers = [
            MicrodataReader(strict_mode=self.strict_mode),
            HtmlReader(strict_mode=self.strict_mode),
            RssReader(strict_mode=self.strict_mode),
            AtomReader(strict_mode=self.strict_mode),
            JsonReader(strict_mode=self.strict_mode),
            TomlReader(strict_mode=self.strict_mode),
            IniReader(strict_mode=self.strict_mode),
            EnvReader(strict_mode=self.strict_mode),
            XmlReader(strict_mode=self.strict_mode),
            CsvReader(strict_mode=self.strict_mode),
            MarkdownReader(strict_mode=self.strict_mode),
            RdfReader(strict_mode=self.strict_mode),
            OwlReader(strict_mode=self.strict_mode),
            JavaPropertiesReader(strict_mode=self.strict_mode),
            ShellScriptReader(strict_mode=self.strict_mode),
            SqlReader(strict_mode=self.strict_mode),
            SparqlReader(strict_mode=self.strict_mode),
        ]

    def detect_and_parse(self, input_text: str):
        """
        Attempt to detect and parse the input text.

        Args:
            input_text (str): Raw text.

        Returns:
            Parsed Python object (dict, list, etc.)

        Raises:
            ValueError: If no suitable reader found.
        """
        for reader in self.readers:
            if reader.can_parse(input_text):
                return reader.parse(input_text)

        raise ValueError("[ReaderFactory] No suitable reader found for the input text.")
