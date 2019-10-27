import pytest
from click.testing import CliRunner

from gobump.console.cli import gobump


@pytest.mark.parametrize("part", ["patch"])
@pytest.mark.parametrize("dry_run", ["-d", "--dry_run"])
def xtest_semantic_versioning_dry_run(part, dry_run):
    runner = CliRunner()
    result = runner.invoke(gobump, ["--part", part, dry_run, "--strategy", "semver"])

    assert result.exit_code == 0
    assert result.output == "stubby\n"
