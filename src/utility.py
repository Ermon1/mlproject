# src/utility.py
from pathlib import Path
import dill
from src.exception import CustomException

def save_object(file_path: Path, obj: object):
    """Saves an object to a file."""
    try:
        DIR_NAME = file_path.parent
        DIR_NAME.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'wb') as f:
            dill.dump(obj, f)
    except Exception as e:
        raise CustomException(f"Error saving object: {str(e)}")

def load_object(file_path: Path):
    """Loads an object from a file."""
    try:
        with open(file_path, 'rb') as f:
            return dill.load(f)
    except Exception as e:
        raise CustomException(f"Error loading object: {str(e)}")