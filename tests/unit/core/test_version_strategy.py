import pytest

from bumpit.core.version_strategy import (
    new_version,
    SEMVER,
    InvalidVersionPart,
    UnsupportedVersioningStrategy,
    InvalidVersion,
)


@pytest.mark.parametrize(
    "part, current_version, expected_new_version",
    [
        pytest.param("major", "0.0.0", "1.0.0"),
        pytest.param("minor", "0.0.0", "0.1.0"),
        pytest.param("patch", "0.0.0", "0.0.1"),
        pytest.param("major", "10.2.3-DEV-SNAPSHOT", "11.0.0-DEV-SNAPSHOT"),
    ],
)
def test_semantic_versioning(part, current_version, expected_new_version):
    actual_new_version = new_version(
        strategy=SEMVER, current_version=current_version, part=part
    )
    assert expected_new_version == actual_new_version


@pytest.mark.parametrize(
    "strategy, current_version, part, expected_exception",
    [
        pytest.param("dummy", "0.0.0", "major", UnsupportedVersioningStrategy),
        pytest.param(SEMVER, "0.0.0", "dummy", InvalidVersionPart),
        pytest.param(SEMVER, "0.0.dummy", "major", InvalidVersion),
    ],
)
def test_new_version_invalid_params(
    strategy, current_version, part, expected_exception
):
    with pytest.raises(expected_exception):
        new_version(strategy=strategy, current_version=current_version, part=part)
