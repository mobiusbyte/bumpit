import os

from bumpit.core.config import Configuration
from bumpit.core.executor import BumpIt
from bumpit.core.vcs import Git
from bumpit.core.version_strategy import new_version


def run(config, logger, dry_run):
    configuration = Configuration.parse(config)
    executor = BumpIt(folder=os.getcwd(), logger=logger, dry_run=dry_run)
    vcs = Git(
        dry_run=dry_run,
        tag=configuration.tag,
        tag_format=configuration.tag_format,
        auto_remote_push=configuration.auto_remote_push,
        logger=logger,
    )

    current_version = configuration.current_version
    bumped_version = new_version(configuration.strategy, current_version)
    executor.bump(
        current_version=current_version,
        bumped_version=bumped_version,
        files=configuration.tracked_files + [config],
    )
    vcs.update(current_version=current_version, bumped_version=bumped_version)
