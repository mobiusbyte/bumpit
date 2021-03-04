import os
from dataclasses import dataclass
from typing import Any

from bumpit.core.config import Configuration
from bumpit.core.folder import FolderManager
from bumpit.core.vcs import Git, GitSettings
from bumpit.core.versions import next_version
from bumpit.core.versions.strategy import StrategySettings


@dataclass
class RunSettings:
    dry_run: bool
    target_part: Any
    force_value: Any


def run(config, logger, run_settings):
    configuration = Configuration.parse(config)

    executor = BumpIt(configuration, run_settings.dry_run, logger)

    part = run_settings.target_part or configuration.strategy.part

    bumped_version = next_version(
        strategy_settings=StrategySettings(
            target_strategy=configuration.strategy.name,
            version_format=configuration.strategy.version_format,
            current_version=configuration.current_version,
        ),
        part=part,
        force_value=run_settings.force_value,
    )

    executor.execute(bumped_version)


class BumpIt:
    def __init__(self, configuration, dry_run, logger):
        self._folder_manager = FolderManager(
            folder=os.getcwd(), logger=logger, dry_run=dry_run
        )
        self._vcs = Git(
            dry_run=dry_run,
            settings=GitSettings(
                author=configuration.commit.author,
                apply_tag=configuration.tag.apply,
                tag_format=configuration.tag.format,
                auto_remote_push=configuration.auto_remote_push,
            ),
            logger=logger,
        )
        self._current_version = configuration.current_version
        self._tracked_files = configuration.tracked_files + [configuration.config_file]
        self._base_branch = configuration.base_branch

    def execute(self, bumped_version):
        self._folder_manager.update(
            current_version=self._current_version,
            bumped_version=bumped_version,
            files=self._tracked_files,
        )

        self._vcs.update(
            current_version=self._current_version,
            bumped_version=bumped_version,
            base_branch=self._base_branch,
        )
