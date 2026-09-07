from .pokemon import get_pokemon_abilities
from .fibonacci import get_fibonacci

def get_fibonacci_and_abilities(n: int) -> dict:
    """
    Return both the nth Fibonacci number and a pokemon's abilities for the pokemon_id = n input.

    Args:
        n (int): Input value, Must be non-negative positive used for both
            - Index for fibonacci number calculation.
            - Pokemon ID to look up

    Returns:
        dict: {
            "input": int,
            "fibonacci": int,
            "pokemon_abilities": list[str]
        }
    """
    return {
        "input" : n,
        "fibonacci" : get_fibonacci(n),
        "pokemon_abilities": get_pokemon_abilities(n)
    }