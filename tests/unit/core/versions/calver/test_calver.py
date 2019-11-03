import pytest

from bumpit.core.versions.calver import CalVer


@pytest.mark.parametrize(
    ("version_format, version"),
    [
        pytest.param("YY", "83"),
        pytest.param("YY.0M", "4.10"),
        pytest.param("YY.0M", "13.10"),
        pytest.param("YY.0M.MICRO", "19.08.10"),
        pytest.param("YY.MINOR.MICRO", "17.2.0"),
        pytest.param("YY.MM.MICRO", "16.1.1"),
        pytest.param(
            "YY.MMMODIFIER", "18.3a0"
        ),  # black; not aligned with https://calver.org/users.html#utilities
        pytest.param("YYYY", "2012"),
        pytest.param("YYYY.MM", "2016.4"),
        pytest.param("YYYY.0M", "2015.03"),
        pytest.param("YYYY.0M.0D", "2018.03.01"),
        pytest.param("YYYY.0M.0D.MICRO", "2016.06.19.1"),
        pytest.param("YYYY.MINOR.MICRO", "2019.2.2"),
        pytest.param("YYYY.MM.DD_MICRO", "2016.2.22_1"),
        pytest.param("YYYYMM.MINOR.MICRO", "201910.100.0"),
    ],
)
def test_parse(version_format, version):
    calver = CalVer.parse(version_format, version)

    assert version == str(calver)


def test_parse_invalid_version_format_no_date_tokens():
    with pytest.raises(ValueError):
        CalVer.parse("MAJOR.MINOR.MICRO.MODIFIER", "1.2.3.nerp")


def test_parse_invalid_version():
    with pytest.raises(ValueError):
        CalVer.parse("YYYY", "1.2.3")
