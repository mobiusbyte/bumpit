import os
import random
import string
from shutil import rmtree

from gobump.core.executor import GoBump


class LoggerSpy:
    def __init__(self):
        self.messages = []

    def log(self, message):
        self.messages.append(message)

    warn = log
    info = log
    error = log


class TestGoBumpDryRun:
    def setup(self):
        self._tmp_folder = tmp_folder()
        self._logger_spy = LoggerSpy()
        self._current_version = "0.0.1"
        self._bumped_version = "0.1.0"

    def teardown(self):
        rmtree(self._tmp_folder, ignore_errors=True)

    def test_bump_dry_run(self):
        file0 = self._stub_file("99.88.77")
        file1 = self._stub_file(self._current_version)
        file2 = self._stub_file(
            f"14.04.6-LTS\n"
            f"            {self._current_version}       \n"
            f"and another one\n"
            f"{self._current_version}"
        )
        file3 = self._stub_file("")

        executor = GoBump(
            folder=self._tmp_folder, logger=self._logger_spy, dry_run=True
        )
        executor.bump(
            current_version=self._current_version,
            bumped_version=self._bumped_version,
            files=[file0, file1, file2, file3],
        )

        assert [
            "Running in DRY-RUN mode...",
            (
                f"Could not find version {self._current_version} in file '{file0}'. "
                f"Skipping..."
            ),
            (
                f"--- before: {file1}\n"
                f"+++ after: {file1}\n"
                f"@@ -1 +1 @@\n"
                f"-{self._current_version}\n"
                f"+{self._bumped_version}"
            ),
            f"Running DRY-RUN mode. Skipping changes to '{file1}'...",
            (
                f"--- before: {file2}\n"
                f"+++ after: {file2}\n"
                f"@@ -1,4 +1,4 @@\n"
                f" 14.04.6-LTS\n"
                f"-            {self._current_version}       \n"
                f"+            {self._bumped_version}       \n"
                f" and another one\n"
                f"-{self._current_version}\n"
                f"+{self._bumped_version}"
            ),
            f"Running DRY-RUN mode. Skipping changes to '{file2}'...",
            (
                f"Could not find version {self._current_version} in file '{file3}'. "
                f"Skipping..."
            ),
        ] == self._logger_spy.messages

    def _stub_file(self, content):
        filename = f"{self._tmp_folder}/{random_string()}"
        with open(filename, "w") as fh:
            fh.write(content)

        return filename


def tmp_folder():
    folder = f"/tmp/{random_string()}"
    os.makedirs(folder)
    return folder


def random_string():
    return "".join(random.choice(string.ascii_letters) for _ in range(6))
