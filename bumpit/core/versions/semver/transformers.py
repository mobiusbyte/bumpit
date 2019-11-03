from bumpit.core.versions.semver.parsers import parse_semver

NUMERICAL_PARTS = ["major", "minor", "patch"]
NON_NUMERICAL_PARTS = ["pre_release", "build_metadata"]


class SemverIncrementingTransformer:
    def __call__(self, part, version):
        if part not in NUMERICAL_PARTS:
            raise ValueError(f"Cannot increment {part}.")

        transform_delegate = SemverStaticTransformer()
        return transform_delegate(part, version, getattr(version, part) + 1)


class SemverStaticTransformer:
    def __call__(self, part, version, static):
        if part in NUMERICAL_PARTS:
            return self._transform_numerical_part(part, version, static)
        elif part in NON_NUMERICAL_PARTS:
            return self._transform_non_numerical_part(part, version, static)
        else:
            raise ValueError(f"Invalid {part} part.")

    @staticmethod
    def _transform_numerical_part(part, version, static):
        try:
            value = int(static)
        except ValueError:
            raise ValueError(f"Expecting {part} to be an integer.")

        if getattr(version, part) >= value:
            raise ValueError(f"Can only increase {part} part.")

        new_version = parse_semver("0.0.0")

        target_part_index = NUMERICAL_PARTS.index(part)
        for current_index, current_part in enumerate(NUMERICAL_PARTS):
            version_part = getattr(version, current_part)
            if current_index == target_part_index:
                version_part = static

            if target_part_index < current_index:
                version_part = 0

            setattr(new_version, current_part, version_part)

        return new_version

    @staticmethod
    def _transform_non_numerical_part(part, version, static):
        new_version = parse_semver(str(version))
        if getattr(version, part) == static:
            raise ValueError("There is no version change.")

        setattr(new_version, part, static)

        if part == "pre_release":
            new_version.build_metadata = ""

        return new_version
