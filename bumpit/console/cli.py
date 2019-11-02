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
@click.option(
    "--part",
    "-p",
    default="",
    help="Strategy part override. Defaults to `strategy_part` from config file.",
)
@click.option(
    "--value",
    "-v",
    default="",
    help=(
        "Part value override. "
        "Any part can be overrode by this value as long as the value is valid."
    ),
)
def bumpit(dry_run, config, part, value):
    try:
        run(config, ConsoleLogger(), dry_run, target_part=part, force_value=value)
    except Exception as e:
        raise ClickException(e)


def main():
    bumpit()  # pragma: no cover
