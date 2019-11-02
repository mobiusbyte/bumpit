from dataclasses import dataclass
import os
import yaml

from bumpit.core.config.strategy import Strategy
from bumpit.core.config.tag import Tag


@dataclass
class Configuration:
    config_file: str
    current_version: str
    strategy: Strategy
    tag: Tag
    auto_remote_push: bool
    tracked_files: list

    @staticmethod
    def parse(file):
        contents = Configuration._load_config(file)

        mandatory_fields = ["current_version", "strategy", "tag", "tracked_files"]
        for field in mandatory_fields:
            if contents.get(field) is None:
                raise ValueError(f"Configuration field is missing '{field}'")

        contents["strategy"] = Strategy.load(contents["strategy"])
        contents["tag"] = Tag.load(contents["tag"])
        contents["config_file"] = file

        return Configuration(**contents)

    @staticmethod
    def _load_config(file):
        if not os.path.isfile(file):
            raise ValueError(f"Invalid config file. Path '{file}' does not exist.")

        with open(file, "rb") as fh:
            contents = yaml.safe_load(fh)

        return contents or {}
