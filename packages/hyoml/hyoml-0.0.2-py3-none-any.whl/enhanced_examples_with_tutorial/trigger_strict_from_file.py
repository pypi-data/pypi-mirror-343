from interface.hyoml import Hyoml

# Input file that starts with 'use strict'
strict_file_path = "examples/strict_input.hyoml"

# Example content of the file:
# use strict
# name: Test
# value: 123

# Initialize parser without forcing strict
hy = Hyoml()

print("🧪 Parsing with implicit strict mode from file:")
data = hy.parse(path=strict_file_path)

# Check if strict mode was activated
print("Strict mode:", hy.parser.options.get("strict", False))
print("Parsed Data:", data)
