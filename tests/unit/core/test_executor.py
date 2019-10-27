from distutils.dir_util import copy_tree
from shutil import rmtree

from bumpit.core.executor import BumpIt
from tests import fixture_path, tmp_folder, LoggerSpy


class TestBumpItDryRun:
    def setup(self):
        self._logger_spy = LoggerSpy()
        self._current_version = "0.0.1"
        self._bumped_version = "0.1.0"

        self._tmp_folder = tmp_folder()
        copy_tree(fixture_path("executors/before"), self._tmp_folder)

    def teardown(self):
        rmtree(self._tmp_folder, ignore_errors=True)

    def test_bump_dry_run(self):
        files = self._tracked_files()
        executor = BumpIt(
            folder=self._tmp_folder, logger=self._logger_spy, dry_run=True
        )
        executor.bump(
            current_version=self._current_version,
            bumped_version=self._bumped_version,
            files=files,
        )

        assert [
            "***Running in DRY-RUN mode...***",
            (
                f"Could not find version {self._current_version} in file '{files[0]}'. "
                f"Skipping..."
            ),
            (
                f"--- before: {files[1]}\n"
                f"+++ after: {files[1]}\n"
                f"@@ -1 +1 @@\n"
                f"-{self._current_version}\n"
                f"+{self._bumped_version}"
            ),
            f"[DRY-RUN] Skipping changes to '{files[1]}'...",
            (
                f"--- before: {files[2]}\n"
                f"+++ after: {files[2]}\n"
                f"@@ -1,4 +1,4 @@\n"
                f" 14.04.6-LTS\n"
                f"-            {self._current_version}...\n"
                f"+            {self._bumped_version}...\n"
                f" and another one\n"
                f"-{self._current_version}\n"
                f"+{self._bumped_version}"
            ),
            f"[DRY-RUN] Skipping changes to '{files[2]}'...",
            (
                f"Could not find version {self._current_version} in file '{files[3]}'. "
                f"Skipping..."
            ),
        ] == self._logger_spy.messages

    def test_bump(self):
        files = self._tracked_files()
        executor = BumpIt(
            folder=self._tmp_folder, logger=self._logger_spy, dry_run=False
        )
        executor.bump(
            current_version=self._current_version,
            bumped_version=self._bumped_version,
            files=files,
        )

        assert [
            (
                f"Could not find version {self._current_version} in file '{files[0]}'. "
                f"Skipping..."
            ),
            (
                f"--- before: {files[1]}\n"
                f"+++ after: {files[1]}\n"
                f"@@ -1 +1 @@\n"
                f"-{self._current_version}\n"
                f"+{self._bumped_version}"
            ),
            f"Updated file '{files[1]}'.",
            (
                f"--- before: {files[2]}\n"
                f"+++ after: {files[2]}\n"
                f"@@ -1,4 +1,4 @@\n"
                f" 14.04.6-LTS\n"
                f"-            {self._current_version}...\n"
                f"+            {self._bumped_version}...\n"
                f" and another one\n"
                f"-{self._current_version}\n"
                f"+{self._bumped_version}"
            ),
            f"Updated file '{files[2]}'.",
            (
                f"Could not find version {self._current_version} in file '{files[3]}'. "
                f"Skipping..."
            ),
        ] == self._logger_spy.messages

        for index in range(0, 4):
            expected = self._file_contents(fixture_path(f"executors/after/file{index}"))
            actual = self._file_contents(files[index])
            assert expected == actual

    def _file_contents(self, file):
        with open(file, "rb") as fh:
            return fh.read().decode("utf-8")

    def _tracked_files(self):
        return [f"{self._tmp_folder}/file{index}" for index in range(0, 4)]
