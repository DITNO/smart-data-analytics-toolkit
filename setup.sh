#!/bin/bash
# Streamlit Cloud setup script
# Runs before the app starts to install the local package.
# Without this, 'import sda_toolkit' would fail because Streamlit
# Cloud only runs requirements.txt, not 'pip install -e .'
pip install -e .
