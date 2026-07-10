# """
# report.py — Report Export Module (Hour 14-17)

# TODO (Hour 14-17):
# - export_cleaned_csv(df, output_path)
# - export_summary_report(stats_dict, output_path)   # markdown or txt summary
# - bundle_report(df, charts_dir, output_dir)         # combine charts + summary
# """


def export_cleaned_csv(df, output_path):
    df.to_csv(output_path,index = False)
    print(f'Cleaned csv saved to: {output_path}')



# with open(drawer) as d:     - for the open fnc below
#     put something in drawer
# # drawer closes automatically when you're done


def export_summary_report(stats, output_path):
    content = "\n".join(f"{key}: {value}" for key, value in stats.items())
    with open(output_path, 'w') as f:
        f.write(content)
    print(f"Summary report saved to:{output_path}")


# Whenever a function saves files, ask yourself:

# What folder am I saving into? → that's a parameter
# What should the files be named? → decide that inside the function
# How do I combine folder + filename? → Path(folder) / "filename"


def bundle_report(df, stats, output_dir):
    from pathlib import Path
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    csv_path = Path(output_dir) / "cleaned_data.csv"
    report_path = Path(output_dir) / "summary_report.txt"
    export_cleaned_csv(df, csv_path)
    export_summary_report(stats, report_path)
    print(f"Report bundled in : {output_dir}")
