from dataclasses import dataclass
import os
import yaml


@dataclass
class Strategy:
    name: str
    part: str

    @staticmethod
    def load(section):
        try:
            strategy = Strategy(**section)
        except TypeError:
            raise ValueError("Missing strategy name and/or part")

        if not strategy.name:
            raise ValueError("Strategy name cannot be empty")

        if strategy.part is None:
            raise ValueError("Strategy part cannot be null")

        return strategy

    def __eq__(self, other):
        return self.name == other.name and self.part == other.part


@dataclass
class Configuration:
    config_file: str
    current_version: str
    strategy: Strategy
    tag: bool
    tag_format: str
    auto_remote_push: bool
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

        contents["strategy"] = Strategy.load(contents["strategy"])
        contents["config_file"] = file

        return Configuration(**contents)

    @staticmethod
    def _load_config(file):
        if not os.path.isfile(file):
            raise ValueError(f"Invalid config file. Path '{file}' does not exist.")

        with open(file, "rb") as fh:
            contents = yaml.safe_load(fh)

        return contents or {}
