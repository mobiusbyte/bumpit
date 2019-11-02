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

        remaining_version_format = version_format
        for mutex_tokens_set in mutex_tokens:
            for index, x_spec in enumerate(mutex_tokens_set):
                if x_spec.token in remaining_version_format:
                    remaining_version_format = version_format.replace(
                        x_spec.token, "", 1
                    )

                    for y_spec in mutex_tokens_set[index:]:
                        if y_spec.token in remaining_version_format:
                            raise ValueError(
                                f"Cannot have '{y_spec.token}'. "
                                f"The '{x_spec.token}' already exists."
                            )
