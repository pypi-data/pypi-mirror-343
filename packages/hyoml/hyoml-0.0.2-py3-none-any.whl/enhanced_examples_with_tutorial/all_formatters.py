from interface.hyoml import Hyoml

hy = Hyoml()
text = "key1: 100\nkey2: some string\nkey3: 1/2\n"

data = hy.parse(text)

print("--- JSON ---")
print(hy.asJSON(data, indent=4))

print("--- YAML ---")
print(hy.asYAML(data))

print("--- CSV ---")
print(hy.asCSV(data))

print("--- ENV ---")
print(hy.asENV(data))

print("--- XML ---")
print(hy.asXML(data))

print("--- HTML ---")
print(hy.asHTML(data))

print("--- Markdown ---")
print(hy.asMarkdown(data))
