from interface.hyoml import Hyoml

hy = Hyoml()

# --- Nested objects with arrays ---
text_nested_array = """
user:
  name: Ali
  roles:
    - admin
    - editor
  profile:
    age: 29
    country: Egypt
    skills:
      - Python
      - Bash
      - SQL
"""

print("🧠 Nested with Arrays")
data1 = hy.parse(text_nested_array)
print(hy.asJSON(data1, indent=2))

# --- Mixed JSON & YML with <hyoml_yml> ---
text_mixed = """
{
  title: "Hybrid Example",
  <hyoml_yml>
  stats:
    views: 1200
    likes: 100
  comments:
    - user: a
      text: good
    - user: b
      text: bad
  </hyoml_yml>
}
"""

print("\n🔁 Mixed JSON + YML")
data2 = hy.parse(text_mixed)
print(hy.asYAML(data2))

# --- Multiline, special chars, math-like values ---
text_specials = """
description: |
  This is a multi-line
  string with percent % values
  and math-like 1/2 + 2*π
ratio: 1/3
score: 12e-5
"""

print("\n🧪 Multiline, special math-like values")
data3 = hy.parse(text_specials)
print(hy.asJSON(data3))

# --- Convert one dataset to all formats and save ---
hy.asJSON(data1, path="examples/nested.json")
hy.asYAML(data1, path="examples/nested.yaml")
hy.asCSV(data1, path="examples/nested.csv")
hy.asXML(data1, path="examples/nested.xml")
hy.asMarkdown(data1, path="examples/nested.md")
