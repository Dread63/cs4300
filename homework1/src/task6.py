def read_file(file_name):
    """
    Reads a text file and returns the number of words in it.

    Words are any whitespace-separated tokens, so extra spaces, tabs,
    and newlines are handled correctly.

    Args:
        file_name: Path to the text file to read.

    Returns:
        The number of words in the file (0 for an empty file).

    Raises:
        FileNotFoundError: If file_name does not exist.
    """
    with open(file_name, "r") as file:
        return len(file.read().split())
