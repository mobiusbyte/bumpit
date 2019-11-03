import re
from dataclasses import dataclass

from bumpit.core.versions.errors import InvalidVersion

SEMVER_STRATEGY = "semver"


def next_semantic_version(current_version, part, force_value, _=None):
    version = SemVer.parse(current_version)
    if force_value is None:
        transform = SemverIncrementingTransformer()
        return str(transform(part, version))
    else:
        transform = SemverStaticTransformer()
        return str(transform(part, version, force_value))


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
            raise InvalidVersion(f"Invalid semantic version '{version}'")

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


class SemverIncrementingTransformer:
    INCREMENTING_FIELDS = ["major", "minor", "patch"]

    def __call__(self, part, version):
        if part not in SemverIncrementingTransformer.INCREMENTING_FIELDS:
            raise ValueError(f"Cannot increment {part}.")

        transform_delegate = SemverStaticTransformer()
        return transform_delegate(part, version, getattr(version, part) + 1)


class SemverStaticTransformer:
    NUMERICAL_FIELDS = ["major", "minor", "patch"]
    NON_NUMERICAL_FIELDS = ["pre_release", "build_metadata"]

    def __call__(self, part, version, static):
        if part in SemverStaticTransformer.NUMERICAL_FIELDS:
            return self._transform_numerical_part(part, version, static)
        elif part in SemverStaticTransformer.NON_NUMERICAL_FIELDS:
            return self._transform_non_numerical_part(part, version, static)
        else:
            raise ValueError(f"Invalid part {part}")

    @staticmethod
    def _transform_numerical_part(part, version, static):
        try:
            value = int(static)
        except ValueError:
            raise ValueError(f"Expecting {part} to be an integer")

        if getattr(version, part) >= value:
            raise ValueError(f"Can only increase {part} part.")

        new_version = SemVer.parse("0.0.0")

        target_part_index = SemverIncrementingTransformer.INCREMENTING_FIELDS.index(
            part
        )
        for current_index, current_part in enumerate(
            SemverStaticTransformer.NUMERICAL_FIELDS
        ):
            version_part = getattr(version, current_part)
            if current_index == target_part_index:
                version_part = static

            if target_part_index < current_index:
                version_part = 0

            setattr(new_version, current_part, version_part)

        return new_version

    @staticmethod
    def _transform_non_numerical_part(part, version, static):
        new_version = SemVer.parse(str(version))
        if getattr(version, part) == static:
            raise ValueError("There is no version change.")

        setattr(new_version, part, static)

        if part == "pre_release":
            new_version.build_metadata = ""

        return new_version
