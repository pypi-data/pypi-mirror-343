"""
Reviver applies post-parsing transformations to primitive values.
Supports user-defined reviver functions and optional handling for dataclass and tuple preservation.
"""

from dataclasses import is_dataclass, asdict
from collections import namedtuple

class Reviver:
    @staticmethod
    def apply(data, reviver_fn=None, options=None, key_path=""):
        """
        Recursively apply a reviver function or built-in type handling.

        Args:
            data (Any): Parsed Hyoml data (dict, list, etc.)
            reviver_fn (Callable): Optional user-defined function with (key, value, context)
            options (dict): Custom behavior flags (e.g., preserve_tuple, expand_dataclass)
            key_path (str): Internal key path used for recursion (auto-managed)

        Returns:
            Any: Transformed structure
        """
        options = options or {}

        try:
            # Handle dataclass expansion
            if is_dataclass(data) and options.get("expand_dataclass"):
                return Reviver.apply(asdict(data), reviver_fn, options, key_path)

            # Handle namedtuple expansion
            if hasattr(data, "_asdict") and isinstance(data, tuple) and options.get("expand_dataclass"):
                return Reviver.apply(data._asdict(), reviver_fn, options, key_path)

            # Handle tuple preservation
            if isinstance(data, tuple) and options.get("preserve_tuple"):
                return {
                    "@type": "tuple",
                    "values": [Reviver.apply(v, reviver_fn, options, f"{key_path}[{i}]") for i, v in enumerate(data)]
                }

            # Recurse into dict
            if isinstance(data, dict):
                result = {}
                for k, v in data.items():
                    full_key = f"{key_path}.{k}" if key_path else k
                    result[k] = Reviver.apply(v, reviver_fn, options, full_key)
                return result

            # Recurse into list
            if isinstance(data, list):
                return [
                    Reviver.apply(v, reviver_fn, options, f"{key_path}[{i}]")
                    for i, v in enumerate(data)
                ]

            # Apply reviver to primitive value
            if reviver_fn:
                context = {"path": key_path, "source": data}
                return reviver_fn(key_path, data, context)

            return data

        except Exception as e:
            print(f"Error: {e}")
            raise ValueError(f"[Reviver] Failed at path '{key_path}': {e}")
