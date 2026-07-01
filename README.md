# Smart Data Analytics Toolkit

A command-line Python application that loads, cleans, analyzes, visualizes,
and reports on tabular datasets (CSV / Excel / JSON) — built as a
professional-grade portfolio project ahead of moving into Machine Learning.

> Status: 🚧 Hour 0–2 complete (project scaffold). Build in progress.

## Why this project exists

Rather than working through another disconnected ML tutorial, this project
is meant to mirror what a real data-tooling codebase looks like: a clean
package layout, error handling, logging, tests, a CLI, and documentation —
all built around one coherent use case.

## Features (target scope)

- [ ] Load datasets from CSV, Excel, and JSON with error handling
- [ ] Clean data: duplicates, missing values, datatype fixes
- [ ] Exploratory analysis: summary stats, correlations, value counts
- [ ] Visualizations: bar, line, histogram, scatter, pie
- [ ] Export cleaned data + summary reports
- [ ] Full CLI (`sda load ...`, `sda clean ...`, `sda analyze ...`, etc.)
- [ ] Logging and YAML-based configuration
- [ ] Test suite with pytest

## Project structure

```
smart-data-analytics-toolkit/
├── src/sda_toolkit/       # Application package
│   ├── loader.py          # File loading (CSV/Excel/JSON)
│   ├── cleaning.py        # Data cleaning
│   ├── analysis.py        # Exploratory analysis
│   ├── visualization.py   # Charts
│   ├── report.py          # Report export
│   ├── cli.py             # Command-line interface
│   └── logging_config.py  # Logging & config
├── tests/                 # Test suite
├── data/raw/               # Input datasets (gitignored)
├── data/processed/         # Cleaned output (gitignored)
├── reports/                # Generated reports (gitignored)
├── assets/screenshots/     # README screenshots
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Setup

```bash
git clone <your-repo-url>
cd smart-data-analytics-toolkit
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .                 # installs the `sda` CLI command
```

## Usage

> CLI commands will be documented here once Hour 17–20 (CLI build) is complete.

```bash
sda load data/raw/sample.csv
sda clean data/raw/sample.csv --strategy mean
sda analyze data/raw/sample.csv
sda visualize data/raw/sample.csv --chart bar --column category
sda report data/raw/sample.csv --output reports/
```

## Architecture

> Architecture diagram and module interaction notes go here once the
> pipeline (loader → cleaning → analysis → visualization → report) is wired
> together in the CLI.

## Build log

| Hour  | Milestone                                   | Status |
|-------|----------------------------------------------|--------|
| 0–2   | Setup: repo, venv, structure, requirements    | ✅ |
| 2–5   | File loader                                   | ⬜ |
| 5–8   | Data cleaning                                 | ⬜ |
| 8–11  | Exploratory analysis                          | ⬜ |
| 11–14 | Visualization                                 | ⬜ |
| 14–17 | Report export                                 | ⬜ |
| 17–20 | CLI                                           | ⬜ |
| 20–22 | Logging & configuration                       | ⬜ |
| 22–24 | Testing, docs, screenshots, release            | ⬜ |

## License

MIT
