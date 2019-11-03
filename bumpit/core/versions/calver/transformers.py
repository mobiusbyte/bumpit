from datetime import datetime

from bumpit.core.versions.calver.parsers import parse_calver
from bumpit.core.versions.calver.calver import CalVer
from bumpit.core.versions.calver.constants import (
    MAJOR_PART,
    MINOR_PART,
    MICRO_PART,
    MODIFIER_PART,
)

TRANSFORM_DATE_PART = "date"
AUTOINCREMENT_PARTS = "auto"
NUMERICAL_PARTS = [MAJOR_PART, MINOR_PART, MICRO_PART]


class CalverIncrementingTransformer:
    def __init__(self):
        self._transform_delegate = CalverStaticTransformer()

    def __call__(self, part, version):
        today = datetime.today().date()

        if part == TRANSFORM_DATE_PART:
            return self._transform_delegate(part, version, today)
        elif part in NUMERICAL_PARTS:
            return self._transform_delegate(part, version, getattr(version, part) + 1)
        elif part == AUTOINCREMENT_PARTS:
            return self._auto_transform(today, version)

        raise ValueError(f"Cannot increment {part}.")

    def _auto_transform(self, today, version):
        version_format = version.version_format

        probe_version = parse_calver(str(version), version_format)
        probe_version.calendar_date = today

        version_str = str(version)

        if str(probe_version) < version_str:
            raise ValueError(
                f"Current version {version_str} is already ahead of today's version."
            )
        elif str(probe_version) > version_str:
            return str(
                CalVer(version_format, calendar_date=today, formatter=version.formatter)
            )
        else:
            return self._auto_update_numerical_parts(probe_version)

    def _auto_update_numerical_parts(self, version):
        for part in NUMERICAL_PARTS:
            if part in version.formatter:
                return self._transform_delegate(
                    part, version, getattr(version, part) + 1
                )

        raise ValueError(f"No detected version change.")


class CalverStaticTransformer:
    def __call__(self, part, version, static):
        if part == TRANSFORM_DATE_PART:
            return self._transform_date_part(part, version, static)
        elif part == MODIFIER_PART:
            return self._transform_modifier_part(part, version, static)
        elif part in NUMERICAL_PARTS:
            return self._transform_numerical_part(part, version, static)
        else:
            raise ValueError(f"Invalid part {part}.")

    @staticmethod
    def _transform_date_part(part, version, static):
        probe_version = parse_calver(str(version), version.version_format)
        probe_version.calendar_date = static

        if str(probe_version) == str(version):
            raise ValueError(f"No detected version change.")

        return CalVer(
            version_format=version.version_format,
            calendar_date=static,
            formatter=version.formatter,
        )

    @staticmethod
    def _transform_numerical_part(part, version, static):
        try:
            value = int(static)
        except ValueError:
            raise ValueError(f"Expecting {part} to be an integer.")

        if getattr(version, part) >= value:
            raise ValueError(f"Can only increase {part} part.")

        new_version = parse_calver(str(version), version.version_format)
        resettable_numeric_fields = {
            MAJOR_PART: [MINOR_PART, MICRO_PART],
            MINOR_PART: [MICRO_PART],
            MICRO_PART: [],
        }[part]

        setattr(new_version, part, static)
        for reset_field in resettable_numeric_fields:
            setattr(new_version, reset_field, 0)

        new_version.modifier = ""

        return new_version

    @staticmethod
    def _transform_modifier_part(part, version, static):
        if version.modifier == static:
            raise ValueError(f"No detected version change.")

        new_version = parse_calver(str(version), version.version_format)
        new_version.modifier = static

        return new_version
