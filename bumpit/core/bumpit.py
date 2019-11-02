import os

from bumpit.core.config import Configuration
from bumpit.core.folder import FolderManager
from bumpit.core.vcs import Git
from bumpit.core.version_strategy import new_version


def run(config, logger, dry_run):
    runner = Runner(config, dry_run, logger)

    configuration = Configuration.parse(config)

    bumped_version = new_version(configuration.strategy, configuration.current_version)
    runner.execute(bumped_version)


class Runner:
    def __init__(self, config, dry_run, logger):
        configuration = Configuration.parse(config)

        self._folder_manager = FolderManager(
            folder=os.getcwd(), logger=logger, dry_run=dry_run
        )
        self._vcs = Git(
            dry_run=dry_run,
            tag=configuration.tag,
            tag_format=configuration.tag_format,
            auto_remote_push=configuration.auto_remote_push,
            logger=logger,
        )
        self._current_version = configuration.current_version
        self._tracked_files = configuration.tracked_files + [config]

    def execute(self, bumped_version):
        self._folder_manager.update(
            current_version=self._current_version,
            bumped_version=bumped_version,
            files=self._tracked_files,
        )

        self._vcs.update(
            current_version=self._current_version, bumped_version=bumped_version
        )
