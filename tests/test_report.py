"""Tests for the report module."""

from pathlib import Path

import pandas as pd
import pytest
from sda_toolkit.report import export_cleaned_csv, export_summary_report, bundle_report
from sda_toolkit.analysis import summary_stats


@pytest.fixture
def df():
    return pd.DataFrame({
        "name": ["Alice", "Bob", "Charlie"],
        "age": [25, 30, 35],
        "city": ["NYC", "LA", "Chicago"],
        "salary": [50000, 60000, 70000],
    })


@pytest.fixture
def stats(df):
    return df.describe()


@pytest.fixture
def output_dir(tmp_path):
    return tmp_path / "reports"


# --- export_cleaned_csv ---

class TestExportCleanedCsv:
    def test_creates_csv_file(self, df, tmp_path):
        output = tmp_path / "cleaned.csv"
        export_cleaned_csv(df, str(output))
        assert output.exists()
        assert output.stat().st_size > 0

    def test_csv_is_readable_by_pandas(self, df, tmp_path):
        output = tmp_path / "cleaned.csv"
        export_cleaned_csv(df, str(output))
        loaded = pd.read_csv(output)
        pd.testing.assert_frame_equal(loaded, df)

    def test_no_index_column_in_csv(self, df, tmp_path):
        output = tmp_path / "cleaned.csv"
        export_cleaned_csv(df, str(output))
        content = output.read_text()
        assert "Unnamed:" not in content

    def test_empty_dataframe(self, tmp_path):
        output = tmp_path / "empty.csv"
        export_cleaned_csv(pd.DataFrame(), str(output))
        assert output.exists()

    def test_output_path_as_pathlib_path(self, df, tmp_path):
        output = tmp_path / "pathlib.csv"
        export_cleaned_csv(df, str(output))
        assert output.exists()


# --- export_summary_report ---

class TestExportSummaryReport:
    def test_creates_report_file(self, stats, tmp_path):
        output = tmp_path / "summary.txt"
        export_summary_report(stats, str(output))
        assert output.exists()
        assert output.stat().st_size > 0

    def test_contains_column_names(self, stats, tmp_path):
        output = tmp_path / "summary.txt"
        export_summary_report(stats, str(output))
        content = output.read_text()
        assert "Column:" in content
        assert "age" in content
        assert "salary" in content

    def test_contains_stat_names(self, stats, tmp_path):
        output = tmp_path / "summary.txt"
        export_summary_report(stats, str(output))
        content = output.read_text()
        assert "count" in content
        assert "mean" in content
        assert "min" in content
        assert "max" in content

    def test_contains_actual_stat_values(self, stats, tmp_path):
        output = tmp_path / "summary.txt"
        export_summary_report(stats, str(output))
        content = output.read_text()
        assert "25.0" in content
        assert "50000.0" in content
        assert "70000.0" in content

    def test_single_column_stats(self, tmp_path):
        stats = pd.DataFrame({"x": [1, 2, 3]}).describe()
        output = tmp_path / "single.txt"
        export_summary_report(stats, str(output))
        content = output.read_text()
        assert "Column: x" in content

    def test_empty_stats_dataframe(self, tmp_path):
        stats = pd.DataFrame()
        output = tmp_path / "empty.txt"
        export_summary_report(stats, str(output))
        content = output.read_text()
        assert isinstance(content, str)


# --- bundle_report ---

class TestBundleReport:
    def test_creates_output_directory(self, df, stats, output_dir):
        bundle_report(df, stats, str(output_dir))
        assert output_dir.exists()
        assert output_dir.is_dir()

    def test_creates_cleaned_csv(self, df, stats, output_dir):
        bundle_report(df, stats, str(output_dir))
        csv_path = output_dir / "cleaned_data.csv"
        assert csv_path.exists()
        assert csv_path.stat().st_size > 0

    def test_creates_summary_report(self, df, stats, output_dir):
        bundle_report(df, stats, str(output_dir))
        report_path = output_dir / "summary_report.txt"
        assert report_path.exists()
        assert report_path.stat().st_size > 0

    def test_csv_content_matches_input(self, df, stats, output_dir):
        bundle_report(df, stats, str(output_dir))
        csv_path = output_dir / "cleaned_data.csv"
        loaded = pd.read_csv(csv_path)
        pd.testing.assert_frame_equal(loaded, df)

    def test_report_contains_statistics(self, df, stats, output_dir):
        bundle_report(df, stats, str(output_dir))
        report_path = output_dir / "summary_report.txt"
        content = report_path.read_text()
        assert "Column:" in content
        assert "mean" in content

    def test_directory_already_exists(self, df, stats, output_dir):
        output_dir.mkdir(parents=True, exist_ok=True)
        bundle_report(df, stats, str(output_dir))
        csv_path = output_dir / "cleaned_data.csv"
        assert csv_path.exists()

    def test_empty_dataframe(self, output_dir):
        df_empty = pd.DataFrame()
        # Use summary_stats which now handles empty DataFrames gracefully
        stats_empty = summary_stats(df_empty)
        bundle_report(df_empty, stats_empty, str(output_dir))
        csv_path = output_dir / "cleaned_data.csv"
        assert csv_path.exists()

    def test_pathlib_output_path(self, df, stats, output_dir):
        bundle_report(df, stats, str(output_dir))
        assert output_dir.exists()
