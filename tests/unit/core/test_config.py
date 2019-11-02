from bumpit.core.config import Configuration, Strategy
from tests import fixture_path
import pytest


class TestStrategy:
    @pytest.mark.parametrize("name", [None, ""])
    def test_load_invalid_name(self, name):
        with pytest.raises(ValueError):
            Strategy.load({"name": name, "part": "minor"})

    def test_load_missing_name(self):
        with pytest.raises(ValueError):
            Strategy.load({"part": "minor"})

    def test_load_invalid_part(self):
        with pytest.raises(ValueError):
            Strategy.load({"name": "semver", "part": None})

    def test_load_missing_part(self):
        with pytest.raises(ValueError):
            Strategy.load({"name": "semver"})

    def test_eq(self):
        lhs = Strategy(name="semver", part="minor")
        rhs = Strategy(name="semver", part="minor")

        assert lhs == rhs


class TestConfig:
    def test_config_semver(self):
        config_file = fixture_path("config/.bumpit-semver.yaml")
        config = Configuration.parse(file=config_file)

        assert config.config_file == config_file
        assert config.current_version == "0.0.1"
        assert config.strategy.name == "semver"
        assert config.strategy.part == "minor"
        assert config.tag
        assert config.tag_format == "{version}"
        assert config.auto_remote_push is False
        assert config.tracked_files == ["setup.py", "sample/VERSION"]

    def test_config_calver(self):
        config_file = fixture_path("config/.bumpit-calver.yaml")
        config = Configuration.parse(file=config_file)

        assert config.config_file == config_file
        assert config.current_version == "201910.1.0"
        assert config.strategy.name == "calver"
        assert config.strategy.part == ""
        assert config.tag
        assert config.tag_format == "{version}"
        assert config.auto_remote_push is False
        assert config.tracked_files == ["setup.py", "sample/VERSION"]

    def test_config_missing_fields(self):
        with pytest.raises(ValueError):
            Configuration.parse(file=fixture_path("config/.bumpit-missing-fields.yaml"))

    def test_config_invalid_tag(self):
        with pytest.raises(ValueError):
            Configuration.parse(file=fixture_path("config/.bumpit-invalid-tag.yaml"))

    def test_config_missing_file(self):
        with pytest.raises(ValueError):
            Configuration.parse(file="/tmp/not-a-file-kaboom")
