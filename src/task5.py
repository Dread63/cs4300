def print_books_list(num_books):
    """
    Prints a list of books up to the specified number.
    """
    books = [
        "Red Rising by Pierce Brown",
        "A Grief Observed by C.S. Lewis",
        "Atomic Habits by James Clear",
        "Iron Gold by Pierce Brown",
        "Romans by Paul"
    ]

    for book in books[:num_books]:
        print(book)

def student_database():
    """
    Returns a dictionary of student names and their corresponding IDs.
    """
    students = {
        "Alice Johnson": "S1001",
        "Brian Lee": "S1002",
        "Carla Diaz": "S1003",
        "Derek Kim": "S1004",
        "Elena Ruiz": "S1005",
    }

    return students