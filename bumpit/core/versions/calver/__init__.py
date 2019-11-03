from bumpit.core.versions.calver.parsers import parse
from bumpit.core.versions.calver.transformers import (
    CalverIncrementingTransformer,
    CalverStaticTransformer,
)


CALVER_STRATEGY = "calver"


def next_calendar_version(current_version, part, force_value, version_format):
    version = parse(version_format, current_version)
    if force_value is None:
        transform = CalverIncrementingTransformer()
        return str(transform(part, version))
    else:
        transform = CalverStaticTransformer()
        return str(transform(part, version, force_value))
