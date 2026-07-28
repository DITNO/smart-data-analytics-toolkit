"""Tests for the visualization module."""

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import pytest
from sda_toolkit.visualization import (
    bar_chart,
    line_chart,
    histogram,
    scatter_plot,
    pie_chart,
)


# Ensure no figures leak between tests
@pytest.fixture(autouse=True)
def close_all_figures():
    """Close all matplotlib figures before each test."""
    plt.close("all")
    yield
    plt.close("all")


@pytest.fixture
def df():
    return pd.DataFrame({
        "city": ["NYC", "LA", "Chicago", "NYC", "LA"],
        "salary": [50000, 60000, 70000, 55000, 65000],
        "age": [25, 30, 35, 40, 45],
        "name": ["A", "B", "C", "D", "E"],
    })


@pytest.fixture
def df_small():
    return pd.DataFrame({
        "x": [1, 2, 3],
        "y": [10, 20, 30],
        "label": ["a", "b", "c"],
    })


@pytest.fixture
def output_dir(tmp_path):
    return tmp_path / "charts"


class TestBarChart:
    def test_saves_to_path(self, df, output_dir):
        output_dir.mkdir()
        save_path = output_dir / "bar.png"
        bar_chart(df, "city", "salary", save_path=str(save_path))
        assert save_path.exists()
        assert save_path.stat().st_size > 0

    def test_creates_figure_and_closes(self, df):
        fig_count_before = len(plt.get_fignums())
        bar_chart(df, "city", "salary")
        fig_count_after = len(plt.get_fignums())
        assert fig_count_after <= fig_count_before

    def test_type_errors_on_missing_column(self, df):
        with pytest.raises(KeyError):
            bar_chart(df, "nonexistent", "salary")

    def test_type_errors_on_missing_y_column(self, df):
        with pytest.raises(KeyError):
            bar_chart(df, "city", "nonexistent")


class TestLineChart:
    def test_saves_to_path(self, df_small, output_dir):
        output_dir.mkdir()
        save_path = output_dir / "line.png"
        line_chart(df_small, "x", "y", save_path=str(save_path))
        assert save_path.exists()
        assert save_path.stat().st_size > 0

    def test_creates_figure_and_closes(self, df_small):
        fig_count_before = len(plt.get_fignums())
        line_chart(df_small, "x", "y")
        fig_count_after = len(plt.get_fignums())
        assert fig_count_after <= fig_count_before

    def test_type_errors_on_missing_column(self, df_small):
        with pytest.raises(KeyError):
            line_chart(df_small, "x", "missing")

    def test_single_point(self, output_dir):
        output_dir.mkdir()
        df = pd.DataFrame({"x": [1], "y": [10]})
        save_path = output_dir / "single_line.png"
        line_chart(df, "x", "y", save_path=str(save_path))
        assert save_path.exists()


class TestHistogram:
    def test_saves_to_path(self, df, output_dir):
        output_dir.mkdir()
        save_path = output_dir / "hist.png"
        histogram(df, "age", bins=5, save_path=str(save_path))
        assert save_path.exists()
        assert save_path.stat().st_size > 0

    def test_default_bins(self, df, output_dir):
        output_dir.mkdir()
        save_path = output_dir / "hist_default.png"
        histogram(df, "age", save_path=str(save_path))
        assert save_path.exists()

    def test_creates_figure_and_closes(self, df):
        fig_count_before = len(plt.get_fignums())
        histogram(df, "age")
        fig_count_after = len(plt.get_fignums())
        assert fig_count_after <= fig_count_before

    def test_type_errors_on_missing_column(self, df):
        with pytest.raises(KeyError):
            histogram(df, "nonexistent")


class TestScatterPlot:
    def test_saves_to_path(self, df, output_dir):
        output_dir.mkdir()
        save_path = output_dir / "scatter.png"
        scatter_plot(df, "age", "salary", save_path=str(save_path))
        assert save_path.exists()
        assert save_path.stat().st_size > 0

    def test_creates_figure_and_closes(self, df):
        fig_count_before = len(plt.get_fignums())
        scatter_plot(df, "age", "salary")
        fig_count_after = len(plt.get_fignums())
        assert fig_count_after <= fig_count_before

    def test_type_errors_on_missing_x(self, df):
        with pytest.raises(KeyError):
            scatter_plot(df, "missing", "salary")

    def test_type_errors_on_missing_y(self, df):
        with pytest.raises(KeyError):
            scatter_plot(df, "age", "missing")


class TestPieChart:
    def test_saves_to_path(self, df, output_dir):
        output_dir.mkdir()
        save_path = output_dir / "pie.png"
        pie_chart(df, "city", save_path=str(save_path))
        assert save_path.exists()
        assert save_path.stat().st_size > 0

    def test_creates_figure_and_closes(self, df):
        fig_count_before = len(plt.get_fignums())
        pie_chart(df, "city")
        fig_count_after = len(plt.get_fignums())
        assert fig_count_after <= fig_count_before

    def test_type_errors_on_missing_column(self, df):
        with pytest.raises(KeyError):
            pie_chart(df, "nonexistent")


class TestCleanup:
    def test_no_leaked_figures(self, df):
        bar_chart(df, "city", "salary")
        line_chart(df, "age", "salary")
        histogram(df, "age")
        scatter_plot(df, "age", "salary")
        pie_chart(df, "city")
        assert len(plt.get_fignums()) == 0
