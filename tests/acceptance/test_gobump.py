import pytest
import subprocess


GOBUMP_CLI = "gobump"


@pytest.mark.parametrize("part", ["patch"])
@pytest.mark.parametrize("dryrun_option", ["-d", "--dryrun"])
def test_semantic_versioning_dryrun(part, dryrun_option):
    result = subprocess.run([GOBUMP_CLI, dryrun_option, part], stdout=subprocess.PIPE)

    assert result.stdout == b"stubby\n"
