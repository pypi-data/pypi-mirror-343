from interface.hyoml import Hyoml

hy = Hyoml()

# --- From file path ---
data1 = hy.parse(path="examples/indented_json_mode.hyoml")
print("From file path:", data1)

# --- From file-like object ---
with open("examples/mixed_array.hyoml", "r", encoding="utf-8") as f:
    data2 = hy.parse(f)
    print("From file object:", data2)

# --- Save output to files ---
hy.asJSON(data1, path="examples/output1.json", indent=2)
hy.asYAML(data2, path="examples/output2.yml")
