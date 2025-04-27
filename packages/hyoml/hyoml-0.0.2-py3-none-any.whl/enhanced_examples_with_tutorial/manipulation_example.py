"""
Example: Data Manipulation with Hyoml

This demonstrates how to sort and search parsed Hyoml data using Hyoml's manipulation utilities.
"""

from interface.hyoml import Hyoml
from python.parser.core.manipulation.sorter import DataSorter
from python.parser.core.manipulation.searcher import DataSearcher

# Sample Hyoml input
hyoml_text = """
name: Ahmed
age: 32
role: developer
city: Cairo
skills:
  - Python
  - AI
  - Data
"""

# Parse the data
parser = Hyoml()
data = parser.parse(hyoml_text)

# === SORTING EXAMPLES ===
print("🔢 Sorted by keys:")
print(DataSorter.sort_dict_by_keys(data))

print("\n🔢 Sorted by values:")
print(DataSorter.sort_dict_by_values(data))

# === SEARCHING EXAMPLES ===
print("\n🔍 Search for key 'city':")
print(DataSearcher.find_key(data, 'city'))

print("\n🔍 Search for value 'Ahmed':")
print(DataSearcher.find_value(data, 'Ahmed'))
