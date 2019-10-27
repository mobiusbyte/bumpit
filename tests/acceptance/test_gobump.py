import pytest
from click.testing import CliRunner

from bumpit.console.cli import bumpit


@pytest.mark.parametrize("part", ["patch"])
@pytest.mark.parametrize("dry_run", ["-d", "--dry_run"])
def xtest_semantic_versioning_dry_run(part, dry_run):
    runner = CliRunner()
    result = runner.invoke(bumpit, ["--part", part, dry_run, "--strategy", "semver"])

    assert result.exit_code == 0
    assert result.output == "stubby\n"
