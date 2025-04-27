from interface.hyoml import Hyoml

hy = Hyoml()

text = """
{
  username: 'Ali's test',
  path: C:\\Users\\Ali,
  percent: 80%,
  <tag1 />
  <strict=true>
  nested:
    val1: 1,
    val2: 2
}
"""

data = hy.parse(text)

print("Parsed with tags and reserved:")
print(data)
print(hy.asYAML(data))
