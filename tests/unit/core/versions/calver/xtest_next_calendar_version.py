from datetime import date

import pytest
from freezegun import freeze_time

from bumpit.core.versions.calver import next_calendar_version


@pytest.mark.parametrize(
    "current_version, current_date, expected_new_version",
    [
        pytest.param("201910.100.1", date(2019, 10, 21), "201910.101.0"),
        pytest.param("201910.100.1", date(2019, 10, 22), "201910.101.0"),
        pytest.param("201910.100.1", date(2019, 11, 1), "201911.0.0"),
        pytest.param("201912.100.1", date(2020, 1, 1), "202001.0.0"),
    ],
)
def test_calendar_versioning_auto_minor(
    current_version, current_date, expected_new_version
):
    with freeze_time(current_date):
        actual_new_version = next_calendar_version(
            current_version=current_version,
            part="MINOR",
            force_value=None,
            version_format="YYYY0M.MINOR.MICRO",
        )
        assert expected_new_version == actual_new_version


@pytest.mark.parametrize(
    "current_version, current_date, expected_new_version",
    [
        pytest.param("201910.100.1", date(2019, 10, 21), "201910.100.2"),
        pytest.param("201910.100.1", date(2019, 10, 22), "201910.100.2"),
        pytest.param("201910.100.1", date(2019, 11, 1), "201911.0.0"),
        pytest.param("201912.100.1", date(2020, 1, 1), "202001.0.0"),
    ],
)
def test_calendar_versioning_auto_micro(
    current_version, current_date, expected_new_version
):
    with freeze_time(current_date):
        actual_new_version = next_calendar_version(
            current_version=current_version,
            part="MICRO",
            force_value=None,
            version_format="YYYY0M.MINOR.MICRO",
        )
        assert expected_new_version == actual_new_version
