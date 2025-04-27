"""
BaseReader - Abstract base class for all Readers.
"""

from abc import ABC, abstractmethod

class BaseReader(ABC):
    """
    Abstract base reader class that all format readers must inherit from.
    Provides strict/relaxed mode control.
    """

    def __init__(self, strict_mode=True):
        """
        Initialize the reader.

        Args:
            strict_mode (bool): If True, enforce strict parsing; else try relaxed fault-tolerant parsing.
        """
        self.strict_mode = strict_mode

    @abstractmethod
    def can_parse(self, input_text: str) -> bool:
        """
        Determine if this reader can handle the given text.

        Args:
            input_text (str): Input text to check.

        Returns:
            bool: True if it can parse, False otherwise.
        """
        pass

    @abstractmethod
    def parse(self, input_text: str):
        """
        Parse the input text into structured data.

        Args:
            input_text (str): Input text to parse.

        Returns:
            dict or list: Parsed data.
        """
        pass
