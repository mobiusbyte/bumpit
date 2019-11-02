from bumpit.core.versions.semver import SemVer


class IncrementingTransformer:
    INCREMENTING_FIELDS = ["major", "minor", "patch"]

    def __call__(self, part, version):
        try:
            target_part_index = IncrementingTransformer.INCREMENTING_FIELDS.index(part)
        except ValueError:
            raise ValueError(f"Cannot increment {part}.")

        new_version = SemVer.parse("0.0.0")
        for current_index, current_part in enumerate(IncrementingTransformer.INCREMENTING_FIELDS):
            version_part = getattr(version, current_part)
            if current_index == target_part_index:
                version_part += 1

            if target_part_index < current_index:
                version_part = 0

            setattr(new_version, current_part, version_part)

        return new_version
