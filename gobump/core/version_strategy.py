import re

SEMANTIC_VERSIONING = "semantic_versioning"


class UnsupportedVersioningStrategy(Exception):
    pass


class InvalidVersion(Exception):
    pass


class InvalidVersionPart(Exception):
    pass


def new_version(strategy, current_version, part):
    if strategy == SEMANTIC_VERSIONING:
        return SemanticVersion(current_version, part).bump()
    else:
        raise UnsupportedVersioningStrategy(f"Invalid strategy {strategy}")


class SemanticVersion:
    VERSION_PARTS = ["major", "minor", "patch"]
    PATTERN = "^(0|[1-9]\\d*)\\.(0|[1-9]\\d*)\\.(0|[1-9]\\d*)(?:-((?:0|[1-9]\\d*|\\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\\.(?:0|[1-9]\\d*|\\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\\+([0-9a-zA-Z-]+(?:\\.[0-9a-zA-Z-]+)*))?$"  # noqa

    def __init__(self, current_version, part):
        self._current_version = current_version
        self._match = re.search(self.PATTERN, current_version)
        if not self._match:
            raise InvalidVersion(f"Invalid semantic version format '{current_version}")

        self._part = part
        if self._part not in self.VERSION_PARTS:
            raise InvalidVersionPart(f"Invalid semantic version part f{self._part}.")

    def bump(self):
        return f"{self._bumped_version}{self._meta_token}"

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
