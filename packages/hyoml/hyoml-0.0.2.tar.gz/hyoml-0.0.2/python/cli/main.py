import argparse
from interface.hyoml import Hyoml
import sys


def main():
    """
    Entry point for Hyoml CLI.

    Supports parsing a file, formatting it to another format, validating its structure,
    and enabling autofix logging or strict mode.

    Command-line flags:
        file           - Required input file (.hyoml)
        --format       - Output format (json, yaml, toml, etc.)
        --validate     - Validate input against format
        --output       - Optional output file path
        --log-autofix  - Enable logging of AutoFixer diffs
        --strict       - Force strict mode regardless of file content
    """
    parser = argparse.ArgumentParser(description="Hyoml CLI - Parse, format, or validate .hyoml files")
    parser.add_argument("file", help="Path to input file")
    parser.add_argument("--format", help="Output format (json, yaml, xml, etc.)")
    parser.add_argument("--validate", help="Validate file as format (json, yaml, etc.)")
    parser.add_argument("--output", help="Output path for formatted content")
    parser.add_argument("--log-autofix", action="store_true", help="Print AutoFixer diff")
    parser.add_argument("--strict", action="store_true", help="Force strict mode")

    args = parser.parse_args()
    options = {}

    if args.log_autofix:
        options["log_autofix"] = True
    if args.strict:
        options["strict"] = True

    try:
        hy = Hyoml(options=options)
    except Exception as e:
        print(f"Error: {e}")
        print(f"❌ Failed to initialize Hyoml parser: {e}")
        sys.exit(1)

    try:
        data = hy.parse(path=args.file)
    except Exception as e:
        print(f"Error: {e}")
        print(f"❌ Failed to parse file '{args.file}': {e}")
        sys.exit(1)

    try:
        if args.validate:
            valid = hy.validate(data, args.validate)
            print(f"✅ Valid {args.validate.upper()}: {valid}")

        if args.format:
            result = hy.format(data, args.format, path=args.output)
            if not args.output:
                print(result)
        else:
            print("✅ Parsed Output:")
            print(data)
            
    except Exception as e:
        print(f"Error: {e}")
        print(f"❌ Operation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
