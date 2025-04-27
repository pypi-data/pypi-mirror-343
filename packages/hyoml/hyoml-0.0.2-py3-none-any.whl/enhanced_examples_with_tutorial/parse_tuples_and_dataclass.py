"""
Example demonstrating how Hyoml handles tuples and dataclasses using options.
"""

from interface.hyoml import Hyoml

# Enable optional support for tuple and dataclass structures
parser = Hyoml(options={"preserve_tuple": True, "expand_dataclass": True})

data = parser.parse(path="examples/tuples_and_dataclass.hyoml")

print("✅ Parsed with Tuple & Dataclass Support:")
print(data)
