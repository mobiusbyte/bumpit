import pytest

from bumpit.core.versions.semver import SemVer


@pytest.mark.parametrize(
    "version, expected_major, expected_minor, expected_patch, expected_prerelease, expected_build_metadata",
    [
        pytest.param("1.2.3", 1, 2, 3, "", ""),
        pytest.param("1.2.3-beta", 1, 2, 3, "beta", ""),
        pytest.param("1.2.3+exp.sha.5114f85", 1, 2, 3, "", "exp.sha.5114f85"),
        pytest.param("1.2.3-beta+exp.sha.5114f85", 1, 2, 3, "beta", "exp.sha.5114f85"),
    ],
)
def test_parse(version, expected_major, expected_minor, expected_patch, expected_prerelease, expected_build_metadata):
    semver = SemVer.parse(version)

    assert expected_major == semver.major
    assert expected_minor == semver.minor
    assert expected_patch == semver.patch
    assert expected_prerelease == semver.pre_release
    assert expected_build_metadata == semver.build_metadata

