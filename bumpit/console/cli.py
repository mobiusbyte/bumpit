import os
import click
from bumpit.core.config import Configuration
from bumpit.core.executor import BumpIt
from bumpit.core.vcs import Git
from bumpit.core.version_strategy import new_version


class ConsoleLogger:
    def __init__(self):
        pass

    def echo(self, message):
        click.echo(message)

    info = echo
    warn = echo


@click.command()
@click.option(
    "--dry-run", "-d", is_flag=True, default=False, help="Run the tool in dry run mode"
)
@click.option("--config", "-c", default=".bumpit.yaml", help="Configuration settings")
def bumpit(dry_run, config):
    configuration = Configuration.parse(config)
    logger = ConsoleLogger()

    executor = BumpIt(folder=os.getcwd(), logger=logger, dry_run=dry_run)
    vcs = Git(
        dry_run=dry_run,
        tag=configuration.tag,
        tag_format=configuration.tag_format,
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


def main():
    bumpit()  # pragma: no cover
