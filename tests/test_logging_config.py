"""Tests for the logging_config module."""

import logging
from pathlib import Path
import yaml
import pytest
from sda_toolkit.logging_config import setup_logging, load_config


# Reset root logger between tests to avoid basicConfig() being a no-op
@pytest.fixture(autouse=True)
def reset_logging():
    """Reset the root logger's handlers before each test."""
    root = logging.getLogger()
    for handler in list(root.handlers):
        root.removeHandler(handler)
        handler.close()
    root.setLevel(logging.WARNING)  # reset to default
    # Also remove any configured loggers
    for name in list(logging.root.manager.loggerDict.keys()):
        logger = logging.getLogger(name)
        for handler in list(logger.handlers):
            logger.removeHandler(handler)
            handler.close()
    yield


# --- setup_logging ---

class TestSetupLogging:
    def test_creates_log_file(self, tmp_path):
        log_file = str(tmp_path / "sda.log")
        setup_logging(level="DEBUG", log_file=log_file)
        assert Path(log_file).exists()

    def test_logs_are_written(self, tmp_path):
        log_file = str(tmp_path / "sda.log")
        setup_logging(level="DEBUG", log_file=log_file)
        logging.info("Test log message")
        # Ensure logs are flushed
        for handler in logging.root.handlers:
            handler.flush()
        content = Path(log_file).read_text()
        assert "Test log message" in content

    def test_log_file_includes_level(self, tmp_path):
        log_file = str(tmp_path / "sda.log")
        setup_logging(level="WARNING", log_file=log_file)
        logging.warning("Warning message")
        for handler in logging.root.handlers:
            handler.flush()
        content = Path(log_file).read_text()
        assert "WARNING" in content

    def test_debug_level_not_logged_when_info_level(self, tmp_path):
        log_file = str(tmp_path / "sda.log")
        setup_logging(level="INFO", log_file=log_file)
        logging.debug("Debug message")
        for handler in logging.root.handlers:
            handler.flush()
        content = Path(log_file).read_text()
        assert "Debug message" not in content

    def test_creates_parent_directories(self, tmp_path):
        nested = tmp_path / "sub" / "dir" / "nested.log"
        setup_logging(level="INFO", log_file=str(nested))
        assert nested.exists()

    def test_log_format_contains_timestamp(self, tmp_path):
        log_file = str(tmp_path / "sda.log")
        setup_logging(level="INFO", log_file=log_file)
        logging.info("Check format")
        for handler in logging.root.handlers:
            handler.flush()
        content = Path(log_file).read_text()
        import re
        assert re.search(r"\d{4}-\d{2}-\d{2}", content)

    def test_log_format_contains_level(self, tmp_path):
        log_file = str(tmp_path / "sda.log")
        setup_logging(level="INFO", log_file=log_file)
        logging.info("Check level")
        for handler in logging.root.handlers:
            handler.flush()
        content = Path(log_file).read_text()
        assert "INFO" in content


# --- load_config ---

class TestLoadConfig:
    def test_loads_yaml_config(self, tmp_path):
        config = {"logging": {"level": "DEBUG"}, "cleaning": {"strategy": "mean"}}
        config_path = tmp_path / "test_config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)
        result = load_config(str(config_path))
        assert result == config

    def test_returns_dict(self, tmp_path):
        config_path = tmp_path / "test_config.yaml"
        with open(config_path, "w") as f:
            yaml.dump({"key": "value"}, f)
        result = load_config(str(config_path))
        assert isinstance(result, dict)

    def test_handles_empty_config(self, tmp_path):
        config_path = tmp_path / "empty.yaml"
        with open(config_path, "w") as f:
            yaml.dump({}, f)
        result = load_config(str(config_path))
        assert result == {}

    def test_raises_on_missing_file(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            load_config(str(tmp_path / "nonexistent.yaml"))

    def test_loads_project_config(self):
        config = load_config()
        assert isinstance(config, dict)
        assert "logging" in config
        assert "cleaning" in config
        assert "visualization" in config
        assert "paths" in config
