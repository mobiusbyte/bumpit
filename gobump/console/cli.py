import click


@click.command()
@click.option(
    "--part", "-p", prompt="version part", help="Specifies the vesion part to update"
)
@click.option(
    "--dryrun",
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
def gobump(part, dryrun, strategy):
    print("stubby")


def main():
    gobump()  # pragma: no cover
