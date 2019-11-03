import re
from dataclasses import dataclass
from datetime import date

from bumpit.core.versions.calver.constants import (
    YEAR_PART,
    MONTH_PART,
    DAY_PART,
    MODIFIER_PART,
)
from bumpit.core.versions.calver.formatters import build_formatter
from bumpit.core.versions.calver.matchers import TokenMatcher


@dataclass
class CalVer:
    version_format: str
    calendar_date: date = date(2000, 1, 1)
    major: int = 0
    minor: int = 0
    micro: int = 0
    modifier: str = ""
    formatter: str = ""

    def __str__(self):
        return self.formatter.format(
            calendar_date=self.calendar_date,
            calendar_short_year=self.calendar_date.year % 100,
            major=self.major,
            minor=self.minor,
            micro=self.micro,
            modifier=self.modifier or "",
        )

    @staticmethod
    def parse(version_format, version):
        regex_pattern, token_specs = TokenMatcher.build(version_format)

        match = re.search(f"^{regex_pattern}$", version)
        if not match:
            raise ValueError(
                f"Invalid calendar version '{version}' with format '{version_format}'."
            )

        calver = CalVer._parsed_calver(version_format, token_specs, match)
        calver.formatter = build_formatter(regex_pattern, token_specs, match)
        return calver

    @staticmethod
    def _parsed_calver(version_format, token_specs, match):
        calver = CalVer(version_format)

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
