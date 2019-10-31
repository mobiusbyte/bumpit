from dataclasses import dataclass
import os
import yaml


@dataclass
class Configuration:
    current_version: str
    strategy: str
    tag: bool
    tag_format: str
    tracked_files: list

    @staticmethod
    def parse(file):
        contents = Configuration._load_config(file)

        mandatory_fields = [
            "current_version",
            "strategy",
            "tag",
            "tag_format",
            "tracked_files",
        ]
        for field in mandatory_fields:
            if contents.get(field) is None:
                raise ValueError(f"Configuration field is missing '{field}'")

        if contents["tag"] not in [True, False]:
            raise ValueError(
                f"Invalid tag value '{contents['tag']}'. It should be a bool."
            )

        return Configuration(**contents)

    @staticmethod
    def _load_config(file):
        if not os.path.isfile(file):
            raise ValueError(f"Invalid config file. Path '{file}' does not exist.")

        with open(file, "rb") as fh:
            contents = yaml.safe_load(fh)

        return contents or {}
