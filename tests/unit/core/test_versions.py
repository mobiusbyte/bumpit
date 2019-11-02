import pytest
from bumpit.core.versions import next_version, SEMVER_STRATEGY


def test_next_version_semver():
    expected_next_version = "2.0.0"
    actual_next_version = next_version(
        strategy=SEMVER_STRATEGY,
        current_version="1.2.3-alpha+exp.sha.1234f56",
        part="major",
        force_value=None,
    )
    assert expected_next_version == actual_next_version


def test_next_version_unsupported_strategy():
    with pytest.raises(ValueError):
        next_version("dummy", "1.0.0", "minor", "2")
