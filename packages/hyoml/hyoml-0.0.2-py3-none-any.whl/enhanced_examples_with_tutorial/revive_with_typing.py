"""
This example demonstrates using a custom reviver function with Hyoml to:
- Capitalize all string values
- Convert 'null' strings to None
- Convert numeric-looking strings to actual numbers
"""

from interface.hyoml import Hyoml

def smart_reviver(key, value, context):
    """
    A custom reviver function that:
    - Converts strings like 'null' to None
    - Converts numeric strings to int or float
    - Capitalizes all other strings
    """
    if isinstance(value, str):
        val_lower = value.strip().lower()
        if val_lower in ("null", "none", "undefined"):
            return None
        if val_lower.isdigit():
            return int(val_lower)
        try:
            return float(val_lower)
        except ValueError:
            return value.capitalize()
            return value.capitalize()
    return value

# Load file that contains various mixed types
parser = Hyoml(options={"reviver": smart_reviver})
data = parser.parse(path="examples/typed_values.hyoml")

print("✅ Transformed Output:")
print(data)
