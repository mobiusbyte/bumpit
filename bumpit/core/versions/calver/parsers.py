import re

from bumpit.core.versions.calver.calver import CalVer
from bumpit.core.versions.calver.constants import YEAR_PART, MODIFIER_PART, DATE_PARTS
from bumpit.core.versions.calver.formatters import build_formatter
from bumpit.core.versions.calver.matchers import TokenMatcher


def parse_calver(version, version_format):
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
        _update_calver_fields(calver, token_spec, raw_value=match.group(i + 1))

    return calver


def _update_calver_fields(calver, token_spec, raw_value):
    part_type = token_spec.part_type
    if part_type == MODIFIER_PART:
        calver.modifier = raw_value
    elif part_type in DATE_PARTS:
        _update_calver_date(calver, part_type, raw_value)
    else:
        setattr(calver, part_type, int(raw_value))


def _update_calver_date(calver, part_type, raw_value):
    value = int(raw_value)
    if part_type == YEAR_PART and len(raw_value) != 4:
        value += 2000

    calver.calendar_date = calver.calendar_date.replace(**{part_type: value})
