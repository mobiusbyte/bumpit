import pytest

from bumpit.core.versions.calver import version_parser


def fixture_generator():
    significant_tokens = [
        ["YYYY", "YY", "0Y"],
        ["MM", "0M"],
        ["DD", "0D"],
        ["MINOR"],
        ["MICRO"],
        ["MODIFIER"],
    ]

    for mutex_tokens in significant_tokens:
        for first in mutex_tokens:
            for last in mutex_tokens:
                token_candidate = f"{first}{last}"
                if token_candidate != "YYYY":
                    yield f"{first}{last}"


@pytest.mark.parametrize("invalid_version_token", list(fixture_generator()))
def test_invalid_version_tokens(invalid_version_token):
    with pytest.raises(ValueError):
        version_parser(invalid_version_token)