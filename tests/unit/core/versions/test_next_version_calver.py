from datetime import date

import pytest
from freezegun import freeze_time

from bumpit.core.versions import next_version, CALVER_STRATEGY
from bumpit.core.versions.strategy import StrategySettings


@pytest.mark.parametrize(
    "part, force_value, expected_next_version",
    [
        pytest.param("date", None, "202001.0.0.0."),
        pytest.param("major", None, "201910.2.0.0."),
        pytest.param("minor", None, "201910.1.11.0."),
        pytest.param("micro", None, "201910.1.10.101."),
        pytest.param("date", date(2019, 11, 9), "201911.0.0.0."),
        pytest.param("auto", None, "202001.0.0.0."),
        pytest.param("major", "9", "201910.9.0.0."),
        pytest.param("minor", "19", "201910.1.19.0."),
        pytest.param("micro", "109", "201910.1.10.109."),
        pytest.param("modifier", "def", "201910.1.10.100.def"),
    ],
)
def test_next_calendar_version(part, force_value, expected_next_version):
    today = date(2020, 1, 1)
    with freeze_time(today):
        actual_new_version = next_version(
            strategy_settings=StrategySettings(
                target_strategy=CALVER_STRATEGY,
                current_version="201910.1.10.100.abc",
                version_format="YYYY0M.MAJOR.MINOR.MICRO.MODIFIER",
            ),
            part=part,
            force_value=force_value,
        )
        assert expected_next_version == actual_new_version
