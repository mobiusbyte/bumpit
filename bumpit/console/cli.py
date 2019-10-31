import click
from click import ClickException
from bumpit.core.bumpit import run


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
@click.option(
    "--config",
    "-c",
    default=".bumpit.yaml",
    type=click.Path(exists=True),
    help="Configuration settings",
)
def bumpit(dry_run, config):
    try:
        run(config, ConsoleLogger(), dry_run)
    except Exception as e:
        raise ClickException(e)


def main():
    bumpit()  # pragma: no cover
