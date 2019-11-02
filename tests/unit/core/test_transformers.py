import pytest

from bumpit.core.transformers import IncrementingTransformer
from bumpit.core.versions.semver import SemVer


class TestIncrementingTransformer:
    def setup(self):
        self._raw_version = "1.2.3+exp.sha.5114f85"
        self._transform = IncrementingTransformer()

    @pytest.mark.parametrize(
        "part, expected_version",
        [
            pytest.param("major", "2.0.0"),
            pytest.param("minor", "1.3.0"),
            pytest.param("patch", "1.2.4"),
        ],
    )
    def test_incrementing_transformer(self, part, expected_version):
        new_semver = self._transform(part, SemVer.parse(self._raw_version))
        assert expected_version == str(new_semver)

    @pytest.mark.parametrize("part", ["pre_release", "build_metadata"])
    def test_incrementing_transformer_invalid_parts(self, part):
        with pytest.raises(ValueError):
            self._transform(part, SemVer.parse(self._raw_version))
