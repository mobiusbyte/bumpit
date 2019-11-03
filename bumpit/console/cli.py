import click
from click import ClickException
from bumpit.core.bumpit import run, RunSettings


class ConsoleLogger:
    def __init__(self):
        pass

    def echo(self, message):
        click.echo(message)

    info = echo
    warn = echo


@click.command()
@click.option(
    "--config",
    "-c",
    default=".bumpit.yaml",
    type=click.Path(exists=True),
    help="(optional) configuration settings. Defaults to `.bumpit.yaml`",
)
@click.option(
    "--part",
    "-p",
    default="",
    help=(
        "(optional) strategy part override. "
        "Defaults to `strategy.part` from the config file."
    ),
)
@click.option(
    "--value",
    "-v",
    default=None,
    help=(
        "(optional) part value override. "
        "Any part can be overrode by this value as long as the value is valid."
    ),
)
@click.option(
    "--dry-run",
    "-d",
    is_flag=True,
    default=False,
    help="(optional) run the tool in dry run mode. Defaults to false.",
)
def bumpit(config, part, value, dry_run):
    try:
        run(
            config,
            ConsoleLogger(),
            run_settings=RunSettings(
                dry_run=dry_run, target_part=part, force_value=value
            ),
        )
    except Exception as e:
        raise ClickException(e)


def main():
    bumpit()  # pragma: no cover
