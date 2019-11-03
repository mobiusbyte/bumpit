import pytest

from bumpit.core.versions.semver.parsers import parse_semver
from bumpit.core.versions.semver.transformers import (
    SemverIncrementingTransformer,
    SemverStaticTransformer,
)


class TestIncrementingTransformer:
    def setup(self):
        self._raw_version = "1.2.3-alpha+exp.sha.5114f85"
        self._transform = SemverIncrementingTransformer()

    @pytest.mark.parametrize(
        "part, expected_version",
        [
            pytest.param("major", "2.0.0"),
            pytest.param("minor", "1.3.0"),
            pytest.param("patch", "1.2.4"),
        ],
    )
    def test_transform(self, part, expected_version):
        new_semver = self._transform(part, parse_semver(self._raw_version))
        assert expected_version == str(new_semver)

    @pytest.mark.parametrize("part", ["pre_release", "build_metadata"])
    def test_transform_invalid_parts(self, part):
        with pytest.raises(ValueError):
            self._transform(part, parse_semver(self._raw_version))


class TestStaticTransformer:
    def setup(self):
        self._raw_version = "1.2.3-alpha+exp.sha.5114f85"
        self._transform = SemverStaticTransformer()

    @pytest.mark.parametrize(
        "part, value, expected_version",
        [
            pytest.param("major", "2", "2.0.0"),
            pytest.param("minor", "3", "1.3.0"),
            pytest.param("patch", "4", "1.2.4"),
            pytest.param("pre_release", "beta", "1.2.3-beta"),
            pytest.param(
                "build_metadata", "exp.sha.9876e54", "1.2.3-alpha+exp.sha.9876e54"
            ),
        ],
    )
    def test_transform(self, part, value, expected_version):
        new_semver = self._transform(part, parse_semver(self._raw_version), value)
        assert expected_version == str(new_semver)

    def test_transform_invalid_part(self):
        with pytest.raises(ValueError):
            self._transform("dummy", parse_semver("2.0.0"), 1)

    def test_transform_invalid_value_for_numerical_part(self):
        with pytest.raises(ValueError):
            self._transform("major", parse_semver("2.0.0"), "a")

    @pytest.mark.parametrize("value", [1, 2])
    def test_transform_non_increasing_numerical_part(self, value):
        with pytest.raises(ValueError):
            self._transform("major", parse_semver("2.0.0"), value)

    @pytest.mark.parametrize("part", ["pre_release", "build_metadata"])
    def test_transform_non_changing_non_numerical_part(self, part):
        version = parse_semver(self._raw_version)
        value = getattr(version, part)

        with pytest.raises(ValueError):
            self._transform(part, version, value)
