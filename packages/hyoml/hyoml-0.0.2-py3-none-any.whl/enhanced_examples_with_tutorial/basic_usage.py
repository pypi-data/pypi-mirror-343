from interface.hyoml import Hyoml

hy = Hyoml()
text = "name: Ali\nadmin: TRUE\nscore: 42.5"
data = hy.parse(text)

print("Parsed:", data)
print("As JSON:", hy.asJSON(data, indent=2))
print("Is valid JSON:", hy.isValidJSON(data))
