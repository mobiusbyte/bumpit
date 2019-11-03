import re
from dataclasses import dataclass
from datetime import date

from bumpit.core.versions.errors import InvalidVersion

CALVER_STRATEGY = "calver"


def next_calendar_version(current_version, part, force_value, version_format):
    return "2019.11.03"


@dataclass
class TokenMatcherSpec:
    token: str
    regex_pattern: str
    part_type: str


YEAR_TYPE = "year"
MONTH_TYPE = "month"
DAY_TYPE = "day"
MAJOR_TYPE = "major"
MINOR_TYPE = "minor"
MICRO_TYPE = "micro"
MODIFIER_TYPE = "modifier"

DATE_TOKEN_TYPES = [YEAR_TYPE, MONTH_TYPE, DAY_TYPE]

MUTEX_TOKEN_GROUPS = [
    [
        TokenMatcherSpec(token="YYYY", part_type=YEAR_TYPE, regex_pattern="(\\d{4})"),
        TokenMatcherSpec(token="0Y", part_type=YEAR_TYPE, regex_pattern="(\\d{2})"),
        TokenMatcherSpec(token="YY", part_type=YEAR_TYPE, regex_pattern="(\\d{1,2})"),
    ],
    [
        TokenMatcherSpec(token="0M", part_type=MONTH_TYPE, regex_pattern="(\\d{2})"),
        TokenMatcherSpec(token="MM", part_type=MONTH_TYPE, regex_pattern="(\\d{1,2})"),
    ],
    [
        TokenMatcherSpec(token="0D", part_type=DAY_TYPE, regex_pattern="(\\d{2})"),
        TokenMatcherSpec(token="DD", part_type=DAY_TYPE, regex_pattern="(\\d{1,2})"),
    ],
    [
        TokenMatcherSpec(
            token="MAJOR", part_type=MAJOR_TYPE, regex_pattern="(0|[1-9]\\d*)"
        )
    ],
    [
        TokenMatcherSpec(
            token="MINOR", part_type=MINOR_TYPE, regex_pattern="(0|[1-9]\\d*)"
        )
    ],
    [
        TokenMatcherSpec(
            token="MICRO", part_type=MICRO_TYPE, regex_pattern="(0|[1-9]\\d*)"
        )
    ],
    [
        TokenMatcherSpec(
            token="MODIFIER", part_type=MODIFIER_TYPE, regex_pattern="([0-9a-zA-Z-]+)"
        )
    ],
]


@dataclass
class CalVer:
    version_format: str
    calendar_date: date = date(2000, 1, 1)
    major: int = None
    minor: int = None
    micro: int = None
    modifier: str = None
    formatter: str = ""

    def __str__(self):
        return self.formatter.format(
            calendar_date=self.calendar_date,
            calendar_short_year=self.calendar_date.year % 100,
            major=self.major,
            minor=self.minor,
            micro=self.micro,
            modifier=self.modifier,
        )

    @staticmethod
    def parse(version_format, version):
        regex_pattern, token_specs = TokenMatcher.build(version_format)

        match = re.search(f"^{regex_pattern}$", version)
        if not match:
            raise InvalidVersion(
                f"Invalid calendar version '{version}' with format '{version_format}'"
            )

        calver = CalVer._parsed_calver(version_format, token_specs, match)
        calver.formatter = CalVer._formatter(regex_pattern, token_specs, match)
        return calver

    @staticmethod
    def _parsed_calver(version_format, token_specs, match):
        calver = CalVer(version_format)

        for i, token_spec in enumerate(token_specs):
            group = match.group(i + 1)

            if token_spec.part_type == YEAR_TYPE:
                year = int(group)
                if len(group) != 4:
                    year += 2000

                calver.calendar_date = calver.calendar_date.replace(year=year)
            elif token_spec.part_type == MONTH_TYPE:
                calver.calendar_date = calver.calendar_date.replace(month=int(group))
            elif token_spec.part_type == DAY_TYPE:
                calver.calendar_date = calver.calendar_date.replace(day=int(group))
            elif token_spec.part_type == MODIFIER_TYPE:
                calver.modifier = group
            else:
                setattr(calver, token_spec.part_type, int(group))

        return calver

    @staticmethod
    def _formatter(regex_pattern, token_specs, match):
        formatter = regex_pattern

        for i, token_spec in enumerate(token_specs):
            group = match.group(i + 1)

            if token_spec.part_type == YEAR_TYPE:
                partial_formatter = {
                    4: "{calendar_date:%Y}",
                    2: "{calendar_date:%y}",
                    1: "{calendar_short_year}",
                }[len(group)]
            elif token_spec.part_type == MONTH_TYPE:
                partial_formatter = {
                    2: "{calendar_date:%m}",
                    1: "{calendar_date.month}",
                }[len(group)]
            elif token_spec.part_type == DAY_TYPE:
                partial_formatter = {2: "{calendar_date:%d}", 1: "{calendar_date.day}"}[
                    len(group)
                ]
            else:
                partial_formatter = f"{{{token_spec.part_type}}}"

            formatter = formatter.replace(
                token_spec.regex_pattern, partial_formatter, 1
            )

        return formatter


class TokenMatcher:
    @staticmethod
    def build(version_format):
        regex_pattern, version_token_specs = TokenMatcher._parse_version_format(
            version_format
        )
        ordered_token_specs = TokenMatcher._ordered_token_specs(
            version_format, version_token_specs
        )

        for token_spec in ordered_token_specs:
            if token_spec.part_type in DATE_TOKEN_TYPES:
                return regex_pattern, ordered_token_specs

        raise ValueError(f"Missing date token in version_format '{version_format}'")

    @staticmethod
    def _parse_version_format(version_format):
        version_token_specs = []
        regex_pattern = f"{version_format}"

        for mutex_tokens in MUTEX_TOKEN_GROUPS:
            for x_spec in mutex_tokens:
                if x_spec.token in regex_pattern:
                    regex_pattern = TokenMatcher._update_regex(
                        regex_pattern, token_matcher_spec=x_spec
                    )

                    for y_spec in mutex_tokens:
                        if y_spec.token in regex_pattern:
                            raise ValueError(
                                f"Cannot have '{y_spec.token}'. "
                                f"The '{x_spec.token}' already exists."
                            )

                    version_token_specs.append(x_spec)

        return regex_pattern, version_token_specs

    @staticmethod
    def _update_regex(regex_pattern, token_matcher_spec):
        swaps = TokenMatcher._safe_swaps(token_matcher_spec)

        for swap in swaps:
            regex_pattern = regex_pattern.replace(swap.upper(), swap)

        reverse_regex_pattern = regex_pattern[::-1]
        reverse_token_replacement = token_matcher_spec.token[::-1]
        regex_replacement = token_matcher_spec.regex_pattern[::-1]

        ordered_regex = reverse_regex_pattern.replace(
            reverse_token_replacement, regex_replacement, 1
        )[::-1]

        for swap in swaps:
            ordered_regex = ordered_regex.replace(swap, swap.upper())

        return ordered_regex

    @staticmethod
    def _safe_swaps(token_matcher_spec):
        if token_matcher_spec.part_type == MONTH_TYPE:
            return ["major", "minor", "micro", "modifier"]
        return []

    @staticmethod
    def _ordered_token_specs(version_format, version_token_specs):
        ranked_token_specs = {
            version_format.rfind(token_spec.token): token_spec
            for token_spec in version_token_specs
        }

        return [ranked_token_specs[key] for key in sorted(ranked_token_specs)]
