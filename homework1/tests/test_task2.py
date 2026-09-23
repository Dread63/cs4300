import pytest

from src.task2 import (
    get_boolean,
    get_floating_point,
    get_integer,
    get_string,
    main,
)


@pytest.mark.parametrize(
    "getter, expected_type",
    [
        (get_integer, int),
        (get_floating_point, float),
        (get_string, str),
        (get_boolean, bool),
    ],
    ids=["int", "float", "str", "bool"],
)
def test_data_types(getter, expected_type):
    # type() rather than isinstance(): bool is a subclass of int, so
    # isinstance(False, int) is True and would pass the wrong type's test.
    assert type(getter()) is expected_type


@pytest.mark.parametrize(
    "getter, expected_value",
    [
        (get_integer, 5),
        (get_floating_point, 5.75),
        (get_string, "Architecture"),
        (get_boolean, False),
    ],
    ids=["int", "float", "str", "bool"],
)
def test_data_type_values(getter, expected_value):
    assert getter() == expected_value


def test_main_output(capsys):
    """
    The demo script still produces its expected printed output.
    """
    main()
    captured = capsys.readouterr()
    output_lines = captured.out.strip().split("\n")

    expected_lines = [
        "5120",
        "32.064875",
        "Architecture is super important!",
        "Architecture iX Xuper important!",
    ]
    assert output_lines[:4] == expected_lines

    expected_boolean_output = [
        "Statement True!" if x % 2 == 0 else "Statement False!" for x in range(10)
    ]
    assert output_lines[4:14] == expected_boolean_output
