from bumpit.core.versions.semver import SEMVER_STRATEGY, next_semantic_version
from bumpit.core.versions.calver import CALVER_STRATEGY, next_calendar_version


def next_version(strategy, current_version, part, force_value, version_format):
    delegate = {
        SEMVER_STRATEGY: next_semantic_version,
        CALVER_STRATEGY: next_calendar_version,
    }.get(strategy)

    if delegate:
        return delegate(current_version, part, force_value, version_format)

    raise ValueError(f"Unsupported strategy {strategy}")
