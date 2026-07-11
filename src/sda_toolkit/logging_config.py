# """
# logging_config.py — Logging & Configuration Module (Hour 20-22)

# TODO (Hour 20-22):
# - setup_logging(level="INFO", log_file="logs/sda_toolkit.log")
# - load_config(path="config.yaml") -> dict
# - Sensible defaults if no config file is present
# """
import logging
import yaml


def setup_logging(level = "INFO", log_file="logs/sda_toolkit.log"):
    from pathlib import Path
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=getattr(logging, level),
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    logging.info("Logging setup complete")


def load_config(path="config.yaml"):
    with open(path, 'r') as f:
        return yaml.safe_load(f)