def read_file(file_name):
    """
    Reads the contents of a file.
    """
    with open(file_name, 'r') as file:
        return len(file.read().split())
