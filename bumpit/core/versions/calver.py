CALVER_STRATEGY = "calver"

CALVER_AUTO = "auto"


def next_calendar_version(current_version, part, force_value, version_format):
    return "2019.11.03"


def version_parser(version_format):
    mutex_tokens = [
        ["YYYY", "YY", "0Y"],
        ["MM", "0M"],
        ["DD", "0D"],
        ["MINOR"],
        ["MICRO"],
        ["MODIFIER"],
    ]

    remaining_version_format = version_format
    for mutex_tokens_set in mutex_tokens:
        for index, x_token in enumerate(mutex_tokens_set):
            if x_token in remaining_version_format:
                remaining_version_format = version_format.replace(x_token, "", 1)

                for y_token in mutex_tokens_set[index:]:
                    if y_token in remaining_version_format:
                        raise ValueError(
                            f"Cannot have {y_token} when there is already {x_token}"
                        )
