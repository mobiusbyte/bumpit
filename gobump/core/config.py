from dataclasses import dataclass
import yaml


@dataclass
class Configuration:
    tracked_files: list

    @staticmethod
    def parse(file):
        contents = {}
        with open(file, "rb") as fh:
            contents = yaml.safe_load(fh)

        return Configuration(tracked_files=contents.get("tracked_files") or [])
