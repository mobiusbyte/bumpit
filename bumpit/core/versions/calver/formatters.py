from bumpit.core.versions.calver.constants import YEAR_PART, MONTH_PART, DAY_PART


def build_formatter(regex_pattern, token_specs, match):
    formatter = regex_pattern

    for i, token_spec in enumerate(token_specs):
        group = match.group(i + 1)
        partial = _partial_formatter(token_spec, group)

        formatter = formatter.replace(token_spec.regex_pattern, partial, 1)

    return formatter


def _partial_formatter(token_spec, group):
    if token_spec.part_type == YEAR_PART:
        return {
            4: "{calendar_date:%Y}",
            2: "{calendar_date:%y}",
            1: "{calendar_short_year}",
        }[len(group)]
    elif token_spec.part_type == MONTH_PART:
        return {2: "{calendar_date:%m}", 1: "{calendar_date.month}"}[len(group)]
    elif token_spec.part_type == DAY_PART:
        return {2: "{calendar_date:%d}", 1: "{calendar_date.day}"}[len(group)]
    else:
        return f"{{{token_spec.part_type}}}"
