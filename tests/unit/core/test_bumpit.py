from bumpit.core.bumpit import run, RunSettings
from tests import fixture_path, LoggerSpy


class TestBumpIt:
    def test_run(self):
        run(
            config=fixture_path("config/.bumpit-lite.yaml"),
            logger=LoggerSpy(),
            run_settings=RunSettings(dry_run=True, target_part=None, force_value=None),
        )
