import pytest

from bumpit.core.versions.calver.matchers import TokenMatcher


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
def test_invalid_version_format(invalid_version_token):
    with pytest.raises(ValueError):
        TokenMatcher.build(invalid_version_token)
