import pytest
from bumpit.core.config.tag import Tag


class TestTag:
    @pytest.mark.parametrize("apply", [None, "not_a_bool", 1, 2.0])
    def test_load_invalid_apply(self, apply):
        with pytest.raises(ValueError):
            Tag.load({"apply": apply, "format": "{version}"})

    def test_load_missing_apply(self):
        with pytest.raises(ValueError):
            Tag.load({"format": "{version}"})

    def test_load_invalid_format(self):
        with pytest.raises(ValueError):
            Tag.load({"apply": False, "format": "not_valid"})

    def test_load_missing_format(self):
        with pytest.raises(ValueError):
            Tag.load({"apply": True})

    def test_eq(self):
        lhs = Tag(apply=True, format="{version}")
        rhs = Tag(apply=True, format="{version}")

        assert lhs == rhs
