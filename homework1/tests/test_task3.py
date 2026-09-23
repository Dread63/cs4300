import pytest

from src.task3 import (
    is_prime,
    positive_negative,
    print_prime_numbers,
    sum_one_one_hundred,
)


@pytest.mark.parametrize(
    "number, expected",
    [
        (1, "Positive"),      # smallest positive integer boundary
        (-1, "Negative"),     # smallest negative integer boundary
        (0, "Zero"),
        (0.5, "Positive"),    # non-integer values
        (-0.5, "Negative"),
        (7, "Positive"),
        (-10, "Negative"),
    ],
    ids=["+1", "-1", "0", "+0.5", "-0.5", "+7", "-10"],
)
def test_positive_negative(number, expected, capsys):
    positive_negative(number)
    captured = capsys.readouterr()
    assert captured.out.strip() == expected


def test_is_prime():
    assert is_prime(2)       # smallest prime
    assert is_prime(3)
    assert not is_prime(1)   # 1 is not prime by definition
    assert not is_prime(0)
    assert not is_prime(-5)  # negatives are never prime


def test_print_prime_numbers(capsys):
    print_prime_numbers()
    captured = capsys.readouterr()
    output_lines = captured.out.strip().split("\n")

    assert output_lines == ["2", "3", "5", "7", "11", "13", "17", "19", "23", "29"]


def test_sum_one_one_hundred(capsys):
    sum_one_one_hundred()
    captured = capsys.readouterr()
    assert captured.out.strip() == "5050"
