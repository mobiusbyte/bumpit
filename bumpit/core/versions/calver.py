from dataclasses import dataclass

CALVER_STRATEGY = "calver"

CALVER_AUTO = "auto"


def next_calendar_version(current_version, part, force_value, version_format):
    return "2019.11.03"


@dataclass
class TokenMatcherSpec:
    token: str
    regex_pattern: str


@dataclass
class Token:
    spec: TokenMatcherSpec
    is_static: bool = False


class CalVerMatcher:
    MUTEX_TOKEN_GROUPS = [
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
        [TokenMatcherSpec(token="MODIFIER", regex_pattern="(?:\\.[0-9a-zA-Z-]+)*))")],
    ]

    def search(self, version_format, version):
        self._assert_version_format(version_format)

    @staticmethod
    def _assert_version_format(version_format):
        regex_pattern = f"^{version_format}$"

        for mutex_tokens in CalVerMatcher.MUTEX_TOKEN_GROUPS:
            for x_spec in mutex_tokens:
                if x_spec.token in regex_pattern:
                    regex_pattern = CalVerMatcher._update_regex(
                        regex_pattern, token_matcher_spec=x_spec
                    )

                    for y_spec in mutex_tokens:
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
