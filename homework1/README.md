# CS 4300 — Homework 1

Introduction to Python & Unit Testing.

## Project Structure

```
cs4300/
|-- homework1/
|   |-- src/
|   |   |-- task1.py              # Prints "Hello, World!"
|   |   |-- task2.py              # Variables and data types demo
|   |   |-- task3.py              # If/for/while control structures
|   |   |-- task4.py              # Duck-typed discount calculator with validation
|   |   |-- task5.py              # Book list slicing + student database dict
|   |   |-- task6.py              # Word-count file reader
|   |   |-- task6_read_me.txt     # Text file read by task6.py
|   |   `-- task7.py              # numpy package demonstration
|   |-- tests/
|   |   `-- test_task1.py ... test_task7.py   # one test module per task
|   |-- conftest.py               # makes `src` importable for pytest
|   |-- requirements.txt          # numpy, pytest
|   `-- homework_1.pdf            # Assignment description
|-- homework2/                    # reserved for Homework 2
`-- README.md
```

## Setup

Create and activate a virtual environment, then install dependencies:

```bash
python3 -m venv venv_hw1 --system-site-packages
source venv_hw1/bin/activate
python3 -m pip install -r requirements.txt
```

## Running the Tasks

Each task is a standalone script. Run them from `homework1/`:

```bash
cd homework1
python3 src/task1.py
python3 src/task2.py
python3 src/task3.py
python3 src/task4.py
python3 src/task5.py
python3 src/task6.py
python3 src/task7.py
```

## Running the Tests

From the `homework1/` directory, run the full suite with:

```bash
python3 -m pytest tests/
```

Or run a single task's tests, e.g.:

```bash
python3 -m pytest tests/test_task5.py
```

All tests should pass.

## Task Overview

| Task | File | Description |
|------|------|-------------|
| 1 | `task1.py` | Prints "Hello, World!"; verified via captured stdout |
| 2 | `task2.py` | Demonstrates int, float, str, and bool types (parametrized tests) |
| 3 | `task3.py` | Positive/negative/zero check; primes via for loop; sum 1–100 via while loop |
| 4 | `task4.py` | `calculate_discount` — duck typing + input validation (TypeError/ValueError) |
| 5 | `task5.py` | Book list with slicing; student-name → ID dictionary |
| 6 | `task6.py` | `read_file` counts words; robust I/O and parametrized tests |
| 7 | `task7.py` | numpy wrappers: `round_number`, `log_ten`, `remainder` |
