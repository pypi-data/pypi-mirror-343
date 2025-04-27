"""
DataSorter provides methods to sort dictionaries or lists of dictionaries,
supporting tuple-aware comparison logic.
"""

class DataSorter:
    @staticmethod
    def sort_dict_by_keys(data: dict, reverse: bool = False) -> dict:
        """
        Sort dictionary by its keys.

        Args:
            data (dict): Input dictionary
            reverse (bool): Sort descending if True

        Returns:
            dict: Sorted dictionary
        """
        if not isinstance(data, dict):
            raise ValueError("Expected a dictionary")
        return dict(sorted(data.items(), key=lambda x: str(x[0]), reverse=reverse))

    @staticmethod
    def sort_dict_by_values(data: dict, reverse: bool = False) -> dict:
        """
        Sort dictionary by its values (as strings for compatibility).

        Args:
            data (dict): Input dictionary
            reverse (bool): Sort descending if True

        Returns:
            dict: Sorted dictionary
        """
        if not isinstance(data, dict):
            raise ValueError("Expected a dictionary")
        return dict(sorted(data.items(), key=lambda x: str(x[1]), reverse=reverse))

    @staticmethod
    def sort_list_of_dicts(data: list, key: str, reverse: bool = False) -> list:
        """
        Sort a list of dictionaries by a shared key.

        Args:
            data (list): List of dicts
            key (str): Key to sort by
            reverse (bool): Sort descending if True

        Returns:
            list: Sorted list
        """
        if not isinstance(data, list):
            raise ValueError("Expected a list of dictionaries")
        return sorted(data, key=lambda d: str(d.get(key)), reverse=reverse)
