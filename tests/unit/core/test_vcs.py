from bumpit.core.vcs import Git
from tests import LoggerSpy
import pytest


class CommandExecutorSpy:
    def __init__(self, return_code=0):
        self.commands = []
        self._return_code = return_code

    def __call__(self, command):
        self.commands.append(command)
        return self._return_code

    @property
    def call_count(self):
        return len(self.commands)


class TestGit:
    def setup(self):
        self._logger_spy = LoggerSpy()
        self._command_executor = CommandExecutorSpy()
        self._tag_format = "v{version}"
        self._current_version = "0.0.0"
        self._bumped_version = "1.0.0"

    def test_update_dry_run_tagging_disabled(self):
        git = Git(
            dry_run=True,
            tag=False,
            tag_format=self._tag_format,
            logger=self._logger_spy,
            command_executor=self._command_executor,
        )
        git.update(self._current_version, self._bumped_version)

        assert self._command_executor.call_count == 0
        assert [
            "[DRY-RUN] Ran `git add .`",
            "[DRY-RUN] Ran `git commit -m 'Bumped version from 0.0.0 → 1.0.0.'`",
            "Skipped tagging...",
        ] == self._logger_spy.messages

    def test_update_tagging_disabled(self):
        git = Git(
            dry_run=False,
            tag=False,
            tag_format=self._tag_format,
            logger=self._logger_spy,
            command_executor=self._command_executor,
        )
        git.update(self._current_version, self._bumped_version)

        assert [
            "git add .",
            "git commit -m 'Bumped version from 0.0.0 → 1.0.0.'",
        ] == self._command_executor.commands
        assert [
            "[OK] git add .",
            "[OK] git commit -m 'Bumped version from 0.0.0 → 1.0.0.'",
            "Skipped tagging...",
        ] == self._logger_spy.messages

    def test_update_dry_run_tagging_enabled(self):
        git = Git(
            dry_run=True,
            tag=True,
            tag_format=self._tag_format,
            logger=self._logger_spy,
            command_executor=self._command_executor,
        )
        git.update(self._current_version, self._bumped_version)

        assert self._command_executor.call_count == 0
        assert [
            "[DRY-RUN] Ran `git add .`",
            "[DRY-RUN] Ran `git commit -m 'Bumped version from 0.0.0 → 1.0.0.'`",
            (
                "[DRY-RUN] "
                "Ran `git tag -a 'v1.0.0' -m 'Bumped version from 0.0.0 → 1.0.0.'`"
            ),
        ] == self._logger_spy.messages

    def test_invalid_tag_format(self):
        with pytest.raises(ValueError):
            Git(
                dry_run=True,
                tag=True,
                tag_format="invalid_format",
                logger=self._logger_spy,
                command_executor=self._command_executor,
            )

    def test_update_non_zero_exist_code(self):
        command_executor = CommandExecutorSpy(return_code=1)

        git = Git(
            dry_run=False,
            tag=False,
            tag_format=self._tag_format,
            logger=self._logger_spy,
            command_executor=command_executor,
        )
        with pytest.raises(Exception):
            git.update(self._current_version, self._bumped_version)
