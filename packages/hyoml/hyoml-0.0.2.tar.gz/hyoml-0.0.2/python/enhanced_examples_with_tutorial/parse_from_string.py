from python.interface.hyoml import Hyoml

example_string = """
{
    name: "Example",
    age: 30,
    country: "Wonderland"
}
"""

def main():
    h = Hyoml()
    parsed = h.parse(example_string)
    print(parsed)

if __name__ == "__main__":
    main()
