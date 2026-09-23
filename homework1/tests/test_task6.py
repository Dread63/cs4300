from pathlib import Path

import pytest

from src.task6 import read_file

SRC_DIR = Path(__file__).resolve().parent.parent / "src"


def test_read_file_word_count():
    """
    The provided lorem ipsum file contains 126 words.
    """
    assert read_file(SRC_DIR / "task6_read_me.txt") == 126


def test_read_file_empty_file(tmp_path):
    """
    An empty file contains zero words (and does not crash).
    """
    empty_file = tmp_path / "empty.txt"
    empty_file.write_text("")
    assert read_file(empty_file) == 0


@pytest.mark.parametrize(
    "content, expected",
    [
        ("hello world", 2),
        ("hello    world", 2),        # multiple spaces collapse
        ("  hello world  ", 2),       # leading/trailing whitespace ignored
        ("one\ntwo\nthree", 3),       # newlines act as separators
        ("tab\tseparated\twords", 3), # tabs act as separators
        ("single", 1),
        ("", 0),
        ("   \n\t  \n ", 0),          # whitespace-only file is empty of words
    ],
    ids=["basic", "extra-spaces", "padding", "newlines", "tabs", "single", "empty", "whitespace-only"],
)
def test_read_file_whitespace_handling(tmp_path, content, expected):
    """
    Any whitespace-separated token counts as a word.
    """
    file = tmp_path / "sample.txt"
    file.write_text(content)
    assert read_file(file) == expected


def test_read_file_missing_file(tmp_path):
    """
    A nonexistent file raises FileNotFoundError.
    """
    with pytest.raises(FileNotFoundError):
        read_file(tmp_path / "does_not_exist.txt")
