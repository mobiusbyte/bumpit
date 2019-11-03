import re
from dataclasses import dataclass
from datetime import date, datetime

from bumpit.core.versions.errors import InvalidVersion

CALVER_STRATEGY = "calver"


def next_calendar_version(current_version, part, force_value, version_format):
    version = CalVer.parse(version_format, current_version)
    if force_value is None:
        transform = CalverIncrementingTransformer()
        return str(transform(part, version))
    else:
        transform = CalverStaticTransformer()
        return str(transform(part, version, force_value))


@dataclass
class TokenMatcherSpec:
    token: str
    regex_pattern: str
    part_type: str


YEAR_PART = "year"
MONTH_PART = "month"
DAY_PART = "day"
MAJOR_PART = "major"
MINOR_PART = "minor"
MICRO_PART = "micro"
MODIFIER_PART = "modifier"

DATE_PARTS = [YEAR_PART, MONTH_PART, DAY_PART]


MUTEX_TOKEN_GROUPS = [
    [
        TokenMatcherSpec(token="YYYY", part_type=YEAR_PART, regex_pattern="(\\d{4})"),
        TokenMatcherSpec(token="0Y", part_type=YEAR_PART, regex_pattern="(\\d{2})"),
        TokenMatcherSpec(token="YY", part_type=YEAR_PART, regex_pattern="(\\d{1,2})"),
    ],
    [
        TokenMatcherSpec(token="0M", part_type=MONTH_PART, regex_pattern="(\\d{2})"),
        TokenMatcherSpec(token="MM", part_type=MONTH_PART, regex_pattern="(\\d{1,2})"),
    ],
    [
        TokenMatcherSpec(token="0D", part_type=DAY_PART, regex_pattern="(\\d{2})"),
        TokenMatcherSpec(token="DD", part_type=DAY_PART, regex_pattern="(\\d{1,2})"),
    ],
    [
        TokenMatcherSpec(
            token="MAJOR", part_type=MAJOR_PART, regex_pattern="(0|[1-9]\\d*)"
        )
    ],
    [
        TokenMatcherSpec(
            token="MINOR", part_type=MINOR_PART, regex_pattern="(0|[1-9]\\d*)"
        )
    ],
    [
        TokenMatcherSpec(
            token="MICRO", part_type=MICRO_PART, regex_pattern="(0|[1-9]\\d*)"
        )
    ],
    [
        TokenMatcherSpec(
            token="MODIFIER", part_type=MODIFIER_PART, regex_pattern="([0-9a-zA-Z-]+)?"
        )
    ],
]


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

    @staticmethod
    def _formatter(regex_pattern, token_specs, match):
        formatter = regex_pattern

        for i, token_spec in enumerate(token_specs):
            group = match.group(i + 1)

            if token_spec.part_type == YEAR_PART:
                partial_formatter = {
                    4: "{calendar_date:%Y}",
                    2: "{calendar_date:%y}",
                    1: "{calendar_short_year}",
                }[len(group)]
            elif token_spec.part_type == MONTH_PART:
                partial_formatter = {
                    2: "{calendar_date:%m}",
                    1: "{calendar_date.month}",
                }[len(group)]
            elif token_spec.part_type == DAY_PART:
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
            if token_spec.part_type in DATE_PARTS:
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
        if token_matcher_spec.part_type == MONTH_PART:
            return ["major", "minor", "micro", "modifier"]
        return []

    @staticmethod
    def _ordered_token_specs(version_format, version_token_specs):
        ranked_token_specs = {
            version_format.rfind(token_spec.token): token_spec
            for token_spec in version_token_specs
        }

        return [ranked_token_specs[key] for key in sorted(ranked_token_specs)]


class CalverIncrementingTransformer:
    NUMERICAL_PARTS = [MAJOR_PART, MINOR_PART, MICRO_PART]

    def __call__(self, part, version):
        transform_delegate = CalverStaticTransformer()
        today = datetime.today().date()

        if part == "date":
            return transform_delegate(part, version, today)
        elif part in self.NUMERICAL_PARTS:
            return transform_delegate(part, version, getattr(version, part) + 1)
        elif part == "auto":
            return self._auto_transform(today, version, transform_delegate)

        raise ValueError(f"Cannot increment {part}.")

    def _auto_transform(self, today, version, transform_delegate):
        version_format = version.version_format

        probe_version = CalVer.parse(version_format, str(version))
        probe_version.calendar_date = today

        version_str = str(version)

        if str(probe_version) < version_str:
            raise ValueError(
                f"Current version {version_str} is already ahead of today's version"
            )
        elif str(probe_version) > version_str:
            return str(
                CalVer(version_format, calendar_date=today, formatter=version.formatter)
            )
        else:
            for part in self.NUMERICAL_PARTS:
                if part in probe_version.formatter:
                    return transform_delegate(
                        part, probe_version, getattr(probe_version, part) + 1
                    )

            raise ValueError(f"No detected version change.")


class CalverStaticTransformer:
    DATE_FIELDS = ["date"]
    NUMERICAL_FIELDS = [MAJOR_PART, MINOR_PART, MICRO_PART]
    NON_NUMERICAL_FIELDS = [MODIFIER_PART]

    def __call__(self, part, version, static):
        if part == "date":
            return self._transform_date_part(part, version, static)
        elif part == MODIFIER_PART:
            return self._transform_modifier_part(part, version, static)
        elif part in CalverStaticTransformer.NUMERICAL_FIELDS:
            return self._transform_numerical_part(part, version, static)
        else:
            raise ValueError(f"Invalid part {part}")

    @staticmethod
    def _transform_date_part(part, version, static):
        probe_version = CalVer.parse(version.version_format, str(version))
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
            raise ValueError(f"Expecting {part} to be an integer")

        if getattr(version, part) >= value:
            raise ValueError(f"Can only increase {part} part.")

        new_version = CalVer.parse(version.version_format, str(version))
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

        new_version = CalVer.parse(version.version_format, str(version))
        new_version.modifier = static

        return new_version
