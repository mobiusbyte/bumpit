from gobump.core.config import Configuration
from tests import fixture_path
import pytest


class TestConfig:
    def test_config(self):
        config = Configuration.parse(file=fixture_path("config/.gobump.yaml"))

        assert config.current_version == "0.0.1"
        assert config.tracked_files == ["setup.py", "sample/VERSION"]

    def test_config_invalid(self):
        with pytest.raises(ValueError):
            Configuration.parse(file=fixture_path("/dev/null"))
