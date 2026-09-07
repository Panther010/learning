import pytest

from cfc_assignment.fibonacci import get_fibonacci


@pytest.mark.parametrize(
    ("input_value", "expected"),
    [(0, 0), (1, 1), (2, 1), (5, 5), (10, 55)],
)
def test_get_fibonacci_returns_expected_value(input_value: int, expected: int) -> None:
    assert get_fibonacci(input_value) == expected


@pytest.mark.parametrize("input_value", [-1, "1"])
def test_get_fibonacci_rejects_invalid_input(input_value: object) -> None:
    with pytest.raises(ValueError):
        get_fibonacci(input_value)  # type: ignore[arg-type]
