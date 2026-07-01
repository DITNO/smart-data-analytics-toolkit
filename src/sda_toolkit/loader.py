"""
loader.py — File Loading Module (Hour 2-5)
"""

from pathlib import Path
import pandas as pd

"""
Responsible for loading datasets from CSV, Excel, and JSON sources
into a pandas DataFrame, with error handling for missing files,
bad formats, and encoding issues.

TODO (Hour 2-5):
- load_csv(path) -> pd.DataFrame
- load_excel(path, sheet_name=0) -> pd.DataFrame
- load_json(path) -> pd.DataFrame
- load_file(path) -> pd.DataFrame   # auto-detect by extension
- Custom exceptions: UnsupportedFileTypeError, FileLoadError
"""
def _validate_path(path):
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    return file_path

def load_csv(path):
    file_path = _validate_path(path)
    try:
        df = pd.read_csv(file_path)
        return df
    except pd.errors.EmptyDataError:
        print(f'This csv file is empty: {file_path}')
        return None
    except Exception as e:
        print(f'error something is wrong with the csv file: {e}')
        return None

result = load_csv("data/raw/sample.csv")
print(result)    