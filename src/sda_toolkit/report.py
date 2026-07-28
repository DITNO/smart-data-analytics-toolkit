# """
# report.py — Report Export Module (Hour 14-17)
#
# Exports cleaned DataFrames and summary statistics to disk:
#   - export_cleaned_csv()    — saves cleaned DataFrame as CSV
#   - export_summary_report() — writes readable stats to a .txt file
#   - bundle_report()         — does both in one call, creating the
#                               output directory if needed
# """


def export_cleaned_csv(df, output_path):
    """
    Save the (cleaned) DataFrame to a CSV file.

    Uses index=False so the row numbers aren't written to the file.
    """
    df.to_csv(output_path, index=False)
    print(f'Cleaned csv saved to: {output_path}')


def export_summary_report(stats, output_path):
    """
    Write summary statistics to a human-readable text file.

    `stats` is expected to be a DataFrame from df.describe().
    Iterates column-by-column and stat-by-stat to produce a
    clean, readable report.

    FIX: The original code used:
        content = "\n".join(f"{key}: {value}" for key, value in stats.items())
    On a DataFrame, .items() yields (column_name, Series) pairs.
    f-string formatting a Series produces a garbled mess. The fix
    iterates properly: for each column, print each stat on its own line.
    """
    lines = ["=== Summary Statistics ===", ""]
    for col_name, col_stats in stats.items():
        lines.append(f"Column: {col_name}")
        lines.append("-" * (len(col_name) + 8))
        for stat_name, stat_value in col_stats.items():
            lines.append(f"  {stat_name}: {stat_value}")
        lines.append("")
    content = "\n".join(lines)
    with open(output_path, 'w') as f:
        f.write(content)
    print(f"Summary report saved to: {output_path}")


def bundle_report(df, stats, output_dir):
    """
    Save both cleaned CSV and summary report into one directory.

    Creates the output directory (and parents) if they don't exist.
    Files are named 'cleaned_data.csv' and 'summary_report.txt'.
    """
    from pathlib import Path
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    csv_path = Path(output_dir) / "cleaned_data.csv"
    report_path = Path(output_dir) / "summary_report.txt"
    export_cleaned_csv(df, csv_path)
    export_summary_report(stats, report_path)
    print(f"Report bundled in : {output_dir}")
