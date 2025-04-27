"""
DataSearcher provides methods to search key-value pairs in parsed Hyoml structures,
supporting tuple-aware deep matching.
"""

class DataSearcher:
    @staticmethod
    def find_key(data: dict, key: str) -> list:
        """
        Find all occurrences of a key in a nested dictionary.

        Args:
            data (dict): Parsed structure
            key (str): Key to search for

        Returns:
            list: Matching values
        """
        matches = []

        def _recurse(d):
            if isinstance(d, dict):
                for k, v in d.items():
                    if k == key:
                        matches.append(v)
                    _recurse(v)
            elif isinstance(d, (list, tuple)):
                for item in d:
                    _recurse(item)

        _recurse(data)
        return matches

    @staticmethod
    def find_value(data: dict, value) -> list:
        """
        Find all key paths that match a specific value.

        Args:
            data (dict): Parsed structure
            value: Value to search for

        Returns:
            list: List of paths to matching values
        """
        matches = []

        def _recurse(d, path=""):
            if isinstance(d, dict):
                for k, v in d.items():
                    new_path = f"{path}.{k}" if path else k
                    if v == value:
                        matches.append(new_path)
                    _recurse(v, new_path)
            elif isinstance(d, (list, tuple)):
                for i, item in enumerate(d):
                    _recurse(item, f"{path}[{i}]")

        _recurse(data)
        return matches
