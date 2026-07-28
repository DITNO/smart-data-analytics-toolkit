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
    # Clear any existing handlers to allow re-configuration
    root = logging.getLogger()
    for handler in list(root.handlers):
        root.removeHandler(handler)
        handler.close()
    # Configure logging with file + stream handlers
    log_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(log_format)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_format)
    root.setLevel(getattr(logging, level))
    root.addHandler(file_handler)
    root.addHandler(stream_handler)
    logging.info("Logging setup complete")


def load_config(path="config.yaml"):
    with open(path, 'r') as f:
        return yaml.safe_load(f)