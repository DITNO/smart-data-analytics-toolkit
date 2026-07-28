"""Tests for the cleaning module."""

import pandas as pd
import pytest
from sda_toolkit.cleaning import drop_duplicates, handle_missing, fix_dtype


def _is_string_dtype(dtype):
    """Check if a dtype represents string data (object, str, or StringDtype)."""
    return dtype in [object, pd.StringDtype()] or pd.api.types.is_string_dtype(dtype)


@pytest.fixture
def df_with_duplicates():
    return pd.DataFrame({
        "name": ["Alice", "Bob", "Alice", "Charlie", "Bob"],
        "age": [25, 30, 25, 35, 30],
        "city": ["NYC", "LA", "NYC", "Chicago", "LA"],
    })


@pytest.fixture
def df_with_missing():
    return pd.DataFrame({
        "name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
        "age": [25, None, 35, None, 28],
        "salary": [50000, 60000, None, 55000, 65000],
        "city": ["NYC", "LA", "Chicago", None, "Seattle"],
    })


@pytest.fixture
def df_with_mixed_dtypes():
    return pd.DataFrame({
        "name": ["A", "B", "C", "D"],
        "age_str": ["25", "30", "35", "40"],
        "salary_str": ["50000", "60000", "70000", "80000"],
        "legacy_code": ["X-001", "Y-002", "Z-003", "W-004"],
        "flag": ["yes", "no", "yes", "no"],
    })


@pytest.fixture
def df_clean():
    return pd.DataFrame({
        "name": ["Alice", "Bob", "Charlie"],
        "age": [25, 30, 35],
        "city": ["NYC", "LA", "Chicago"],
    })


# --- drop_duplicates ---

class TestDropDuplicates:
    def test_removes_duplicate_rows(self, df_with_duplicates):
        result = drop_duplicates(df_with_duplicates)
        assert len(result) == 3
        assert result.iloc[0]["name"] == "Alice"
        assert result.iloc[1]["name"] == "Bob"
        assert result.iloc[2]["name"] == "Charlie"

    def test_no_duplicates_returns_same_length(self, df_clean):
        result = drop_duplicates(df_clean)
        assert len(result) == len(df_clean)

    def test_returns_dataframe(self, df_with_duplicates):
        result = drop_duplicates(df_with_duplicates)
        assert isinstance(result, pd.DataFrame)

    def test_preserves_columns(self, df_with_duplicates):
        result = drop_duplicates(df_with_duplicates)
        assert list(result.columns) == list(df_with_duplicates.columns)

    def test_empty_dataframe(self):
        empty = pd.DataFrame()
        result = drop_duplicates(empty)
        assert len(result) == 0


# --- handle_missing ---

class TestHandleMissing:
    def test_drop_strategy_removes_missing_rows(self, df_with_missing):
        result = handle_missing(df_with_missing, strategy="drop")
        assert len(result) < len(df_with_missing)

    def test_drop_strategy_removes_only_rows_with_any_null(self, df_with_missing):
        result = handle_missing(df_with_missing, strategy="drop")
        assert len(result) == 2

    def test_mean_strategy_fills_numeric(self, df_with_missing):
        result = handle_missing(df_with_missing, strategy="mean")
        expected_age_mean = (25 + 35 + 28) / 3
        assert result.loc[1, "age"] == pytest.approx(expected_age_mean, rel=1e-2)
        assert result.loc[3, "age"] == pytest.approx(expected_age_mean, rel=1e-2)

    def test_median_strategy_fills_numeric(self, df_with_missing):
        result = handle_missing(df_with_missing, strategy="median")
        assert result.loc[1, "age"] == 28.0
        assert result.loc[3, "age"] == 28.0

    def test_fill_strategy_fills_with_zero(self, df_with_missing):
        result = handle_missing(df_with_missing, strategy="fill")
        assert result.loc[3, "city"] == 0

    def test_unknown_strategy_returns_original(self, df_with_missing):
        result = handle_missing(df_with_missing, strategy="invalid")
        pd.testing.assert_frame_equal(result, df_with_missing)

    def test_missing_count_reported(self, df_with_missing, capsys):
        handle_missing(df_with_missing, strategy="mean")
        captured = capsys.readouterr()
        assert "missing values before cleaning" in captured.out
        assert "4" in captured.out

    def test_no_missing_values_unchanged(self, df_clean):
        result = handle_missing(df_clean, strategy="mean")
        pd.testing.assert_frame_equal(result, df_clean)


# --- fix_dtype ---

class TestFixDtype:
    def test_converts_numeric_strings_to_numbers(self, df_with_mixed_dtypes):
        result = fix_dtype(df_with_mixed_dtypes)
        assert result["age_str"].dtype in ["int64", "float64"]
        assert result["salary_str"].dtype in ["int64", "float64"]

    def test_keeps_non_numeric_columns_as_non_numeric(self, df_with_mixed_dtypes):
        result = fix_dtype(df_with_mixed_dtypes)
        assert _is_string_dtype(result["name"].dtype)
        assert _is_string_dtype(result["legacy_code"].dtype)
        assert _is_string_dtype(result["flag"].dtype)

    def test_returns_dataframe(self, df_with_mixed_dtypes):
        result = fix_dtype(df_with_mixed_dtypes)
        assert isinstance(result, pd.DataFrame)

    def test_preserves_row_count(self, df_with_mixed_dtypes):
        result = fix_dtype(df_with_mixed_dtypes)
        assert len(result) == len(df_with_mixed_dtypes)
