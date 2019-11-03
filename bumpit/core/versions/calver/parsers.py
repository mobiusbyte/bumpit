import re

from bumpit.core.versions.calver.calver import CalVer
from bumpit.core.versions.calver.constants import (
    YEAR_PART,
    MONTH_PART,
    DAY_PART,
    MODIFIER_PART,
)
from bumpit.core.versions.calver.formatters import build_formatter
from bumpit.core.versions.calver.matchers import TokenMatcher


def parse(version_format, version):
    regex_pattern, token_specs = TokenMatcher.build(version_format)

    match = re.search(f"^{regex_pattern}$", version)
    if not match:
        raise ValueError(
            f"Invalid calendar version '{version}' with format '{version_format}'."
        )

    formatter = build_formatter(regex_pattern, token_specs, match)
    return _build_calver(version_format, formatter, token_specs, match)


def _build_calver(version_format, formatter, token_specs, match):
    calver = CalVer(version_format=version_format, formatter=formatter)

    for i, token_spec in enumerate(token_specs):
        group = match.group(i + 1)

        if token_spec.part_type == YEAR_PART:
            year = int(group)
            if len(group) != 4:
                year += 2000

            calver.calendar_date = calver.calendar_date.replace(year=year)
        elif token_spec.part_type == MONTH_PART:
            calver.calendar_date = calver.calendar_date.replace(month=int(group))
        elif token_spec.part_type == DAY_PART:
            calver.calendar_date = calver.calendar_date.replace(day=int(group))
        elif token_spec.part_type == MODIFIER_PART:
            calver.modifier = group
        else:
            setattr(calver, token_spec.part_type, int(group))

    return calver
