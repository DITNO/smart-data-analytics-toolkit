# Smart Data Analytics Toolkit

A **CLI + Web** Python application that loads, cleans, analyzes, visualizes,
and reports on tabular datasets (CSV / Excel / JSON). Built as a
professional-grade portfolio project with a full test suite.

🌐 **Try the web app:** Deploy your own copy on [Streamlit Cloud](https://streamlit.io/cloud)
(see [Deployment](#deployment) below).

---

## Quick Start

```bash
git clone https://github.com/DITNO/smart-data-analytics-toolkit.git
cd smart-data-analytics-toolkit
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

### CLI Usage

```bash
# Analyze a dataset
sda analyze data/raw/sample.csv

# Clean a dataset
sda clean data/raw/sample.csv

# Visualize
sda visualize data/raw/sample.csv --chart bar --x city --y salary
sda visualize data/raw/sample.csv --chart histogram --column age

# Generate full report
sda report data/raw/sample.csv
```

### Web Dashboard

```bash
streamlit run app.py
# Opens at http://localhost:8501
```

---

## Features

- ✅ **Load** datasets from CSV, Excel (`.xlsx`/`.xls`), and JSON with error handling
- ✅ **Clean** data: remove duplicates, handle missing values (mean/median/drop/fill), auto-fix data types
- ✅ **Analyze**: summary statistics, correlation matrix, IQR outlier detection, value counts
- ✅ **Visualize**: bar, line, histogram, scatter, and pie charts
- ✅ **Export**: download cleaned CSV + formatted summary report
- ✅ **Web Dashboard**: interactive Streamlit UI (upload → clean → analyze → chart → download)
- ✅ **CLI**: full command-line interface for scripting and automation
- ✅ **Logging & Config**: YAML-based configuration, file + console logging
- ✅ **Tests**: 104 pytest tests covering all modules

---

## Project Structure

```
smart-data-analytics-toolkit/
├── app.py                  # Streamlit web dashboard
├── src/sda_toolkit/
│   ├── loader.py           # File loading (CSV/Excel/JSON)
│   ├── cleaning.py         # Data cleaning
│   ├── analysis.py         # Exploratory analysis
│   ├── visualization.py    # Charts
│   ├── report.py           # Report export
│   ├── cli.py              # CLI entry point
│   └── logging_config.py   # Logging & config
├── tests/                  # 104 pytest tests
├── data/raw/               # Input datasets (gitignored)
├── data/processed/         # Cleaned output (gitignored)
├── reports/                # Generated reports (gitignored)
├── config.yaml             # Default configuration
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## Deployment

### Streamlit Community Cloud (free)

1. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
2. Sign in with your GitHub account
3. Click **"New app"** → select this repository
4. Set **Main file** to `app.py`
5. Click **Deploy**

Once deployed, your app will be live at a URL like:
```
https://YOUR_USERNAME-smart-data-analytics-toolkit.streamlit.app
```

> **Requirements for deployment:** The `streamlit` dependency is already in
> `requirements.txt` and `pyproject.toml`. No additional setup needed.

### Other hosting options

- **Hugging Face Spaces**: Create a Space with Streamlit SDK and point it to this repo
- **Self-hosted**: `streamlit run app.py --server.port 80` behind a reverse proxy

---

## Build Log

| Hour  | Milestone                                   | Status |
|-------|---------------------------------------------|--------|
| 0–2   | Setup: repo, venv, structure, requirements  | ✅ |
| 2–5   | File loader                                 | ✅ |
| 5–8   | Data cleaning                               | ✅ |
| 8–11  | Exploratory analysis                        | ✅ |
| 11–14 | Visualization                               | ✅ |
| 14–17 | Report export                               | ✅ |
| 17–20 | CLI                                         | ✅ |
| 20–22 | Logging & configuration                     | ✅ |
| 22–24 | Testing, docs, screenshots, release         | ✅ |

---

## License

MIT
