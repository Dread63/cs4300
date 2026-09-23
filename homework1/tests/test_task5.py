import pytest
from src.task5 import print_books_list, student_database

def test_book_list(capsys):

    print_books_list(3)
    captured = capsys.readouterr()
    output_lines = captured.out.strip().split("\n")
    assert len(output_lines) == 3
    assert output_lines[0] == "Red Rising by Pierce Brown"
    assert output_lines[1] == "A Grief Observed by C.S. Lewis"
    assert output_lines[2] == "Atomic Habits by James Clear"

def test_student_database():

    db = student_database()
    assert len(db) == 5
    assert "Alice Johnson" in db
    assert db["Alice Johnson"] == "S1001"
    assert "S1005" in db.values()