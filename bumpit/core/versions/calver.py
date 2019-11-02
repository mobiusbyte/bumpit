from dataclasses import dataclass

CALVER_STRATEGY = "calver"

CALVER_AUTO = "auto"


def next_calendar_version(current_version, part, force_value, version_format):
    return "2019.11.03"


@dataclass
class TokenMatcherSpec:
    token: str
    regex_pattern: str


class VersionParser:
    def __init__(self, version_format):
        self._init_matcher(version_format)

    def _init_matcher(self, version_format):

        # (0|[1-9]\\d*)
        mutex_tokens = [
            [
                TokenMatcherSpec(token="YYYY", regex_pattern="(\\d{4})"),
                TokenMatcherSpec(token="YY", regex_pattern="(\\d{1,2})"),
                TokenMatcherSpec(token="0Y", regex_pattern="(\\d{2})"),
            ],
            [
                TokenMatcherSpec(token="MM", regex_pattern="(\\d{1,2})"),
                TokenMatcherSpec(token="0M", regex_pattern="(\\d{2})"),
            ],
            [
                TokenMatcherSpec(token="DD", regex_pattern="(\\d{1,2})"),
                TokenMatcherSpec(token="0D", regex_pattern="(\\d{2})"),
            ],
            [TokenMatcherSpec(token="MINOR", regex_pattern="(0|[1-9]\\d*))")],
            [TokenMatcherSpec(token="MICRO", regex_pattern="(0|[1-9]\\d*))")],
            [
                TokenMatcherSpec(
                    token="MODIFIER", regex_pattern="(?:\\.[0-9a-zA-Z-]+)*))"
                )
            ],
        ]

        regex_pattern = f"^{version_format}$"

        for mutex_tokens_set in mutex_tokens:
            for x_spec in mutex_tokens_set:
                if x_spec.token in regex_pattern:
                    regex_pattern = VersionParser._update_regex(
                        regex_pattern, token_matcher_spec=x_spec
                    )

                    for y_spec in mutex_tokens_set:
                        if y_spec.token in regex_pattern:
                            raise ValueError(
                                f"Cannot have '{y_spec.token}'. "
                                f"The '{x_spec.token}' already exists."
                            )

    @staticmethod
    def _update_regex(regex_pattern, token_matcher_spec):
        reverse_regex_pattern = regex_pattern[::-1]
        reverse_token_replacement = token_matcher_spec.token[::-1]
        regex_replacement = token_matcher_spec.regex_pattern[::-1]

        return reverse_regex_pattern.replace(
            reverse_token_replacement, regex_replacement, 1
        )[::-1]
