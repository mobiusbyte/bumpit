import os

from bumpit.core.config import Configuration
from bumpit.core.folder import FolderManager
from bumpit.core.vcs import Git
from bumpit.core.versions import next_version


def run(config, logger, dry_run, target_part=None, force_value=None):
    configuration = Configuration.parse(config)

    executor = BumpIt(configuration, dry_run, logger)

    part = target_part or configuration.strategy.part

    bumped_version = next_version(
        configuration.strategy.name,
        configuration.current_version,
        part,
        force_value=force_value,
    )

    executor.execute(bumped_version)


class BumpIt:
    def __init__(self, configuration, dry_run, logger):
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
        self._tracked_files = configuration.tracked_files + [configuration.config_file]

    def execute(self, bumped_version):
        self._folder_manager.update(
            current_version=self._current_version,
            bumped_version=bumped_version,
            files=self._tracked_files,
        )

        self._vcs.update(
            current_version=self._current_version, bumped_version=bumped_version
        )
