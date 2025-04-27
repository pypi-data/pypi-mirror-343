from interface.hyoml import Hyoml

hy = Hyoml()

# --- Load from JSON file ---
print("🔁 Loading standard JSON")
json_data = hy.parse(path="examples/sample.json")
print("Parsed JSON:", json_data)
print(hy.asYAML(json_data))  # Convert to YAML

# --- Load from YAML file ---
print("\n🔁 Loading standard YAML")
yaml_data = hy.parse(path="examples/sample.yaml")
print("Parsed YAML:", yaml_data)
print(hy.asJSON(yaml_data, indent=2))  # Convert to JSON

# --- Load from CSV file ---
print("\n🔁 Loading pseudo-CSV (flat key-value assumed)")
csv_like = "name: Ali\nage: 30"
csv_data = hy.parse(csv_like)
print("Parsed CSV-like:", csv_data)
print(hy.asTOML(csv_data))  # Convert to TOML

# --- Load from INI file ---
print("\n🔁 Loading pseudo-INI (flat key-value assumed)")
ini_like = "server: localhost\nport: 8080"
ini_data = hy.parse(ini_like)
print("Parsed INI-like:", ini_data)
print(hy.asENV(ini_data))  # Convert to .env format

# --- Save output in multiple formats ---
hy.asXML(ini_data, path="examples/output.ini.xml")
hy.asMarkdown(yaml_data, path="examples/output.yaml.md")
