from bumpit.core.versions.semver import SemVer
from bumpit.core.versions.transformers import IncrementingTransformer, StaticTransformer


def next_version(strategy, current_version, part, force_value):
    if strategy == "semver":
        version = SemVer.parse(current_version)
        if force_value:
            transform = StaticTransformer()
            return str(transform(part, version, force_value))
        else:
            transform = IncrementingTransformer()
            return str(transform(part, version))

    raise ValueError(f"Unsupported strategy {strategy}")
