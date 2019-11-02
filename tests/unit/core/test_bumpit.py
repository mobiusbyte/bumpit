from bumpit.core.bumpit import run
from tests import fixture_path, LoggerSpy


class TestBumpIt:
    def test_run(self):
        run(
            config=fixture_path("config/.bumpit-lite.yaml"),
            logger=LoggerSpy(),
            dry_run=True,
            target_part=None,
        )
