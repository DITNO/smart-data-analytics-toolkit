import pytest
import pandas as pd
from sda_toolkit.loader import load_csv, load_file, FileLoadError, UnsupportedFileTypeError

def test_load_csv_return_df():
    df = load_csv("data/raw/sample.csv")
    assert isinstance(df, pd.DataFrame)

def test_load_csv_has_correct_rows():
    df = load_csv("data/raw/sample.csv")
    assert list(df.columns) == ['name','age','city','salary']

def test_load_csv_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        load_csv("data/raw/missing.csv")

def test_load_file_unsupported_extension_raises(tmp_path):
    bad_file = tmp_path / "data.txt"
    bad_file.write_text("some text")
    with pytest.raises(UnsupportedFileTypeError):
        load_file(str(bad_file))