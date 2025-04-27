from python.interface.hyoml import Hyoml

def main():
    h = Hyoml()
    parsed = h.parse_from_file("data/sample.json")
    print("As YAML:")
    print(h.format(parsed, format="yaml"))
    print("As Hyoml:")
    print(h.format(parsed, format="hyoml"))

if __name__ == "__main__":
    main()
