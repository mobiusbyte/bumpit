import re
from dataclasses import dataclass


@dataclass
class SemVer:
    major: int
    minor: int
    patch: int
    pre_release: str
    build_metadata: str

    @staticmethod
    def parse(version):
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

    def __str__(self):
        as_str = f"{self.major}.{self.minor}.{self.patch}"

        if self.pre_release:
            as_str += f"-{self.pre_release}"

        if self.build_metadata:
            as_str += f"+{self.build_metadata}"

        return as_str
