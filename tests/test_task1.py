import pytest
from src.task1 import main

def test_hello_world(capsys):
    main()
    captured = capsys.readouterr()

    assert captured.out == "Hello World!\n"
