# """
# cli.py — Command Line Interface (Hour 17-20)

# TODO (Hour 17-20):
# - Build argparse interface with subcommands:
#     sda load <file>
#     sda clean <file> --strategy mean
#     sda analyze <file>
#     sda visualize <file> --chart bar --column X
#     sda report <file> --output reports/
# - Wire together loader -> cleaning -> analysis -> visualization -> report
# - Entry point: main()
# """

# def main():
#     raise NotImplementedError("CLI will be implemented in Hour 17-20")



import argparse
from sda_toolkit import loader, cleaning, analysis, visualization, report

def main():
    parser = argparse.ArgumentParser(description="Smart Data Analytics Toolkit")
    parser.add_argument("command", help="analyze, clean, visualize, report")
    parser.add_argument("file", help="Path to data file")
    parser.add_argument("--chart", help="Chart type: bar, line, histogram, scatter, pie")
    parser.add_argument("--column", help="Column name")
    parser.add_argument("--x", help="X axis column")
    parser.add_argument("--y", help="Y axis column")
    args = parser.parse_args()

    if args.command == "analyze":
        df = loader.load_file(args.file)
        analysis.summary_stats(df)
        analysis.correlation_matrix(df)
        analysis.value_counts_report(df)

    elif args.command == "clean":
        df = loader.load_file(args.file)
        df = cleaning.drop_duplicates(df)
        df = cleaning.handle_missing(df)
        df = cleaning.fix_dtype(df)
        print("Cleaning complete")

    elif args.command == "visualize":
        df = loader.load_file(args.file)
        if args.chart == "bar":
            visualization.bar_chart(df, args.x, args.y)
        elif args.chart == "line":
            visualization.line_chart(df, args.x, args.y)
        elif args.chart == "histogram":
            visualization.histogram(df, args.column)
        elif args.chart == "scatter":
            visualization.scatter_plot(df, args.x, args.y)
        elif args.chart == "pie":
            visualization.pie_chart(df, args.column)
        else:
            print("Specify --chart: bar, line, histogram, scatter, pie")

    elif args.command == "report":
        df = loader.load_file(args.file)
        stats = analysis.summary_stats(df)
        report.bundle_report(df, stats, "reports/")

    else:
        print("Unknown command. Use: analyze, clean, visualize, report")


if __name__ == "__main__":
    main()