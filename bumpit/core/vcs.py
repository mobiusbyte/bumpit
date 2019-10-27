import os


class Git:
    def __init__(self, dry_run, logger, command_executor=None):
        self._dry_run = dry_run
        self._logger = logger
        self._command_executor = command_executor or os.system

    def commit(self, current_version, bumped_version):
        self._execute_command("git add .")
        self._execute_command(
            f"git commit -m 'Bumped version from {current_version} → {bumped_version}.'"
        )

    def _execute_command(self, command):
        if self._dry_run:
            self._logger.info(f"Running DRY-RUN mode. Ran `{command}`")
        else:
            if self._command_executor(command) != 0:
                raise Exception(f"Failed to execute {command}")

            self._logger.info(f"[OK] {command}")
