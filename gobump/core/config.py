from dataclasses import dataclass
import yaml


@dataclass
class Configuration:
    version: str
    tracked_files: list

    @staticmethod
    def parse(file):
        contents = {}
        with open(file, "rb") as fh:
            contents = yaml.safe_load(fh)

        mandatory_fields = ["version", "tracked_files"]
        for field in mandatory_fields:
            if contents.get(field) is None:
                raise ValueError(f"Configuration file is missing '{field}'")

        return Configuration(**contents)
