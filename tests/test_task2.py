import pytest
from src.task2 import main

def test_task2_operations(capsys):
    main()
    captured = capsys.readouterr()

    expected_lines = [
        "5120",
        "32.064875",
        "Architecture is super important!",
        "Architecture iX Xuper important!",
    ]

    output_lines = captured.out.strip().split('\n')

    for i, expected in enumerate(expected_lines):
        assert output_lines[i] == expected, f"Line {i+1} mismatch: expected '{expected}', got '{output_lines[i]}'"

    expected_boolean_output = []
    for x in range(10):
        if x % 2 == 0:
            expected_boolean_output.append("Statement True!")
        else:
            expected_boolean_output.append("Statement False!")

    actual_boolean_section = output_lines[4:14]
    assert actual_boolean_section == expected_boolean_output, f"Boolean loop section mismatch"