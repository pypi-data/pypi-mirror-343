from interface.hyoml import Hyoml

hy = Hyoml()
text = "key1: 1\nkey2: 2"

data = hy.parse(text)

formats = ["json", "yaml", "env", "ini", "toml", "csv", "xml", "markdown", "html", "strictyml"]

for fmt in formats:
    result = hy.validate(data, fmt)
    print(f"{fmt.upper()} valid:", result)
