import os
import click
from bumpit.core.config import Configuration
from bumpit.core.executor import BumpIt
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
    "--dry-run",
    "-d",
    is_flag=True,
    default=False,
    help="Run the tool in dry run mode",
)
@click.option("--config", "-c", default=".bumpit.yaml", help="Configuration settings")
def bumpit(dry_run, config):
    configuration = Configuration.parse(config)
    bumped_version = new_version(configuration.strategy, configuration.current_version)
    executor = BumpIt(folder=os.getcwd(), logger=ConsoleLogger(), dry_run=dry_run)
    executor.bump(
        current_version=configuration.current_version,
        bumped_version=bumped_version,
        files=configuration.tracked_files + [config],
    )


def main():
    bumpit()  # pragma: no cover
