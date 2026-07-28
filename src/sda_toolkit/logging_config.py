# """
# logging_config.py — Logging & Configuration Module (Hour 20-22)
#
# - setup_logging() : configures Python's root logger with a file
#                     handler and a stream (console) handler.
# - load_config()   : loads toolkit settings from a YAML file.
# """
import logging
import yaml


def setup_logging(level="INFO", log_file="logs/sda_toolkit.log"):
    """
    Configure Python's root logger with file + stream handlers.

    Creates the log directory if it doesn't exist. Clears any
    pre-existing handlers first so that calling this function
    multiple times works correctly (unlike logging.basicConfig()
    which is a no-op on subsequent calls).

    FIX: Originally used logging.basicConfig() which only works
    ONCE per Python process. Any subsequent call is silently
    ignored, making it impossible to reconfigure logging in tests
    or long-running apps. Replaced with direct root logger setup
    that clears old handlers and installs new ones every time.
    """
    from pathlib import Path
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)

    # FIXED: Clear existing handlers so this function can be called
    # multiple times (e.g. during testing). basicConfig() would
    # silently do nothing on the second call.
    root = logging.getLogger()
    for handler in list(root.handlers):
        root.removeHandler(handler)
        handler.close()

    # Set up new handlers with a consistent format
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
    """
    Load toolkit configuration from a YAML file.

    Defaults to 'config.yaml' in the project root. Returns a dict
    with keys like 'logging', 'cleaning', 'visualization', 'paths'.
    """
    with open(path, 'r') as f:
        return yaml.safe_load(f)