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
class Tag:
    apply: bool
    format: str

    @staticmethod
    def load(section):
        apply = section.get("apply", "")
        if not (apply is True or apply is False):
            raise ValueError(
                f"Invalid tag.apply value '{section.get('apply')}'. It should be a bool."
            )

        try:
            tag = Tag(**section)
        except TypeError:
            raise ValueError("Missing tag apply and/or format")

        if "{version}" not in tag.format:
            raise ValueError("Tag format must include '{version}' token")

        return tag

    def __eq__(self, other):
        return self.apply == other.apply and self.format == other.format


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
