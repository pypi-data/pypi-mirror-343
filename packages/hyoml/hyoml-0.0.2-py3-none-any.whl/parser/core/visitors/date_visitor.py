from datetime import datetime
import re
from typing import Any


class DateVisitor:
    """
    Visitor to detect and convert ISO date strings to datetime.date objects.
    """

    @staticmethod
    def visit(data: Any) -> Any:
        """
        Traverse the data and convert date strings.

        Args:
            data (Any): The parsed data structure.

        Returns:
            Any: Data with date values converted.
        """

        def parse_date(value):
            if isinstance(value, str):
                if re.match(r'^\\d{4}-\\d{2}-\\d{2}$', value):
                    try:
                        return datetime.strptime(value, "%Y-%m-%d").date()
                    except Exception:
                        return value
                        return value
            return value

        def walk(obj):
            if isinstance(obj, dict):
                return {k: walk(parse_date(v)) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [walk(parse_date(i)) for i in obj]
            return parse_date(obj)

        return walk(data)
