from bumpit.core.versions.semver.semver import SemVer
from bumpit.core.versions.semver.transformers import (
    SemverIncrementingTransformer,
    SemverStaticTransformer,
)

SEMVER_STRATEGY = "semver"


def next_semantic_version(current_version, part, force_value, _=None):
    version = SemVer.parse(current_version)
    if force_value is None:
        transform = SemverIncrementingTransformer()
        return str(transform(part, version))
    else:
        transform = SemverStaticTransformer()
        return str(transform(part, version, force_value))
