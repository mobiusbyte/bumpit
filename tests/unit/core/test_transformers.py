import pytest

from bumpit.core.transformers import IncrementingTransformer
from bumpit.core.versions.semver import SemVer


@pytest.mark.parametrize(
    "part, expected_version",
    [
        pytest.param("major", "2.0.0"),
        pytest.param("minor", "1.3.0"),
        pytest.param("patch", "1.2.4"),
    ],
)
def test_incrementing_transformer(part, expected_version):
    transform = IncrementingTransformer()

    raw_version = "1.2.3+exp.sha.5114f85"
    new_semver = transform(part, SemVer.parse(raw_version))

    assert expected_version == str(new_semver)

