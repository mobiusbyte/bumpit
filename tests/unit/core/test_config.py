from bumpit.core.config import Configuration
from tests import fixture_path
import pytest


class TestConfig:
    def test_config_semver(self):
        config_file = fixture_path("config/.bumpit-semver.yaml")
        config = Configuration.parse(file=config_file)

        assert config.config_file == config_file
        assert config.current_version == "0.0.1"
        assert config.strategy.name == "semver"
        assert config.strategy.part == "minor"
        assert config.tag.apply
        assert config.tag.format == "{version}"
        assert config.auto_remote_push is False
        assert config.tracked_files == ["setup.py", "sample/VERSION"]
        assert config.base_branch == "master"

    def test_config_calver(self):
        config_file = fixture_path("config/.bumpit-calver.yaml")
        config = Configuration.parse(file=config_file)

        assert config.config_file == config_file
        assert config.current_version == "201910.1.0"
        assert config.strategy.name == "calver"
        assert config.strategy.part == "auto"
        assert config.strategy.version_format == "YYYYMM.MINOR.MICRO"
        assert config.tag.apply
        assert config.tag.format == "{version}"
        assert config.auto_remote_push is False
        assert config.tracked_files == ["setup.py", "sample/VERSION"]
        assert config.base_branch == "master"

    def test_config_custom_base_branch(self):
        config_file = fixture_path("config/.bumpit-custom-base.yaml")
        config = Configuration.parse(file=config_file)

        assert config.base_branch == "main"
        assert config.config_file == config_file
        assert config.current_version == "0.0.1"
        assert config.strategy.name == "semver"
        assert config.strategy.part == "minor"
        assert config.tag.apply
        assert config.tag.format == "{version}"
        assert config.auto_remote_push is False
        assert config.tracked_files == ["setup.py"]

    def test_config_missing_fields(self):
        with pytest.raises(ValueError):
            Configuration.parse(file=fixture_path("config/.bumpit-missing-fields.yaml"))

    def test_config_invalid_tag(self):
        with pytest.raises(ValueError):
            Configuration.parse(file=fixture_path("config/.bumpit-invalid-tag.yaml"))

    def test_config_missing_file(self):
        with pytest.raises(ValueError):
            Configuration.parse(file="/tmp/not-a-file-kaboom")
