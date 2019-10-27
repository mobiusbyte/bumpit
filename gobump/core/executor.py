from difflib import unified_diff


class GoBump:
    def __init__(self, folder, logger):
        self._folder = folder
        self._logger = logger

    def bump(self, current_version, bumped_version, files):
        for file in files:
            with open(file, "rb") as fh:
                before_bump = fh.read().decode("utf-8")

                after_bump = before_bump.replace(current_version, bumped_version)

            if before_bump == after_bump:
                self._logger.warn(
                    f"Could not find version {current_version} in file '{file}'. "
                    f"Skipping..."
                )
            else:
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
