import re

from bumpit.core.versions.semver.semver import SemVer


def parse_semver(version, version_format=None):
    semver_pattern = "^(0|[1-9]\\d*)\\.(0|[1-9]\\d*)\\.(0|[1-9]\\d*)(?:-((?:0|[1-9]\\d*|\\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\\.(?:0|[1-9]\\d*|\\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\\+([0-9a-zA-Z-]+(?:\\.[0-9a-zA-Z-]+)*))?$"  # noqa
    match = re.search(semver_pattern, version)
    if not match:
        raise ValueError(f"Invalid semantic version '{version}'.")

    return SemVer(
        major=int(match.group(1)),
        minor=int(match.group(2)),
        patch=int(match.group(3)),
        pre_release=match.group(4) or "",
        build_metadata=match.group(5) or "",
    )
