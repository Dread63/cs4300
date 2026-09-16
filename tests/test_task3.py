import pytest
from src.task3 import positive_negative, print_prime_numbers, sum_one_one_hundred

def test_task3_positive_negative(capsys):
    positive_negative(-10)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Negative"

    positive_negative(0)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Zero"

    positive_negative(10)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Positive"

    positive_negative(-0)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Zero"

    positive_negative(+0)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Zero"

def test_task3_print_prime_numbers(capsys):

    print_prime_numbers()
    captured = capsys.readouterr()
    
    output_lines = captured.out.strip().split('\n')

    assert output_lines == ["2", "3", "5", "7", "11", "13", "17", "19", "23", "29"]

def test_task3_sum_one_one_hundred(capsys):

    sum_one_one_hundred()
    captured = capsys.readouterr()

    assert captured.out.strip() == "5050"
