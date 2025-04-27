"""
Aggregator - Handles merging, listing, or grouping of loaded resources.
"""

class Aggregator:
    """
    Aggregator for combining multiple loaded resources.
    Supports modes: 'merge', 'list', 'groupby:<key>'.
    """

    def __init__(self, mode="merge"):
        """
        Initialize aggregator.

        Args:
            mode (str): Aggregation mode ('merge', 'list', or 'groupby:key')
        """
        self.mode = mode

    def aggregate(self, items):
        """
        Aggregate multiple parsed items.

        Args:
            items (list): List of parsed resource data (dicts or lists).

        Returns:
            Aggregated structure (dict or list)
        """
        if self.mode == "merge":
            return self._merge(items)
        elif self.mode == "list":
            return list(items)
        elif self.mode.startswith("groupby:"):
            key = self.mode.split(":", 1)[1]
            return self._groupby(items, key)
        else:
            raise ValueError(f"[Aggregator] Unknown aggregation mode: {self.mode}")

    def _merge(self, items):
        result = {}
        for item in items:
            if isinstance(item, dict):
                result.update(item)
        return result

    def _groupby(self, items, key):
        grouped = {}
        for item in items:
            if isinstance(item, dict) and key in item:
                group_key = item[key]
                if group_key not in grouped:
                    grouped[group_key] = []
                grouped[group_key].append(item)
        return grouped
