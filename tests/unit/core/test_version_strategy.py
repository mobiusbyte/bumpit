import pytest

from bumpit.core.version_strategy import (
    new_version,
    InvalidVersionPart,
    UnsupportedVersioningStrategy,
    InvalidVersion,
)


@pytest.mark.parametrize(
    "strategy, current_version, expected_new_version",
    [
        pytest.param("semver-major", "0.0.0", "1.0.0"),
        pytest.param("semver-minor", "0.0.0", "0.1.0"),
        pytest.param("semver-patch", "0.0.0", "0.0.1"),
        pytest.param("semver-major", "10.2.3-DEV-SNAPSHOT", "11.0.0-DEV-SNAPSHOT"),
    ],
)
def test_semantic_versioning(strategy, current_version, expected_new_version):
    actual_new_version = new_version(
        strategy=strategy, current_version=current_version
    )
    assert expected_new_version == actual_new_version


@pytest.mark.parametrize(
    "strategy, current_version, expected_exception",
    [
        pytest.param("dummy", "0.0.0", UnsupportedVersioningStrategy),
        pytest.param("semver-dummy", "0.0.0", InvalidVersionPart),
        pytest.param("semver-major", "0.0.dummy", InvalidVersion),
    ],
)
def test_new_version_invalid_params(
    strategy, current_version, expected_exception
):
    with pytest.raises(expected_exception):
        new_version(strategy=strategy, current_version=current_version)
