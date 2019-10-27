from datetime import date

import pytest
from freezegun import freeze_time

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
    actual_new_version = new_version(strategy=strategy, current_version=current_version)
    assert expected_new_version == actual_new_version


@pytest.mark.parametrize(
    "current_version, current_date, expected_new_version",
    [
        pytest.param("201910.100", date(2019, 10, 21), "201910.101"),
        pytest.param("201910.100", date(2019, 10, 22), "201910.101"),
        pytest.param("201910.100", date(2019, 11, 1), "201911.1"),
        pytest.param("201912.100", date(2020, 1, 1), "202001.1"),
    ],
)
def test_calendar_versioning(current_version, current_date, expected_new_version):
    with freeze_time(current_date):
        actual_new_version = new_version(
            strategy="calver", current_version=current_version
        )
        assert expected_new_version == actual_new_version


@pytest.mark.parametrize(
    "strategy, current_version, expected_exception",
    [
        pytest.param("dummy", "0.0.0", UnsupportedVersioningStrategy),
        pytest.param("semver-dummy", "0.0.0", InvalidVersionPart),
        pytest.param("semver-major", "0.0.dummy", InvalidVersion),
        pytest.param("calver", "dummy.1", InvalidVersion),
    ],
)
def test_new_version_invalid_params(strategy, current_version, expected_exception):
    with pytest.raises(expected_exception):
        new_version(strategy=strategy, current_version=current_version)
