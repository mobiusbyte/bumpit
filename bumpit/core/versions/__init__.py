from bumpit.core.versions.calver.parsers import parse_calver
from bumpit.core.versions.calver.transformers import (
    CalverIncrementingTransformer,
    CalverStaticTransformer,
)
from bumpit.core.versions.semver.parsers import parse_semver
from bumpit.core.versions.semver.transformers import (
    SemverIncrementingTransformer,
    SemverStaticTransformer,
)
from bumpit.core.versions.strategy import Strategy


CALVER_STRATEGY = "calver"
SEMVER_STRATEGY = "semver"


def next_version(strategy_settings, part, force_value):
    delegate = _resolve_strategy(strategy_settings.target_strategy)

    version = delegate.version_parser(
        strategy_settings.current_version, strategy_settings.version_format
    )
    if force_value is None:
        bumped_version = delegate.increment_transform(part, version)
    else:
        bumped_version = delegate.static_transform(part, version, force_value)

    return str(bumped_version)


def _resolve_strategy(target_strategy):
    if target_strategy == CALVER_STRATEGY:
        return Strategy(
            name=CALVER_STRATEGY,
            increment_transform=CalverIncrementingTransformer(),
            static_transform=CalverStaticTransformer(),
            version_parser=parse_calver,
        )
    elif target_strategy == SEMVER_STRATEGY:
        return Strategy(
            name=SEMVER_STRATEGY,
            increment_transform=SemverIncrementingTransformer(),
            static_transform=SemverStaticTransformer(),
            version_parser=parse_semver,
        )

    raise ValueError(f"Unsupported strategy {target_strategy}.")
