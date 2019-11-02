from bumpit.core.versions.semver import next_semantic_version


def next_version(strategy, current_version, part, force_value):
    if strategy == "semver":
        return next_semantic_version(current_version, part, force_value)

    raise ValueError(f"Unsupported strategy {strategy}")
