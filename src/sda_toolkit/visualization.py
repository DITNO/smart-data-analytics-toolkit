# """
# visualization.py — Visualization Module (Hour 11-14)
#
# Charting functions that create matplotlib figures from DataFrame
# columns. Each function either saves the chart to disk (save_path)
# or displays it interactively (plt.show()).
#
# FIX: All functions now use `plt.close(fig)` instead of bare
# `plt.close()`. The bare call closes whichever figure matplotlib
# considers "current," which can be the wrong figure when multiple
# figures are open (e.g. during testing or in notebooks). Passing
# the explicit figure reference guarantees we close exactly what
# we created.
#
# Note: These functions are reused by the Streamlit dashboard (app.py)
# which has its own chart wrappers that return figures for st.pyplot().
# """

import matplotlib.pyplot as plt


def bar_chart(df, x, y, save_path=None):
    """Bar chart: x=categorical, y=numeric."""
    fig, ax = plt.subplots()
    ax.bar(df[x], df[y])
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(f'{x} vs {y}')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
        plt.close(fig)   # FIXED: was bare plt.close()
    else:
        plt.show()
        plt.close(fig)   # FIXED: was bare plt.close()


def line_chart(df, x, y, save_path=None):
    """Line chart: x=numeric/ordered, y=numeric."""
    fig, ax = plt.subplots()
    ax.plot(df[x], df[y])
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(f'{x} vs {y}')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
        plt.close(fig)
    else:
        plt.show()
        plt.close(fig)


def histogram(df, column, bins=20, save_path=None):
    """Histogram: distribution of a single numeric column."""
    fig, ax = plt.subplots()
    ax.hist(df[column], bins=bins)
    ax.set_xlabel(column)
    ax.set_ylabel('Frequency')
    ax.set_title(f'Distribution of {column}')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
        plt.close(fig)
    else:
        plt.show()
        plt.close(fig)


def scatter_plot(df, x, y, save_path=None):
    """Scatter plot: x vs y (both numeric)."""
    fig, ax = plt.subplots()
    ax.scatter(df[x], df[y])
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(f'Scatter plot {x} vs {y}')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
        plt.close(fig)
    else:
        plt.show()
        plt.close(fig)


def pie_chart(df, column, save_path=None):
    """Pie chart: proportional breakdown of a categorical column."""
    fig, ax = plt.subplots()
    counts = df[column].value_counts()
    ax.pie(counts, labels=counts.index, autopct='%1.1f%%')
    ax.set_title(f'Pie Chart — {column}')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
        plt.close(fig)
    else:
        plt.show()
        plt.close(fig)
