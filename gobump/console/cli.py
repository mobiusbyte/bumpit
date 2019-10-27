import os
import click
from gobump.core.config import Configuration
from gobump.core.executor import GoBump
from gobump.core.version_strategy import new_version


class ConsoleLogger:
    def __init__(self):
        pass

    def echo(self, message):
        click.echo(message)

    info = echo
    warn = echo


@click.command()
@click.option(
    "--part", "-p", prompt="version part", help="Specifies the vesion part to update"
)
@click.option(
    "--dry_run",
    "-d",
    is_flag=True,
    prompt="do a dry run?",
    help="Run the tool in dry run mode",
)
@click.option(
    "--strategy",
    "-s",
    prompt="versioning strategy",
    help="Versioning strategy. Supported strategies: semver",
)
@click.option("--config", "-c", default=".gobump.yaml", help="Configuration settings")
def gobump(part, dry_run, strategy, config):
    configuration = Configuration.parse(config)
    bumped_version = new_version(strategy, configuration.current_version, part)
    executor = GoBump(folder=os.getcwd(), logger=ConsoleLogger(), dry_run=dry_run)
    executor.bump(
        current_version=configuration.current_version,
        bumped_version=bumped_version,
        files=configuration.tracked_files + [config],
    )


def main():
    gobump()  # pragma: no cover
