import re
from datetime import datetime


class UnsupportedVersioningStrategy(Exception):
    pass


class InvalidVersion(Exception):
    pass


class InvalidVersionPart(Exception):
    pass


def new_version(strategy, current_version):
    if SemanticVersion.matches(strategy):
        return SemanticVersion(current_version, strategy).bump()
    elif CalendarVersion.matches(strategy):
        return CalendarVersion(current_version, strategy).bump()
    else:
        raise UnsupportedVersioningStrategy(f"Invalid strategy {strategy}")


class SemanticVersion:
    STRATEGY_PREFIX = f"semver-"
    VERSION_PARTS = ["major", "minor", "patch"]

    def __init__(self, current_version, strategy):
        self._current_version = current_version
        self._match = self._parse_version_match(current_version)
        self._part = self._parse_part(strategy)

    def bump(self):
        return f"{self._bumped_version}{self._meta_token}"

    @staticmethod
    def matches(strategy):
        return strategy.startswith(SemanticVersion.STRATEGY_PREFIX)

    @property
    def _bumped_version(self):
        target_part_index = self.VERSION_PARTS.index(self._part)
        tokens = []
        for index, part in enumerate(self.VERSION_PARTS):
            version_part = int(self._match.group(index + 1))
            if index == target_part_index:
                version_part += 1
            if target_part_index < index:
                version_part = 0

            tokens.append(f"{version_part}")

        return ".".join(tokens)

    @property
    def _meta_token(self):
        prefix_meta_length = len(
            f"{self._match.group(1)}.{self._match.group(2)}.{self._match.group(3)}"
        )
        return self._current_version[prefix_meta_length:]

    @staticmethod
    def _parse_version_match(version):
        semver_pattern = "^(0|[1-9]\\d*)\\.(0|[1-9]\\d*)\\.(0|[1-9]\\d*)(?:-((?:0|[1-9]\\d*|\\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\\.(?:0|[1-9]\\d*|\\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\\+([0-9a-zA-Z-]+(?:\\.[0-9a-zA-Z-]+)*))?$"  # noqa
        match = re.search(semver_pattern, version)
        if not match:
            raise InvalidVersion(f"Invalid semantic version format '{version}")
        return match

    @staticmethod
    def _parse_part(strategy):
        prefix_len = len(SemanticVersion.STRATEGY_PREFIX)
        part = strategy[prefix_len:]
        if part not in SemanticVersion.VERSION_PARTS:
            raise InvalidVersionPart(f"Invalid semantic version part f{part}.")
        return part


class CalendarVersion:
    def __init__(self, current_version, _):
        self._current_version = current_version
        self._match = self._parse_version_match(current_version)

    def bump(self):
        version_month = datetime.strptime(self._match.group(1), "%Y%m")
        variant_id = int(self._match.group(2))
        today = datetime.today()
        if today.month == version_month.month:
            variant_id += 1
        else:
            version_month = today
            variant_id = 1

        version_format = f"{{formatted_version_month}}.{{formatted_variant_id}}"
        return version_format.format(
            formatted_version_month=version_month.strftime("%Y%m"),
            formatted_variant_id=variant_id,
        )

    @staticmethod
    def matches(strategy):
        return strategy == "calver"

    @staticmethod
    def _parse_version_match(version):
        regex_pattern = "^(\\d{6})\\.(\\d+)$"
        match = re.search(regex_pattern, version)
        if not match:
            raise InvalidVersion(f"Invalid calendar version format '{version}")
        return match
