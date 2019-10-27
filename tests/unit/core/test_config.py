from bumpit.core.config import Configuration
from tests import fixture_path
import pytest


class TestConfig:
    def test_config_semver(self):
        config = Configuration.parse(file=fixture_path("config/.bumpit-semver.yaml"))

        assert config.current_version == "0.0.1"
        assert config.strategy == "semver-minor"
        assert config.tag
        assert config.tag_format == "{version}"
        assert config.tracked_files == ["setup.py", "sample/VERSION"]

    def test_config_calver(self):
        config = Configuration.parse(file=fixture_path("config/.bumpit-calver.yaml"))

        assert config.current_version == "201910.1"
        assert config.strategy == "calver"
        assert config.tag
        assert config.tag_format == "{version}"
        assert config.tracked_files == ["setup.py", "sample/VERSION"]

    def test_config_missing_fields(self):
        with pytest.raises(ValueError):
            Configuration.parse(file=fixture_path("config/.bumpit-missing-fields.yaml"))

    def test_config_invalid_tag(self):
        with pytest.raises(ValueError):
            Configuration.parse(file=fixture_path("config/.bumpit-invalid-tag.yaml"))
