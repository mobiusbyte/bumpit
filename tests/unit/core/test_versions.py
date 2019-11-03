from datetime import date

import pytest
from freezegun import freeze_time

from bumpit.core.versions import next_version, SEMVER_STRATEGY, CALVER_STRATEGY
from bumpit.core.versions.strategy import StrategySettings


def test_next_version_semver():
    expected_next_version = "2.0.0"
    actual_next_version = next_version(
        strategy_settings=StrategySettings(
            target_strategy=SEMVER_STRATEGY,
            current_version="1.2.3-alpha+exp.sha.1234f56",
            version_format=None,
        ),
        part="major",
        force_value=None,
    )
    assert expected_next_version == actual_next_version


def test_next_version_calver():
    expected_next_version = "2019.11.03"
    with freeze_time(date(2019, 11, 3)):
        actual_next_version = next_version(
            strategy_settings=StrategySettings(
                target_strategy=CALVER_STRATEGY,
                current_version="2019.11.02",
                version_format="YYYY.0M.0D",
            ),
            part="date",
            force_value=None,
        )
    assert expected_next_version == actual_next_version


def test_next_version_unsupported_strategy():
    with pytest.raises(ValueError):
        next_version(
            strategy_settings=StrategySettings(
                target_strategy="dummy", current_version="1.0.0", version_format=""
            ),
            part="minor",
            force_value="2",
        )
