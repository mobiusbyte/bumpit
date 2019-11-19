import pytest

from bumpit.core.config.commit import Commit


class TestCommit:
    @pytest.mark.parametrize("author", [None, ""])
    def test_load_invalid_author(self, author):
        with pytest.raises(ValueError):
            Commit.load({"author": author})

    def test_load_missing_author(self):
        with pytest.raises(ValueError):
            Commit.load({})

    def test_eq(self):
        lhs = Commit(author="Homer Simpson <homer@simpson.com>")
        rhs = Commit(author="Homer Simpson <homer@simpson.com>")

        assert lhs == rhs
