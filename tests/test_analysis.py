"""Tests for the analysis module."""

import pandas as pd
import pytest
from sda_toolkit.analysis import summary_stats, correlation_matrix, value_counts_report, detect_outliers


@pytest.fixture
def df_numeric():
    return pd.DataFrame({
        "age": [25, 30, 35, 40, 45],
        "salary": [50000, 60000, 70000, 80000, 90000],
        "experience": [2, 5, 8, 12, 15],
    })


@pytest.fixture
def df_mixed():
    return pd.DataFrame({
        "name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
        "age": [25, 30, 35, 40, 45],
        "city": ["NYC", "LA", "Chicago", "NYC", "LA"],
        "salary": [50000, 60000, 70000, 80000, 90000],
    })


@pytest.fixture
def df_with_outliers():
    return pd.DataFrame({
        "value": [10, 12, 11, 13, 14, 100, 12, 11, 10, 14, 8],
    })


@pytest.fixture
def df_no_outliers():
    return pd.DataFrame({
        "value": [10, 11, 12, 13, 14, 11, 12, 10, 14],
    })


@pytest.fixture
def df_empty():
    return pd.DataFrame()


# --- summary_stats ---

class TestSummaryStats:
    def test_returns_dataframe(self, df_numeric):
        result = summary_stats(df_numeric)
        assert isinstance(result, pd.DataFrame)

    def test_includes_count_and_mean(self, df_numeric):
        result = summary_stats(df_numeric)
        assert "count" in result.index
        assert "mean" in result.index

    def test_includes_all_numeric_columns(self, df_numeric):
        result = summary_stats(df_numeric)
        assert "age" in result.columns
        assert "salary" in result.columns
        assert "experience" in result.columns

    def test_excludes_non_numeric_columns(self, df_mixed):
        result = summary_stats(df_mixed)
        assert "name" not in result.columns
        assert "city" not in result.columns
        assert "age" in result.columns
        assert "salary" in result.columns

    def test_mean_value_is_correct(self, df_numeric):
        result = summary_stats(df_numeric)
        assert result.loc["mean", "age"] == 35.0
        assert result.loc["mean", "salary"] == 70000.0

    def test_count_is_correct(self, df_numeric):
        result = summary_stats(df_numeric)
        assert result.loc["count", "age"] == 5.0

    def test_empty_dataframe_returns_empty_stats(self, df_empty):
        result = summary_stats(df_empty)
        assert result.empty


# --- correlation_matrix ---

class TestCorrelationMatrix:
    def test_returns_dataframe(self, df_numeric):
        result = correlation_matrix(df_numeric)
        assert isinstance(result, pd.DataFrame)

    def test_square_matrix(self, df_numeric):
        result = correlation_matrix(df_numeric)
        assert result.shape[0] == result.shape[1]

    def test_diagonal_is_one(self, df_numeric):
        result = correlation_matrix(df_numeric)
        for col in result.columns:
            assert result.loc[col, col] == pytest.approx(1.0)

    def test_symmetric(self, df_numeric):
        result = correlation_matrix(df_numeric)
        for i in range(len(result.columns)):
            for j in range(len(result.columns)):
                assert result.iloc[i, j] == pytest.approx(result.iloc[j, i])

    def test_positive_correlation_age_experience(self, df_numeric):
        result = correlation_matrix(df_numeric)
        assert result.loc["age", "experience"] > 0.9

    def test_excludes_non_numeric(self, df_mixed):
        result = correlation_matrix(df_mixed)
        assert "name" not in result.columns
        assert "city" not in result.columns

    def test_single_column(self):
        df = pd.DataFrame({"x": [1, 2, 3]})
        result = correlation_matrix(df)
        assert result.shape == (1, 1)
        assert result.loc["x", "x"] == pytest.approx(1.0)

    def test_empty_dataframe(self, df_empty):
        result = correlation_matrix(df_empty)
        assert result.empty


# --- value_counts_report ---

class TestValueCountsReport:
    def test_returns_dict(self, df_mixed):
        result = value_counts_report(df_mixed)
        assert isinstance(result, dict)

    def test_has_all_columns_as_keys(self, df_mixed):
        result = value_counts_report(df_mixed)
        assert sorted(result.keys()) == sorted(df_mixed.columns.tolist())

    def test_each_value_is_series(self, df_mixed):
        result = value_counts_report(df_mixed)
        for col in df_mixed.columns:
            assert isinstance(result[col], pd.Series)

    def test_counts_sum_to_row_count(self, df_mixed):
        result = value_counts_report(df_mixed)
        for col in df_mixed.columns:
            assert result[col].sum() == len(df_mixed)

    def test_city_counts_are_correct(self, df_mixed):
        result = value_counts_report(df_mixed)
        assert result["city"]["NYC"] == 2
        assert result["city"]["LA"] == 2
        assert result["city"]["Chicago"] == 1

    def test_empty_dataframe(self, df_empty):
        result = value_counts_report(df_empty)
        assert result == {}

    def test_single_column_dataframe(self):
        df = pd.DataFrame({"x": [1, 1, 2]})
        result = value_counts_report(df)
        assert result["x"][1] == 2
        assert result["x"][2] == 1


# --- detect_outliers ---

class TestDetectOutliers:
    def test_returns_dict(self, df_with_outliers):
        result = detect_outliers(df_with_outliers)
        assert isinstance(result, dict)

    def test_detects_outlier_in_noisy_data(self, df_with_outliers):
        result = detect_outliers(df_with_outliers)
        assert result["value"] > 0

    def test_no_outliers_in_clean_data(self, df_no_outliers):
        result = detect_outliers(df_no_outliers)
        assert result["value"] == 0

    def test_skips_non_numeric_columns(self, df_mixed):
        result = detect_outliers(df_mixed)
        assert "name" not in result
        assert "city" not in result
        assert "age" in result
        assert "salary" in result

    def test_correct_outlier_count_known_data(self):
        # Q1=3.5, Q3=8.5, IQR=5.0, upper fence=16.0 → 20 is outlier, 15 is not
        df = pd.DataFrame({"x": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20]})
        result = detect_outliers(df)
        assert result["x"] == 1

    def test_no_outliers_when_all_within_bounds(self):
        df = pd.DataFrame({"x": [1, 2, 3, 4, 5, 6, 7]})
        result = detect_outliers(df)
        assert result["x"] == 0

    def test_multi_column_outliers(self, df_with_outliers):
        result = detect_outliers(df_with_outliers)
        assert len(result) == 1

    def test_empty_dataframe(self, df_empty):
        result = detect_outliers(df_empty)
        assert result == {}

    def test_single_column_no_outliers(self):
        df = pd.DataFrame({"x": [5, 5, 5, 5]})
        result = detect_outliers(df)
        assert result["x"] == 0
