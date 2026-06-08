from pathlib import Path

def get_project_root() -> Path:
    """
    Find the project root by walking up the directory tree

    Returns:
    --------
    Path
        Absolute path to project root directory
    """
    current = Path(__file__).resolve()

    for parent in current.parents:
        if (parent/ 'pyproject.toml').exists():
            return parent

    raise FileNotFoundError(f"Could not find project root "
                            f"Searched upward from: {current}. "
                            f"Make sure pyproject.toml exists at the project root")

def get_data_dir() -> Path:
    """Return absolute path to <project_root>/data/"""
    return get_project_root() / 'data'

def get_raw_data_dir() -> Path:
    """Return absolute path to <project_root>/data/raw/"""
    return get_data_dir() / 'raw'

def get_processed_data_dir() -> Path:
    """Return absolute path to <project_root>/data/processed"""
    return get_data_dir() / 'processed'
