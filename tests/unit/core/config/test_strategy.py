import pytest
from bumpit.core.config.strategy import Strategy


class TestStrategy:
    @pytest.mark.parametrize("name", [None, ""])
    def test_load_invalid_name(self, name):
        with pytest.raises(ValueError):
            Strategy.load({"name": name, "part": "minor"})

    def test_load_missing_name(self):
        with pytest.raises(ValueError):
            Strategy.load({"part": "minor"})

    def test_load_invalid_part(self):
        with pytest.raises(ValueError):
            Strategy.load({"name": "semver", "part": None})

    def test_load_missing_part(self):
        with pytest.raises(ValueError):
            Strategy.load({"name": "semver"})

    def test_eq(self):
        lhs = Strategy(name="semver", part="minor")
        rhs = Strategy(name="semver", part="minor")

        assert lhs == rhs
