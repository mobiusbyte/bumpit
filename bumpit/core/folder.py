from difflib import unified_diff


class FolderManager:
    def __init__(self, folder, logger, dry_run):
        self._folder = folder
        self._logger = logger
        self._dry_run = dry_run

    def update(self, current_version, bumped_version, files):
        if self._dry_run:
            self._logger.info("***Running in DRY-RUN mode...***")

        for file in files:
            self._update_file(file, current_version, bumped_version)

    def _update_file(self, file, current_version, bumped_version):
        with open(file, "rb") as fh:
            before_bump = fh.read().decode("utf-8")

            after_bump = before_bump.replace(current_version, bumped_version)

        if before_bump != after_bump:
            self._apply_file_changes(file, before_bump, after_bump)
        else:
            self._logger.info(
                f"Could not find version {current_version} in file '{file}'. "
                f"Skipping..."
            )

    def _apply_file_changes(self, file, before_bump, after_bump):
        self._logger.info(
            "\n".join(
                list(
                    unified_diff(
                        before_bump.splitlines(),
                        after_bump.splitlines(),
                        lineterm="",
                        fromfile="before: " + file,
                        tofile="after: " + file,
                    )
                )
            )
        )

        if self._dry_run:
            self._logger.info(f"[DRY-RUN] Skipping changes to '{file}'...")
        else:
            with open(file, "wb") as fh:
                fh.write(after_bump.encode("utf-8"))

            self._logger.info(f"Updated file '{file}'.")
