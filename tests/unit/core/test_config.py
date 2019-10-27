from gobump.core.config import Configuration
from tests import fixture_path


class TestConfig:
    def test_config(self):
        config = Configuration.parse(file=fixture_path("config/.gobump.yaml"))

        assert config.version == "0.0.1"
        assert config.tracked_files == ["setup.py", "sample/VERSION"]
