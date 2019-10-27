import os


class Git:
    def __init__(self, dry_run, tag, tag_format, logger, command_executor=None):
        self._dry_run = dry_run
        self._tag = tag
        self._tag_format = self._parse_tag_format(tag_format)
        self._logger = logger
        self._command_executor = command_executor or os.system

    def update(self, current_version, bumped_version):
        self._git_commit(current_version, bumped_version)
        self._git_tag(current_version, bumped_version)

    def _git_commit(self, current_version, bumped_version):
        self._execute_command("git add .")
        self._execute_command(
            f"git commit -m '{self._bump_message(current_version, bumped_version)}'"
        )

    def _git_tag(self, current_version, bumped_version):
        if not self._tag:
            self._logger.info("Skipped tagging...")
            return

        tag_command_format = (
            f"git tag "
            f"-a '{self._tag_format}' "
            f"-m '{self._bump_message(current_version, bumped_version)}'"
        )
        tag_command = tag_command_format.format(version=bumped_version)

        self._execute_command(tag_command)

    def _bump_message(self, current_version, bumped_version):
        return f"Bumped version from {current_version} → {bumped_version}."

    def _execute_command(self, command):
        if self._dry_run:
            self._logger.info(f"[DRY-RUN] Ran `{command}`")
        else:
            if self._command_executor(command) != 0:
                raise Exception(f"Failed to execute {command}")

            self._logger.info(f"[OK] {command}")

    @staticmethod
    def _parse_tag_format(tag_format):
        if "{version}" not in tag_format:
            raise ValueError(
                f"Invalid tag_format '{tag_format}'. "
                f"Value must include the string `{{version}}`."
            )
        return tag_format
