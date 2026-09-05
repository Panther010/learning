def get_fibonacci(n: int) -> int:
    """
    Calculate and return the nth Fibonacci number (0-indexed).

    Args:
        n (int) Given input value. Input must be integer and non-negative.

    Returns:
        int: Fibonacci number for give input value.

    Raises:
        ValueError: If invalid(string/negative) input is given.
    """
    if not isinstance(n, int):
        raise ValueError("Input must be an integer.")

    if n < 0:
        raise ValueError("Input must be a non-negative integer.")

    if n == 0:
        return 0
    if n == 1:
        return 1

    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr

    return curr