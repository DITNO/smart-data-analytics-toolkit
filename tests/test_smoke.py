"""
Smoke test — confirms the package imports correctly.
Real tests for each module get added as they're built (Hour 22-24).
"""
import sda_toolkit


def test_package_has_version():
    assert hasattr(sda_toolkit, "__version__")
    assert isinstance(sda_toolkit.__version__, str)
