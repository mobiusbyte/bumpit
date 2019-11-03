from bumpit.core.versions.calver.constants import YEAR_PART, MONTH_PART, DAY_PART


def build_formatter(regex_pattern, token_specs, match):
    formatter = regex_pattern

    for i, token_spec in enumerate(token_specs):
        group = match.group(i + 1)

        if token_spec.part_type == YEAR_PART:
            partial = {
                4: "{calendar_date:%Y}",
                2: "{calendar_date:%y}",
                1: "{calendar_short_year}",
            }[len(group)]
        elif token_spec.part_type == MONTH_PART:
            partial = {2: "{calendar_date:%m}", 1: "{calendar_date.month}"}[len(group)]
        elif token_spec.part_type == DAY_PART:
            partial = {2: "{calendar_date:%d}", 1: "{calendar_date.day}"}[len(group)]
        else:
            partial = f"{{{token_spec.part_type}}}"

        formatter = formatter.replace(token_spec.regex_pattern, partial, 1)

    return formatter
