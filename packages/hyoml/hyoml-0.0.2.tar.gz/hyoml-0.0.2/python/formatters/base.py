"""
BaseFormatter defines a common interface and shared logic for all Hyoml formatters.

Features:
- Unified constructor
- Shared tuple restoration method
- Abstract `_walk()` for recursive traversal
"""

from abc import ABC, abstractmethod


class BaseFormatter(ABC):
    def __init__(self, options=None):
        """
        Initialize the formatter with optional configuration.

        Args:
            options (dict): Optional settings like formatting flags or restore behavior
        """
        self.options = options or {}
        self.restore_tuple = self.options.get("restore_tuple", False)

    def _restore_tuple(self, value):
        """
        Convert {"@type": "tuple", "values": [...]} into Python tuple.

        Args:
            value (Any): Input node

        Returns:
            Any: tuple or original value
        """
        try:
            if (
                isinstance(value, dict)
                and value.get("@type") == "tuple"
                and isinstance(value.get("values"), list)
            ):
                return tuple(value["values"])
            return value
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[BaseFormatter._restore_tuple] Failed: {e}")

    @abstractmethod
    def _walk(self, value):
        """
        Recursively traverse and transform the data.

        This must be implemented by subclasses.

        Args:
            value (Any): Node to process

        Returns:
            Any: Transformed output
        """
        raise NotImplementedError("Subclasses must implement _walk()")
