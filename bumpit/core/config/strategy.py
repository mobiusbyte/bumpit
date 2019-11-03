from dataclasses import dataclass


@dataclass
class Strategy:
    name: str
    part: str
    version_format: str = None

    @staticmethod
    def load(section):
        try:
            strategy = Strategy(**section)
        except TypeError as e:
            raise ValueError(f"Missing strategy field(s). {e}")

        if not strategy.name:
            raise ValueError("Strategy name cannot be empty.")

        if strategy.part is None:
            raise ValueError("Strategy part cannot be null.")

        return strategy

    def __eq__(self, other):
        return self.name == other.name and self.part == other.part
