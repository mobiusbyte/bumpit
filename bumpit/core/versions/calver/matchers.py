from dataclasses import dataclass

from bumpit.core.versions.calver.constants import (
    DATE_PARTS,
    MONTH_PART,
    YEAR_PART,
    DAY_PART,
    MAJOR_PART,
    MINOR_PART,
    MICRO_PART,
    MODIFIER_PART,
)


@dataclass
class TokenMatcherSpec:
    token: str
    regex_pattern: str
    part_type: str


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
