"""
File I/O utilities for Hyoml.
"""

def load_file(path, mode="r", encoding="utf-8"):
    """
    Loads content from a file.

    Args:
        path (str): Path to the file.
        mode (str): Mode to open the file.
        encoding (str): File encoding.

    Returns:
        str: File contents as string.
    """
    try:
        with open(path, mode, encoding=encoding) as f:
            return f.read()
    except Exception as e:
        print(f"Error: {e}")
        raise IOError(f"Failed to load file: {path}") from e

def save_file(path, content, mode="w", encoding="utf-8"):
    """
    Saves content to a file.

    Args:
        path (str): Path to save the file.
        content (str): Data to write.
        mode (str): Mode to open the file.
        encoding (str): File encoding.
    """
    try:
        with open(path, mode, encoding=encoding) as f:
            f.write(content)
    except Exception as e:
        print(f"Error: {e}")
        raise IOError(f"Failed to save file: {path}") from e
