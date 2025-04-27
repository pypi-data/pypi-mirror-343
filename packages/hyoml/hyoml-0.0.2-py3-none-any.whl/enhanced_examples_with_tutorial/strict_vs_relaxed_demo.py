from python.interface.hyoml import Hyoml

strict_example = """
strict: true
numbers: [1, 2, 3]
"""

relaxed_example = """
strict true
numbers [1, 2, 3]
"""

def main():
    h = Hyoml(strict=True)
    parsed_strict = h.parse(strict_example)
    print("Strict Mode:")
    print(parsed_strict)
    
    h_relaxed = Hyoml(strict=False)
    parsed_relaxed = h_relaxed.parse(relaxed_example)
    print("Relaxed Mode:")
    print(parsed_relaxed)

if __name__ == "__main__":
    main()
