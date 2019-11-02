import pytest

from bumpit.core.versions import next_semantic_version


@pytest.mark.parametrize(
    "part, force_value, expected_next_version",
    [
        pytest.param("major", None, "2.0.0"),
        pytest.param("minor", None, "1.3.0"),
        pytest.param("patch", None, "1.2.4"),
        pytest.param("pre_release", "beta", "1.2.3-beta"),
        pytest.param("pre_release", "", "1.2.3"),
        pytest.param(
            "build_metadata", "exp.sha.5114f85", "1.2.3-alpha+exp.sha.5114f85"
        ),
        pytest.param("major", "9", "9.0.0"),
        pytest.param("minor", "9", "1.9.0"),
        pytest.param("patch", "9", "1.2.9"),
    ],
)
def test_next_semantic_version(part, force_value, expected_next_version):
    assert expected_next_version == next_semantic_version(
        current_version="1.2.3-alpha+exp.sha.1234f56",
        part=part,
        force_value=force_value,
    )