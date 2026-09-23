import pytest
from pathlib import Path
from src.task6 import read_file

TASK6_DIR = Path(__file__).parent.parent / "src"

def test_read_file():

    assert read_file(TASK6_DIR / "task6_read_me.txt") == 126
