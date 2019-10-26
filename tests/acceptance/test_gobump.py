import pytest
from click.testing import CliRunner

from gobump.console.cli import gobump


@pytest.mark.parametrize("part", ["patch"])
@pytest.mark.parametrize("dryrun", ["-d", "--dryrun"])
def test_semantic_versioning_dryrun(part, dryrun):
    runner = CliRunner()
    result = runner.invoke(gobump, ["--part", part, dryrun, "--strategy", "semver"])

    assert result.exit_code == 0
    assert result.output == "stubby\n"
