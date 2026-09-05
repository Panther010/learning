import sys
from app.combined import get_fibonacci_and_abilities

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <integer>")
        sys.exit(1)

    try:
        val = int(sys.argv[1])
        result = get_fibonacci_and_abilities(val)
        print(f"Result: {result}")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)