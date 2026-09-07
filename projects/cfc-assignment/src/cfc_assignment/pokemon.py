import requests

POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/pokemon/"

def get_pokemon_abilities(pokemon_id: int) -> list[str]:
    """
    Fetch a Pokemon's ability from the PokeAPI

    Args:
        pokemon_id (int): pokemon id non-negative integer

    Return:
        list[str]: List of pokemon abilities

    Raises:
        ValueError: If pokemon_id is non integer or a negative value or no pokemon with id exist
        RuntimeError: If the API request fails for any other reason
    """

    if not isinstance(pokemon_id, int):
        raise ValueError("Input ID must be an integer.")

    if pokemon_id < 0:
        raise ValueError("Input ID must be a non-negative integer.")

    try:
        response = requests.get(f"{POKEAPI_BASE_URL}{pokemon_id}", timeout=10)
        response.raise_for_status()

        return [ability["ability"]["name"] for ability in response.json()["abilities"]]
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            raise ValueError(f"Pokemon ID {pokemon_id} not found") from e
        raise RuntimeError(f"API request failed: {e}") from e
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Network error: {e}") from e