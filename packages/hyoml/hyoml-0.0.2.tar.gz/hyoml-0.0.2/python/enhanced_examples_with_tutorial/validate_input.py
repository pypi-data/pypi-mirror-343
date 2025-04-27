from python.interface.hyoml import Hyoml

example_string = """
{
    name: "Example",
    invalid_field: unknown_value
}
"""

def main():
    h = Hyoml()
    parsed = h.parse(example_string)
    if h.validate(parsed):
        print("Valid Hyoml structure!")
    else:
        print("Invalid Hyoml structure!")

if __name__ == "__main__":
    main()
